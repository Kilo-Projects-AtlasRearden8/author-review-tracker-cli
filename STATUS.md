# STATUS.md

## What was built

**ARC Tracker CLI** (`arc-tracker`) — a local-first Python command-line tool
for authors to track ARC readers, review requests, and follow-ups.

Components:

* `src/arc_tracker/models.py` — dataclasses for `Reader`, `ReviewRequest`,
  `FollowUp` (statuses: pending, mailed, received, declined).
* `src/arc_tracker/storage.py` — atomic local JSON storage (`Store`) with
  graceful handling of missing/corrupt files.
* `src/arc_tracker/date_utils.py` — date math: days between timestamps,
  follow-up due dates, overdue detection.
* `src/arc_tracker/reports.py` — totals aggregation (readers, requests,
  follow-ups, by status).
* `src/arc_tracker/export.py` — CSV export of review requests with reader
  names.
* `src/arc_tracker/cli.py` — argparse CLI: `add-reader`, `list-readers`,
  `request`, `list-requests`, `follow-up`, `mark-sent`, `mark-received`,
  `mark-declined`, `totals`, `due`, `export`.
* `tests/` — pytest suite: `test_totals.py`, `test_dates.py`,
  `test_storage.py` (7 tests).
* `pyproject.toml` — packaging with `arc-tracker` console script entry point.
* `LICENSE` — MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`.
* `README.md` — install/usage guide crediting Asdale Dynamics, LLC.
* `STATUS.md` — this file.

## How to run it

```bash
cd /workspace/kilo-lab/author-review-tracker-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

arc-tracker add-reader --name "Jordan Reader" --genre "Sci-Fi"
arc-tracker request --reader <id> --book "The Massive AI Manual"
arc-tracker list-requests
arc-tracker mark-sent --request <id>
arc-tracker follow-up --request <id> --note "Gentle reminder"
arc-tracker totals
arc-tracker due --days 7
arc-tracker export --out arc-requests.csv
```

Without installing: `PYTHONPATH=src python3 -m arc_tracker.cli --help`.

Storage path defaults to `~/.arc_tracker/data.json`; override with
`--data` or `ARC_TRACKER_DATA`.

## Verification results

* `python3 -m pytest -q` → **7 passed** (totals counts and by-status,
  follow-up totals, date math incl. due dates/overdue, JSON round-trip
  persistence, corrupt-file degradation).
* CLI smoke test passed end to end: add reader, request review, list,
  mark-sent, follow-up, totals, CSV export — all produced correct output and
  a valid CSV file.
* Python 3.13.5, stdlib-only (no third-party runtime dependencies).

## Known gaps

* No web/GUI interface — CLI only, by design (local-first, no keys).
* No reader deactivation/editing beyond adding; reader email/genre are stored
  but not used in reporting.
* Follow-up window (`--days`) is a fixed integer; no per-request overrides.
* No deduplication of readers or requests by name/book.
* Status transitions are not validated (any status can follow any status).
* Packaging not published to PyPI — install from source via `pip install -e .`.
