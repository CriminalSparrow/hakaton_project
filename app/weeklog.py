from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, Optional, List

import matplotlib.pyplot as plt

from .daylog import DayLog


@dataclass
class WeekLog:
    logs: Dict[date, DayLog] = field(default_factory=dict)

    def add_daylog(self, log: DayLog, log_date: Optional[date] = None):
        if log_date is None:
            if log.date is None:
                raise ValueError("DayLog has no date, specify log_date")
            log_date = log.date
        self.logs[log_date] = log

    def total_by_day(self) -> Dict[date, float]:
        result = {}
        for d, log in self.logs.items():
            result[d] = log.total_calories()
        return result

    def week_range(self) -> List[date]:
        if not self.logs:
            today = date.today()
            start = today - timedelta(days=today.weekday())
        else:
            any_date = sorted(self.logs.keys())[0]
            start = any_date - timedelta(days=any_date.weekday())

        return [start + timedelta(days=i) for i in range(7)]

    def plot_week_calories(self, save_path: Optional[str] = None):
        days = self.week_range()
        totals = []
        totals_map = self.total_by_day()

        for d in days:
            totals.append(totals_map.get(d, 0))

        plt.figure(figsize=(10, 4))
        plt.plot([d.strftime("%d.%m") for d in days], totals, marker="o")
        plt.title("Калории по дням недели")
        plt.xlabel("Дата")
        plt.ylabel("Калории (kcal)")
        plt.grid(True)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        else:
            plt.show()
