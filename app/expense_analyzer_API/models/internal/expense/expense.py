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

    def to_records(self) -> list[ExpenseRecord]:
        return [
            ExpenseRecord(
                date=row['date'],
                amount=row['amount'],
                category=row['category']
            )
            for row in self._df.to_dict(orient='records')
        ]

    @classmethod
    def from_records(cls, records: list[ExpenseRecord]) -> 'CleanedExpenseData':
        if not records:
            return cls(pd.DataFrame(columns=['date', 'amount', 'category']))
        return cls(pd.DataFrame([
            {'date': r.date, 'amount': r.amount, 'category': r.category}
            for r in records
        ]))
