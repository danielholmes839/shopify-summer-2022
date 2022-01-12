from ariadne import make_executable_schema, load_schema_from_path
from middleware.context import Context

from middleware.middleware import ObjectTypeWithContext

query = ObjectTypeWithContext('Query')


@query.field('product')
def product_resolver(_, ctx: Context, **input):
    """ Product look up by id """
    return ctx.db.get_product(input['productId'])


@query.field('products')
def products_resolver(_, ctx: Context):
    """ All products """
    return ctx.db.get_products()


sdl = load_schema_from_path('./schema.graphql')

resolvers = make_executable_schema(sdl, query)
