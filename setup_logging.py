"""Модуль настройки логирования для калькулятора калорий"""

import logging
from logging import FileHandler, StreamHandler, Filter
import sys
import os

# создаём папку для логов
os.makedirs("logs", exist_ok=True)


class CaloriesFilter(Filter):
    # pylint: disable=too-few-public-methods
    """Фильтр: пропускает только WARNING и ERROR"""
    def filter(self, record):
        return record.levelno >= logging.WARNING


def setup_logging(to_stdout=True,
                  use_filter=False,
                  log_file="logs/calorie_app.log"):
    """
    Настройка логирования для калькулятора калорий.

    Параметры:
    - to_stdout: выводить лог в консоль
    - use_filter: использовать фильтр для предупреждений/ошибок
    - log_file: путь к файлу для логов
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # общий уровень для всех хендлеров

    # --- лог в файл ---
    file_handler = FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(file_handler)

    # --- вывод в stdout ---
    if to_stdout:
        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(
            logging.Formatter("[STDOUT] %(levelname)s: %(message)s")
        )
        logger.addHandler(stdout_handler)

    # --- фильтр ---
    if use_filter:
        logger.addFilter(CaloriesFilter())
