"""Загрузка и сохранение JSON-данных приложения."""

import json
from pathlib import Path


def load_data(filename: Path) -> list[dict]:
    """Загрузить список словарей из JSON-файла безопасным способом."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename.name} не найден. Используется пустой список.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename.name} содержит некорректный JSON.")
        return []
    except OSError as error:
        print(f"Не удалось прочитать {filename.name}: {error}")
        return []

    if not isinstance(data, list):
        print(f"Файл {filename.name} должен содержать список записей.")
        return []
    return data


def save_data(filename: Path, data: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Не удалось сохранить {filename.name}: {error}")
