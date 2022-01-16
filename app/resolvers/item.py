from app.middleware import ObjectTypeWithContext
from app.db import Item

item = ObjectTypeWithContext('Item')


@item.field('createdAt')
def created_at(item: Item, _):
    return item.created_at


@item.field('updatedAt')
def updated_at(item: Item, _):
    return item.updated_at
