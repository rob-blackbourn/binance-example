"""GraphQL trade type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLString,
    GraphQLID,
)

from .numeric import GraphQLNumeric

GraphQLBookTickerEvent = GraphQLObjectType(
    name="BookTickerEvent",
    fields=lambda: {
        "updateId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "symbol": GraphQLField(GraphQLNonNull(GraphQLString)),
        "bidPrice": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "bidQuantity": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "askPrice": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "askQuantity": GraphQLField(GraphQLNonNull(GraphQLNumeric))
    }
)
