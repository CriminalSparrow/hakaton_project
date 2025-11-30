"""Модуль для формирования недельного отчета."""
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, Optional, List
from daylog import DayLog


@dataclass
class WeekLog:
    """Хранит 7 дневников питания и позволяет получать статистику за неделю."""
    logs: Dict[date, DayLog] = field(default_factory=dict)

    def add_daylog(self, log: DayLog, log_date: Optional[date] = None):
        """Добавляет дневник определённого дня в недельный лог."""
        actual_date = log_date or log.date
        if actual_date is None:
            raise ValueError("Не указана дата для добавления дневника")

        # Приводим к date при необходимости
        if isinstance(actual_date, datetime):
            actual_date = actual_date.date()

        # Сохраняем дату в самом дневнике для дальнейшего доступа
        log.date = actual_date
        self.logs[actual_date] = log

    # Сводные показатели за неделю

    def total_calories(self) -> float:
        """Считаем сумму калорий."""
        return sum(log.total_calories() for log in self.logs.values())

    def total_protein(self) -> float:
        """Считаем сумму протеинов."""
        return sum(log.total_protein() for log in self.logs.values())

    def total_fat(self) -> float:
        """Считаем сумму жиров."""
        return sum(log.total_fat() for log in self.logs.values())

    def total_carbs(self) -> float:
        """Считаем сумму углеводов."""
        return sum(log.total_carbs() for log in self.logs.values())

    # По дням
    def total_by_day(self) -> Dict[date, float]:
        """Возвращает словарь {дата: общее количество калорий за день}."""
        return {d: log.total_calories() for d, log in self.logs.items()}

    # Для недели
    def week_range(self) -> List[date]:
        """Возвращает список из 7 дней недели, начиная с понедельника."""

        if not self.logs:
            today = date.today()
            start = today - timedelta(days=today.weekday())
        else:
            first = sorted(self.logs.keys())[0]
            start = first - timedelta(days=first.weekday())

        return [start + timedelta(days=i) for i in range(7)]
