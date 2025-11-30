"""Учет рациона за один день."""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from entries import FoodEntry


class DayLog:
    """Класс для формирования дневного отчета."""

    def __init__(self,
                 log_date: Optional[date] = None,
                 **kwargs):
        alias_date = kwargs.pop("date", None)
        log_date = log_date or alias_date or datetime.today().date()
        # Приводим datetime к дате, если передали.
        if isinstance(log_date, datetime):
            log_date = log_date.date()
        self.date: date = log_date
        # Элемент словаря: name, calories, time, meal, food_entry.
        self.entries: List[Dict[str, Any]] = []

    def add(self,
            name: str,
            calories: float,
            when: Optional[datetime] = None,
            meal: Optional[str] = None) -> None:
        """Добавить запись по названию и калориям."""
        if calories < 0:
            raise ValueError("Калории не могут быть отрицательными")
        record = {
            "name": name,
            "calories": float(calories),
            "time": when,
            "meal": meal,
            "food_entry": None,
        }
        self.entries.append(record)

    def add_entry(self,
                  entry: FoodEntry,
                  when: Optional[datetime] = None,
                  meal: Optional[str] = None) -> None:
        """Добавить запись из FoodEntry, сохранив рассчитанные калории."""
        if not isinstance(entry, FoodEntry):
            raise TypeError("Ожидался FoodEntry")
        self.entries.append({
            "name": entry.product_name,
            "calories": entry.calories(),
            "time": when,
            "meal": meal,
            "food_entry": entry,
        })

    # Суммы
    def total_calories(self) -> float:
        """Считаем сумму калорий."""
        return sum(e["calories"] for e in self.entries)

    def total_protein(self) -> float:
        """Считаем сумму протеинов по FoodEntry, если они есть."""
        return sum(
            e["food_entry"].protein() for e in self.entries
            if e.get("food_entry") is not None
        )

    def total_fat(self) -> float:
        """Считаем сумму жиров по FoodEntry, если они есть."""
        return sum(
            e["food_entry"].fat() for e in self.entries
            if e.get("food_entry") is not None
        )

    def total_carbs(self) -> float:
        """Считаем сумму углеводов по FoodEntry, если они есть."""
        return sum(
            e["food_entry"].carbs() for e in self.entries
            if e.get("food_entry") is not None
        )

    def _comment(self, total: float) -> str:
        if total == 0:
            return "Записи отсутствуют"
        if total < 800:
            return "мало еды — риск голода"
        if total <= 2200:
            return "норма"
        return "много — стоит сократить рацион"

    # Текстовый отчёт
    def report(self) -> str:
        """Вывод отчета за день."""
        lines = [f"Дневник питания — дата: {self.date.isoformat()}"]

        for idx, entry in enumerate(self.entries, start=1):
            meal = f" ({entry['meal']})" if entry.get("meal") else ""
            time_part = ""
            if isinstance(entry.get("time"), datetime):
                time_part = f" [{entry['time'].strftime('%H:%M')}]"
            lines.append(
                f"{idx}. {entry['name']}{meal}{time_part}: "
                f"{entry['calories']:.0f} kcal"
            )

        total = self.total_calories()
        lines.append("-" * 42)
        lines.append(f"Итого: {total:.0f} kcal")
        lines.append(self._comment(total))

        return "\n".join(lines)
