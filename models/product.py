"""Класс товара ярмарки."""

from typing import Dict, List, TYPE_CHECKING

from .seller import Seller

if TYPE_CHECKING:
    from .sale import Sale


class Product:
    """Товар продавца, размещённый на стенде ярмарки."""

    def __init__(
        self,
        product_id: int,
        name: str,
        seller: Seller,
        stand: str,
        total_quantity: int,
        unit_price: float,
    ) -> None:
        """Создать товар с исходным количеством и ценой."""
        self.id = product_id
        self.name = name
        self.seller = seller
        self.stand = stand
        self.total_quantity = total_quantity
        self.unit_price = unit_price

    @staticmethod
    def validate_values(total_quantity: int, unit_price: float) -> bool:
        """Проверить допустимость исходного количества и цены."""
        return total_quantity >= 0 and unit_price >= 0

    @classmethod
    def from_data(cls, data: Dict, seller: Seller) -> "Product":
        """Создать товар из данных JSON и связанного объекта продавца."""
        return cls(
            data["id"],
            data["name"],
            seller,
            data["stand"],
            data["total_quantity"],
            data["unit_price"],
        )

    def to_data(self) -> Dict:
        """Преобразовать товар в данные для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "seller_id": self.seller.id,
            "stand": self.stand,
            "total_quantity": self.total_quantity,
            "unit_price": self.unit_price,
        }

    def get_sold_quantity(self, sales: List["Sale"]) -> int:
        """Рассчитать количество активных продаж этого товара."""
        sold_quantity = 0
        for sale in sales:
            if sale.product.id == self.id and not sale.is_cancelled:
                sold_quantity += sale.quantity
        return sold_quantity

    def get_remaining_quantity(self, sales: List["Sale"]) -> int:
        """Рассчитать текущий остаток товара."""
        return self.total_quantity - self.get_sold_quantity(sales)

    def is_available(self, sales: List["Sale"], quantity: int) -> bool:
        """Проверить наличие товара в требуемом количестве."""
        return quantity > 0 and self.get_remaining_quantity(sales) >= quantity

    def calculate_revenue(self, quantity: int) -> float:
        """Рассчитать выручку от продажи заданного количества товара."""
        return quantity * self.unit_price

    def get_stock_status(self, sales: List["Sale"]) -> str:
        """Определить состояние запаса товара."""
        remaining_quantity = self.get_remaining_quantity(sales)
        if remaining_quantity == 0:
            return "товар закончился"
        if remaining_quantity <= 10:
            return "товар заканчивается"
        return "товар в наличии"

    def __str__(self) -> str:
        """Вернуть строковое представление товара."""
        return (
            f"{self.id} | {self.name} | {self.seller.name} | "
            f"{self.stand} | {self.unit_price:.2f} руб."
        )
