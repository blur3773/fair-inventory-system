"""Пакет объектной модели системы учёта товаров на ярмарке."""

from .product import Product
from .sale import Sale
from .seller import Seller

__all__ = ["Product", "Sale", "Seller"]
