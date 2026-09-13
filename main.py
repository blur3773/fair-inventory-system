"""Стартовый сценарий системы учёта товаров на ярмарке."""

from datetime import date


def is_inventory_data_valid(
    total_quantity: int,
    sold_quantity: int,
    unit_price: float,
) -> bool:
    """Проверить количество товара и цену."""
    if total_quantity < 0 or sold_quantity < 0 or unit_price < 0:
        return False
    if sold_quantity > total_quantity:
        return False
    return True


def calculate_remaining_quantity(
    total_quantity: int,
    sold_quantity: int,
) -> int:
    """Рассчитать остаток товара на стенде."""
    return total_quantity - sold_quantity


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


def main() -> None:
    """Запустить демонстрационный сценарий проекта."""
    seller_name = "ИП Иванов"
    product_name = "Мёд цветочный"
    stand_name = "Стенд A-12"
    total_quantity = int("50")
    sold_quantity = int("18")
    unit_price = float("450.00")
    fair_date = date(2026, 9, 13)

    if not is_inventory_data_valid(
        total_quantity,
        sold_quantity,
        unit_price,
    ):
        print("Ошибка: проверьте количество товара и цену.")
        return

    remaining_quantity = calculate_remaining_quantity(
        total_quantity,
        sold_quantity,
    )
    revenue = calculate_revenue(total_quantity, unit_price)
    stock_status = get_stock_status(remaining_quantity)

    print("СИСТЕМА УЧЁТА ТОВАРОВ НА ЯРМАРКЕ")
    print(f"Дата: {fair_date.strftime('%d.%m.%Y')}")
    print(f"Продавец: {seller_name}")
    print(f"Товар: {product_name}")
    print(f"Стенд: {stand_name}")
    print(f"Исходное количество: {total_quantity} шт.")
    print(f"Продано: {sold_quantity} шт.")
    print(f"Остаток: {remaining_quantity} шт.")
    print(f"Состояние: {stock_status}")
    print(f"Выручка: {revenue:.2f} руб.")


if __name__ == "__main__":
    main()
