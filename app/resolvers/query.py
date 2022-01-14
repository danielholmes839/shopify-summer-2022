from app.db import ProductNotFound
from app.middleware import Context, ObjectTypeWithContext


query = ObjectTypeWithContext('Query')


@query.field('product')
def product_resolver(_, ctx: Context, id):
    """ Product by id """
    try:
        return ctx.db.get_product(id)
    except ProductNotFound:
        return None


@query.field('products')
def products_resolver(_, ctx: Context):
    """ All products """
    return ctx.db.get_products()


@query.field('productsByCategory')
def products_by_category_resolver(_, ctx: Context, category):
    """ All products by category """
    return ctx.db.get_products_by_category(category)
