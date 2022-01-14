from fastapi import FastAPI
from starlette.responses import RedirectResponse
from ariadne import asgi
from mangum import Mangum

from app.middleware import ContextExtension
from app.resolvers import resolvers
from app.settings import settings

app = FastAPI()

# GraphQL endpoint
graphql = asgi.GraphQL(
    resolvers, debug=True, extensions=[ContextExtension(settings.context_maker)])

app.add_route('/graphql', graphql)
app.add_route('/', lambda _: RedirectResponse('/graphql'))

# AWS Lambda handler
handler = Mangum(app)
