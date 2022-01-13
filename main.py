from fastapi import FastAPI

from ariadne import asgi
from middleware import ContextExtension
from resolvers import resolvers
from settings import settings

app = FastAPI()

# GraphQL endpoint
graphql = asgi.GraphQL(
    resolvers, debug=True, extensions=[ContextExtension(settings.context_maker)])

app.add_route('/graphql', graphql)
app.add_route('/', graphql)
