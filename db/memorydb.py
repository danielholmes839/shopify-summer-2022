from typing import List, Optional
from .product import Product
from .db import DB


class MemoryDB(DB):
    def __init__(self, products):
        self.products = products

    def insert_product(self, product: Product) -> bool:
        self.products[product.id] = product

    def get_product(self, id: str) -> Optional[Product]:
        return self.products.get(id)

    def get_products(self) -> List[Product]:
        return self.products.values()

    def get_products_by_collection(self, collection: str) -> List[Product]:
        return [product for product in self.products.values() if product.collection == collection]

    def update_product(self, product: Product) -> bool:
        if product.id not in self.products:
            return False

        self.products[product.id] = product
        return True

    def delete_product(self, id: str) -> bool:
        if id not in self.products:
            return False

        del self.products[id]
        return True
