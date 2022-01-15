from typing import Optional

from .exceptions import ItemAttributeException


class Item:
    def __init__(self, item: dict):
        """ item constructor
        - the dictionary will come from a "ItemInput" in the graphql schema
        - the .get will replace missing attributes with None
          for example when inserting a item the id isn't generated until the db "insert_item" method is called
        - the price is automatically rounded to 2 decimal places
        """
        self.id: str = item.get('id')
        self.name: str = item.get('name')
        self.description: str = item.get('description')
        self.price: float = round(item.get('price'), 2)
        self.stock: int = int(item.get('stock'))
        self.collection: Optional[str] = item.get('collection')

    def validate(self):
        """ validation logic for before adding to a database
        - id is required
        - name cannot be empty and cannot exceed 20 characters
        - description cannot exceed 200 characters
        - price must be greater than 0
        - collection cannot be empty the default should be "None" which is like null
        """
        if self.id is None:
            raise ItemAttributeException('item id missing')

        elif len(self.name) == 0:
            raise ItemAttributeException('item name cannot be empty')

        elif len(self.name) > 20:
            raise ItemAttributeException(
                'item name cannot exceed 20 characters')

        elif len(self.description) > 200:
            raise ItemAttributeException(
                'item description cannot exceed 200 characters')

        elif self.price <= 0:
            raise ItemAttributeException('item price must be greater than 0')

        elif self.stock < 0:
            raise ItemAttributeException('item stock must be greater than 0')

        elif self.collection is not None and len(self.collection) == 0:
            raise ItemAttributeException('item collection cannot be empty')

    def copy(self):
        """ create a copy of the item """
        return Item(self.dict())

    def dict(self):
        """ create a dictionary of the item """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'collection': self.collection
        }

    def __repr__(self) -> str:
        """ formatting for debugging """
        return f'Item({self.id}, {self.name}, {self.price}, {self.collection})'

    def __eq__(self, other: "Item") -> bool:
        return \
            self.id == other.id and \
            self.name == other.name and \
            self.description == other.description and \
            self.price == other.price and \
            self.stock == other.stock and \
            self.collection == other.collection
