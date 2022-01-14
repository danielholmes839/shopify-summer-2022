import pytest
import boto3
from app.db import DynamoDB, MemoryDB
from moto import mock_dynamodb2


def dynamodb_client(table_name: str, shop_name: str) -> DynamoDB:
    """ Function to intialize a DynamoDB instance """
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='ca-central-1',
        aws_access_key_id='',
        aws_secret_access_key=''
    )

    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}
        ]
    )

    table = dynamodb.Table(table_name)
    return DynamoDB(table, shop_name)


def parameterized_db(unit_test: callable):
    """ Parameterized databases decorator"""
    databases = [
        (lambda: MemoryDB([])),
        (lambda: dynamodb_client('table', 'shop'))
    ]

    @pytest.mark.parametrize("db_lambda", databases)
    @mock_dynamodb2
    # test is callable with the database lambda function passed in
    def parameterized_test(db_lambda):
        return unit_test(db_lambda())

    return parameterized_test
