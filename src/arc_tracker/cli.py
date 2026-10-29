from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timezone
from typing import List, Optional

from .date_utils import days_between, follow_up_due_date, is_overdue
from .export import export_requests
from .models import ReviewRequest
from .reports import compute_totals
from .storage import Store


DEFAULT_DATA_PATH = os.path.expanduser("~/.arc_tracker/data.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arc-tracker",
        description=(
            "Track ARC readers, review requests, and follow-ups with "
            "local JSON storage and CSV export. No accounts, no keys."
        ),
    )
    parser.add_argument(
        "--data",
        default=os.environ.get("ARC_TRACKER_DATA", DEFAULT_DATA_PATH),
        help="Path to the JSON storage file (default: %(default)s)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-reader", help="Add a new ARC reader")
    p.add_argument("--name", required=True, help="Reader name")
    p.add_argument("--email", default="", help="Reader email")
    p.add_argument("--genre", default="", help="Preferred genre")

    sub.add_parser("list-readers", help="List all readers")

    p = sub.add_parser("request", help="Request a review from a reader")
    p.add_argument("--reader", required=True, help="Reader id")
    p.add_argument("--book", required=True, help="Book title")
    p.add_argument("--format", default="ebook", help="ARC format (ebook, paperback, etc.)")

    p = sub.add_parser("list-requests", help="List all review requests")
    p.add_argument("--status", default=None, help="Filter by status (pending, mailed, received, declined)")

    p = sub.add_parser("follow-up", help="Log a follow-up for a review request")
    p.add_argument("--request", required=True, help="Request id")
    p.add_argument("--date", default=None, help="Follow-up date (YYYY-MM-DD); defaults to today")
    p.add_argument("--note", default="", help="Follow-up notes")

    p = sub.add_parser("mark-sent", help="Mark a request as mailed/sent")
    p.add_argument("--request", required=True, help="Request id")

    p = sub.add_parser("mark-received", help="Mark a request as received")
    p.add_argument("--request", required=True, help="Request id")

    p = sub.add_parser("mark-declined", help="Mark a request as declined")
    p.add_argument("--request", required=True, help="Request id")

    sub.add_parser("totals", help="Show totals for readers, requests, and follow-ups")

    p = sub.add_parser("export", help="Export review requests to CSV")
    p.add_argument("--out", required=True, help="Output CSV path")

    p = sub.add_parser("due", help="List requests whose follow-up is due or overdue")
    p.add_argument("--days", type=int, default=7, help="Follow-up window in days (default: 7)")

    return parser


def _print_readers(store: Store) -> int:
    readers = store.list_readers()
    if not readers:
        print("No readers yet.")
        return 0
    print(f"{'ID':<16} {'NAME':<30} {'EMAIL':<30} {'GENRE'}")
    print("-" * 90)
    for r in readers:
        print(f"{r.id:<16} {r.name:<30} {r.email:<30} {r.genre}")
    return 0


def _print_requests(store: Store, status: Optional[str]) -> int:
    requests = store.list_requests()
    readers = {r.id: r for r in store.list_readers()}
    if status:
        requests = [r for r in requests if r.status == status]
    if not requests:
        print("No requests.")
        return 0
    print(f"{'ID':<16} {'READER':<28} {'BOOK':<34} {'STATUS':<10} {'FORMAT'}")
    print("-" * 95)
    for r in requests:
        reader = readers.get(r.reader_id)
        name = reader.name if reader else "(unknown)"
        print(f"{r.id:<16} {name:<28} {r.book_title:<34} {r.status:<10} {r.format}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = Store(args.data)

    if args.command == "add-reader":
        reader = store.add_reader(args.name, args.email, args.genre)
        print(f"Added reader {reader.id}: {reader.name}")
        return 0

    if args.command == "list-readers":
        return _print_readers(store)

    if args.command == "request":
        reader = store.get_reader(args.reader)
        if reader is None:
            print(f"Reader {args.reader} not found.")
            return 1
        request = store.add_request(args.reader, args.book, args.format)
        print(f"Requested review from {reader.name} for '{args.book}' (request {request.id})")
        return 0

    if args.command == "list-requests":
        return _print_requests(store, args.status)

    if args.command == "follow-up":
        request = store.get_request(args.request)
        if request is None:
            print(f"Request {args.request} not found.")
            return 1
        followup_date = args.date or date.today().isoformat()
        followup = store.add_followup(args.request, followup_date, args.note)
        print(f"Logged follow-up {followup.id} for request {args.request} on {followup_date}")
        return 0

    if args.command in ("mark-sent", "mark-received", "mark-declined"):
        request = store.get_request(args.request)
        if request is None:
            print(f"Request {args.request} not found.")
            return 1
        now = datetime.now(timezone.utc).isoformat()
        if args.command == "mark-sent":
            request.status = "mailed"
            request.sent_at = now
        elif args.command == "mark-received":
            request.status = "received"
            request.received_at = now
        else:
            request.status = "declined"
        store.update_request(request)
        print(f"Request {args.request} marked {request.status}.")
        return 0

    if args.command == "totals":
        totals = compute_totals(store)
        print(f"Readers:        {totals['readers']}")
        print(f"Requests:       {totals['requests']}")
        print(f"Follow-ups:     {totals['followups']}")
        print("By status:")
        for status in ("pending", "mailed", "received", "declined"):
            print(f"  {status:<10} {totals[status]}")
        return 0

    if args.command == "export":
        count = export_requests(store, args.out)
        print(f"Exported {count} requests to {args.out}")
        return 0

    if args.command == "due":
        today = date.today().isoformat()
        flagged = []
        for request in store.list_requests():
            if request.status not in ("pending", "mailed"):
                continue
            due = follow_up_due_date(request.requested_at, args.days)
            overdue = is_overdue(request.requested_at, args.days)
            if overdue or due == today:
                flagged.append((request, due, overdue))
        if not flagged:
            print("No follow-ups due.")
            return 0
        print(f"{'ID':<16} {'BOOK':<34} {'DUE':<12} {'STATUS'}")
        print("-" * 70)
        for request, due, overdue in flagged:
            tag = "OVERDUE" if overdue else "due today"
            print(f"{request.id:<16} {request.book_title:<34} {due:<12} {tag}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
