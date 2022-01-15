import os
import boto3
from starlette.requests import Request

from app.db import DynamoDB, MemoryDB
from app.middleware import Context


class LocalContextMaker:
    def __init__(self):
        self.db = MemoryDB([])

    def __call__(self, request: Request):
        return Context(request, self.db),


class AWSContextMaker:
    def __init__(self, **credentials):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ['AWS_REGION_NAME'],
            **credentials
        )

        self.table = dynamodb.Table(os.environ['AWS_DYNAMODB_TABLE'])

    def __call__(self, request: Request = None):
        """ Context maker creates a DynamoDB client pointed that the correct partition """
        shop = request.headers.get('shop')
        if shop is None:
            shop = 'default'

        db = DynamoDB(self.table, shop)
        return Context(request, db)