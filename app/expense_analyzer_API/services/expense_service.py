from fastapi.concurrency import run_in_threadpool
from utils.exception_handler import FileValidationError, SchemaValidationError, QueryValidationError
from services.validation_service import validate_rows, validate_columns
from fastapi import UploadFile
import pandas as pd
import numpy as np

PRECISION = 2
MAX_ERRORS = 100
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Load the data from the CSV
def load_expenses(content):
    try:
        if len(content) > MAX_FILE_SIZE:
            raise FileValidationError("File too large")
        return pd.read_csv(pd.io.common.BytesIO(content))
    except Exception as e:
        raise FileValidationError(f"Invalid CSV format: {str(e)}")

# Clean the data
def clean_data(df):
    df['category'] = df['category'].str.strip().str.lower()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    return df

# Calculate the total
def calculate_total(df):
    return df['amount'].sum() if not df.empty else 0.0

# Group by category
def group_by_category(df):
    return {k: safe_float(v) for k, v in df.groupby('category')['amount'].sum().items()}

# Get the top category
def get_top_category(grouped):
    if not grouped:
        return None
    return max(grouped, key=grouped.get)

# Error sumary
def summarize_errors(errors):
    summary = {}
    for error in errors:
        for issue in error["issues"]:
            field = issue["field"]
            summary[field] = summary.get(field, 0) + 1
    return summary

# Calculate filter window
def calculate_filter_window(df, filter_type):
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
def filter_by_date(df, filter_type):
    if df.empty:
        return df
    start_date, end_date = calculate_filter_window(df, filter_type)
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    return filtered_df

# Safe float
def safe_float(value):
    value = float(value)
    if np.isnan(value) or np.isinf(value):
        return 0.0
    return round(float(value), PRECISION)

# Calculate stats
def calculate_expense_stats(amounts: np.ndarray) -> dict:
    if amounts.size == 0:
        return {
            "mean": 0.0,
            "median": 0.0,
            "variance": 0.0,
            "std_dev": 0.0,
            "count": 0
        }
    return {
        "mean": safe_float(np.mean(amounts)),
        "median": safe_float(np.median(amounts)),
        "variance": safe_float(np.var(amounts)),
        "std_dev": safe_float(np.std(amounts)),
        "count": amounts.size
    }

async def analyze_expenses(file: UploadFile, filter_type: str):
      # Check if the file is a CSV
    if not file.filename.endswith(".csv"):
        raise FileValidationError("Only CSV files allowed")

    # Check if the filter type is valid
    if filter_type not in ["last_7_days", "last_30_days", "none"]:
        raise QueryValidationError("Invalid filter type")

    # Read the file content
    content = await file.read()

    result = await run_in_threadpool(
        process_expenses, content, filter_type
    )

    return result

# Analyze the data
def process_expenses(content: bytes, filter_type: str) -> dict:
    # Load the data from the CSV
    df = load_expenses(content)

    # Check if the dataframe has too many rows
    if len(df) > 55000:
        raise FileValidationError("Too many rows")

    # Check if the dataframe is empty
    if df.empty:
        raise FileValidationError("CSV file is empty")

    # Validate columns
    validate_columns(df)

    # Clean the data
    df = clean_data(df)

    # Check file and validate the rows
    valid_df, errors = validate_rows(df)

    # Check if the dataframe is empty
    if valid_df.empty:
        df_filtered = valid_df
    else:
        # Filter by date
        df_filtered = filter_by_date(valid_df, filter_type)

    if df_filtered.empty:
        date_range = {
            "start": None,
            "end": None
        }
    else:
        date_range = {
            "start": df_filtered["date"].min(),
            "end": df_filtered["date"].max()
        }

    # Calculate stats
    amounts = df_filtered["amount"].to_numpy()
    stats = calculate_expense_stats(amounts)

    # Calculate the total
    total = calculate_total(df_filtered)

    # Group by category
    grouped = group_by_category(df_filtered)

    # Sort by category
    grouped = dict(sorted(grouped.items(), key=lambda x: x[1], reverse=True))

    # Get the top category
    top = get_top_category(grouped)

    # Return the results
    return {
        "total": safe_float(total),
        "category_breakdown": grouped,
        "top_category": top,
        "error_summary": summarize_errors(errors),
        "invalid_rows": errors[:MAX_ERRORS],
        "metadata": {
            "total_rows": len(df),
            "valid_rows": len(valid_df),
            "invalid_rows": len(errors),
            "invalid_rows_truncated": len(errors) > MAX_ERRORS,
            "date_range": {
                "start": date_range["start"],
                "end": date_range["end"]
            },
            "filter": {
                "filter_type": filter_type,
            }
        },
        "stats": stats
    }
