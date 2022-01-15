from uuid import uuid4
from typing import List

from .item import Item
from .helpers import now
from .db import DB
from .exceptions import ItemNotFound


class MemoryDB(DB):
    def __init__(self, items: List[Item]):
        self.items = dict([(p.id, p) for p in items])

    def get_item(self, id: str) -> Item:
        """ get item """
        item = self.items.get(id)
        if item is None:
            raise ItemNotFound(id)

        return item.copy()

    def get_items(self) -> List[Item]:
        """ get items """
        return [p.copy() for p in self.items.values()]

    def get_items_by_collection(self, collection: str) -> List[Item]:
        """ get items by collection """
        return [
            p.copy() for p in self.items.values()
            if p.collection == collection
        ]

    def insert_item(self, item: Item) -> Item:
        """ insert a item """
        item = item.copy()
        item.id = str(uuid4())

        t = now()
        item.created_at = t
        item.updated_at = t

        item.validate()

        self.items[item.id] = item
        return item

    def update_item(self, item: Item) -> Item:
        """ update a item """
        if not self.has(item.id):
            raise ItemNotFound(item.id)

        # update the item
        item = item.copy()
        item.updated_at = now()
        item.validate()

        self.items[item.id] = item

        return item

    def delete_item(self, id: str) -> Item:
        """ delete a item """
        if not self.has(id):
            raise ItemNotFound(id)

        # delete the item
        item = self.items.pop(id)
        return item.copy()

    def has(self, item_id: str) -> bool:
        """ has item """
        return item_id in self.items
