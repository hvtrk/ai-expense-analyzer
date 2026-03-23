from fastapi import HTTPException, UploadFile
import tempfile
import pandas as pd

def load_expenses(content):
    try:
        return pd.read_csv(pd.io.common.BytesIO(content))
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {content}")


def clean_data(df):
    try:
        df['category'] = df['category'].str.strip().str.lower()
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        return df.dropna(subset=['category', 'amount'])
    except KeyError:
        raise ValueError("Invalid CSV format")

def calculate_total(df):
    return df['amount'].sum()


def group_by_category(df):
    return df.groupby('category')['amount'].sum().to_dict()


def get_top_category(grouped):
    if not grouped:
        return None
    return max(grouped, key=grouped.get)


async def analyze_expenses(file: UploadFile) -> dict:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    content = await file.read()

    df = load_expenses(content)
    df = clean_data(df)

    total = calculate_total(df)
    grouped = group_by_category(df)
    grouped = dict(sorted(grouped.items(), key=lambda x: x[1], reverse=True))
    top = get_top_category(grouped)

    return {
        "total": total,
        "category_breakdown": grouped,
        "top_category": top
    }