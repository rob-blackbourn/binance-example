"""Queries for kline"""

from graphql import (
    GraphQLField,
    GraphQLString,
    GraphQLList,
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLInt
)

from ...resolvers import resolve_klines

from ..types import GraphQLDateTime, GraphQLKLine

KLineQuery = GraphQLField(
    GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLKLine))),
    args={
        'symbol': GraphQLArgument(GraphQLNonNull(GraphQLString)),
        'interval': GraphQLArgument(GraphQLNonNull(GraphQLString)),
        'startTime': GraphQLArgument(
            GraphQLDateTime,
            default_value=None,
            out_name='start_time'
        ),
        'endTime': GraphQLArgument(
            GraphQLDateTime,
            default_value=None,
            out_name='end_time'
        ),
        'limit': GraphQLArgument(GraphQLInt, default_value=None),
    },
    resolve=resolve_klines
)
