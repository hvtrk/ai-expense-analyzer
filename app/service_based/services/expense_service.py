import pandas as pd

def load_expenses(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def clean_data(df):
    df['category'] = df['category'].str.strip().str.lower()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    return df.dropna(subset=['category', 'amount'])


def calculate_total(df):
    return df['amount'].sum()


def group_by_category(df):
    return df.groupby('category')['amount'].sum().to_dict()


def get_top_category(grouped):
    if not grouped:
        return None
    return max(grouped, key=grouped.get)


def analyze_expenses(file_path: str) -> dict:
    df = load_expenses(file_path)
    if df is None:
        return None
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