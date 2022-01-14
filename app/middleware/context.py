from ariadne.types import Extension
from typing import Callable
from starlette.requests import Request
from app.db import DB


class Context:
    def __init__(self, request: Request, db: DB):
        self.request: Request = request
        self.db: DB = db


ContextMaker = Callable[[Request], Context]


class ContextExtension(Extension):
    """ Adds a context instance to the request """

    def __init__(self, context_maker=None):
        self.context_maker = context_maker

    def request_started(self, context):
        context['context'] = self.context_maker(context['request'])

    def __call__(self):
        # Tricking the framework
        return self
