"""GraphQL trade type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLString,
    GraphQLID,
)

from .decimal import GraphQLDecimal

GraphQLBookTickerEvent = GraphQLObjectType(
    name="BookTickerEvent",
    fields=lambda: {
        "updateId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "symbol": GraphQLField(GraphQLNonNull(GraphQLString)),
        "bidPrice": GraphQLField(GraphQLNonNull(GraphQLDecimal)),
        "bidQuantity": GraphQLField(GraphQLNonNull(GraphQLDecimal)),
        "askPrice": GraphQLField(GraphQLNonNull(GraphQLDecimal)),
        "askQuantity": GraphQLField(GraphQLNonNull(GraphQLDecimal))
    }
)
