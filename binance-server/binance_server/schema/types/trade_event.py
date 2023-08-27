"""GraphQL trade event type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLString,
    GraphQLFloat,
    GraphQLID,
    GraphQLBoolean
)

from .datetime import GraphQLDateTime

GraphQLTradeEvent = GraphQLObjectType(
    name="TradeEvent",
    fields=lambda: {
        "eventTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "symbol": GraphQLField(GraphQLNonNull(GraphQLString)),
        "tradeId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "price": GraphQLField(GraphQLNonNull(GraphQLFloat)),
        "quantity": GraphQLField(GraphQLNonNull(GraphQLFloat)),
        "buyerOrderId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "sellerOrderId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "tradeTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "isBuyerMaker": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
    }
)
