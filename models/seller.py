"""Класс продавца ярмарки."""

from typing import Dict


class Seller:
    """Продавец, реализующий товары на ярмарке."""

    def __init__(self, seller_id: int, name: str, contact: str) -> None:
        """Создать объект продавца."""
        self.id = seller_id
        self.name = name
        self.contact = contact

    @classmethod
    def from_data(cls, data: Dict) -> "Seller":
        """Создать продавца из записи JSON."""
        return cls(data["id"], data["name"], data["contact"])

    def to_data(self) -> Dict:
        """Преобразовать продавца в данные для JSON."""
        return {"id": self.id, "name": self.name, "contact": self.contact}

    def __str__(self) -> str:
        """Вернуть краткое строковое представление продавца."""
        return f"{self.id} | {self.name} | Контакт: {self.contact}"
