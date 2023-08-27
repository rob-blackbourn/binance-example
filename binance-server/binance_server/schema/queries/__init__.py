"""GraphQL queries"""

from graphql import GraphQLObjectType

from .kline import KLineQuery
from .trade import TradesQuery, HistoricalTradesQuery

GraphQLQueries = GraphQLObjectType(
    name='Queries',
    fields=lambda: {
        'klines': KLineQuery,
        'trades': TradesQuery,
        'historicalTrades': HistoricalTradesQuery
    }
)
