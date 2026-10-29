from arc_tracker.storage import Store


def test_storage_round_trip(tmp_path):
    path = str(tmp_path / "roundtrip.json")
    store = Store(path)
    alice = store.add_reader("Alice", "alice@example.com", "Sci-Fi")
    request = store.add_request(alice.id, "Book One")
    store.add_followup(request.id, "2026-01-05", "Checked in")

    # Re-open from the same file: data must persist.
    store2 = Store(path)
    readers = store2.list_readers()
    requests = store2.list_requests()
    followups = store2.list_followups()

    assert len(readers) == 1
    assert readers[0].name == "Alice"
    assert len(requests) == 1
    assert requests[0].book_title == "Book One"
    assert requests[0].status == "pending"
    assert len(followups) == 1
    assert followups[0].note == "Checked in"


def test_corrupt_file_degrades_gracefully(tmp_path):
    path = str(tmp_path / "corrupt.json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("{ not valid json")
    store = Store(path)
    assert store.list_readers() == []
    store.add_reader("Zelda", "z@example.com", "Fantasy")
    assert len(store.list_readers()) == 1
