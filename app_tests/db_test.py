import pytest
from app.db import DB, Item, ItemNotFound, ItemAttributeException
from app_tests.helpers import parameterized_db


data = {
    'product': 'test_product',
    'cost': 1,
    'stock': 2,
    'collection': None
}

data2 = {
    'product': 'new_test_product',
    'cost': 10,
    'stock': 20,
    'collection': 'new_test_collection'
}


@parameterized_db
def test_insert_get_delete(db: DB):
    """ insert -> get -> delete a item """
    item = Item(data)

    assert item.id is None

    # insert a item
    inserted = db.insert_item(item)
    assert inserted.id is not None

    # get the item to verify it was inserted
    actual = db.get_item(inserted.id)
    assert actual == inserted

    # get all items in the database
    items = db.get_items()
    assert len(items) == 1
    assert items[0] == inserted

    # delete item
    deleted = db.delete_item(inserted.id)
    assert deleted == actual

    # delete the item twice
    with pytest.raises(ItemNotFound):
        db.delete_item(inserted.id)


@parameterized_db
def test_get_items_by_collection(db: DB):
    categories = ['A', 'B', 'B', None]

    for collection in categories:
        item = Item(data)
        item.collection = collection
        db.insert_item(item)

    # check for the correct amounts
    assert len(db.get_items_by_collection('A')) == 1
    assert len(db.get_items_by_collection('B')) == 2
    assert len(db.get_items_by_collection(None)) == 1

    # check for the correct categories
    for collection in set(categories):
        assert all([
            item.collection == collection
            for item in db.get_items_by_collection(collection)
        ])


@parameterized_db
def test_update(db: DB):
    # insert a item
    inserted = db.insert_item(Item(data))

    # update the item
    expected = Item(
        {'id': inserted.id, 'created_at': inserted.created_at, **data2})
    db.update_item(expected)

    # query the item
    actual = db.get_item(inserted.id)
    assert actual == expected


@parameterized_db
def test_not_found(db: DB):
    # get
    with pytest.raises(ItemNotFound):
        db.get_item('missing')

    # delete
    with pytest.raises(ItemNotFound):
        db.delete_item('missing')

    # update
    with pytest.raises(ItemNotFound):
        item = Item({'id': 'missing', 'created_at': '', **data})
        db.update_item(item)


@parameterized_db
def test_item_invalid(db: DB):
    # insert an invalid item
    with pytest.raises(ItemAttributeException):
        item = Item(data)
        item.cost = -1
        db.insert_item(item)

    # insert a valid item then update it with an invalid item
    with pytest.raises(ItemAttributeException):
        item = db.insert_item(Item(data))
        item.cost = -1

        db.update_item(item)
