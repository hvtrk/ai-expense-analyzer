from fastapi import FastAPI, UploadFile
from routes.expense_routes import router as expense_router


app = FastAPI()

app.include_router(expense_router)