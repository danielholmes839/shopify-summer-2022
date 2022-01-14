import pytest
from app.db import DB, Product, ProductNotFound, ProductAttributeException
from app_tests.helpers import parameterized_db


@parameterized_db
def test_insert_get_delete(db: DB):
    """ insert -> get -> delete a product """
    product = Product({
        'name': '1984',
        'description': '1984 by George Orwell. The greatest book of all time',
        'price': 20.0,
        'category': None
    })

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
    for category in ['A', 'B', 'B', None]:
        db.insert_product(Product({
            'name': 'product_name',
            'description': 'product_description',
            'price': 9.99,
            'category': category
        }))

    assert len(db.get_products_by_category('A')) == 1
    assert len(db.get_products_by_category('B')) == 2
    assert len(db.get_products_by_category(None)) == 1


@parameterized_db
def test_update(db: DB):
    # insert a product
    inserted = db.insert_product(Product({
        'name': 'product_name',
        'description': 'product_description',
        'price': 1,
        'category': 'product_category'
    }))

    # update the product
    expected = Product({
        'id': inserted.id,
        'name': 'new_product_name',
        'description': 'new_product_description',
        'price': 2,
        'category': 'new_product_category'
    })

    updated = db.update_product(expected)
    assert expected == updated

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
        db.update_product(Product({
            'id': 'missing',
            'name': 'product_name',
            'description': 'product_description',
            'price': 1,
            'category': 'product_category'
        }))


@parameterized_db
def test_product_invalid(db: DB):
    # insert an invalid product
    with pytest.raises(ProductAttributeException):
        db.insert_product(Product({
            'name': 'product_name',
            'description': 'product_description',
            'price': -1,
            'category': 'product_category'
        }))

    # insert a valid product then update it with an invalid product
    with pytest.raises(ProductAttributeException):
        product = db.insert_product(Product({
            'name': 'product_name',
            'description': 'product_description',
            'price': 1,
            'category': 'product_category'
        }))

        product.price = -1
        db.update_product(product)
