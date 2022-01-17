from app.db import Item, ItemNotFound, ItemAttributeException
from app.middleware import Context, ObjectTypeWithContext


def item_payload(resolver: callable):
    """ Catches exception and returns a ItemPayload """
    def wrapper(parent, ctx, **kwargs):
        try:
            item = resolver(parent, ctx, **kwargs)
            return {
                'item': item,
                'error': None
            }
        except (ItemNotFound, ItemAttributeException) as e:
            return {
                'item': None,
                'error': repr(e)
            }
        except Exception as e:
            return {
                'item': None,
                'error': f'unexpected error: {type(e).__name__}'
            }

    return wrapper


mutation = ObjectTypeWithContext('Mutation')


@mutation.field('itemCreate')
@item_payload
def create(_, ctx: Context, input: dict):
    """ itemCreate mutation"""
    item = Item(input)
    return ctx.db.insert_item(item)


@mutation.field('itemUpdate')
@item_payload
def update(_, ctx: Context, id: str, input: dict):
    """ itemUpdate mutation """
    created_at = ctx.db.get_item(id).created_at
    item = Item({'id': id, 'created_at': created_at, **input})
    return ctx.db.update_item(item)


@mutation.field('itemUpdateCollection')
@item_payload
def update_collection(_, ctx: Context, id: str, collection: str = None):
    """ itemUpdateCollection mutation """
    item = ctx.db.get_item(id)
    item.collection = collection
    return ctx.db.update_item(item)


@mutation.field('itemUpdateStock')
@item_payload
def update_stock(_, ctx: Context, id: str, change: int):
    """ itemUpdateStock mutation """
    item = ctx.db.get_item(id)
    item.stock += change
    return ctx.db.update_item(item)


@mutation.field('itemDelete')
@item_payload
def delete(_, ctx: Context, id: str):
    """ itemDelete mutation """
    return ctx.db.delete_item(id)
