from datetime import datetime
from models.internal.stats.stats import StatsResult, CategoryStat, DailyStat
import matplotlib.pyplot as plt
import io
import base64


class ChartData:
    """Typed container for generated chart images (base64-encoded)."""

    def __init__(self, category_chart: str, trend_chart: str):
        self.category_chart = category_chart
        self.trend_chart = trend_chart


def generate_category_chart(data: list[CategoryStat]) -> str:
    if not data:
        return ""
    categories = [c.category for c in data]
    values = [c.total for c in data]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(categories, values)
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Category Breakdown")
    ax.tick_params(axis='x', rotation=90)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return base64_string


def generate_trend_chart(data: list[DailyStat]) -> str:
    if not data:
        return ""
    dates = [datetime.strptime(d.date, "%Y-%m-%d") for d in data]
    values = [d.total for d in data]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Daily Spend Trend")
    ax.tick_params(axis='x', rotation=90)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return base64_string


def generate(stats_result: StatsResult) -> ChartData:
    category_chart = generate_category_chart(stats_result.category_breakdown)
    trend_chart = generate_trend_chart(stats_result.daily_trend)
    return ChartData(
        category_chart=category_chart,
        trend_chart=trend_chart,
    )
