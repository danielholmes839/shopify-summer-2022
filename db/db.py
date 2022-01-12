from abc import ABC, abstractmethod
from typing import Optional, List
from .product import Product


class DB(ABC):
    @abstractmethod
    def insert_product(self, product: Product) -> bool:
        pass

    @abstractmethod
    def get_product(self, id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_products_by_collection(self, ) -> List[Product]:
        pass

    @abstractmethod
    def update_product(self, update: Product) -> bool:
        pass

    @abstractmethod
    def delete_product(self, id: str) -> bool:
        pass
