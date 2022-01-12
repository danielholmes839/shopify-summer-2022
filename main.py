from fastapi import FastAPI

from ariadne import asgi
from starlette.requests import Request
from middleware import ContextExtension, Context

from db import MemoryDB, Product
from resolvers import resolvers

app = FastAPI()

# Temporary memory db
db = MemoryDB({
    "1": Product("1", "Eggs", "great eggs", "food"),
    "2": Product("2", "1984", "1984 by George Orwell. The greatest book of all time", "books"),
    "3": Product("3", "Mystery Product", "1/10 chance of $500", None)
})


def context_maker(request: Request) -> Context:
    return Context(request, db)


# GraphQL endpoint
graphql_endpoint = asgi.GraphQL(
    resolvers, debug=True, extensions=[ContextExtension(context_maker)])

app.add_route('/graphql', graphql_endpoint)
