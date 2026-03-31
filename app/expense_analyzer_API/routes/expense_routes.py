from services import expense_pipeline, visualization_service
from schemas.api import mapper
from fastapi import APIRouter, HTTPException, UploadFile, File
from schemas.api.response import ExpenseResponse
from core.exceptions import FileValidationError, SchemaValidationError, QueryValidationError
from services.visualization_service import ChartData

router = APIRouter()

@router.post("/analyze-expenses", response_model=ExpenseResponse)
async def analyze_expenses_api(
    file: UploadFile = File(..., media_type="text/csv", description="Path to the CSV file"),
    filter: str = 'none',
    include_charts: bool = True,
):
    try:
        stats_result, validation_result, metadata = await expense_pipeline.run_pipeline(file, filter_type=filter)

        charts = ChartData(category_chart="", trend_chart="")
        if include_charts:
            charts = visualization_service.generate(stats_result)

        mapped_response = mapper.response_mapper(stats_result, validation_result, metadata, charts)
        return mapped_response
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SchemaValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except QueryValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
