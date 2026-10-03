"""Операции над коллекциями объектов товаров, продавцов и продаж."""

from datetime import date
from typing import Dict, List, Optional

from models import Product, Sale, Seller


def get_product_by_id(
    products: List[Product], product_id: int
) -> Optional[Product]:
    """Найти объект товара по идентификатору."""
    for product in products:
        if product.id == product_id:
            return product
    return None


def get_seller_by_id(
    sellers: List[Seller], seller_id: int
) -> Optional[Seller]:
    """Найти объект продавца по идентификатору."""
    for seller in sellers:
        if seller.id == seller_id:
            return seller
    return None


def add_seller(sellers: List[Seller], name: str, contact: str) -> Seller:
    """Создать продавца и добавить его в коллекцию."""
    next_id = max((seller.id for seller in sellers), default=0) + 1
    seller = Seller(next_id, name, contact)
    sellers.append(seller)
    return seller


def add_product(
    products: List[Product],
    name: str,
    seller: Seller,
    stand: str,
    total_quantity: int,
    unit_price: float,
) -> Optional[Product]:
    """Создать товар и добавить его в коллекцию объектов."""
    if not Product.validate_values(total_quantity, unit_price):
        return None
    next_id = max((product.id for product in products), default=0) + 1
    product = Product(
        next_id,
        name,
        seller,
        stand,
        total_quantity,
        unit_price,
    )
    products.append(product)
    return product


def find_products(products: List[Product], query: str) -> List[Product]:
    """Найти объекты товаров по части названия без учёта регистра."""
    normalized_query = query.lower()
    return [
        product
        for product in products
        if normalized_query in product.name.lower()
    ]


def check_product_availability(
    product: Product, sales: List[Sale], required_quantity: int
) -> bool:
    """Проверить наличие товара через метод конкретного объекта."""
    return product.is_available(sales, required_quantity)


def register_sale(
    products: List[Product],
    sales: List[Sale],
    product_id: int,
    quantity: int,
    sale_date: date,
) -> Optional[Sale]:
    """Создать объект продажи при достаточном остатке товара."""
    product = get_product_by_id(products, product_id)
    if product is None or not product.is_available(sales, quantity):
        return None

    next_id = max((sale.id for sale in sales), default=0) + 1
    sale = Sale(
        next_id,
        product,
        quantity,
        sale_date.isoformat(),
        product.calculate_revenue(quantity),
    )
    sales.append(sale)
    return sale


def cancel_sale(sales: List[Sale], sale_id: int) -> bool:
    """Отменить активную продажу, не удаляя объект из журнала."""
    for sale in sales:
        if sale.id == sale_id and not sale.is_cancelled:
            sale.cancel()
            return True
    return False


def filter_products_by_stock(
    products: List[Product], sales: List[Sale], minimum_quantity: int
) -> List[Product]:
    """Отобрать товары с остатком не меньше заданного значения."""
    return [
        product
        for product in products
        if product.get_remaining_quantity(sales) >= minimum_quantity
    ]


def sort_products_by_remaining(
    products: List[Product], sales: List[Sale]
) -> List[Product]:
    """Отсортировать объекты товаров по остаткам."""
    return sorted(
        products,
        key=lambda product: product.get_remaining_quantity(sales),
    )


def get_inventory_statistics(
    products: List[Product], sales: List[Sale]
) -> Dict[str, float]:
    """Сформировать статистику, игнорируя отменённые продажи."""
    remaining_quantity = sum(
        product.get_remaining_quantity(sales) for product in products
    )
    active_sales = [sale for sale in sales if not sale.is_cancelled]
    sold_quantity = sum(sale.quantity for sale in active_sales)
    revenue = sum(sale.revenue for sale in active_sales)
    return {
        "product_count": float(len(products)),
        "sold_quantity": float(sold_quantity),
        "remaining_quantity": float(remaining_quantity),
        "revenue": revenue,
    }
