from __future__ import annotations

import csv

from .storage import Store


def export_requests(store: Store, path: str) -> int:
    """Export review requests (with reader names) to CSV. Returns row count."""
    readers = {r.id: r for r in store.list_readers()}
    requests = store.list_requests()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "id", "reader_id", "reader_name", "book_title", "status",
            "format", "requested_at", "sent_at", "received_at",
        ])
        for request in requests:
            reader = readers.get(request.reader_id)
            writer.writerow([
                request.id,
                request.reader_id,
                reader.name if reader else "",
                request.book_title,
                request.status,
                request.format,
                request.requested_at,
                request.sent_at or "",
                request.received_at or "",
            ])
    return len(requests)
