from utils.exception_handler import FileValidationError, SchemaValidationError
from services.validation_service import validate_rows, validate_columns
from fastapi import UploadFile
import pandas as pd

# Load the data from the CSV
def load_expenses(content):
    try:
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
    return df['amount'].sum()

# Group by category
def group_by_category(df):
    return df.groupby('category')['amount'].sum().to_dict()

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

# Analyze the data
async def analyze_expenses(file: UploadFile) -> dict:
    if not file.filename.endswith(".csv"):
        raise FileValidationError("Only CSV files allowed")

    content = await file.read()

    # Load the data from the CSV
    df = load_expenses(content)

    # Check if the dataframe is empty
    if df.empty:
        raise FileValidationError("CSV file is empty")

    # Validate columns
    validate_columns(df)

    # Clean the data
    df = clean_data(df)

    # Check file and validate the rows
    valid_df, errors = validate_rows(df)

    # Calculate the total
    total = calculate_total(valid_df)

    # Group by category
    grouped = group_by_category(valid_df)

    # Sort by category
    grouped = dict(sorted(grouped.items(), key=lambda x: x[1], reverse=True))

    # Get the top category
    top = get_top_category(grouped)

    # Return the results
    return {
        "total": total,
        "category_breakdown": grouped,
        "top_category": top,
        "error_summary": summarize_errors(errors),
        "invalid_rows": errors,
        "valid_row_count": len(valid_df),
        "invalid_row_count": len(errors),
        "total_row_count": len(df)
    }
