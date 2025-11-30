"""Модуль для формирования недельного отчета"""
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, Optional, List
from daylog import DayLog


@dataclass
class WeekLog:
    """Хранит 7 дневников питания и позволяет получать статистику за неделю."""
    logs: Dict[date, DayLog] = field(default_factory=dict)

    def add_daylog(self, log: DayLog, log_date: Optional[date] = None):
        """Добавляет дневник определённого дня в недельный лог"""
        if log_date is None:
            if log.date is None:
                raise ValueError("DayLog не содержит даты,\
                                 передайте её через log_date")
            log_date = log.date

        # Если log.date хранится как datetime, приводим к date
        if isinstance(log_date, datetime):
            log_date = log_date.date()

        self.logs[log_date] = log

    # Сводные показатели за неделю

    def total_calories(self) -> float:
        """Считаем сумму калорий"""
        return sum(log.total_calories() for log in self.logs.values())

    def total_protein(self) -> float:
        """Считаем сумму протеинов"""
        return sum(log.total_protein() for log in self.logs.values())

    def total_fat(self) -> float:
        """Считаем сумму жиров"""
        return sum(log.total_fat() for log in self.logs.values())

    def total_carbs(self) -> float:
        """Считаем сумму углеводов"""
        return sum(log.total_carbs() for log in self.logs.values())

    # По дням
    def total_by_day(self) -> Dict[date, dict]:
        """
        Возвращает структуру:
        {
            date: {"kcal":..., "protein":..., "fat":..., "carbs":...}
        }
        """
        result = {}
        for d, log in self.logs.items():
            result[d] = {
                "kcal": log.total_calories(),
                "protein": log.total_protein(),
                "fat": log.total_fat(),
                "carbs": log.total_carbs(),
            }
        return result

    # Для недели
    def week_range(self) -> List[date]:
        """Возвращает список из 7 дней недели, начиная с понедельника"""

        if not self.logs:
            today = date.today()
            start = today - timedelta(days=today.weekday())
        else:
            first = sorted(self.logs.keys())[0]
            start = first - timedelta(days=first.weekday())

        return [start + timedelta(days=i) for i in range(7)]
