from ariadne import make_executable_schema, load_schema_from_path
from .query import query
from .mutation import mutation


sdl = load_schema_from_path('./schema.graphql')

resolvers = make_executable_schema(sdl, query, mutation)
