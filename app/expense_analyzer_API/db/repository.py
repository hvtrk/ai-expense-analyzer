from models.internal.stats.stats import TotalSpendResult
from utils.logger import logger
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from db.mapper import to_orm, to_domain
from models.internal.expense.expense import ExpenseRecord
from db.models.transactions import ExpenseTransaction

# Save cleaned data to database
def save_expenses(db: Session, records: List[ExpenseRecord], batch_id: str) -> None:
    orm_objects = [to_orm(record, batch_id) for record in records]

    try:
        db.add_all(orm_objects)
        db.commit()
        logger.info(f"Batch {batch_id} saved with {len(records)} records")
    except Exception:
        db.rollback()
        raise

# Fetch cleaned data from database
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

from sqlalchemy import func

# Get total spend from database
def get_total_spend(db: Session, batch_id: str, start_date=None, end_date=None) -> TotalSpendResult:
    query = db.query(func.sum(ExpenseTransaction.amount))

    if batch_id:
        query = query.filter(ExpenseTransaction.batch_id == batch_id)

    if start_date:
        query = query.filter(ExpenseTransaction.date >= start_date)

    if end_date:
        query = query.filter(ExpenseTransaction.date <= end_date)

    total = query.scalar() or 0.0

    return TotalSpendResult(total)
