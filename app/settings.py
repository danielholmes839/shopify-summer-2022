import os
import boto3
from starlette.requests import Request
from dotenv import load_dotenv

from app.db import Product, DynamoDB, MemoryDB
from app.middleware import Context


load_dotenv('.env')


class Local:
    def __init__(self):
        self.db = MemoryDB([])

    def context_maker(self, request: Request):
        return Context(request, self.db),


class AWS:
    def __init__(self):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ['AWS_REGION_NAME'],
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )

        self.table = dynamodb.Table(os.environ['AWS_DYNAMODB_TABLE'])

    def context_maker(self, request: Request = None):
        """ Context maker creates a DynamoDB client pointed that the correct partition """
        shop = request.headers.get("shop")
        if shop is None:
            shop = 'default'

        db = DynamoDB(self.table, shop)
        return Context(request, db)


settings = AWS()
