"""GraphQL kline event type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLInt,
    GraphQLString,
    GraphQLBoolean
)

from .datetime import GraphQLDateTime
from .numeric import GraphQLNumeric

GraphQLKLineEvent = GraphQLObjectType(
    name="KLineEvent",
    fields=lambda: {
        "startTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "closeTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "symbol": GraphQLField(GraphQLNonNull(GraphQLString)),
        "open": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "close": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "high": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "low": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "volume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "tradeCount": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "isClosed": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "quoteAssetVolume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "takerBuyBaseAssetVolume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "takerBuyBaseAssetVolume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
    }
)
