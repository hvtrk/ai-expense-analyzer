import numpy as np
import pandas as pd

np.random.seed(42)

n = 50000

# Base clean dataset
df = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=n, freq="h"),
    "category": np.random.choice(
        ["food", "travel", "shopping", "bills", "health"], n
    ),
    "amount": np.random.normal(500, 200, n)
})

# -----------------------------
# 🔥 Introduce Realistic Noise
# -----------------------------

# 1. Missing values (NaN)
nan_indices = np.random.choice(df.index, int(0.05 * n), replace=False)
df.loc[nan_indices, "amount"] = np.nan

# 2. Invalid date formats
invalid_date_indices = np.random.choice(df.index, int(0.02 * n), replace=False)
df["date"] = df["date"].astype(object)
df.loc[invalid_date_indices, "date"] = "invalid_date"

# 3. Negative values (invalid business logic)
negative_indices = np.random.choice(df.index, int(0.03 * n), replace=False)
df.loc[negative_indices, "amount"] = -abs(df.loc[negative_indices, "amount"])

# 4. Extreme outliers
outlier_indices = np.random.choice(df.index, int(0.01 * n), replace=False)
df.loc[outlier_indices, "amount"] = df["amount"].mean() * 50

# 5. Category noise (case + whitespace + typos)
def corrupt_category(cat):
    if np.random.rand() < 0.3:
        return cat.upper()
    elif np.random.rand() < 0.6:
        return f" {cat} "
    elif np.random.rand() < 0.8:
        return cat[:3]  # truncated
    return cat

df["category"] = df["category"].apply(corrupt_category)

# 6. Duplicate rows
duplicate_indices = np.random.choice(df.index, int(0.02 * n), replace=False)
duplicates = df.loc[duplicate_indices]
df = pd.concat([df, duplicates], ignore_index=True)

# 7. Mixed types in amount column (strings injected)
string_indices = np.random.choice(df.index, int(0.02 * n), replace=False)
df["amount"] = df["amount"].astype(object)
df.loc[string_indices, "amount"] = "invalid_amount"

# -----------------------------
# Save dataset
# -----------------------------
# df.to_csv("noisy_expense_dataset.csv", index=False)
df.to_csv("app/expense_analyzer_API/expenses.csv", index=False)

print("Dataset generated: app/expense_analyzer_API/expenses.csv")
print(f"Total rows: {len(df)}")
