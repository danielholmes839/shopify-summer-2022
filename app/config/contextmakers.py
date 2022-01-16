import os
import boto3
from starlette.requests import Request

from app.db import DynamoDB, MemoryDB
from app.middleware import Context


class LocalContextMaker:
    def __init__(self):
        self.inventories = {
            'default': MemoryDB([])
        }

    def __call__(self, request: Request):
        inventory = request.headers.get('inventory')
        if inventory is None:
            inventory = 'default'
        
        if inventory not in self.inventories:
            self.inventories[inventory] = MemoryDB([])

        db = self.inventories[inventory]
        return Context(request, db)


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
        inventory = request.headers.get('inventory')
        if inventory is None:
            inventory = 'default'

        db = DynamoDB(self.table, inventory)
        return Context(request, db)
