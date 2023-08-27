"""Subscription for trade"""

import logging

from graphql import (
    GraphQLField,
    GraphQLNonNull,
    GraphQLArgument,
    GraphQLList,
    GraphQLString
)

from ...resolvers import subscribe_trade, resolve_trade_subscription
from ..types import GraphQLTradeEvent

LOGGER = logging.getLogger(__name__)


TradeSubscription = GraphQLField(
    GraphQLTradeEvent,
    args={
        'symbols': GraphQLArgument(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))
        )
    },
    subscribe=subscribe_trade,
    resolve=resolve_trade_subscription,
    description="Subscribe to trade"
)
