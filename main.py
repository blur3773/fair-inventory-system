"""Консольный интерфейс объектной модели учёта товаров на ярмарке."""

from pathlib import Path
from typing import List

from inventory import (
    add_product,
    add_seller,
    cancel_sale,
    check_product_availability,
    filter_products_by_stock,
    find_products,
    get_inventory_statistics,
    get_product_by_id,
    get_seller_by_id,
    register_sale,
    sort_products_by_remaining,
)
from models import Product, Sale, Seller
from storage import (
    load_products,
    load_sales,
    load_sellers,
    save_products,
    save_sales,
    save_sellers,
)
from utils import input_date, input_float, input_int

DATA_DIR = Path(__file__).parent / "data"
SELLERS_FILE = DATA_DIR / "sellers.json"
PRODUCTS_FILE = DATA_DIR / "products.json"
SALES_FILE = DATA_DIR / "sales.json"


def show_products(products: List[Product], sales: List[Sale]) -> None:
    """Вывести объекты товаров, остатки и статусы запасов."""
    if not products:
        print("Список товаров пуст.")
        return

    print("\nID | Товар | Продавец | Стенд | Цена | Остаток | Состояние")
    print("-" * 80)
    for product in products:
        remaining_quantity = product.get_remaining_quantity(sales)
        stock_status = product.get_stock_status(sales)
        print(f"{product} | {remaining_quantity} шт. | {stock_status}")


def show_sellers(sellers: List[Seller]) -> None:
    """Вывести объекты продавцов."""
    if not sellers:
        print("Список продавцов пуст.")
        return

    print("\nID | Продавец | Контакт")
    print("-" * 50)
    for seller in sellers:
        print(seller)


def show_sales(sales: List[Sale]) -> None:
    """Вывести объекты продаж, включая отменённые."""
    if not sales:
        print("Продаж пока нет.")
        return

    print("\nID | Товар | Количество | Дата | Выручка | Статус")
    print("-" * 80)
    for sale in sales:
        print(sale)


def show_statistics(products: List[Product], sales: List[Sale]) -> None:
    """Вывести статистику только по активным продажам."""
    statistics = get_inventory_statistics(products, sales)
    print("\nСТАТИСТИКА ЯРМАРКИ")
    print(f"Товарных позиций: {int(statistics['product_count'])}")
    print(f"Продано единиц: {int(statistics['sold_quantity'])} шт.")
    print(f"Текущий остаток: {int(statistics['remaining_quantity'])} шт.")
    print(f"Общая выручка: {statistics['revenue']:.2f} руб.")


def save_all(
    sellers: List[Seller], products: List[Product], sales: List[Sale]
) -> None:
    """Сохранить все изменённые коллекции объектов в JSON."""
    save_sellers(SELLERS_FILE, sellers)
    save_products(PRODUCTS_FILE, products)
    save_sales(SALES_FILE, sales)


def main() -> None:
    """Загрузить объекты и запустить главное меню приложения."""
    sellers = load_sellers(SELLERS_FILE)
    products = load_products(PRODUCTS_FILE, sellers)
    sales = load_sales(SALES_FILE, products)

    while True:
        print("\n=== СИСТЕМА УЧЁТА ТОВАРОВ НА ЯРМАРКЕ ===")
        print("1. Показать товары")
        print("2. Показать продавцов")
        print("3. Найти товар")
        print("4. Проверить наличие")
        print("5. Добавить продавца")
        print("6. Добавить товар")
        print("7. Зарегистрировать продажу")
        print("8. Отменить продажу")
        print("9. Отсортировать товары по остатку")
        print("10. Отобрать товары по минимальному остатку")
        print("11. Показать журнал продаж")
        print("12. Показать статистику")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_products(products, sales)
        elif choice == "2":
            show_sellers(sellers)
        elif choice == "3":
            query = input("Введите часть названия товара: ").strip()
            show_products(find_products(products, query), sales)
        elif choice == "4":
            product_id = input_int("Введите ID товара: ")
            quantity = input_int("Введите требуемое количество: ")
            product = get_product_by_id(products, product_id)
            if product is None:
                print("Товар с таким ID не найден.")
            elif check_product_availability(product, sales, quantity):
                print("Товар доступен в нужном количестве.")
            else:
                print("Недостаточно товара на остатке.")
        elif choice == "5":
            name = input("Имя продавца: ").strip()
            contact = input("Контакт продавца: ").strip()
            if not name or not contact:
                print("Имя и контакт не могут быть пустыми.")
                continue
            seller = add_seller(sellers, name, contact)
            save_all(sellers, products, sales)
            print(f"Продавец «{seller.name}» добавлен с ID {seller.id}.")
        elif choice == "6":
            show_sellers(sellers)
            seller_id = input_int("Введите ID продавца: ")
            seller = get_seller_by_id(sellers, seller_id)
            if seller is None:
                print("Продавец с таким ID не найден.")
                continue
            name = input("Название товара: ").strip()
            stand = input("Стенд: ").strip()
            total_quantity = input_int("Исходное количество: ")
            unit_price = input_float("Цена за единицу: ")
            if not name or not stand:
                print("Название и стенд не могут быть пустыми.")
                continue
            product = add_product(
                products, name, seller, stand, total_quantity, unit_price
            )
            if product is None:
                print("Количество и цена не могут быть отрицательными.")
                continue
            save_all(sellers, products, sales)
            print(f"Товар «{product.name}» добавлен с ID {product.id}.")
        elif choice == "7":
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
                save_all(sellers, products, sales)
                print(f"Продажа создана: {sale}")
        elif choice == "8":
            sale_id = input_int("Введите ID продажи для отмены: ")
            if cancel_sale(sales, sale_id):
                save_all(sellers, products, sales)
                print("Продажа отменена, запись сохранена в журнале.")
            else:
                print("Активная продажа с таким ID не найдена.")
        elif choice == "9":
            show_products(sort_products_by_remaining(products, sales), sales)
        elif choice == "10":
            minimum_quantity = input_int("Минимальный остаток: ")
            filtered_products = filter_products_by_stock(
                products, sales, minimum_quantity
            )
            show_products(filtered_products, sales)
        elif choice == "11":
            show_sales(sales)
        elif choice == "12":
            show_statistics(products, sales)
        elif choice == "0":
            save_all(sellers, products, sales)
            print("Работа завершена. Данные сохранены.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")


if __name__ == "__main__":
    main()
