from functools import wraps
from db.product import Product
from middleware import Context, ObjectTypeWithContext


def product_mutation(resolver: callable):
    """ Catches exception and returns a ProductPayload """
    def wrapper(parent, ctx, **kwargs):
        try:
            product = resolver(parent, ctx, **kwargs)
            print(product)
            return {
                'product': product,
                'error': None
            }
        except Exception as exception:
            return {
                'product': None,
                'error': repr(exception)
            }

    return wrapper


mutation = ObjectTypeWithContext('Mutation')


@mutation.field('productCreate')
@product_mutation
def create(_, ctx: Context, **args):
    product = ctx.db.insert_product(Product(args['input']))
    return product


@mutation.field('productUpdate')
@product_mutation
def update(_, ctx: Context, **args):
    """ Update a product """
    product = Product({
        'id': args['productId'],
        **args['input']
    })

    return ctx.db.update_product(product)


@mutation.field('productUpdateCategory')
@product_mutation
def update_category(_, ctx: Context, **args):
    """ Update the product category """
    product = ctx.db.get_product(args['productId'])
    product.category = args['category']

    return ctx.db.update_product(product)


@mutation.field('productDelete')
@product_mutation
def delete(_, ctx: Context, **args):
    """ Delete the product """
    product_id = args['productId']
    return ctx.db.delete_product(product_id)
