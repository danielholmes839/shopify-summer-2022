from re import T
from boto3.dynamodb.conditions import Key, Attr
from uuid import uuid4
from typing import List
from decimal import Decimal

from .item import Item
from .helpers import now
from .exceptions import ItemNotFound


class DynamoDB:
    def __init__(self, table, inventory: str):
        """ DynamoDB access """
        self.table = table  # table resource
        self.inventory = inventory

    def get_item(self, id: str) -> Item:
        """ get item by id"""
        response = self.table.get_item(Key=self.key(id))

        if 'Item' not in response:
            raise ItemNotFound(id)

        return self.parse(response['Item'])

    def get_items(self) -> List[Item]:
        # key conditions
        conditions = \
            Key('PK').eq(f'INVENTORY#{self.inventory}') & \
            Key('SK').begins_with('ITEM')

        response = self.table.query(
            KeyConditionExpression=conditions
        )

        return [self.parse(item) for item in response['Items']]

    def get_items_by_collection(self, collection: str) -> List[Item]:
        """ get items by collection """
        conditions = \
            Key('PK').eq(f'INVENTORY#{self.inventory}') & \
            Key('SK').begins_with('ITEM')

        # TODO add an index do make this query more efficient
        response = self.table.query(
            KeyConditionExpression=conditions,
            FilterExpression=Attr('collection').eq(collection)
        )

        return [self.parse(item) for item in response['Items']]

    def insert_item(self, item: Item) -> Item:
        """ Insert the item in dynamodb"""

        # assign a new uuid to the item
        item = item.copy()
        item.id = str(uuid4())
        t = now()
        item.created_at = t
        item.updated_at = t
        item.validate()

        # serialize and insert the item
        data = self.serialize(item)
        self.table.put_item(Item=data)

        return item

    def update_item(self, item: Item) -> Item:
        item.copy()
        item.updated_at = now()
        item.validate()

        # raises an exception if the item doesn't exist
        self.get_item(item.id)

        # serialize and update the item
        data = self.serialize(item)
        self.table.put_item(Item=data)

        return item

    def delete_item(self, id: str) -> Item:
        # raises an exception if the item doesn't exist
        item = self.get_item(id)

        self.table.delete_item(Key=self.key(id))
        return item

    def parse(self, data: dict) -> Item:
        """ Parse a item returned from dynamodb """
        data['cost'] = float(data['cost'])

        return Item(data)

    def serialize(self, item: Item) -> dict:
        """ Serializes a item  """
        data = {
            **self.key(item.id),
            **item.dict()
        }

        data['cost'] = Decimal(str(data['cost']))
        return data

    def key(self, id: str) -> dict:
        """ Creates the DynamoDB composite key"""
        return {
            'PK': f'INVENTORY#{self.inventory}',
            'SK': f'ITEM#{id}',
        }
