"""Работа с отчетами через консоль"""

from datetime import datetime, date
from daylog import DayLog
from weeklog import WeekLog
from daylog_io import save_daylog, load_daylog, list_user_logs
from entries import FoodEntry, PRODUCT_NUTRITION
# pylint: disable=broad-exception-caught


def parse_date_or_today(date_str: str) -> date:
    """Преобразует 'YYYY-MM-DD' в date или возвращает today"""
    s = (date_str or "").strip()
    if not s:
        return date.today()
    return datetime.strptime(s, "%Y-%m-%d").date()


def main():
    """Основная функция для работы с консолью"""
    week = WeekLog()

    while True:
        print("\n=== КАЛОРИЙНЫЙ ДНЕВНИК ===")
        print("1 - Добавить запись за день")
        print("2 - Показать отчёт за день")
        print("3 - Показать отчёт за неделю")
        print("4 - Сохранить все дни")
        print("5 - Загрузить все дни пользователя")
        print("6 - Выйти")

        choice = input("Выберите пункт: ").strip()

        #  1) Добавление записи
        if choice == "1":
            try:
                date_str = input(
                    "Введите дату YYYY-MM-DD (Enter=сегодня): ").strip()
                log_date = parse_date_or_today(date_str)

                # получаем существующий дневник или создаём новый с датой
                log = week.logs.get(log_date) or DayLog(log_date)

                print("\nДоступные продукты:", ", ".join(
                    PRODUCT_NUTRITION.keys()))
                product = input("Продукт: ").strip()
                if not product:
                    print("Продукт не указан.")
                    continue

                grams_raw = input("Граммы: ").strip()
                grams = float(grams_raw)

                entry = FoodEntry(product, grams)
                log.add_entry(entry)
                week.add_daylog(log, log_date)
                print("Добавлено!")
            except ValueError as ve:
                print("Ошибка ввода:", ve)
            except Exception as e:
                print("Ошибка:", e)

        # 2) Отчёт за день
        elif choice == "2":
            try:
                date_str = input(
                    "Дата отчёта (YYYY-MM-DD, Enter=сегодня): ").strip()
                log_date = parse_date_or_today(date_str)
                day = week.logs.get(log_date)
                print("\n" + (day.report() if day else "Записей нет."))
            except Exception as e:
                print("Ошибка:", e)

        #  3) Отчёт за неделю
        elif choice == "3":
            stat = week.total_by_day()
            print("\n===== Отчёт за неделю =====")

            if not stat:
                print("Нет данных.")
                continue

            for d in sorted(stat.keys()):
                s = stat[d]
                print(f"{d}: {s['kcal']:.0f} ккал (Б:{s['protein']:.1f}\
                      Ж:{s['fat']:.1f} У:{s['carbs']:.1f})")

            print("\nИТОГО за неделю:")
            print(f"Калорий:   {week.total_calories():.0f}")
            print(f"Белков:    {week.total_protein():.1f}")
            print(f"Жиров:     {week.total_fat():.1f}")
            print(f"Углеводов: {week.total_carbs():.1f}")

        #  4) Сохранение всех дней
        elif choice == "4":
            user = input("Имя пользователя: ").strip()
            if not user:
                print("Имя пользователя не указано.")
                continue
            for d, log in week.logs.items():
                save_daylog(log, user, d.isoformat())
            print("Все дни сохранены!")

        # 5) Загрузка всех доступных дней
        elif choice == "5":
            user = input("Имя пользователя: ").strip()
            if not user:
                print("Имя пользователя не указано.")
                continue

            week = WeekLog()
            for d_str in list_user_logs(user):
                # list_user_logs возвращает строки (даты в isoformat)
                day = load_daylog(user, d_str)
                # Попробуем назначить дату дневнику
                try:
                    parsed_date = datetime.strptime(d_str, "%Y-%m-%d").date()
                except Exception:
                    parsed_date = None

                if parsed_date and hasattr(day, "date") and (day.date is None):
                    day.date = parsed_date

                if parsed_date is not None:
                    day.date = parsed_date

                week.add_daylog(day, parsed_date)
            print("Загружена вся доступная неделя.")

        # 6) Выход
        elif choice == "6":
            print("Выход...")
            break

        else:
            print("Неизвестная команда!")


if __name__ == "__main__":
    main()
