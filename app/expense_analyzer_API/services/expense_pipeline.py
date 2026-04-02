from utils.logger import logger
import uuid
from fastapi import UploadFile
from services import ingestion_service, validation_service, stats_service
from db.connections.session import SessionLocal
from db import repository
from models.internal.validation.validation import ValidationResult
from models.internal.stats.stats import StatsResult
from models.internal.metadata.metadata import Metadata
from models.internal.expense.expense import CleanedExpenseData

def build_metadata(validation_result: ValidationResult, stats_result: StatsResult, filter_type: str) -> Metadata:
    """Build response metadata from typed validation and stats results."""
    return Metadata(
        total_rows=validation_result.total_rows,
        valid_rows=validation_result.valid_rows,
        invalid_rows=len(validation_result.invalid_rows),
        date_range=stats_result.date_range,
        filter_type=filter_type,
    )
def generate_batch_id() -> str:
    return str(uuid.uuid4())


async def run_pipeline(file: UploadFile, filter_type: str = 'none'):
    if filter_type not in ("last_7_days", "last_30_days", "none"):
        raise ValueError("Invalid filter type")

    df = await ingestion_service.load(file)

    validation_result = validation_service.validate(df)

    db = SessionLocal()
    try:
        batch_id = generate_batch_id()
        repository.save_expenses(
            db,
            validation_result.cleaned_data.to_records(),
            batch_id
        )
        fetched_expenses = repository.fetch_expenses(db, filter_type)
        stats_result = stats_service.compute_stats(
            CleanedExpenseData.from_records(fetched_expenses),
            filter_type,
        )
    except Exception as e:
        logger.error(f"Error in pipeline: {e}")
        db.rollback()
        db.close()
        raise
    finally:
        db.close()

    metadata = build_metadata(validation_result, stats_result, filter_type)

    return stats_result, validation_result, metadata
