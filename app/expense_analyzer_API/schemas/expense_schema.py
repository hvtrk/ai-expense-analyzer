from fastapi import UploadFile
from fastapi import File
from pydantic import BaseModel, Field
from typing import Dict, Optional

class ExpenseResponse(BaseModel):
    total: int
    category_breakdown: Dict[str, int]
    top_category: Optional[str] = None