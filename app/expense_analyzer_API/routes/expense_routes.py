from fastapi import APIRouter, HTTPException, UploadFile, File
from schemas.expense_schema import ExpenseResponse
from services.expense_service import analyze_expenses
from utils.exception_handler import FileValidationError, SchemaValidationError

router = APIRouter()

@router.post("/analyze-expenses", response_model=ExpenseResponse)
async def analyze_expenses_api(file: UploadFile = File(..., media_type="text/csv", description="Path to the CSV file")):
    try:
        result = await analyze_expenses(file)
        return result
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SchemaValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
