"""Queries for trade"""

from graphql import (
    GraphQLField,
    GraphQLString,
    GraphQLList,
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLInt
)

from ...resolvers import resolve_trades, resolve_historical_trades

from ..types import GraphQLTrade

TradesQuery = GraphQLField(
    GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLTrade))),
    args={
        'symbol': GraphQLArgument(GraphQLNonNull(GraphQLString)),
        'limit': GraphQLArgument(GraphQLInt, default_value=None),
    },
    resolve=resolve_trades
)

HistoricalTradesQuery = GraphQLField(
    GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLTrade))),
    args={
        'symbol': GraphQLArgument(GraphQLNonNull(GraphQLString)),
        'limit': GraphQLArgument(GraphQLInt, default_value=None),
        'fromId': GraphQLArgument(GraphQLInt, out_name="from_id", default_value=None),
    },
    resolve=resolve_historical_trades
)
