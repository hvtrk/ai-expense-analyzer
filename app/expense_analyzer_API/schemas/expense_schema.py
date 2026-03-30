from pydantic import Field
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class Issue(BaseModel):
    field: str
    message: str

class InvalidRow(BaseModel):
    row_index: int
    issues: List[Issue]

class Category(BaseModel):
    category: str
    total: float

class DailySpend(BaseModel):
    date: date
    total: float

class ErrorSummary(BaseModel):
    field: str
    count: int

class DateRange(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None

class Filter(BaseModel):
    filter_type: str = Field(default="") # "last_7_days", "last_30_days", "none"

class Metadata(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    invalid_rows_truncated:int
    date_range: DateRange
    filter: Filter

class StatsSchema(BaseModel):
    mean: float
    median: float
    variance: float
    std_dev: float
    count: int

class ChartResponse(BaseModel):
    category_chart: str
    trend_chart: str

class ExpenseResponse(BaseModel):
    total: float
    category_breakdown: List[Category] = Field(default_factory=list)
    daily_spend_trend: List[DailySpend] = Field(default_factory=list)
    top_category: Optional[str]
    error_summary: List[ErrorSummary] = Field(default_factory=list)
    invalid_rows: List[InvalidRow] = Field(default_factory=list)
    charts: ChartResponse
    metadata: Metadata
    stats: StatsSchema
