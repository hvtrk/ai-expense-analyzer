from pydantic import BaseModel
from typing import Dict, Optional, List

class Issue(BaseModel):
    field: str
    issue: str

class InvalidRow(BaseModel):
    row: int
    issues: List[Issue]

class ExpenseResponse(BaseModel):
    total: float
    category_breakdown: Dict[str, float]
    top_category: Optional[str] = None
    error_summary: Dict[str, int] = {}
    invalid_rows: List[InvalidRow] = []
    valid_row_count: int
    invalid_row_count: int
    total_row_count: int
