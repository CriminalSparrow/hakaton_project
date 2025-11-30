"""Тесты для FoodEntry и базы продуктов с КБЖУ."""

# pylint: disable=import-error

import pytest

from entries import FoodEntry
from products import PRODUCT_NUTRITION


def test_product_exists_in_db():
    """Проверяем, что в базе есть несколько ожидаемых продуктов."""
    assert "яблоко" in PRODUCT_NUTRITION
    assert "курица" in PRODUCT_NUTRITION


def test_apple_200g_kbzu():
    """Проверяем расчёт КБЖУ для 200 г яблока."""
    entry = FoodEntry("яблоко", 200)

    nutrition = PRODUCT_NUTRITION["яблоко"]
    factor = 200 / 100

    assert entry.calories() == pytest.approx(nutrition["kcal"] * factor)
    assert entry.protein() == pytest.approx(nutrition["protein"] * factor)
    assert entry.fat() == pytest.approx(nutrition["fat"] * factor)
    assert entry.carbs() == pytest.approx(nutrition["carbs"] * factor)


def test_chicken_150g_kbzu():
    """Проверяем расчёт КБЖУ для 150 г курицы (дробный множитель)."""
    entry = FoodEntry("курица", 150)

    nutrition = PRODUCT_NUTRITION["курица"]
    factor = 150 / 100

    assert entry.calories() == pytest.approx(nutrition["kcal"] * factor)
    assert entry.protein() == pytest.approx(nutrition["protein"] * factor)
    assert entry.fat() == pytest.approx(nutrition["fat"] * factor)
    assert entry.carbs() == pytest.approx(nutrition["carbs"] * factor)


def test_name_normalization():
    """Название продукта должно нормализоваться (пробелы, регистр)."""
    entry = FoodEntry("  КИВИ  ", 100)
    assert entry.product_name == "киви"
    assert entry.calories() == pytest.approx(PRODUCT_NUTRITION["киви"]["kcal"])


@pytest.mark.parametrize("grams", [0, -1, -50])
def test_invalid_grams_raises(grams):
    """Нулевые и отрицательные граммы должны вызывать ValueError."""
    with pytest.raises(ValueError):
        FoodEntry("яблоко", grams)


def test_unknown_product_raises():
    """Неизвестный продукт должен вызывать ValueError."""
    with pytest.raises(ValueError):
        FoodEntry("арбузик_левый", 100)


def test_summary_has_all_fields():
    """summary() должен возвращать все необходимые ключи."""
    entry = FoodEntry("банан", 100)
    summary = entry.summary()

    assert summary["product"] == "банан"
    assert summary["grams"] == 100

    for key in ("kcal", "protein", "fat", "carbs"):
        assert key in summary
        assert isinstance(summary[key], (float, int))


def test_summary_values_are_rounded():
    """summary() должен округлять значения КБЖУ до 2 знаков после запятой."""
    entry = FoodEntry("яблоко", 203.5)

    raw_kcal = entry.calories()
    raw_protein = entry.protein()
    raw_fat = entry.fat()
    raw_carbs = entry.carbs()

    summary = entry.summary()

    # Проверяем именно округлённые значения
    assert summary["kcal"] == round(raw_kcal, 2)
    assert summary["protein"] == round(raw_protein, 2)
    assert summary["fat"] == round(raw_fat, 2)
    assert summary["carbs"] == round(raw_carbs, 2)
