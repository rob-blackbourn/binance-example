"""Subscription for kline"""

import logging

from graphql import (
    GraphQLField,
    GraphQLNonNull,
    GraphQLArgument,
    GraphQLList,
    GraphQLString
)

from ...resolvers import subscribe_kline, resolve_kline_subscription
from ..types import GraphQLKLineEvent

LOGGER = logging.getLogger(__name__)


KLineSubscription = GraphQLField(
    GraphQLKLineEvent,
    args={
        'symbols': GraphQLArgument(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))
        ),
        'interval': GraphQLArgument(
            GraphQLNonNull(GraphQLString)
        )
    },
    subscribe=subscribe_kline,
    resolve=resolve_kline_subscription,
    description="Subscribe to kline"
)
