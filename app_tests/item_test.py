import pytest
from app.db import Item, ItemAttributeException


def test_eq():
    item = Item({
        'id': 'test_id',
        'name': 'test_name',
        'description': 'test_description',
        'price': 10.99,
        'stock': 1,
        'collection': None,
    })

    assert item == item.copy()


def test_validate():
    valid = Item({
        'id': 'test_id',
        'name': 'test_name',
        'description': 'test_description',
        'price': 10.99,
        'stock': 1,
        'collection': None,
    })

    valid.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.id = None
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.name = ''
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.name = 'X'*21
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.description = 'X'*201
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.price = 0
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.stock = -1
        item.validate()

    with pytest.raises(ItemAttributeException):
        item = valid.copy()
        item.collection = ''  # must use None
        item.validate()
