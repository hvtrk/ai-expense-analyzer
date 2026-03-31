# Expense Analyzer API — Architecture & Snapshot Guide

## Project Overview
This document represents the current architectural snapshot of the FastAPI application located exclusively in `app/expense_analyzer_API`.

This backend application processes, validates, and analyzes user expenses using a strictly enforced **Clean Architecture**, completely decoupling API schemas from internal business logic and preserving pandas `DataFrame` operations rigidly within explicit internal validation limits.

## Directory Structure
```text
app/expense_analyzer_API/
├── main.py             # FastAPI App Entrypoint
├── expenses.csv        # Localized dataset
│
├── routes/             # Controller layer defining API endpoints
│   └── expense_routes.py
│
├── schemas/api/        # Defines Pydantic Models for Web Contracts
│   ├── request.py
│   ├── response.py
│   └── mapper.py       # Exclusively maps internal models to Pydantic responses
│
├── services/           # Business Logic layer
│   ├── expense_pipeline.py      # Orchestrator (Coordinates ingestion -> stats -> visualization)
│   ├── ingestion_service.py     # Data extraction
│   ├── validation_service.py    # Rule-sets, normalizing, and calculating errors
│   ├── stats_service.py         # Expense computations (averages, grouping lists)
│   └── visualization_service.py # Generates base64-encoded visual plots
│
├── models/internal/    # Internal DTOs representing state (NO DICTS AT BOUNDARIES)
│   ├── expense/expense.py       # Holds CleanedExpenseData (Wrapper for DataFrame)
│   ├── stats/stats.py           # StatsResult, CategoryStat, DailyStat
│   ├── validation/validation.py # ValidationResult, InvalidRow, ErrorSummary (Internal)
│   └── metadata/metadata.py     # Explicit strictly-typed metadata tracking container
│
├── core/
│   └── exceptions.py   # Global Exception Handlers
│
└── utils/
    └── math_utils.py   # Float formatting wrappers
```

---

## Architectural Data Flow
The orchestration is exclusively handled by `services/expense_pipeline.py`. Here is how the sequence acts sequentially, adhering strictly to bounded contexts:

1. **Ingestion**: The `csv` payload drops into `ingestion_service` and produces a raw `pandas.DataFrame`.
2. **Validation**: The raw `DataFrame` routes to `validation_service.py`. Bad rows are logged as internal `InvalidRow` objects, Error frequencies are aggregated as `ErrorSummary` lists, and the payload is successfully normalized into a `CleanedExpenseData` wrapper object.
3. **Computation**: The `.df` is executed securely inside `stats_service.py`, tracking date-windows and outputting explicit lists of `CategoryStat`, `DailyStat`, and `ExpenseStats` objects merged tightly into a `StatsResult`.
4. **Metadata Extraction**: Context is constructed natively returning a `Metadata` internal object.
5. **Chart Generation**: `StatsResult` native objects are passed into `visualization_service.py` natively extracting list metrics to return `ChartData`.
6. **API Orchestration**: The sequence drops the compiled sequence of objects safely over the boundary back to the API Route (`route -> pipeline -> route`).
7. **Mapping Interface**: The API passes the resulting internal objects into `schemas/api/mapper.py`. The mapper strictly traverses native object parameters (zero iteration checks or aggregation intelligence allowed here) returning final explicitly typed Pydantic objects.

---

## Strict Behavioral Constraints & Guidelines (For AI Agents)
Any future agent traversing, auditing, or adding to this specific FastAPI codebase (`app/expense_analyzer_API`) MUST comprehend and strictly abide by these 5 rules:

1. **Zero Dictionary Tolerance**: Dicts (`{}`, `dict[str, type]`) are strictly banned from crossing inter-service boundaries. Functions can build frequency maps internally, but they MUST transform into instances of explicit Typed classes (`list[DailyStat]`, `list[ErrorSummaryInternal]`, etc.) before being returned across the service layer.
2. **No Logic Inside Mappers**: `schemas/api/mapper.py` exists EXCLUSIVELY to map internal objects `A -> B` onto API models. No default `.get()` fallbacks, aggregation loops, or decision mechanics are allowed inside the mapping layer. It must be "dumb" transformation.
3. **No Tuple Returns Across Services**: Function responses across `services/` must return explicit objects wrapping the variables. The only acceptable tuple boundary crosses uniquely from `expense_pipeline` output directly to the `FastAPI Router` handler.
4. **DataFrames Boundary Box**: The pandas `DataFrame` is an internal utility explicitly designed to only belong safely inside `validation_service.py` and `stats_service.py`. It is passed around exclusively inside the structured `CleanedExpenseData` box instance. It must NEVER cross into `mapper.py` or `expense_routes.py`.
5. **No Mixed Layers**: Internal representations (everything residing in `models/internal/`) must never be marked with `pydantic.BaseModel`. API contracts (`schemas/api/response.py`) must never leak their rules deep into the interior algorithm implementations.
