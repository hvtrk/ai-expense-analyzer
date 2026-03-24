#!/bin/bash
. .venv/bin/activate
cd app/expense_analyzer_API/
uvicorn main:app --reload
