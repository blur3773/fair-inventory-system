"""Функции безопасного ввода значений в консольном приложении."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с обработкой ошибки ввода."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Введите число, например 450.00.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ с обработкой ошибки."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Введите дату в формате ДД.ММ.ГГГГ.")
