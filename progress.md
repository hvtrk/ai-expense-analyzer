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

## Day 3

### Planned:

- Implement strict validation system
- Prevent silent data corruption
- Introduce structured error reporting

### Completed:

- Schema validation (required columns, empty file handling)
- Row-level validation with detailed issue tracking
- Partial processing (valid + invalid row separation)
- Clean data pipeline (load → validate → clean → analyze)
- Custom exception handling (file + schema errors)
- Structured API response using Pydantic
- Error summary aggregation for data quality insights

## Hours:
- 5 Hours 15 Mins

## What Broke:

- Initial mixing of validation and service responsibilities
- Incorrect validation order causing potential runtime failures
- Weak exception handling design

## Fix:

- Refactored validation into pure layer
- Reordered pipeline (schema → clean → row validation)
- Introduced custom exception system
- Removed unnecessary abstractions and duplicate checks

## Learning:

- Importance of strict data validation before analytics
- Clear separation of concerns across layers
- Designing APIs with structured, predictable contracts
- Avoiding silent failures in data pipelines

## Next:

- Day 4: API contract redesign (nested schemas, stronger typing)
