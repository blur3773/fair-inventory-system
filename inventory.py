"""Функции для работы с товарами и продажами ярмарки."""

from datetime import date
from typing import Optional


def get_product_by_id(products: list[dict], product_id: int) -> Optional[dict]:
    """Найти товар по идентификатору."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def get_sold_quantity(sales: list[dict], product_id: int) -> int:
    """Рассчитать количество проданных единиц товара."""
    sold_quantity = 0
    for sale in sales:
        if sale["product_id"] == product_id:
            sold_quantity += sale["quantity"]
    return sold_quantity


def calculate_remaining_quantity(
    total_quantity: int, sold_quantity: int
) -> int:
    """Рассчитать остаток товара на стенде."""
    return total_quantity - sold_quantity


def get_remaining_quantity(product: dict, sales: list[dict]) -> int:
    """Рассчитать текущий остаток выбранного товара."""
    sold_quantity = get_sold_quantity(sales, product["id"])
    return calculate_remaining_quantity(
        product["total_quantity"], sold_quantity
    )


def calculate_revenue(sold_quantity: int, unit_price: float) -> float:
    """Рассчитать выручку от проданных единиц товара."""
    return sold_quantity * unit_price


def get_stock_status(remaining_quantity: int) -> str:
    """Определить состояние запаса товара."""
    if remaining_quantity == 0:
        return "товар закончился"
    if remaining_quantity <= 10:
        return "товар заканчивается"
    return "товар в наличии"


def add_product(
    products: list[dict],
    name: str,
    seller: str,
    stand: str,
    total_quantity: int,
    unit_price: float,
) -> dict:
    """Добавить товар в список и вернуть созданную запись."""
    next_id = max((product["id"] for product in products), default=0) + 1
    product = {
        "id": next_id,
        "name": name,
        "seller": seller,
        "stand": stand,
        "total_quantity": total_quantity,
        "unit_price": unit_price,
    }
    products.append(product)
    return product


def find_products(products: list[dict], query: str) -> list[dict]:
    """Найти товары по части названия без учёта регистра."""
    found_products = []
    normalized_query = query.lower()
    for product in products:
        if normalized_query in product["name"].lower():
            found_products.append(product)
    return found_products


def check_product_availability(
    product: dict, sales: list[dict], required_quantity: int
) -> bool:
    """Проверить, доступен ли товар в нужном количестве."""
    remaining_quantity = get_remaining_quantity(product, sales)
    return required_quantity > 0 and remaining_quantity >= required_quantity


def register_sale(
    products: list[dict],
    sales: list[dict],
    product_id: int,
    quantity: int,
    sale_date: date,
) -> Optional[dict]:
    """Зарегистрировать продажу при достаточном остатке товара."""
    product = get_product_by_id(products, product_id)
    if product is None or not check_product_availability(
        product, sales, quantity
    ):
        return None

    next_id = max((sale["id"] for sale in sales), default=0) + 1
    sale = {
        "id": next_id,
        "product_id": product_id,
        "quantity": quantity,
        "sale_date": sale_date.isoformat(),
        "revenue": calculate_revenue(quantity, product["unit_price"]),
    }
    sales.append(sale)
    return sale


def cancel_sale(sales: list[dict], sale_id: int) -> bool:
    """Отменить продажу по идентификатору."""
    for sale in sales:
        if sale["id"] == sale_id:
            sales.remove(sale)
            return True
    return False


def filter_products_by_stock(
    products: list[dict], sales: list[dict], minimum_quantity: int
) -> list[dict]:
    """Отобрать товары с остатком не меньше заданного значения."""
    return [
        product
        for product in products
        if get_remaining_quantity(product, sales) >= minimum_quantity
    ]


def sort_products_by_remaining(
    products: list[dict], sales: list[dict]
) -> list[dict]:
    """Отсортировать товары по остатку от меньшего к большему."""
    return sorted(
        products,
        key=lambda product: get_remaining_quantity(product, sales),
    )


def get_inventory_statistics(products: list[dict], sales: list[dict]) -> dict:
    """Сформировать статистику по товарам, остаткам и выручке."""
    remaining_quantity = 0
    for product in products:
        remaining_quantity += get_remaining_quantity(product, sales)

    sold_quantity = sum(sale["quantity"] for sale in sales)
    revenue = sum(sale["revenue"] for sale in sales)
    return {
        "product_count": len(products),
        "sold_quantity": sold_quantity,
        "remaining_quantity": remaining_quantity,
        "revenue": revenue,
    }
