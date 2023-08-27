"""GraphQL Subscriptions"""

from graphql import GraphQLObjectType

from .book_ticker import BookTickerSubscription
from .kline import KLineSubscription
from .trade import TradeSubscription

GraphQLSubscriptions = GraphQLObjectType(
    name="Subscriptions",
    fields=lambda: {
        'bookTickers': BookTickerSubscription,
        'klines': KLineSubscription,
        'trades': TradeSubscription
    }
)

__all__ = [
    'GraphQLSubscriptions'
]
