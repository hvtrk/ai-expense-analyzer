from models.internal.stats.stats import TotalSpendResult, CategoryStat
from utils.logger import logger
from typing import List
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

from db.mapper import to_orm, to_domain
from models.internal.expense.expense import ExpenseRecord
from db.models.transactions import ExpenseTransaction

# Apply Filter
def apply_filters(model, query, batch_id, start_date=None, end_date=None):
    if batch_id:
        query = query.filter(model.batch_id == batch_id)

    if start_date and end_date:
        query = query.filter(model.date.between(start_date, end_date))

    return query

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
def fetch_expenses(db: Session, batch_id: str, start_date:date =None, end_date:date =None) -> List[ExpenseRecord]:
    query = db.query(ExpenseTransaction)

    apply_filters(ExpenseTransaction, query, batch_id, start_date, end_date)

    query = query.order_by(ExpenseTransaction.date.asc())
    results = query.all()

    return [to_domain(row) for row in results]

from sqlalchemy import func

# Get total spend from database
def get_total_spend(db: Session, batch_id: str, start_date:date =None, end_date:date =None) -> TotalSpendResult:
    query = db.query(func.sum(ExpenseTransaction.amount))

    apply_filters(ExpenseTransaction, query, batch_id, start_date, end_date)

    total = query.scalar()
    if total is None:
        total = Decimal("0.0")

    return TotalSpendResult(total)

# Get category breakdown from database
def get_category_breakdown(db: Session, batch_id: str, start_date:date =None, end_date:date =None) -> List[CategoryStat]:
    total_amount = func.sum(ExpenseTransaction.amount)
    query = db.query(ExpenseTransaction.category, total_amount)

    apply_filters(ExpenseTransaction, query, batch_id, start_date, end_date)

    query = query.group_by(ExpenseTransaction.category).order_by(total_amount.desc())
    results = query.all()

    return [CategoryStat(category, total) for category, total in results]
