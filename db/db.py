from abc import ABC, abstractmethod
from typing import List

from .product import Product


class DB(ABC):
    @abstractmethod
    def get_product(self, id: str) -> Product:
        pass

    @abstractmethod
    def get_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_products_by_category(self, category: str) -> List[Product]:
        pass
    
    @abstractmethod
    def insert_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, id: str) -> Product:
        pass
