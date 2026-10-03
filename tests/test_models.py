"""Тесты классов объектной модели ярмарки."""

from models import Product, Sale, Seller


def make_product() -> Product:
    """Создать объект тестового товара."""
    seller = Seller(1, "ИП Иванов", "ivanov@example.com")
    return Product(1, "Мёд цветочный", seller, "Стенд A-12", 50, 450.0)


def test_seller_creation_and_string_representation() -> None:
    """Продавец хранит атрибуты и имеет понятное строковое представление."""
    seller = Seller(1, "ИП Иванов", "ivanov@example.com")

    assert seller.name == "ИП Иванов"
    assert "ИП Иванов" in str(seller)


def test_product_checks_stock_through_object_method() -> None:
    """Товар сам рассчитывает остаток и проверяет доступность."""
    product = make_product()
    sale = Sale(1, product, 18, "2026-09-13", 8100.0)

    assert product.get_remaining_quantity([sale]) == 32
    assert product.is_available([sale], 32)
    assert not product.is_available([sale], 33)


def test_sale_cancel_changes_state_without_deleting_object() -> None:
    """Отмена сохраняет объект продажи, но меняет его состояние."""
    product = make_product()
    sale = Sale(1, product, 50, "2026-09-13", 22500.0)

    sale.cancel()

    assert sale.is_cancelled
    assert product.is_available([sale], 50)
    assert "отменена" in str(sale)


def test_json_factories_restore_object_relations() -> None:
    """Классы восстанавливают объекты и связи из JSON-данных."""
    seller = Seller.from_data(
        {"id": 1, "name": "ИП Иванов", "contact": "ivanov@example.com"}
    )
    product = Product.from_data(
        {
            "id": 1,
            "name": "Мёд цветочный",
            "seller_id": 1,
            "stand": "Стенд A-12",
            "total_quantity": 50,
            "unit_price": 450.0,
        },
        seller,
    )
    sale = Sale.from_data(
        {
            "id": 1,
            "product_id": 1,
            "quantity": 18,
            "sale_date": "2026-09-13",
            "revenue": 8100.0,
            "is_cancelled": False,
        },
        product,
    )

    assert product.seller is seller
    assert sale.product is product
