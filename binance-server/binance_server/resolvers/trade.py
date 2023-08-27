"""Resolvers for trade"""

from asyncio import CancelledError
from datetime import datetime
import json
import logging
from typing import (
    Any,
    AsyncIterator,
    Optional,
    Sequence,
    TypedDict,
    Union,
    cast
)

from graphql import GraphQLResolveInfo
import httpx
import websockets

from .common import (
    BINANCE_HTtP_URL,
    to_datetime,
    to_stream_url
)
from .types import (
    DataStreamDict,
    ErrorMessageDict,
    StreamResponseDict,
    Numeric
)

LOGGER = logging.getLogger(__name__)


class TradeEventDict(TypedDict):
    e: str      # Event type
    E: int      # Event time
    s: str      # Symbol
    t: int      # Trade ID
    p: str      # Price
    q: str      # Quantity
    b: int      # Buyer order ID
    a: int      # Seller order ID
    T: int      # Trade time
    m: bool     # Is the buyer the market maker?
    M: bool     # Ignore


TradeStreamDict = DataStreamDict[TradeEventDict]

Response = Union[TradeStreamDict, ErrorMessageDict, StreamResponseDict]


async def subscribe_trade(
        _obj: Any,
        info: GraphQLResolveInfo,
        symbols: Sequence[str]
) -> AsyncIterator[TradeEventDict]:

    if not symbols:
        return

    url = to_stream_url(symbols, "trade")

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


def resolve_trade_subscription(
        obj: dict[str, str | int | float],
        info: GraphQLResolveInfo,
        *args,
        **kwargs
) -> dict[str, str | int | float | datetime]:
    return {
        "eventTime": to_datetime(cast(int, obj['E'])),
        "symbol": obj['s'],
        "tradeId": obj['t'],
        "price": obj['p'],
        "quantity": obj['q'],
        "buyerOrderId": obj['b'],
        "sellerOrderId": obj['a'],
        "tradeTime": to_datetime(cast(int, obj['T'])),
        "isBuyerMaker": obj['m']
    }


async def resolve_trades(
        _obj: dict[str, str | int | float],
        _info: GraphQLResolveInfo,
        symbol: str,
        limit: Optional[int]
) -> list[dict[str, Any]]:
    LOGGER.debug("Fetching trades for %s", symbol)
    url = f"{BINANCE_HTtP_URL}/api/v3/trades?symbol={symbol}"
    if limit is not None:
        url += f'&limit={limit}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        trades = json.loads(response.content)
        return [
            {
                "id": trade['id'],
                "price": Numeric(trade['price']),
                "qty": Numeric(trade['qty']),
                "quoteQty": Numeric(trade['quoteQty']),
                "time": to_datetime(trade['time']),
                "isBuyerMaker": trade['isBuyerMaker'],
                "isBestMatch": trade['isBestMatch']
            }
            for trade in trades
        ]


async def resolve_historical_trades(
        _obj: dict[str, str | int | float],
        _info: GraphQLResolveInfo,
        symbol: str,
        limit: Optional[int],
        from_id: Optional[int]
) -> list[dict[str, Any]]:
    url = f"{BINANCE_HTtP_URL}/api/v3/historicalTrades?symbol={symbol}"
    if limit is not None:
        url += f'&limit={limit}'
    if from_id is not None:
        url += f'&fromId={from_id}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        trades = json.loads(response.content)
        return [
            {
                "id": trade['id'],
                "price": Numeric(trade['price']),
                "qty": Numeric(trade['qty']),
                "quoteQty": Numeric(trade['quoteQty']),
                "time": to_datetime(trade['time']),
                "isBuyerMaker": trade['isBuyerMaker'],
                "isBestMatch": trade['isBestMatch']
            }
            for trade in trades
        ]
