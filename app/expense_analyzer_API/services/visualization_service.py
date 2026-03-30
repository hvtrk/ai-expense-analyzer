from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

def generate_category_chart(data):
    if not data:
        return ""
    # extract categories + values
    categories = [category for category, amount in data.items()]
    values = [amount for category, amount in data.items()]
    # create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(categories, values)
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Category Breakdown")
    ax.tick_params(axis='x', rotation=90)
    fig.tight_layout()
    # save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    # convert to base64
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return base64_string

def generate_trend_chart(data):
    if not data:
        return ""
    # line plot
    dates = [datetime.strptime(date, "%Y-%m-%d") for date, amount in data.items()]
    values = [amount for date, amount in data.items()]
    # proper date sorting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Daily Spend Trend")
    ax.tick_params(axis='x', rotation=90)
    fig.tight_layout()
    # save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    # convert to base64
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return base64_string
