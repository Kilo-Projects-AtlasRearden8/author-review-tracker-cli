from __future__ import annotations

from datetime import date, datetime, timedelta, timezone


def parse_iso(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value)


def days_between(start: str | None, end: str | None = None) -> int | None:
    """Whole days between two ISO timestamps. ``end`` defaults to now."""
    start_dt = parse_iso(start)
    end_dt = parse_iso(end) if end else datetime.now(timezone.utc)
    if start_dt is None:
        return None
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    return (end_dt - start_dt).days


def follow_up_due_date(requested_at: str | None, days: int = 7) -> str | None:
    """ISO date when a follow-up is due, ``days`` after the request."""
    start_dt = parse_iso(requested_at)
    if start_dt is None:
        return None
    due = start_dt + timedelta(days=days)
    return due.date().isoformat()


def is_overdue(requested_at: str | None, days: int = 7) -> bool:
    """True if the follow-up window has passed."""
    due = follow_up_due_date(requested_at, days)
    if due is None:
        return False
    return date.today() > date.fromisoformat(due)
