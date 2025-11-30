"""Работа с записями питания и расчётом КБЖУ."""

from products import PRODUCT_NUTRITION


class FoodEntry:
    """Одна запись о съеденной пище с расчётом КБЖУ."""

    def __init__(self, product_name: str, grams: int):
        self.product_name = product_name.strip().lower()
        self.grams = grams

        if self.product_name not in PRODUCT_NUTRITION:
            raise ValueError(f"Неизвестный продукт: {self.product_name}")

        if self.grams <= 0:
            raise ValueError("Количество граммов должно быть положительным")

    def _per_100(self) -> dict:
        """КБЖУ на 100 г для продукта."""
        return PRODUCT_NUTRITION[self.product_name]

    def _calc(self, field: str) -> float:
        """Универсальный расчёт по полю kcal, protein, fat, carbs."""
        value_per_100 = self._per_100()[field]
        return value_per_100 * self.grams / 100

    def calories(self) -> float:
        """Подсчёт калорий в граммах продукта."""
        return self._calc("kcal")

    def protein(self) -> float:
        """Подсчёт белков в граммах продукта."""
        return self._calc("protein")

    def fat(self) -> float:
        """Подсчёт жиров в граммах продукта."""
        return self._calc("fat")

    def carbs(self) -> float:
        """Подсчёт углеводов в граммах продукта."""
        return self._calc("carbs")

    def summary(self) -> dict:
        """Краткое резюме КБЖУ по записи"""
        return {
            "product": self.product_name,
            "grams": self.grams,
            "kcal": round(self.calories(), 2),
            "protein": round(self.protein(), 2),
            "fat": round(self.fat(), 2),
            "carbs": round(self.carbs(), 2),
        }
