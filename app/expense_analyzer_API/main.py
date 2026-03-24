from fastapi import FastAPI
from routes.expense_routes import router as expense_router


app = FastAPI(
    title="Expense Analyzer API",
    description="API for analyzing expenses from a CSV file",
    version="1.0.0"
)

app.include_router(expense_router)
