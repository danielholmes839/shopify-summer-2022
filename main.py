from fastapi import FastAPI

from ariadne import asgi
from starlette.requests import Request
from middleware import ContextExtension, Context

from db import MemoryDB, Product
from resolvers import resolvers

app = FastAPI()

# Temporary memory db
db = MemoryDB([
    Product({
        'id': '1',
        'name': '1984',
        'description': '1984 by George Orwell. The greatest book of all time',
        'price': 20.0,
        'category': 'books'
    }),
    Product({
        'id': '2',
        'name': 'In Order To Live',
        'description': '"In Order To Live" by Yeonmi Park a north korean girl\'s journey to freedom',
        'price': 19.99,
        'category': 'books'
    }),
    Product({
        'id': '3',
        'name': 'Eggs',
        'description': '6 eggs',
        'price': 3.00,
        'category': 'food'
    }),
    Product({
        'id': '4',
        'name': 'Mystery Item',
        'description': 'suspicious box',
        'price': 100.00,
        'category': None
    }),
])


def context_maker(request: Request) -> Context:
    return Context(request, db)


# GraphQL endpoint
graphql_endpoint = asgi.GraphQL(
    resolvers, debug=True, extensions=[ContextExtension(context_maker)])

app.add_route('/graphql', graphql_endpoint)
