from utils.exception_handler import SchemaValidationError, FileValidationError
import pandas as pd

REQUIRED_COLUMNS = ['date', 'amount', 'category']

# Validate date
def is_valid_date(date_str):
    try:
        pd.to_datetime(date_str, errors='raise', format='%Y-%m-%d')
        return True
    except ValueError:
        return False

# Validate columns
def validate_columns(df):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise SchemaValidationError(f"Missing column: {', '.join(missing_columns)}")
    else:
        return True

# Validate rows data
def validate_rows(df):
    errors = []
    valid_rows = []
    for index, row in df.iterrows():
        row_errors = []
        try:
            if float(row["amount"]) <= 0:
                row_errors.append({
                    "field": "amount",
                    "issue": "Amount must be positive value"
                })
        except ValueError:
            row_errors.append({
                "field": "amount",
                "issue": "Amount must be a valid number"
            })
        if pd.isna(row["category"]) or str(row["category"]).strip() == "":
            row_errors.append({
                "field": "category",
                "issue": "Category cannot be empty"
            })
        if str(row["category"]).strip().isdigit():
            row_errors.append({
                "field": "category",
                "issue": "Category cannot be a number"
            })
        if pd.isna(row["date"]) or str(row["date"]).strip() == "" or not is_valid_date(row["date"]):
            row_errors.append({
                "field": "date",
                "issue": "Date cannot be empty or invalid"
            })
        if row_errors:
            errors.append({
                "row": index+1,
                "issues": row_errors
            })
        else:
            valid_rows.append(row)
    valid_df = pd.DataFrame(valid_rows)
    return valid_df, errors
