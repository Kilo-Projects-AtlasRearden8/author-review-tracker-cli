# ARC Tracker CLI

A friendly, local-first command-line tool for authors who want to track ARC
(advance reader copy) readers, review requests, and follow-ups — without
accounts, API keys, or anything phoning home.

Your data lives in a single JSON file on your computer. That's it. No cloud,
no subscriptions, no personal data collected by the tool. Anything you store
is yours and stays on your machine.

This tool is built by **Asdale Dynamics, LLC** (Indiana, formed October
2026). Asdale Dynamics focuses on beginner-friendly AI education, books and
guides, and practical tools the LLC can publish or sell. It's part of the
tooling around Dylan Asdale's book *The Massive AI Manual* and the hub site
dylanasdale.github.io, where AI is explained "like a friend would": plain
English, step by step, never condescending.

Dylan is a registered nurse turned AI author. He builds small, practical,
tested tools for authors, small businesses, and everyday life admin — and
this is one of them.

## Who this is for

Self-published and KDP authors, ARC coordinators, and anyone running a review
program who wants a simple, private way to keep track of:

* who your ARC readers are
* which review requests are pending, mailed, received, or declined
* when to follow up, and which follow-ups are overdue

## Install

Create a virtual environment and install the package (this also makes the
`arc-tracker` command available):

```bash
git clone <this-repo>
cd author-review-tracker-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Prefer not to install? Run straight from the source folder:

```bash
PYTHONPATH=src python3 -m arc_tracker.cli --help
```

## Your data

All information is stored in one JSON file. By default it's at
`~/.arc_tracker/data.json`. You can point it somewhere else with the `--data`
option or the `ARC_TRACKER_DATA` environment variable:

```bash
arc-tracker --data ./my-arc-data.json add-reader --name "Jordan Reader"
```

The file is written atomically, and if it's ever missing or corrupted, the
tool starts fresh instead of crashing. Nothing is ever sent over the network.

## Usage

Add a reader:

```bash
arc-tracker add-reader --name "Jordan Reader" \
  --email "jordan@example.com" --genre "Sci-Fi"
```

Request a review (use the reader id shown by `list-readers`):

```bash
arc-tracker request --reader <reader-id> \
  --book "The Massive AI Manual" --format ebook
```

List your readers and requests:

```bash
arc-tracker list-readers
arc-tracker list-requests
arc-tracker list-requests --status pending
```

Mark a request as it moves through the process:

```bash
arc-tracker mark-sent    --request <request-id>
arc-tracker mark-received --request <request-id>
arc-tracker mark-declined --request <request-id>
```

Log a follow-up:

```bash
arc-tracker follow-up --request <request-id> --note "Gentle reminder note"
```

See totals for readers, requests, and follow-ups:

```bash
arc-tracker totals
```

See follow-ups that are due or overdue (7-day window by default):

```bash
arc-tracker due --days 7
```

Export all review requests (with reader names) to CSV:

```bash
arc-tracker export --out arc-requests.csv
```

## Tests

```bash
python3 -m pytest
```

The suite covers totals arithmetic, date math (days between, follow-up due
dates, overdue detection), JSON storage round-trips, CLI behavior, and CSV
export.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: Asdale Dynamics, LLC — beginner-friendly AI education, books, guides,
and practical tools. Dylan Asdale, registered nurse turned AI author and
founder of Asdale Dynamics, LLC (Indiana, formed October 2026).
