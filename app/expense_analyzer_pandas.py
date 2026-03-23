import pandas as pd
import sys

def load_expenses(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    # df.info()
    # df.head()
    return df 

def clean_data(df):
    df['category'] = df['category'].str.strip().str.lower()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    new_df = df.dropna()
    new_df['amount'] = new_df['amount'].astype(int)
    return new_df

def calculate_totals(df):
    return df['amount'].sum()

def group_by_category(df):
    return df.groupby('category')['amount'].sum().sort_values(ascending=False)

def get_top_category(df):
    df.sort_values(ascending=False, inplace=True)
    return df.head(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        return

    file_path = sys.argv[1]
    expenses = load_expenses(file_path)
    cleaned_expenses = clean_data(expenses)
    total = calculate_totals(cleaned_expenses)
    grouped = group_by_category(cleaned_expenses)
    top = get_top_category(grouped)
    
    print(f"Total Expenses: ₹{total}")
    for cat, amount in grouped.items():
        print(f"{cat}: ₹{amount}")
    print(f"Top Category: {top.index[0]}")


if __name__ == "__main__":
    main()