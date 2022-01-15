import pytest
from app.db import Product, ProductAttributeException


def test_eq():
    product = Product({
        'id': 'test_id',
        'name': 'test_name',
        'description': 'test_description',
        'price': 10.99,
        'stock': 1,
        'category': None,
    })

    assert product == product.copy()


def test_validate():
    valid = Product({
        'id': 'test_id',
        'name': 'test_name',
        'description': 'test_description',
        'price': 10.99,
        'stock': 1,
        'category': None,
    })

    valid.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.id = None
        product.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.name = ''
        product.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.name = 'X'*21
        product.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.description = 'X'*201
        product.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.price = 0
        product.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.stock = -1
        product.validate()

    with pytest.raises(ProductAttributeException):
        product = valid.copy()
        product.category = ''  # must use None
        product.validate()
