from decimal import Decimal
from db.models.transactions import ExpenseTransaction
from models.internal.expense.expense import ExpenseRecord


def to_domain(record: ExpenseTransaction) -> ExpenseRecord:
    return ExpenseRecord(
        date=record.date,
        amount=float(record.amount),
        category=record.category,
    )


def to_orm(record: ExpenseRecord, batch_id: str) -> ExpenseTransaction:
    return ExpenseTransaction(
        date=record.date,
        amount=Decimal(str(record.amount)),
        category=record.category,
        batch_id=batch_id,
    )
