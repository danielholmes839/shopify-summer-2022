from uuid import uuid4
from typing import List

from .product import Product
from .db import DB
from .exceptions import ProductNotFound


class MemoryDB(DB):
    def __init__(self, products: List[Product]):
        self.products = dict([(p.id, p) for p in products])

    def get_product(self, id: str) -> Product:
        """ get product """
        product = self.products.get(id)
        if product is None:
            raise ProductNotFound(id)

        return product.copy()

    def get_products(self) -> List[Product]:
        """ get products """
        return [p.copy() for p in self.products.values()]

    def get_products_by_category(self, category: str) -> List[Product]:
        """ get products by category """
        return [
            p.copy() for p in self.products.values()
            if p.category == category
        ]

    def insert_product(self, product: Product) -> Product:
        """ insert a product """
        product = product.copy()
        product.id = self._uuid()
        product.validate()

        self.products[product.id] = product
        return product

    def update_product(self, product: Product) -> Product:
        """ update a product """
        if not self.has(product.id):
            raise ProductNotFound(product.id)

        # update the product
        product.validate()
        product = product.copy()
        self.products[product.id] = product

        return product

    def delete_product(self, id: str) -> Product:
        """ delete a product """
        if not self.has(id):
            raise ProductNotFound(id)

        # delete the product
        product = self.products.pop(id)
        return product.copy()

    def _uuid(self) -> str:
        return str(uuid4())

    def has(self, product_id: str) -> bool:
        """ has product """
        return product_id in self.products
