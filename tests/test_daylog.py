import pytest
from datetime import datetime
from app.daylog import DayLog


def test_add_and_total():

    dl = DayLog()
    dl.add("A", 100)
    dl.add("B", 200)
    assert dl.total_calories() == 300


def test_report_contains_entries_and_total():

    dl = DayLog(date=datetime(2025, 11, 30))
    dl.add("Овсянка", 300, datetime(2025, 11, 30, 8, 0), "завтрак")
    dl.add("Обед", 600, datetime(2025, 11, 30, 13, 0))
    report = dl.report()
    assert "Овсянка" in report
    assert "Обед" in report
    assert "Итого: 900 kcal" in report
    assert "норма" in report


def test_negative_calories_raises():
    dl = DayLog()
    with pytest.raises(ValueError):
        dl.add("Bad", -100)


def test_empty_report():
    dl = DayLog()
    r = dl.report()
    assert "Записи отсутствуют" in r or "Итого: 0 kcal" in r
