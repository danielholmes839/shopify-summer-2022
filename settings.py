import os
import boto3
from starlette.requests import Request
from dotenv import load_dotenv

from db import Product, DynamoDB, MemoryDB
from middleware import Context


load_dotenv('.env')


class Local:
    def __init__(self):
        self.db = MemoryDB([
            Product({'id': '1', 'name': '1984', 'description': '1984 by George Orwell. The greatest book of all time',
                    'price': 20.0, 'category': 'books'}),
            Product({'id': '2', 'name': 'In Order To Live',
                    'description': '"In Order To Live" by Yeonmi Park a north korean girl\'s journey to freedom', 'price': 19.99, 'category': 'books'}),
            Product({'id': '4', 'name': 'Mystery Item',
                    'description': 'suspicious box', 'price': 100.00, 'category': None}),
        ])

    def context_maker(self, request: Request):
        return Context(request, self.db),


class AWS:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ['AWS_REGION_NAME'],
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )

        table_name = os.environ['AWS_DYNAMODB_TABLE']
        self.table = self.dynamodb.Table(table_name)

    def context_maker(self, request: Request = None):
        """ Context maker creates a DynamoDB client pointed that the correct partition """
        shop = request.headers.get("shop")
        if shop is None:
            shop = 'default'

        db = DynamoDB(self.table, shop)
        return Context(request, db)


settings = AWS()
