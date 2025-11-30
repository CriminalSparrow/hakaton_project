from datetime import datetime
from app.daylog import DayLog
from app.weeklog import WeekLog


def test_week_totals():
    w = WeekLog()

    d1 = DayLog(date=datetime(2025, 11, 24))
    d1.add("A", 100)
    d1.add("B", 200)

    d2 = DayLog(date=datetime(2025, 11, 25))
    d2.add("C", 300)

    w.add_daylog(d1)
    w.add_daylog(d2)

    totals = w.total_by_day()
    assert totals[d1.date] == 300
    assert totals[d2.date] == 300
