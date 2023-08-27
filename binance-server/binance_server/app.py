"""The ASGI application"""

from bareasgi import Application
from bareasgi_cors import add_cors_middleware
from bareasgi_graphql_next import add_graphql_next

from .schema import schema
from .utils import dumps_ex


def make_application() -> Application:

    app = Application()

    add_cors_middleware(app)

    add_graphql_next(app, schema, dumps=dumps_ex)

    return app
