"""GraphQL trade type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLString,
    GraphQLID,
    GraphQLBoolean
)

from .datetime import GraphQLDateTime

GraphQLTrade = GraphQLObjectType(
    name="Trade",
    fields=lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLID)),
        "price": GraphQLField(GraphQLNonNull(GraphQLString)),
        "qty": GraphQLField(GraphQLNonNull(GraphQLString)),
        "quoteQty": GraphQLField(GraphQLNonNull(GraphQLString)),
        "time": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "isBuyerMaker": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "isBestMatch": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
    }
)
