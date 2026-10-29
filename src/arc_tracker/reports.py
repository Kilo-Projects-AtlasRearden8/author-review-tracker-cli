from __future__ import annotations

from .storage import Store


def compute_totals(store: Store) -> dict:
    readers = store.list_readers()
    requests = store.list_requests()
    followups = store.list_followups()
    by_status: dict[str, int] = {}
    for request in requests:
        status = request.status or "pending"
        by_status[status] = by_status.get(status, 0) + 1
    return {
        "readers": len(readers),
        "requests": len(requests),
        "followups": len(followups),
        "by_status": by_status,
        "pending": by_status.get("pending", 0),
        "mailed": by_status.get("mailed", 0),
        "received": by_status.get("received", 0),
        "declined": by_status.get("declined", 0),
    }
