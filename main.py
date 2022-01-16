from fastapi import FastAPI
from starlette.responses import RedirectResponse
from ariadne import asgi
from mangum import Mangum

from app.resolvers import resolvers
from app.config import extensions

app = FastAPI()

# GraphQL endpoint
graphql = asgi.GraphQL(
    resolvers, debug=True, extensions=extensions)

app.add_route('/graphql', graphql)
app.add_route('/', lambda _: RedirectResponse('/graphql'))

# AWS Lambda handler
handler = Mangum(app)
