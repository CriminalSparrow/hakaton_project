from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class FoodEntry:
    name: str
    calories: float
    time: Optional[datetime] = None
    note: Optional[str] = None


class DayLog:
    def __init__(self, date: Optional[datetime] = None):
        self.date = date
        self.entries: List[FoodEntry] = []

    def add(
            self,
            name: str,
            calories: float,
            time: Optional[datetime] = None,
            note: Optional[str] = None
            ):
        if calories < 0:
            raise ValueError("Calories cannot be negative")
        self.entries.append(FoodEntry(name, calories, time, note))

    def total_calories(self) -> float:
        return sum(entry.calories for entry in self.entries)

    def report(self) -> str:
        lines = [
            "Дневник питания — дата: " +
            (str(self.date.date()) if self.date else "не указана"),
            "-" * 40,
            ]

        for i, entry in enumerate(self.entries, start=1):
            time_str = entry.time.strftime("%H:%M") if entry.time else "--:--"
            note_str = f" ({entry.note})" if entry.note else ""
            lines.append(
                f"{i}. {time_str} — {entry.name}: {entry.calories} kcal"
                f"{note_str}"
                )

        lines.append("-" * 40)
        total = self.total_calories()
        lines.append(f"Итого: {total} kcal")

        if total < 800:
            comment = "мало — можно добавить калорий (возможно вы голодны)"
        elif total <= 2200:
            comment = "норма"
        else:
            comment = "много — старайтесь есть меньше"

        lines.append(comment)

        return "\n".join(lines)
