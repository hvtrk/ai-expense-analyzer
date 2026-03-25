# AI Expense Analyzer (AI Engineering Sprint)

## Objective
Build a production-grade AI-powered backend system for expense analysis, prediction, and insights.

---

## 🚀 Current Capabilities (Day 3)

### Validation System (Production-Grade)

A robust data validation layer ensures data integrity before processing.

### Key Features

- Schema Validation (date, amount, category)
- Row-Level Validation
- Partial Processing (valid + invalid separation)
- Structured Error Reporting
- Vectorized Performance Optimization

---

### Example API Response

```json
{
  "total": 3350,
  "category_breakdown": {
    "travel": 1700,
    "shopping": 1000,
    "food": 650
  },
  "top_category": "travel",
  "error_summary": {
    "category": 2
  },
  "valid_row_count": 7,
  "invalid_row_count": 2,
  "total_row_count": 9
}
```

---

## 🧱 Architecture

Routes → Services → Validation → Processing

---

## 🛠 Tech Stack

- FastAPI
- Python (Pandas, NumPy)
- scikit-learn (planned)
- LLM APIs (planned)

---

## 📈 Features (Planned)

- Data ingestion API ✅
- Validation system ✅
- Data processing 🔄
- ML predictions
- LLM insights
- RAG assistant

---

## 📊 Progress Tracking
See [progress.md](progress.md)
