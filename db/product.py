from typing import Optional

from .exceptions import ProductAttributeException


class Product:
    def __init__(self, product: dict):
        """ product constructor
        - the dictionary will come from a "ProductInput" in the graphql schema
        - the .get will replace missing attributes with None
          for example when inserting a product the id isn't generated until the db "insert_product" method is called
        - the price is automatically rounded to 2 decimal places
        """
        self.id: str = product.get('id')
        self.name: str = product.get('name')
        self.description: str = product.get('description')
        self.price: float = round(product.get('price'), 2)
        self.category: Optional[str] = product.get('category')

    def validate(self, id_required=True):
        """ validation logic for before adding to a database
        - id is required
        - name cannot be empty and cannot exceed 20 characters
        - description cannot exceed 200 characters
        - price must be greater than 0
        - category cannot be empty the default should be "None" which is like null
        """
        if self.id is None and id_required:
            raise ProductAttributeException('product id missing')

        elif len(self.name) == 0:
            raise ProductAttributeException('product name cannot be empty')
        
        elif len(self.name) > 20:
            raise ProductAttributeException('product name cannot exceed 20 characters')
        
        elif len(self.description) > 200:
            raise ProductAttributeException('product description cannot exceed 200 characters')
        
        elif self.price <= 0:
            raise ProductAttributeException('product price must be greater than 0')

        elif self.category is not None and len(self.category) == 0:
            raise ProductAttributeException('product category cannot be empty')

    def copy(self):
        """ create a copy of the product """
        return Product(self.dict())

    def dict(self):
        """ create a dictionary of the product """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category
        }

    def __repr__(self) -> str:
        """ formatting for debugging """
        return f'Product({self.id}, {self.name}, {self.price}, {self.category})'


