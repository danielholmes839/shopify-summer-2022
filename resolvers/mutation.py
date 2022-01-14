from db import Product, ProductNotFound, ProductAttributeException
from middleware import Context, ObjectTypeWithContext


def product_payload(resolver: callable):
    """ Catches exception and returns a ProductPayload """
    def wrapper(parent, ctx, **kwargs):
        try:
            product = resolver(parent, ctx, **kwargs)
            return {
                'product': product,
                'error': None
            }
        except (ProductNotFound, ProductAttributeException) as e:
            return {
                'product': None,
                'error': repr(e)
            }
        except Exception as e:
            return {
                'product': None,
                'error': f'unexpected error: {type(e).__name__}'
            }

    return wrapper


mutation = ObjectTypeWithContext('Mutation')


@mutation.field('productCreate')
@product_payload
def create(_, ctx: Context, input: dict):
    """ productCreate mutation"""
    product = Product(input)
    return ctx.db.insert_product(product)


@mutation.field('productUpdate')
@product_payload
def update(_, ctx: Context, id: str, input: dict):
    """ productUpdate mutation """
    product = Product({'id': id, **input})
    return ctx.db.update_product(product)


@mutation.field('productUpdateCategory')
@product_payload
def update_category(_, ctx: Context, id: str, category: str):
    """ productUpdateCategory mutation """
    product = ctx.db.get_product(id)
    product.category = category
    return ctx.db.update_product(product)


@mutation.field('productDelete')
@product_payload
def delete(_, ctx: Context, id: str):
    """ productDelete mutation """
    return ctx.db.delete_product(id)
