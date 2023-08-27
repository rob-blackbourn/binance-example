"""GraphQL trade event type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLString,
    GraphQLID,
    GraphQLBoolean
)

from .datetime import GraphQLDateTime
from .numeric import GraphQLNumeric

GraphQLTradeEvent = GraphQLObjectType(
    name="TradeEvent",
    fields=lambda: {
        "eventTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "symbol": GraphQLField(GraphQLNonNull(GraphQLString)),
        "tradeId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "price": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "quantity": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "buyerOrderId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "sellerOrderId": GraphQLField(GraphQLNonNull(GraphQLID)),
        "tradeTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "isBuyerMaker": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
    }
)
