"""Subscription for bookTicker"""

import logging

from graphql import (
    GraphQLField,
    GraphQLNonNull,
    GraphQLArgument,
    GraphQLString,
    GraphQLList
)
from ...resolvers import subscribe_book_ticker, resolve_book_ticker_subscription

from ..types import GraphQLBookTickerEvent

LOGGER = logging.getLogger(__name__)


BookTickerSubscription = GraphQLField(
    GraphQLBookTickerEvent,
    args={
        'symbols': GraphQLArgument(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))
        )
    },
    subscribe=subscribe_book_ticker,
    resolve=resolve_book_ticker_subscription,
    description="Subscribe to book ticker"
)
