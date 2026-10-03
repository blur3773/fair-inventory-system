"""Тесты операций над коллекциями объектов ярмарки."""

from datetime import date

from inventory import (
    cancel_sale,
    check_product_availability,
    find_products,
    get_inventory_statistics,
    register_sale,
)
from models import Product, Seller


def make_product() -> Product:
    """Создать объект тестового товара."""
    seller = Seller(1, "ИП Иванов", "ivanov@example.com")
    return Product(1, "Мёд цветочный", seller, "Стенд A-12", 50, 450.0)


def test_find_products_ignores_letter_case() -> None:
    """Поиск находит объект товара независимо от регистра букв."""
    products = [make_product()]

    assert find_products(products, "МЁД") == products


def test_register_sale_reduces_remaining_quantity() -> None:
    """Созданная продажа уменьшает остаток и связывается с товаром."""
    product = make_product()
    products = [product]
    sales = []

    sale = register_sale(products, sales, 1, 18, date(2026, 9, 13))

    assert sale is not None
    assert sale.product is product
    assert product.get_remaining_quantity(sales) == 32
    assert sale.revenue == 8100.0


def test_sale_is_rejected_when_product_is_unavailable() -> None:
    """Продажа не создаётся при недостаточном остатке."""
    product = make_product()
    sale = register_sale([product], [], 1, 51, date(2026, 9, 13))

    assert sale is None
    assert not check_product_availability(product, [], 51)


def test_cancel_sale_restores_product_availability() -> None:
    """Отмена меняет состояние продажи и восстанавливает наличие."""
    product = make_product()
    sales = []
    sale = register_sale([product], sales, 1, 50, date(2026, 9, 13))

    assert sale is not None
    assert cancel_sale(sales, sale.id)
    assert sale.is_cancelled
    assert check_product_availability(product, sales, 50)


def test_inventory_statistics_ignores_cancelled_sales() -> None:
    """Статистика не учитывает отменённые продажи."""
    product = make_product()
    sales = []
    sale = register_sale([product], sales, 1, 18, date(2026, 9, 13))

    assert sale is not None
    cancel_sale(sales, sale.id)
    statistics = get_inventory_statistics([product], sales)

    assert statistics["sold_quantity"] == 0.0
    assert statistics["remaining_quantity"] == 50.0
    assert statistics["revenue"] == 0.0
