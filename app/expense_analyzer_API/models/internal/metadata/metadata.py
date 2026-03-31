class Metadata:
    def __init__(self, total_rows: int, valid_rows: int, invalid_rows: int, date_range, filter_type: str):
        self.total_rows = total_rows
        self.valid_rows = valid_rows
        self.invalid_rows = invalid_rows
        self.date_range = date_range
        self.filter_type = filter_type
