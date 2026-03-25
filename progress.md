# Progress Log

## Day 1–2
- FastAPI backend setup
- CSV upload (in-memory)
- Pandas processing
- Category aggregation
- Basic validation

### Issues:
- Weak validation design
- Silent data drops
- API response not structured

---

## Day 3 — Validation System (Production-Grade)

### Objective
Build a strict validation layer to eliminate silent data corruption and enforce data integrity before analytics.

---

### What Was Built

#### 1. Schema Validation
- Enforced required columns: `date`, `amount`, `category`
- Fail-fast approach for:
  - Missing columns
  - Empty files

---

#### 2. Row-Level Validation Engine
- Implemented validation rules:
  - `amount > 0`
  - `amount` must be numeric
  - `category` must be non-empty and non-numeric
  - `date` must follow strict `YYYY-MM-DD` format
- Structured error output:
  ```json
  {
    "row": 1,
    "issues": [
      { "field": "amount", "issue": "..." }
    ]
  }
  ```

---

#### 3. Partial Processing (Critical Improvement)
- System now:
  - Processes valid rows
  - Separates invalid rows
  - Avoids silent data drops

---

#### 4. Vectorized Validation (Performance Optimization)
- Replaced `iterrows()` with Pandas mask-based validation
- Implemented:
  - amount_invalid
  - category_invalid
  - date_invalid
- Reduced loop scope:
  - Loop runs only on invalid rows
- Used `.loc` for correct row + column selection

---

#### 5. Data Pipeline Flow (Corrected)

Upload → Load → Schema Validate → Clean → Row Validate → Analyze

---

#### 6. Error Aggregation Layer
- Added error_summary:
  ```json
  {
    "category": 2,
    "amount": 1
  }
  ```

---

#### 7. Exception System
- Introduced:
  - FileValidationError
  - SchemaValidationError

---

#### 8. API Contract (Initial)
- Introduced Pydantic response model
- Structured response with:
  - totals
  - category breakdown
  - invalid rows
  - error summary

---

### Key Learnings

- Silent data corruption is the biggest risk in data systems
- Validation must be explicit, structured, and non-destructive
- Vectorization is critical for performance in Pandas
- `.loc` is required for correct row + column selection
- Separation of concerns is non-negotiable

---

### Outcome

- Built a production-grade validation system
- Eliminated silent failures
