from schemas.api.response import (
    Category, DailySpend, ErrorSummary, Issue, InvalidRow,
    ChartResponse, Metadata, DateRange, Filter, StatsSchema, ExpenseResponse,
)
from models.internal.stats.stats import StatsResult
from models.internal.validation.validation import ValidationResult
from models.internal.metadata.metadata import Metadata as InternalMetadata
from services.visualization_service import ChartData
from utils.math_utils import safe_float

MAX_ERRORS = 100


def response_mapper(
    stats_result: StatsResult,
    validation_result: ValidationResult,
    metadata: InternalMetadata,
    charts: ChartData,
) -> ExpenseResponse:

    category_breakdown = [
        Category(category=cat.category, total=cat.total)
        for cat in stats_result.category_breakdown
    ]

    daily_spend_trend = [
        DailySpend(date=d.date, total=d.total)
        for d in stats_result.daily_trend
    ]

    error_summary = [
        ErrorSummary(field=item.field, count=item.count)
        for item in validation_result.error_summary
    ]

    invalid_rows = [
        InvalidRow(
            row_index=row.row_index,
            issues=[
                Issue(field=issue.field, message=issue.message)
                for issue in row.issues
            ],
        )
        for row in validation_result.invalid_rows
    ]

    return ExpenseResponse(
        total=stats_result.total,
        category_breakdown=category_breakdown,
        daily_spend_trend=daily_spend_trend,
        top_category=stats_result.top_category,
        error_summary=error_summary,
        invalid_rows=invalid_rows,
        charts=ChartResponse(
            category_chart=charts.category_chart,
            trend_chart=charts.trend_chart,
        ),
        metadata=Metadata(
            total_rows=metadata.total_rows,
            valid_rows=metadata.valid_rows,
            invalid_rows=metadata.invalid_rows,
            invalid_rows_truncated=metadata.invalid_rows > MAX_ERRORS,
            date_range=DateRange(
                start=metadata.date_range.start,
                end=metadata.date_range.end,
            ),
            filter=Filter(filter_type=metadata.filter_type),
        ),
        stats=StatsSchema(
            mean=safe_float(stats_result.stats.mean),
            median=safe_float(stats_result.stats.median),
            variance=safe_float(stats_result.stats.variance),
            std_dev=safe_float(stats_result.stats.std_dev),
            count=int(stats_result.stats.count),
        ),
    )
