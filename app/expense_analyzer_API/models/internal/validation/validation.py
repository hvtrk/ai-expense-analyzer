from models.internal.expense.expense import CleanedExpenseData


class ErrorSummary:
    def __init__(self, field: str, count: int):
        self.field = field
        self.count = count


class Issue:
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message


class InvalidRow:
    def __init__(self, row_index: int, issues: list):
        self.row_index = row_index
        self.issues = issues


class ValidationResult:
    """Typed result from validation_service.validate(). No dicts, no raw DataFrames."""

    def __init__(
        self,
        cleaned_data: CleanedExpenseData,
        invalid_rows: list,
        error_summary: list,
        total_rows: int,
        valid_rows: int,
    ):
        self.cleaned_data = cleaned_data
        self.invalid_rows = invalid_rows
        self.error_summary = error_summary
        self.total_rows = total_rows
        self.valid_rows = valid_rows
