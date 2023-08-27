"""Resolvers for bookTicker"""

from asyncio import CancelledError
from datetime import datetime
import json
import logging
from typing import Any, AsyncIterator, Sequence, TypedDict, Union, cast

from graphql import GraphQLResolveInfo
import websockets

from .common import BINANCE_WS_URL
from .types import (
    DataStreamDict,
    ErrorMessageDict,
    StreamResponseDict,
    Numeric
)

LOGGER = logging.getLogger(__name__)


class BookTickerEventDict(TypedDict):
    u: int  # order book updateId
    s: str  # symbol
    b: str  # best bid price
    B: str  # best bid qty
    a: str  # best ask price
    A: str  # best ask qty


BookTickerStreamDict = DataStreamDict[BookTickerEventDict]

Response = Union[BookTickerStreamDict, ErrorMessageDict, StreamResponseDict]


async def subscribe_book_ticker(
        _obj: Any,
        _info: GraphQLResolveInfo,
        symbols: Sequence[str]
) -> AsyncIterator[BookTickerEventDict]:

    if not symbols:
        return

    streams = [symbol + '@bookTicker' for symbol in symbols]
    query_string = f"streams={'/'.join(streams)}"
    url = f"{BINANCE_WS_URL}/stream?{query_string}"

    try:
        async with websockets.connect(url) as ws:  # type: ignore

            LOGGER.info("Subscribed to %s", symbols)

            async for msg in ws:

                response = cast(Response, json.loads(msg))

                if 'data' in response:
                    yield response['data']
                else:
                    raise ValueError("Unhandled message")

    except CancelledError:
        LOGGER.debug("Unsubscribed")
    except:
        LOGGER.exception("Subscription failed")

    LOGGER.debug("Unsubscribed from %s", symbols)


def resolve_book_ticker_subscription(
        obj: BookTickerEventDict,
        _info: GraphQLResolveInfo,
        symbols: Sequence[str]
) -> dict[str, str | int | float | Numeric | datetime]:
    return {
        "updateId": obj['u'],
        "symbol": obj['s'],
        "bidPrice": Numeric(obj['b']),
        "bidQuantity": Numeric(obj['B']),
        "askPrice": Numeric(obj['a']),
        "askQuantity": Numeric(obj['A'])
    }
