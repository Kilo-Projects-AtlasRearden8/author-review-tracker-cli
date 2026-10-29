from arc_tracker.date_utils import days_between, follow_up_due_date, is_overdue


def test_days_between():
    assert days_between("2026-01-01T00:00:00+00:00", "2026-01-10T00:00:00+00:00") == 9
    assert days_between("2026-01-01T00:00:00+00:00") is not None
    assert days_between(None) is None


def test_follow_up_due_date():
    assert follow_up_due_date("2026-01-01T00:00:00+00:00", 7) == "2026-01-08"
    assert follow_up_due_date("2026-01-01T00:00:00+00:00") == "2026-01-08"
    assert follow_up_due_date(None) is None


def test_is_overdue():
    assert is_overdue("2026-01-01T00:00:00+00:00", 7) is True
    assert is_overdue("2099-01-01T00:00:00+00:00", 7) is False
    assert is_overdue(None, 7) is False
