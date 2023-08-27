"""GraphQL Subscriptions"""

from graphql import GraphQLObjectType

from .book_ticker import BookTickerSubscription
from .trade import TradeSubscription

GraphQLSubscriptions = GraphQLObjectType(
    name="Subscriptions",
    fields=lambda: {
        'bookTickers': BookTickerSubscription,
        'trades': TradeSubscription
    }
)

__all__ = [
    'GraphQLSubscriptions'
]
