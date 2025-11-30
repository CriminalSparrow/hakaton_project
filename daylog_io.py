"""Модуль для сохранения и загрузки дневников питания в CSV файлы."""

import csv
import logging
import os
from datetime import date
from typing import Optional

from daylog import DayLog
from entries import FoodEntry
from setup_logging import setup_logging

# pylint: disable=logging-fstring-interpolation
# pylint: disable=broad-exception-caught

setup_logging()
logger = logging.getLogger(__name__)

os.makedirs("daylogs", exist_ok=True)


def sanitize_filename(name: str) -> str:
    """Пропускаем только цифры/буквы в названии файла."""
    return "".join(c if c.isalnum() else "_" for c in name).strip("_")


def get_daylog_filename(username: str, log_date: Optional[str] = None) -> str:
    """Получаем путь до файла с daylog для пользователя для даты."""
    if log_date is None:
        log_date = date.today().isoformat()
    safe_user = sanitize_filename(username) or "unknown_user"
    return os.path.join("daylogs", f"{safe_user}_{log_date}.csv")


def save_daylog(daylog: DayLog,
                username: str,
                log_date: Optional[str] = None) -> bool:
    """Сохраняем отчет в csv файл."""
    filename = get_daylog_filename(username, log_date)
    try:
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["product", "calories"])
            for entry in daylog.entries:
                product = None
                calories = None
                if isinstance(entry, dict):
                    product = entry.get("name")
                    calories = entry.get("calories")
                if product is None and isinstance(entry, FoodEntry):
                    product = entry.product_name
                    calories = entry.calories()
                if product is None or calories is None:
                    continue
                writer.writerow([product, calories])
        logger.info(
            "Дневник сохранен: %s (%s записей)",
            filename,
            len(daylog.entries),
        )
        return True
    except Exception as e:
        logger.error("Ошибка при сохранении дневника %s: %s", username, e)
        return False


def load_daylog(username: str, log_date: Optional[str] = None) -> DayLog:
    """Загружаем отчет из csv файла."""
    filename = get_daylog_filename(username, log_date)
    daylog = DayLog()
    if not os.path.exists(filename):
        logger.warning("Файл дневника не найден: %s", filename)
        return daylog

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                try:
                    daylog.add(row["product"], float(row["calories"]))
                except Exception:
                    logger.warning(
                        "Пропущена некорректная строка %s в файле %s",
                        row_num,
                        filename,
                    )
        logger.info(
            "Дневник загружен: %s (%s записей)",
            filename,
            len(daylog.entries),
        )
    except Exception as e:
        logger.error("Ошибка при загрузке дневника %s: %s", username, e)

    return daylog


def list_user_logs(username: str) -> list[str]:
    """Получаем список дневников для данного пользователя."""
    safe_user = sanitize_filename(username)
    logs = []
    try:
        logs = [
            filename[len(safe_user) + 1:-4]
            for filename in os.listdir("daylogs")
            if filename.startswith(f"{safe_user}_")
            and filename.endswith(".csv")
        ]
    except Exception as e:
        logger.error("Ошибка при чтении списка дневников для %s: %s",
                     username, e)
    return sorted(logs)
