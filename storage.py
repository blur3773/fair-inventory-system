"""Загрузка объектов из JSON и сохранение объектов в JSON."""

import json
from pathlib import Path
from typing import Dict, List

from inventory import get_product_by_id, get_seller_by_id
from models import Product, Sale, Seller


def load_data(filename: Path) -> List[Dict]:
    """Безопасно загрузить список словарей из JSON-файла."""
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


def save_data(filename: Path, data: List[Dict]) -> None:
    """Безопасно сохранить список словарей в JSON-файл."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Не удалось сохранить {filename.name}: {error}")


def load_sellers(filename: Path) -> List[Seller]:
    """Загрузить коллекцию объектов Seller."""
    return [Seller.from_data(data) for data in load_data(filename)]


def save_sellers(filename: Path, sellers: List[Seller]) -> None:
    """Сохранить коллекцию объектов Seller."""
    save_data(filename, [seller.to_data() for seller in sellers])


def load_products(filename: Path, sellers: List[Seller]) -> List[Product]:
    """Загрузить товары и восстановить связи с объектами Seller."""
    products = []
    for data in load_data(filename):
        seller = get_seller_by_id(sellers, data.get("seller_id", 0))
        if seller is None:
            print(f"Товар {data.get('id')} пропущен: продавец не найден.")
            continue
        products.append(Product.from_data(data, seller))
    return products


def save_products(filename: Path, products: List[Product]) -> None:
    """Сохранить коллекцию объектов Product."""
    save_data(filename, [product.to_data() for product in products])


def load_sales(filename: Path, products: List[Product]) -> List[Sale]:
    """Загрузить продажи и восстановить связи с объектами Product."""
    sales = []
    for data in load_data(filename):
        product = get_product_by_id(products, data.get("product_id", 0))
        if product is None:
            print(f"Продажа {data.get('id')} пропущена: товар не найден.")
            continue
        sales.append(Sale.from_data(data, product))
    return sales


def save_sales(filename: Path, sales: List[Sale]) -> None:
    """Сохранить коллекцию объектов Sale."""
    save_data(filename, [sale.to_data() for sale in sales])
