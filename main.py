"""Консольный интерфейс системы учёта товаров на ярмарке."""

from pathlib import Path

from inventory import (
    add_product,
    cancel_sale,
    check_product_availability,
    filter_products_by_stock,
    find_products,
    get_inventory_statistics,
    get_product_by_id,
    get_remaining_quantity,
    get_stock_status,
    register_sale,
    sort_products_by_remaining,
)
from storage import load_data, save_data
from utils import input_date, input_float, input_int

DATA_DIR = Path(__file__).parent / "data"
PRODUCTS_FILE = DATA_DIR / "products.json"
SALES_FILE = DATA_DIR / "sales.json"


def show_products(products: list[dict], sales: list[dict]) -> None:
    """Вывести товары, их остатки и состояние запаса."""
    if not products:
        print("Список товаров пуст.")
        return

    print("\nID | Товар | Продавец | Стенд | Остаток | Цена | Состояние")
    print("-" * 80)
    for product in products:
        remaining_quantity = get_remaining_quantity(product, sales)
        stock_status = get_stock_status(remaining_quantity)
        print(
            f"{product['id']} | {product['name']} | {product['seller']} | "
            f"{product['stand']} | {remaining_quantity} шт. | "
            f"{product['unit_price']:.2f} руб. | {stock_status}"
        )


def show_sales(sales: list[dict], products: list[dict]) -> None:
    """Вывести журнал продаж."""
    if not sales:
        print("Продаж пока нет.")
        return

    print("\nID | Товар | Количество | Дата | Выручка")
    print("-" * 60)
    for sale in sales:
        product = get_product_by_id(products, sale["product_id"])
        product_name = product["name"] if product else "Удалённый товар"
        print(
            f"{sale['id']} | {product_name} | {sale['quantity']} шт. | "
            f"{sale['sale_date']} | {sale['revenue']:.2f} руб."
        )


def show_statistics(products: list[dict], sales: list[dict]) -> None:
    """Вывести статистику по товарам и продажам."""
    statistics = get_inventory_statistics(products, sales)
    print("\nСТАТИСТИКА ЯРМАРКИ")
    print(f"Товарных позиций: {statistics['product_count']}")
    print(f"Продано единиц: {statistics['sold_quantity']} шт.")
    print(f"Текущий остаток: {statistics['remaining_quantity']} шт.")
    print(f"Общая выручка: {statistics['revenue']:.2f} руб.")


def main() -> None:
    """Запустить цикл меню приложения."""
    products = load_data(PRODUCTS_FILE)
    sales = load_data(SALES_FILE)

    while True:
        print("\n=== СИСТЕМА УЧЁТА ТОВАРОВ НА ЯРМАРКЕ ===")
        print("1. Показать товары")
        print("2. Найти товар")
        print("3. Проверить наличие")
        print("4. Добавить товар")
        print("5. Зарегистрировать продажу")
        print("6. Отменить продажу")
        print("7. Отсортировать товары по остатку")
        print("8. Отобрать товары по минимальному остатку")
        print("9. Показать журнал продаж")
        print("10. Показать статистику")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_products(products, sales)
        elif choice == "2":
            query = input("Введите часть названия товара: ").strip()
            show_products(find_products(products, query), sales)
        elif choice == "3":
            product_id = input_int("Введите ID товара: ")
            quantity = input_int("Введите требуемое количество: ")
            product = get_product_by_id(products, product_id)
            if product is None:
                print("Товар с таким ID не найден.")
            elif check_product_availability(product, sales, quantity):
                print("Товар доступен в нужном количестве.")
            else:
                print("Недостаточно товара на остатке.")
        elif choice == "4":
            name = input("Название товара: ").strip()
            seller = input("Продавец: ").strip()
            stand = input("Стенд: ").strip()
            total_quantity = input_int("Исходное количество: ")
            unit_price = input_float("Цена за единицу: ")
            if not name or not seller or not stand:
                print("Название, продавец и стенд не могут быть пустыми.")
                continue
            if total_quantity < 0 or unit_price < 0:
                print("Количество и цена не могут быть отрицательными.")
                continue
            product = add_product(
                products, name, seller, stand, total_quantity, unit_price
            )
            save_data(PRODUCTS_FILE, products)
            print(f"Товар «{product['name']}» добавлен с ID {product['id']}.")
        elif choice == "5":
            product_id = input_int("Введите ID товара: ")
            quantity = input_int("Количество продажи: ")
            sale_date = input_date("Дата продажи в формате ДД.ММ.ГГГГ: ")
            sale = register_sale(
                products, sales, product_id, quantity, sale_date
            )
            if sale is None:
                print(
                    "Продажа не зарегистрирована: "
                    "проверьте ID и остаток товара."
                )
            else:
                save_data(SALES_FILE, sales)
                print(
                    "Продажа зарегистрирована. "
                    f"Выручка: {sale['revenue']:.2f} руб."
                )
        elif choice == "6":
            sale_id = input_int("Введите ID продажи для отмены: ")
            if cancel_sale(sales, sale_id):
                save_data(SALES_FILE, sales)
                print("Продажа отменена, остаток товара восстановлен.")
            else:
                print("Продажа с таким ID не найдена.")
        elif choice == "7":
            show_products(sort_products_by_remaining(products, sales), sales)
        elif choice == "8":
            minimum_quantity = input_int("Минимальный остаток: ")
            filtered_products = filter_products_by_stock(
                products, sales, minimum_quantity
            )
            show_products(filtered_products, sales)
        elif choice == "9":
            show_sales(sales, products)
        elif choice == "10":
            show_statistics(products, sales)
        elif choice == "0":
            print("Работа завершена.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")


if __name__ == "__main__":
    main()
