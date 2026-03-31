import pandas as pd


class ExpenseRecord:
    def __init__(self, date, amount, category):
        self.date = date
        self.amount = amount
        self.category = category


class CleanedExpenseData:
    """Wraps a validated DataFrame. Keeps raw pandas isolated to ingestion/validation."""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def empty(self) -> bool:
        return self._df.empty
