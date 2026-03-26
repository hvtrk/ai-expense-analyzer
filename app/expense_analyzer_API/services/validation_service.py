from utils.exception_handler import SchemaValidationError, FileValidationError
import pandas as pd

REQUIRED_COLUMNS = ['date', 'amount', 'category']

# Validate columns
def validate_columns(df):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise SchemaValidationError(f"Missing column: {', '.join(missing_columns)}")

# Validate rows data
def validate_rows(df):
    errors = []
    df = df.copy()

    # Normalize
    df["amount_clean"] = pd.to_numeric(df["amount"], errors="coerce")
    df["category_clean"] = df["category"].astype(str).str.strip()
    df["date_clean"] = pd.to_datetime(df["date"], errors='coerce', format='%Y-%m-%d')

    # Masks
    amount_invalid = (df["amount_clean"].isna()) | (df["amount_clean"] <= 0)

    category_invalid = (
        df["category"].isna() |
        (df["category_clean"] == "") |
        (df["category_clean"].str.isdigit())
    )

    date_invalid = df["date_clean"].isna()

    # Combine Errors
    invalid_mask = amount_invalid | category_invalid | date_invalid
    invalid_indices = df.index[invalid_mask]

    for idx in invalid_indices:
        row_errors = []
        row = df.loc[idx]

        if amount_invalid.loc[idx]:
            row_errors.append({
                "field": "amount",
                "message": "Amount must be positive value"
                if not pd.isna(row["amount_clean"])
                else "Amount must be a valid number"
            })

        if category_invalid.loc[idx]:
            row_errors.append({
                "field": "category",
                "message": "Category cannot be empty or numeric"
            })

        if date_invalid.loc[idx]:
            row_errors.append({
                "field": "date",
                "message": "Date cannot be empty or invalid"
            })

        if row_errors:
            errors.append({
                "row_index": idx + 1,
                "issues": row_errors
            })
    df["amount"] = df["amount_clean"]
    df["category"] = df["category_clean"]
    df["date"] = df["date_clean"]

    valid_df = df.loc[~invalid_mask, REQUIRED_COLUMNS].copy()
    return valid_df, errors
