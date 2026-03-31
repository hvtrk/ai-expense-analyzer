from fastapi import UploadFile
from services import ingestion_service, validation_service, stats_service
from models.internal.validation.validation import ValidationResult
from models.internal.stats.stats import StatsResult
from models.internal.metadata.metadata import Metadata


def build_metadata(validation_result: ValidationResult, stats_result: StatsResult, filter_type: str) -> Metadata:
    """Build response metadata from typed validation and stats results."""
    return Metadata(
        total_rows=validation_result.total_rows,
        valid_rows=validation_result.valid_rows,
        invalid_rows=len(validation_result.invalid_rows),
        date_range=stats_result.date_range,
        filter_type=filter_type,
    )


async def run_pipeline(file: UploadFile, filter_type: str = 'none', include_charts: bool = True):
    df = await ingestion_service.load(file)

    validation_result = validation_service.validate(df)

    stats_result = stats_service.compute_stats(
        validation_result.cleaned_data,
        filter_type,
    )

    metadata = build_metadata(validation_result, stats_result, filter_type)

    return stats_result, validation_result, metadata
