from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, Numeric, Date
from sqlalchemy.sql import func
from db.connections.base import Base

class ExpenseTransaction(Base):
    __tablename__ = "expense_transactions"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    batch_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("batch_id", "date", "amount", "category", name="uq_expense_record"),
    )

    def __repr__(self):
        return f"<ExpenseTransaction(id={self.id}, date={self.date}, category={self.category}, amount={self.amount})>"
