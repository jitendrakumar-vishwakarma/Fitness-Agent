"""
Time utility functions
"""

from datetime import datetime, timedelta
from typing import Tuple


def get_week_range(date: datetime = None) -> Tuple[datetime, datetime]:
    """Get start and end of the week for a given date"""
    if date is None:
        date = datetime.now()

    start = date - timedelta(days=date.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return start, end


def get_month_range(date: datetime = None) -> Tuple[datetime, datetime]:
    """Get start and end of the month for a given date"""
    if date is None:
        date = datetime.now()

    start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get last day of month
    if date.month == 12:
        end = date.replace(year=date.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end = date.replace(month=date.month + 1, day=1) - timedelta(days=1)

    end = end.replace(hour=23, minute=59, second=59)

    return start, end


def parse_relative_date(text: str) -> datetime:
    """Parse relative date strings like 'today', 'yesterday', 'last week'"""
    text = text.lower().strip()
    now = datetime.now()

    if text in ["today", "now"]:
        return now
    elif text == "yesterday":
        return now - timedelta(days=1)
    elif text == "last week":
        return now - timedelta(weeks=1)
    elif text == "last month":
        return now - timedelta(days=30)
    else:
        # Try to parse as date
        try:
            return datetime.fromisoformat(text)
        except ValueError:
            return now
