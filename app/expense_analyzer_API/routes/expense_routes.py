from utils.expense_mapper import expense_response_mapper
from fastapi import APIRouter, HTTPException, UploadFile, File
from schemas.expense_schema import ExpenseResponse
from services.expense_service import analyze_expenses
from utils.exception_handler import FileValidationError, SchemaValidationError

router = APIRouter()

@router.post("/analyze-expenses", response_model=ExpenseResponse)
async def analyze_expenses_api(file: UploadFile = File(..., media_type="text/csv", description="Path to the CSV file"), filter: str = 'none'):
    try:
        result = await analyze_expenses(file, filter_type = filter)
        mapped_result = expense_response_mapper(result)
        return mapped_result
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SchemaValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except QueryValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
