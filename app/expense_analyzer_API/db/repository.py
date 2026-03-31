from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from db.mapper import to_orm, to_domain
from models.internal.expense.expense import ExpenseRecord
from db.models.transactions import ExpenseTransaction


def save_expenses(db: Session, records: List[ExpenseRecord], batch_id: str) -> None:
    orm_objects = [to_orm(record, batch_id) for record in records]

    try:
        db.add_all(orm_objects)
        db.commit()
    except Exception:
        db.rollback()
        raise


def fetch_expenses(db: Session, filter_type: str) -> List[ExpenseRecord]:
    query = db.query(ExpenseTransaction)

    if filter_type == "last_7_days":
        cutoff = datetime.utcnow().date() - timedelta(days=7)
        query = query.filter(ExpenseTransaction.date >= cutoff)

    elif filter_type == "last_30_days":
        cutoff = datetime.utcnow().date() - timedelta(days=30)
        query = query.filter(ExpenseTransaction.date >= cutoff)

    query = query.order_by(ExpenseTransaction.date.asc())
    results = query.all()

    return [to_domain(row) for row in results]
