"""Модуль для формирования дневного отчета"""
from datetime import date
from typing import Optional, List
from entries import FoodEntry


class DayLog:
    """Класс для формирования дневного отчета"""
    def __init__(self, log_date: Optional[date] = None):
        # Если дату не передали — сегодня
        self.date: date = log_date or date.today()
        self.entries: List[FoodEntry] = []

    def add_entry(self, entry: FoodEntry):
        """Добавить запись"""
        if not isinstance(entry, FoodEntry):
            raise TypeError("Ожидался FoodEntry")
        self.entries.append(entry)

    # Суммы по КБЖУ
    def total_calories(self) -> float:
        """Считаем сумму калорий"""
        return sum(e.calories() for e in self.entries)

    def total_protein(self) -> float:
        """Считаем сумму протеинов"""
        return sum(e.protein() for e in self.entries)

    def total_fat(self) -> float:
        """Считаем сумму жиров"""
        return sum(e.fat() for e in self.entries)

    def total_carbs(self) -> float:
        """Считаем сумму углеводов"""
        return sum(e.carbs() for e in self.entries)

    # Текстовый отчёт
    def report(self) -> str:
        """Вывод отчета за день"""
        lines = [
            f"Дневник питания — дата: {self.date.isoformat()}",
            "-" * 42
        ]

        for i, entry in enumerate(self.entries, start=1):
            s = entry.summary()
            lines.append(
                f"{i}. {s['product']}: {s['grams']} г — {s['kcal']} ккал, "
                f"Б:{s['protein']} Ж:{s['fat']} У:{s['carbs']}"
            )

        lines.append("-" * 42)
        lines.append(
            f"ИТОГО: {self.total_calories():.1f} ккал  "
            f"(Б:{self.total_protein():.1f} "
            f"Ж:{self.total_fat():.1f} "
            f"У:{self.total_carbs():.1f})"
        )

        total = self.total_calories()
        if total < 800:
            lines.append("мало еды — риск голода")
        elif total <= 2200:
            lines.append("норма")
        else:
            lines.append("много — стоит сократить рацион")

        return "\n".join(lines)
