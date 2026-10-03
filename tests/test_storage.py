"""Тесты преобразования объектов предметной области в JSON и обратно."""

from pathlib import Path

from models import Product, Sale, Seller
from storage import (
    load_products,
    load_sales,
    load_sellers,
    save_products,
    save_sales,
    save_sellers,
)


def test_storage_restores_object_links_and_sale_state(tmp_path: Path) -> None:
    """JSON сохраняет идентификаторы и восстанавливает связанные объекты."""
    seller = Seller(1, "ИП Иванов", "ivanov@example.com")
    product = Product(1, "Мёд цветочный", seller, "Стенд A-12", 50, 450.0)
    sale = Sale(1, product, 18, "2026-09-13", 8100.0)
    sale.cancel()

    sellers_file = tmp_path / "sellers.json"
    products_file = tmp_path / "products.json"
    sales_file = tmp_path / "sales.json"
    save_sellers(sellers_file, [seller])
    save_products(products_file, [product])
    save_sales(sales_file, [sale])

    loaded_sellers = load_sellers(sellers_file)
    loaded_products = load_products(products_file, loaded_sellers)
    loaded_sales = load_sales(sales_file, loaded_products)

    assert loaded_products[0].seller is loaded_sellers[0]
    assert loaded_sales[0].product is loaded_products[0]
    assert loaded_sales[0].is_cancelled
