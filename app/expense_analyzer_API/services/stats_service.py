from models.internal.stats.stats import StatsResult, DateRange, ExpenseStats, CategoryStat, DailyStat
from models.internal.expense.expense import CleanedExpenseData
from core import exceptions
from utils.math_utils import safe_float
import pandas as pd
import numpy as np


# Calculate filter window
def calculate_filter_window(df: pd.DataFrame, filter_type: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    if df.empty:
        return None, None
    if filter_type == "last_7_days":
        start_date = df["date"].max() - pd.Timedelta(days=7)
        end_date = df["date"].max()
    elif filter_type == "last_30_days":
        start_date = df["date"].max() - pd.Timedelta(days=30)
        end_date = df["date"].max()
    else:
        start_date = df["date"].min()
        end_date = df["date"].max()
    return start_date, end_date


# Filter by date
def filter_by_date(df: pd.DataFrame, filter_type: str) -> pd.DataFrame:
    if df.empty:
        return df
    start_date, end_date = calculate_filter_window(df, filter_type)
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    return filtered_df


# Calculate descriptive stats
def calculate_expense_stats(amounts: np.ndarray) -> ExpenseStats:
    if amounts.size == 0:
        return ExpenseStats(mean=0.0, median=0.0, variance=0.0, std_dev=0.0, count=0)
    return ExpenseStats(
        mean=safe_float(np.mean(amounts)),
        median=safe_float(np.median(amounts)),
        variance=safe_float(np.var(amounts)),
        std_dev=safe_float(np.std(amounts)),
        count=int(amounts.size),
    )


# Calculate the total
def calculate_total(df: pd.DataFrame) -> float:
    return df['amount'].sum() if not df.empty else 0.0


# Group by category
def group_by_category(df: pd.DataFrame) -> dict:
    return {k: safe_float(v) for k, v in df.groupby('category')['amount'].sum().items()}


# Group by date
def group_by_date(df: pd.DataFrame) -> dict:
    return {k.strftime("%Y-%m-%d"): safe_float(v) for k, v in df.groupby('date')['amount'].sum().items()}


# Get the top category
def get_top_category(grouped: dict) -> str:
    if not grouped:
        return None
    return max(grouped, key=grouped.get)


# Compute stats
def compute_stats(cleaned_data: CleanedExpenseData, filter_type: str) -> StatsResult:
    if filter_type not in ["last_7_days", "last_30_days", "none"]:
        raise exceptions.QueryValidationError("Invalid filter type")

    df_filtered = filter_by_date(cleaned_data.df, filter_type)

    if df_filtered.empty:
        date_range = DateRange(start=None, end=None)
    else:
        date_range = DateRange(
            start=df_filtered["date"].min(),
            end=df_filtered["date"].max(),
        )

    amounts = df_filtered["amount"].to_numpy()
    expense_stats = calculate_expense_stats(amounts)
    total = calculate_total(df_filtered)

    grouped_category = group_by_category(df_filtered)
    grouped_category_sorted = sorted(grouped_category.items(), key=lambda x: x[1], reverse=True)
    category_breakdown_list = [CategoryStat(category=k, total=v) for k, v in grouped_category_sorted]

    grouped_date = group_by_date(df_filtered)
    grouped_date_sorted = sorted(grouped_date.items(), key=lambda x: x[0])
    daily_trend_list = [DailyStat(date=k, total=v) for k, v in grouped_date_sorted]

    top = get_top_category(grouped_category)

    return StatsResult(
        total=safe_float(total),
        category_breakdown=category_breakdown_list,
        daily_trend=daily_trend_list,
        top_category=top,
        stats=expense_stats,
        date_range=date_range,
    )
