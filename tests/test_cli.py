import csv
import os

from arc_tracker.cli import main
from arc_tracker.export import export_requests
from arc_tracker.storage import Store


def _run(args):
    return main(args)


def test_cli_add_reader_and_list(tmp_path, capsys):
    data = str(tmp_path / "cli.json")
    assert _run(["--data", data, "add-reader", "--name", "Ada",
                 "--email", "ada@example.com", "--genre", "Sci-Fi"]) == 0
    out = capsys.readouterr().out
    assert "Added reader" in out
    assert "Ada" in out

    assert _run(["--data", data, "list-readers"]) == 0
    out = capsys.readouterr().out
    assert "Ada" in out
    assert "Sci-Fi" in out


def test_cli_request_flow(tmp_path, capsys):
    data = str(tmp_path / "cli2.json")
    _run(["--data", data, "add-reader", "--name", "Ada", "--genre", "Sci-Fi"])
    out = capsys.readouterr().out
    rid = out.split("Added reader ")[1].split(":")[0].strip()

    _run(["--data", data, "request", "--reader", rid,
          "--book", "The Massive AI Manual", "--format", "ebook"])
    out = capsys.readouterr().out
    assert "The Massive AI Manual" in out
    reqid = out.split("(request ")[1].split(")")[0].strip()

    _run(["--data", data, "mark-sent", "--request", reqid])
    _run(["--data", data, "follow-up", "--request", reqid, "--note", "ping"])

    _run(["--data", data, "totals"])
    out = capsys.readouterr().out
    assert "Readers:" in out
    assert "Requests:" in out
    assert "Follow-ups:" in out

    _run(["--data", data, "export", "--out", str(tmp_path / "out.csv")])
    assert os.path.exists(str(tmp_path / "out.csv"))


def test_cli_missing_reader(tmp_path, capsys):
    data = str(tmp_path / "cli3.json")
    assert _run(["--data", data, "request", "--reader", "nope",
                 "--book", "Manual"]) == 1
    out = capsys.readouterr().out
    assert "not found" in out


def test_cli_due_and_status_filter(tmp_path, capsys):
    data = str(tmp_path / "cli4.json")
    _run(["--data", data, "add-reader", "--name", "Ada", "--genre", "Sci-Fi"])
    out = capsys.readouterr().out
    rid = out.split("Added reader ")[1].split(":")[0].strip()
    _run(["--data", data, "request", "--reader", rid,
          "--book", "Old Book", "--format", "ebook"])
    out = capsys.readouterr().out
    reqid = out.split("(request ")[1].split(")")[0].strip()

    # Force the request to be old so it's overdue in the 7-day window.
    req = Store(data).get_request(reqid)
    req.requested_at = "2020-01-01T00:00:00+00:00"
    Store(data).update_request(req)

    _run(["--data", data, "due", "--days", "7"])
    out = capsys.readouterr().out
    assert "OVERDUE" in out or "Old Book" in out

    _run(["--data", data, "list-requests", "--status", "pending"])
    out = capsys.readouterr().out
    assert "Old Book" in out


def test_export_requests(tmp_path):
    store = Store(str(tmp_path / "e.json"))
    alice = store.add_reader("Alice", "a@x.com", "Sci-Fi")
    store.add_request(alice.id, "Book One", "ebook")
    store.add_request(alice.id, "Book Two", "paperback")

    out = str(tmp_path / "out.csv")
    count = export_requests(store, out)
    assert count == 2

    with open(out, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0][0] == "id"
    assert len(rows) == 3
    assert rows[1][2] == "Alice"
    assert rows[1][3] == "Book One"
    assert rows[1][4] == "pending"
    assert rows[2][3] == "Book Two"
