from app.db import ItemNotFound
from app.middleware import Context, ObjectTypeWithContext


query = ObjectTypeWithContext('Query')


@query.field('item')
def item_resolver(_, ctx: Context, id):
    """ Item by id """
    try:
        return ctx.db.get_item(id)
    except ItemNotFound:
        return None


@query.field('items')
def items_resolver(_, ctx: Context):
    """ All items """
    products = ctx.db.get_items()
    return sorted(products, key=lambda product: product.created_at, reverse=True)


@query.field('itemsByCollection')
def items_by_collection_resolver(_, ctx: Context, collection):
    """ All items by collection """
    products = ctx.db.get_items_by_collection(collection)
    return sorted(products, key=lambda product: product.created_at, reverse=True)
