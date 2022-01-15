from math import prod
import pytest
from app.db import DB, Product, ProductNotFound, ProductAttributeException
from app_tests.helpers import parameterized_db


data = {
    'name': 'test_name',
    'description': 'test_description',
    'price': 1,
    'stock': 2,
    'category': None
}

data2 = {
    'name': 'new_test_name',
    'description': 'new_test_description',
    'price': 10,
    'stock': 20,
    'category': 'new_test_category'
}


@parameterized_db
def test_insert_get_delete(db: DB):
    """ insert -> get -> delete a product """
    product = Product(data)

    assert product.id is None

    # insert a product
    inserted = db.insert_product(product)
    assert inserted.id is not None

    # get the product to verify it was inserted
    actual = db.get_product(inserted.id)
    assert actual == inserted

    # get all products in the database
    products = db.get_products()
    assert len(products) == 1
    assert products[0] == inserted

    # delete product
    deleted = db.delete_product(inserted.id)
    assert deleted == actual

    # delete the product twice
    with pytest.raises(ProductNotFound):
        db.delete_product(inserted.id)


@parameterized_db
def test_get_products_by_category(db: DB):
    categories = ['A', 'B', 'B', None]

    for category in categories:
        product = Product(data)
        product.category = category
        db.insert_product(product)

    # check for the correct amounts
    assert len(db.get_products_by_category('A')) == 1
    assert len(db.get_products_by_category('B')) == 2
    assert len(db.get_products_by_category(None)) == 1

    # check for the correct categories
    for category in set(categories):
        assert all([
            product.category == category
            for product in db.get_products_by_category(category)
        ])


@parameterized_db
def test_update(db: DB):
    # insert a product
    inserted = db.insert_product(Product(data))

    # update the product
    expected = Product({'id': inserted.id, **data2})
    db.update_product(expected)

    # query the product
    actual = db.get_product(inserted.id)
    assert actual == expected


@parameterized_db
def test_not_found(db: DB):
    # get
    with pytest.raises(ProductNotFound):
        db.get_product('missing')

    # delete
    with pytest.raises(ProductNotFound):
        db.delete_product('missing')

    # update
    with pytest.raises(ProductNotFound):
        product = Product({'id': 'missing', **data})
        db.update_product(product)


@parameterized_db
def test_product_invalid(db: DB):
    # insert an invalid product
    with pytest.raises(ProductAttributeException):
        product = Product(data)
        product.price = -1
        db.insert_product(product)

    # insert a valid product then update it with an invalid product
    with pytest.raises(ProductAttributeException):
        product = db.insert_product(Product(data))
        product.price = -1

        db.update_product(product)
