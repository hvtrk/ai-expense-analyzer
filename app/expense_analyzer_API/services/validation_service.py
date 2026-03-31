from models.internal.validation.validation import ValidationResult, InvalidRow, Issue, ErrorSummary
from models.internal.expense.expense import CleanedExpenseData
from core import exceptions
import pandas as pd

REQUIRED_COLUMNS = ['date', 'amount', 'category']


# Validate columns
def validate_columns(df: pd.DataFrame):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise exceptions.SchemaValidationError(f"Missing column: {', '.join(missing_columns)}")


def summarize_errors(invalid_rows: list) -> list:
    summary = {}
    for row in invalid_rows:
        for issue in row.issues:
            summary[issue.field] = summary.get(issue.field, 0) + 1
    return [ErrorSummary(field=k, count=v) for k, v in summary.items()]


# Validate rows data
def validate_rows(df: pd.DataFrame) -> tuple[CleanedExpenseData, list[InvalidRow]]:
    invalid_rows = []
    df = df.copy()

    # Normalize
    df["amount_clean"] = pd.to_numeric(df["amount"], errors="coerce")
    df["category_clean"] = df["category"].astype(str).str.strip().str.lower()
    df["date_clean"] = pd.to_datetime(df["date"], errors='coerce').dt.date

    # Masks
    amount_invalid = (df["amount_clean"].isna()) | (df["amount_clean"] <= 0)

    category_invalid = (
        df["category"].isna() |
        (df["category_clean"] == "") |
        (df["category_clean"].str.isdigit())
    )

    date_invalid = df["date_clean"].isna()

    # Combine errors
    invalid_mask = amount_invalid | category_invalid | date_invalid
    invalid_indices = df.index[invalid_mask]

    for idx in invalid_indices:
        row_issues = []
        row = df.loc[idx]

        if amount_invalid.loc[idx]:
            row_issues.append(Issue(
                field="amount",
                message=(
                    "Amount must be positive value"
                    if not pd.isna(row["amount_clean"])
                    else "Amount must be a valid number"
                )
            ))

        if category_invalid.loc[idx]:
            row_issues.append(Issue(
                field="category",
                message="Category cannot be empty or numeric"
            ))

        if date_invalid.loc[idx]:
            row_issues.append(Issue(
                field="date",
                message="Date cannot be empty or invalid"
            ))

        if row_issues:
            invalid_rows.append(InvalidRow(row_index=idx + 1, issues=row_issues))

    df["amount"] = df["amount_clean"]
    df["category"] = df["category_clean"]
    df["date"] = df["date_clean"]

    valid_df = df.loc[~invalid_mask, REQUIRED_COLUMNS].copy()
    return CleanedExpenseData(valid_df), invalid_rows


# Validate the data
def validate(df: pd.DataFrame) -> ValidationResult:
    if df.empty:
        raise exceptions.ValidationError("No data provided")
    total_rows = len(df)
    validate_columns(df)
    cleaned_data, invalid_rows = validate_rows(df)
    valid_rows = len(cleaned_data.df)
    error_summary = summarize_errors(invalid_rows)
    return ValidationResult(
        cleaned_data=cleaned_data,
        invalid_rows=invalid_rows,
        error_summary=error_summary,
        total_rows=total_rows,
        valid_rows=valid_rows,
    )
