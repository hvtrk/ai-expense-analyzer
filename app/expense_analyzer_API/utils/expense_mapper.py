from schemas.expense_schema import Category, ExpenseResponse, ErrorSummary, DateRange, Filter, InvalidRow, Issue, Metadata, StatsSchema, DailySpend, ChartResponse
from services.expense_service import safe_float
import logging

logger = logging.getLogger(__name__)

def expense_response_mapper(result: dict) -> ExpenseResponse:
    category_data = result.get("category_breakdown", {})
    if not isinstance(category_data, dict):
        logger.warning("Invalid category_breakdown format")
        category_data = {}

    category_breakdown = [
        Category(category=category, total=amount)
        for category, amount in category_data.items()
    ]

    daily_spend_trend_data = result.get("daily_spend_trend", {})
    if not isinstance(daily_spend_trend_data, dict):
        daily_spend_trend_data = {}
        logger.warning("Invalid daily_spend_trend format")

    daily_spend_trend = [
        DailySpend(date=date, total=amount)
        for date, amount in daily_spend_trend_data.items()
    ]

    error_summary_data = result.get("error_summary", {})
    if not isinstance(error_summary_data, dict):
        error_summary_data = {}
        logger.warning("Invalid error_summary format")

    error_summary = [
        ErrorSummary(field=field, count=count)
        for field, count in error_summary_data.items()
    ]

    invalid_rows_data = result.get("invalid_rows")
    if not isinstance(invalid_rows_data, list):
        invalid_rows_data = []
    invalid_rows = []
    for row in invalid_rows_data:
        if not isinstance(row, dict):
            continue
        issues_data = row.get("issues", [])
        if not isinstance(issues_data, list):
            issues_data = []
        issues = [
            Issue(
                field=issue.get("field", ""),
                message=issue.get("message", "")
            )
            for issue in issues_data
            if isinstance(issue, dict)
        ]
        invalid_rows.append(
            InvalidRow(
                row_index=row.get("row_index", -1),
                issues=issues
            )
        )

    return ExpenseResponse(
        total=result.get("total", 0.0),
        category_breakdown=category_breakdown,
        daily_spend_trend=daily_spend_trend,
        top_category=result.get("top_category", None),
        error_summary=error_summary,
        invalid_rows=invalid_rows,
        charts=ChartResponse(
            category_chart=result.get("charts", {}).get("category_chart", ""),
            trend_chart=result.get("charts", {}).get("trend_chart", "")
        ),
        metadata= Metadata(
            total_rows=result.get("metadata", {}).get("total_rows", 0),
            valid_rows=result.get("metadata", {}).get("valid_rows", 0),
            invalid_rows=result.get("metadata", {}).get("invalid_rows", 0),
            invalid_rows_truncated=result.get("metadata", {}).get("invalid_rows_truncated", False),
            date_range=DateRange(
                start=result.get("metadata", {}).get("date_range", {}).get("start", None),
                end=result.get("metadata", {}).get("date_range", {}).get("end", None)
            ),
            filter=Filter(
                filter_type=result.get("metadata", {}).get("filter", {}).get("filter_type", "none")
            )
        ),
        stats=StatsSchema(
            mean=safe_float(result.get("stats", {}).get("mean", 0.0)),
            median=safe_float(result.get("stats", {}).get("median", 0.0)),
            variance=safe_float(result.get("stats", {}).get("variance", 0.0)),
            std_dev=safe_float(result.get("stats", {}).get("std_dev", 0.0)),
            count=int(result.get("stats", {}).get("count", 0))
        )
    )
