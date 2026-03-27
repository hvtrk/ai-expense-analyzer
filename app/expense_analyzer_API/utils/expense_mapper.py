from schemas.expense_schema import Category, ExpenseResponse, ErrorSummary, DateRange, Filter, InvalidRow, Issue, Metadata, StatsSchema

def expense_response_mapper(result: dict) -> ExpenseResponse:
    return ExpenseResponse(
        total=result["total"],
        category_breakdown=[Category(category=category, total=amount) for category, amount in result["category_breakdown"].items()],
        top_category=result["top_category"],
        error_summary=[ErrorSummary(field=field, count=count) for field, count in result["error_summary"].items()],
        invalid_rows=[InvalidRow(row_index=row["row_index"], issues=[Issue(field=issue["field"], message=issue["message"]) for issue in row["issues"]]) for row in result["invalid_rows"]],
        metadata= Metadata(
            total_rows=result["metadata"]["total_rows"],
            valid_rows=result["metadata"]["valid_rows"],
            invalid_rows=result["metadata"]["invalid_rows"],
            invalid_rows_truncated=result["metadata"]["invalid_rows_truncated"],
            date_range=DateRange(
                start=result["metadata"]["date_range"]["start"],
                end=result["metadata"]["date_range"]["end"]
            ),
            filter=Filter(
                filter_type=result["metadata"]["filter"]["filter_type"]
            )
        ),
        stats=StatsSchema(
            mean=result["stats"]["mean"],
            median=result["stats"]["median"],
            variance=result["stats"]["variance"],
            std_dev=result["stats"]["std_dev"],
            count=result["stats"]["count"]
        )
    )
