from ariadne import ObjectType
from functools import wraps
from graphql.type import GraphQLResolveInfo


def resolver_with_context(resolver):
    """ Pull the context instance generated by the ContextMiddleware out """
    @wraps(resolver)
    def wrapper(parent, info: GraphQLResolveInfo, **kwargs):
        ctx = info.context['context']
        return resolver(parent, ctx, **kwargs)

    return wrapper


class ObjectTypeWithContext:
    """ Extends Ariadnes ObjectType to add a Context instance, 
    and update argument names when necessary """

    def __init__(self, name: str, *args, **kwargs):
        self.obj = ObjectType(name, *args, **kwargs)

    def field(self, name: str):
        """ Add field to schema using a decorator """
        def decorator(resolver):
            new_resolver = resolver_with_context(resolver)

            # register the resolver
            self.obj.field(name)(new_resolver)

            # "non-wrapping" returns the original resolver
            return resolver

        return decorator

    def add_field(self, name, resolver_function):
        """ Add field to schema """
        self.obj.field(name)(resolver_function)

    def bind_to_schema(self, schema):
        """ Required by Ariadne library """
        self.obj.bind_to_schema(schema)
