class DateRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Filter:
    def __init__(self, filter_type):
        self.filter_type = filter_type


class CategoryStat:
    def __init__(self, category, total):
        self.category = category
        self.total = total


class DailyStat:
    def __init__(self, date, total):
        self.date = date
        self.total = total


class ExpenseStats:
    """Typed container for descriptive statistics. Replaces dict-based stats."""

    def __init__(self, mean: float, median: float, variance: float, std_dev: float, count: int):
        self.mean = mean
        self.median = median
        self.variance = variance
        self.std_dev = std_dev
        self.count = count


class StatsResult:
    def __init__(
        self,
        total: float,
        category_breakdown: list[CategoryStat],
        daily_trend: list[DailyStat],
        top_category: str,
        stats: ExpenseStats,
        date_range: DateRange,
    ):
        self.total = total
        self.category_breakdown = category_breakdown
        self.daily_trend = daily_trend
        self.top_category = top_category
        self.stats = stats
        self.date_range = date_range
