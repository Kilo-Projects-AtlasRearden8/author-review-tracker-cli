from arc_tracker.storage import Store
from arc_tracker.reports import compute_totals


def test_totals_counts(tmp_path):
    store = Store(str(tmp_path / "totals.json"))
    alice = store.add_reader("Alice", "alice@example.com", "Sci-Fi")
    bob = store.add_reader("Bob", "bob@example.com", "Fantasy")

    store.add_request(alice.id, "Book One")
    store.add_request(alice.id, "Book Two")
    store.add_request(bob.id, "Book Three")

    totals = compute_totals(store)
    assert totals["readers"] == 2
    assert totals["requests"] == 3
    assert totals["followups"] == 0
    assert totals["pending"] == 3


def test_totals_by_status_and_followups(tmp_path):
    store = Store(str(tmp_path / "status.json"))
    alice = store.add_reader("Alice", "alice@example.com", "Sci-Fi")

    r1 = store.add_request(alice.id, "Book One")
    r2 = store.add_request(alice.id, "Book Two")
    store.add_followup(r1.id, "2026-01-05", "Checked in")

    received = store.get_request(r1.id)
    received.status = "received"
    received.received_at = "2026-01-10T00:00:00+00:00"
    store.update_request(received)

    totals = compute_totals(store)
    assert totals["readers"] == 1
    assert totals["requests"] == 2
    assert totals["followups"] == 1
    assert totals["received"] == 1
    assert totals["pending"] == 1
