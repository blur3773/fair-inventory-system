"""Автоматические тесты функций учёта товаров и продаж."""

from datetime import date

from inventory import (
    cancel_sale,
    check_product_availability,
    find_products,
    get_inventory_statistics,
    get_remaining_quantity,
    register_sale,
)


def make_product() -> dict:
    """Создать тестовый товар."""
    return {
        "id": 1,
        "name": "Мёд цветочный",
        "seller": "ИП Иванов",
        "stand": "Стенд A-12",
        "total_quantity": 50,
        "unit_price": 450.0,
    }


def test_find_products_ignores_letter_case() -> None:
    """Поиск находит товар независимо от регистра букв."""
    products = [make_product()]

    assert find_products(products, "МЁД") == products


def test_register_sale_reduces_remaining_quantity() -> None:
    """Зарегистрированная продажа уменьшает остаток."""
    products = [make_product()]
    sales: list[dict] = []

    sale = register_sale(products, sales, 1, 18, date(2026, 9, 13))

    assert sale is not None
    assert get_remaining_quantity(products[0], sales) == 32
    assert sale["revenue"] == 8100.0


def test_sale_is_rejected_when_product_is_unavailable() -> None:
    """Продажа не создаётся при недостаточном остатке."""
    products = [make_product()]
    sales: list[dict] = []

    sale = register_sale(products, sales, 1, 51, date(2026, 9, 13))

    assert sale is None
    assert not check_product_availability(products[0], sales, 51)


def test_cancel_sale_restores_product_availability() -> None:
    """Отмена продажи снова делает товар доступным."""
    products = [make_product()]
    sales: list[dict] = []
    sale = register_sale(products, sales, 1, 50, date(2026, 9, 13))

    assert sale is not None
    assert cancel_sale(sales, sale["id"])
    assert check_product_availability(products[0], sales, 50)


def test_inventory_statistics_calculates_revenue() -> None:
    """Статистика содержит число проданных единиц и общую выручку."""
    products = [make_product()]
    sales: list[dict] = []
    register_sale(products, sales, 1, 18, date(2026, 9, 13))

    statistics = get_inventory_statistics(products, sales)

    assert statistics["sold_quantity"] == 18
    assert statistics["remaining_quantity"] == 32
    assert statistics["revenue"] == 8100.0
