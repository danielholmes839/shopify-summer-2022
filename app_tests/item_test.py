import pytest
from app.db import Item, ItemAttributeException


def test_eq():
    item = Item({
        'id': 'test_id',
        'product': 'test_product',
        'cost': 10.99,
        'stock': 1,
        'collection': None,
        'created_at': '',
        'updated_at': '',
    })

    assert item == item.copy()


def test_validate():
    valid = Item({
        'id': 'test_id',
        'product': 'test_product',
        'cost': 10.99,
        'stock': 1,
        'collection': None,
        'created_at': '',
        'updated_at': '',
    })

    valid.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.id = None
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.product = ''
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.product = 'X'*21
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.cost = 0
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.stock = -1
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.collection = ''  # must use None
        item.validate()
