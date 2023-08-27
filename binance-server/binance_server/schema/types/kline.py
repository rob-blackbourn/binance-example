"""GraphQL kline type"""

from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLInt,
)

from .datetime import GraphQLDateTime
from .numeric import GraphQLNumeric

GraphQLKLine = GraphQLObjectType(
    name="KLine",
    fields=lambda: {
        "openTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "open": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "high": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "low": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "close": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "volume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "closeTime": GraphQLField(GraphQLNonNull(GraphQLDateTime)),
        "quoteAssetVolume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "tradeCount": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "takerBuyBaseAssetVolume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
        "takerBuyQuoteAssetVolume": GraphQLField(GraphQLNonNull(GraphQLNumeric)),
    }
)
