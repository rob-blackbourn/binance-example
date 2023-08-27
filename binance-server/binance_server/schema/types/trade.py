"""GraphQL trade type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLID,
    GraphQLBoolean
)

from .datetime import GraphQLDateTime
from .numeric import GraphQLNumeric

GraphQLTrade = GraphQLObjectType(
    name="Trade",
    fields=lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLID)),
        "price": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "qty": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "quoteQty": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "time": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "isBuyerMaker": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "isBestMatch": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
    }
)
