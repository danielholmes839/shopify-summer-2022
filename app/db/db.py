from abc import ABC, abstractmethod
from typing import List

from .item import Item


class DB(ABC):
    @abstractmethod
    def get_item(self, id: str) -> Item:
        pass

    @abstractmethod
    def get_items(self) -> List[Item]:
        pass

    @abstractmethod
    def get_items_by_collection(self, collection: str) -> List[Item]:
        pass

    @abstractmethod
    def insert_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def update_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def delete_item(self, id: str) -> Item:
        pass
