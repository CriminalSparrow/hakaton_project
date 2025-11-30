"""Модуль для сохранения и загрузки дневников питания в CSV файлы"""

import csv
import os
from datetime import date
from typing import Optional
import logging
from setup_logging import setup_logging
from daylog import DayLog
from entries import FoodEntry

# pylint: disable=logging-fstring-interpolation
# pylint: disable=broad-exception-caught

setup_logging()
logger = logging.getLogger(__name__)

os.makedirs("daylogs", exist_ok=True)


def sanitize_filename(name: str) -> str:
    """Пропускаем только цифры/буквы в названии файла"""
    return "".join(c if c.isalnum() else "_" for c in name).strip("_")


def get_daylog_filename(username: str, log_date: Optional[str] = None) -> str:
    """Получаем путь до файла с daylog для пользователя для даты"""
    if log_date is None:
        log_date = date.today().isoformat()
    safe_user = sanitize_filename(username) or "unknown_user"
    return os.path.join("daylogs", f"{safe_user}_{log_date}.csv")


def save_daylog(daylog: DayLog,
                username: str,
                log_date: Optional[str] = None) -> bool:
    """Сохраняем отчет в csv файл"""
    filename = get_daylog_filename(username, log_date)
    try:
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["product", "grams"])
            for entry in daylog.entries:
                # записываем граммы продукта
                writer.writerow([entry.product_name, entry.grams])
        logger.info(f"Дневник сохранен: {filename}\
                    ({len(daylog.entries)} записей)")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении дневника {username}: {e}")
        return False


def load_daylog(username: str, log_date: Optional[str] = None) -> DayLog:
    """Загружаем отчет из csv файла"""
    filename = get_daylog_filename(username, log_date)
    daylog = DayLog()
    if not os.path.exists(filename):
        logger.warning(f"Файл дневника не найден: {filename}")
        return daylog

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                try:
                    entry = FoodEntry(row["product"], float(row["grams"]))
                    daylog.add_entry(entry)
                except Exception:
                    logger.warning(f"""Пропущена некорректная строка {row_num}
                                   в файле {filename}""")
        logger.info(f"""Дневник загружен: {filename}
                    ({len(daylog.entries)} записей)""")
    except Exception as e:
        logger.error(f"Ошибка при загрузке дневника {username}: {e}")

    return daylog


def list_user_logs(username: str) -> list[str]:
    """Получаем список дневников для данного пользователя"""
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
        logger.error(f"Ошибка при чтении списка дневников для {username}: {e}")
    return sorted(logs)
