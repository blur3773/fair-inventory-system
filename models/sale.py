"""Класс продажи товара на ярмарке."""

from typing import Dict

from .product import Product


class Sale:
    """Продажа, связанная с объектом товара."""

    def __init__(
        self,
        sale_id: int,
        product: Product,
        quantity: int,
        sale_date: str,
        revenue: float,
    ) -> None:
        """Создать объект продажи."""
        self.id = sale_id
        self.product = product
        self.quantity = quantity
        self.sale_date = sale_date
        self.revenue = revenue
        self.is_cancelled = False

    @classmethod
    def from_data(cls, data: Dict, product: Product) -> "Sale":
        """Создать продажу из данных JSON и связанного товара."""
        sale = cls(
            data["id"],
            product,
            data["quantity"],
            data["sale_date"],
            data["revenue"],
        )
        sale.is_cancelled = data.get("is_cancelled", False)
        return sale

    def to_data(self) -> Dict:
        """Преобразовать продажу в данные для JSON."""
        return {
            "id": self.id,
            "product_id": self.product.id,
            "quantity": self.quantity,
            "sale_date": self.sale_date,
            "revenue": self.revenue,
            "is_cancelled": self.is_cancelled,
        }

    def cancel(self) -> None:
        """Отменить продажу без удаления записи из журнала."""
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление продажи и её статуса."""
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"{self.id} | {self.product.name} | {self.quantity} шт. | "
            f"{self.sale_date} | {self.revenue:.2f} руб. | {status}"
        )
