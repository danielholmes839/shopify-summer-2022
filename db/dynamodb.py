from boto3.dynamodb.conditions import Key, Attr
from uuid import uuid4
from typing import List
from decimal import Decimal

from .product import Product
from .exceptions import ProductNotFound


class DynamoDB:
    def __init__(self, table, shop: str):
        """ DynamoDB access """
        self.table = table  # table resource
        self.shop = shop

    def get_product(self, id: str) -> Product:
        """ get product by id"""
        response = self.table.get_item(Key=self.key(id))

        if 'Item' not in response:
            raise ProductNotFound(id)

        return self.parse(response['Item'])

    def get_products(self) -> List[Product]:
        # key conditions
        conditions = \
            Key('PK').eq(f'SHOP#{self.shop}') & \
            Key('SK').begins_with('PRODUCT')

        response = self.table.query(
            KeyConditionExpression=conditions
        )

        return [self.parse(item) for item in response['Items']]

    def get_products_by_category(self, category: str) -> List[Product]:
        """ get products by category """
        conditions = \
            Key('PK').eq(f'SHOP#{self.shop}') & \
            Key('SK').begins_with('PRODUCT')
        
        # TODO add an index do make this query more efficient
        response = self.table.query(
            KeyConditionExpression=conditions,
            FilterExpression=Attr('category').eq(category)
        )

        return [self.parse(item) for item in response['Items']]

    def insert_product(self, product: Product) -> Product:
        """ Insert the product in dynamodb"""

        # assign a new uuid to the product
        product = product.copy()
        product.id = str(uuid4())
        product.validate()

        # serialize and insert the product
        data = self.serialize(product)
        self.table.put_item(Item=data)

        return product

    def update_product(self, product: Product) -> Product:
        product.copy()
        product.validate()

        # raises an exception if the product doesn't exist
        self.get_product(product.id)

        # serialize and update the product
        data = self.serialize(product)
        self.table.put_item(Item=data)

        return product

    def delete_product(self, id: str) -> Product:
        # raises an exception if the product doesn't exist
        product = self.get_product(id)

        self.table.delete_item(Key=self.key(id))
        return product

    def parse(self, data: dict) -> Product:
        """ Parse a product returned from dynamodb """
        data['price'] = float(data['price'])
        if data['category'] == '':
            data['category'] = None

        return Product(data)

    def serialize(self, product: Product) -> dict:
        """ Serializes a product  """
        data = {
            **self.key(product.id),
            **product.dict()
        }

        if data['category'] is None:
            data['category'] = ''

        data['price'] = Decimal(str(data['price']))
        return data

    def key(self, id: str) -> dict:
        """ Creates the DynamoDB composite key"""
        return {
            'PK': f'SHOP#{self.shop}',
            'SK': f'PRODUCT#{id}',
        }
