"""GraphQL queries"""

from graphql import GraphQLObjectType

from .trade import TradesQuery, HistoricalTradesQuery

GraphQLQueries = GraphQLObjectType(
    name='Queries',
    fields=lambda: {
        'trades': TradesQuery,
        'historicalTrades': HistoricalTradesQuery
    }
)
