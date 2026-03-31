from fastapi.concurrency import run_in_threadpool
from fastapi import UploadFile
import pandas as pd
from core import exceptions

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Load the data from the CSV
async def load(file: UploadFile)-> pd.DataFrame:
    # Check if the file is a CSV
    if not file.filename.endswith(".csv"):
        raise exceptions.FileValidationError("Only CSV files allowed")

    # Read the file content
    content = await file.read()

    result = await run_in_threadpool(
        process_csv, content
    )

    validate_csv(result)

    return result

def process_csv(content: bytes):
    try:
        if len(content) > MAX_FILE_SIZE:
            raise exceptions.FileValidationError("File too large")

        return pd.read_csv(pd.io.common.BytesIO(content))
    except Exception as e:
        raise exceptions.FileValidationError(f"Invalid CSV format: {str(e)}")

def validate_csv(df):
    # Check if the dataframe has too many rows
    if len(df) > 55000:
        raise exceptions.FileValidationError("Too many rows")

    # Check if the dataframe is empty
    if df.empty:
        raise exceptions.FileValidationError("CSV file is empty")
