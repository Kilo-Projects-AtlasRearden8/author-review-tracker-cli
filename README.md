# ARC Tracker CLI

A local-first command-line tool for authors to track ARC (advance reader copy)
readers, review requests, and follow-ups. Your data lives in a local JSON file
— no accounts, no API keys, no cloud, nothing phones home.

Built by **Asdale Dynamics, LLC** (Indiana, formed October 2026). Asdale
Dynamics focuses on beginner-friendly AI education, books and guides, and
practical tools the LLC can publish or sell. This CLI is part of the tooling
around Dylan Asdale's book *The Massive AI Manual* and the hub site
dylanasdale.github.io, where AI is explained "like a friend would": plain
English, step by step, never condescending.

## Who this is for

Self-published and KDP authors, ARC coordinators, and anyone running a review
program who wants a simple, private way to track:

* who your ARC readers are
* which review requests are pending, mailed, received, or declined
* when to follow up, and which follow-ups are overdue

## Install

```bash
git clone <this-repo>
cd author-review-tracker-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or run without installing:

```bash
PYTHONPATH=src python3 -m arc_tracker.cli --help
```

## Usage

All data is stored in one JSON file. By default it lives at
`~/.arc_tracker/data.json`; override with `--data` or the
`ARC_TRACKER_DATA` environment variable.

Add a reader:

```bash
arc-tracker add-reader --name "Jordan Reader" --email "jordan@example.com" --genre "Sci-Fi"
```

Request a review:

```bash
arc-tracker request --reader <reader-id> --book "The Massive AI Manual" --format ebook
```

List readers and requests:

```bash
arc-tracker list-readers
arc-tracker list-requests
arc-tracker list-requests --status pending
```

Mark progress:

```bash
arc-tracker mark-sent --request <request-id>
arc-tracker mark-received --request <request-id>
arc-tracker mark-declined --request <request-id>
```

Log a follow-up:

```bash
arc-tracker follow-up --request <request-id> --note "Gentle reminder note"
```

See totals:

```bash
arc-tracker totals
```

See follow-ups due or overdue (7-day window by default):

```bash
arc-tracker due --days 7
```

Export review requests to CSV:

```bash
arc-tracker export --out arc-requests.csv
```

## Storage

One JSON file, written atomically. If the file is missing or corrupt, the
tool starts fresh rather than crashing. No network access, no secrets, no
personal data is collected by the tool itself — anything you store is yours
and stays on your machine.

## Tests

```bash
python3 -m pytest
```

The suite covers totals arithmetic, date math (days between, follow-up due
dates, overdue detection), and JSON storage round-trips.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: Asdale Dynamics, LLC — beginner-friendly AI education, books, guides,
and practical tools. Dylan Asdale, registered nurse turned AI author and
founder of Asdale Dynamics, LLC (Indiana, formed October 2026).
