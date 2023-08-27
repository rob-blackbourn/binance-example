"""GraphQL Schema"""

from graphql import GraphQLSchema

from .queries import GraphQLQueries
from .subscriptions import GraphQLSubscriptions

schema = GraphQLSchema(
    query=GraphQLQueries,
    subscription=GraphQLSubscriptions
)

__all__ = [
    'schema'
]
