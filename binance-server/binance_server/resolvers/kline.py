"""Resolvers for kline"""

from asyncio import CancelledError
from datetime import datetime
import json
import logging
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Optional,
    Sequence,
    TypedDict,
    Union,
    cast
)

from graphql import GraphQLResolveInfo
import httpx
import websockets

from .common import BINANCE_HTtP_URL, to_datetime, from_datetime, to_stream_url
from .types import (
    KLineInterval,
    Numeric,
    DataStreamDict,
    ErrorMessageDict,
    StreamResponseDict
)

LOGGER = logging.getLogger(__name__)


class KLineDetailDict(TypedDict):
    t: int  # Kline start time
    T: int  # Kline close time
    s: str  # Symbol
    i: str  # Interval
    f: int  # First trade ID
    L: int  # Last trade ID
    o: str  # Open price
    c: str  # Close price
    h: str  # High price
    l: str  # Low price
    v: str  # Base asset volume
    n: int  # Number of trades
    x: bool  # Is this kline closed?
    q: str  # Quote asset volume
    V: str  # Taker buy base asset volume
    Q: str  # Taker buy quote asset volume


class KLineEventDict(TypedDict):
    e: str  # event type ("kline")
    E: int  # Event time
    s: str  # Symbol
    k: KLineDetailDict


KLineStreamDict = DataStreamDict[KLineEventDict]

Response = Union[KLineStreamDict, ErrorMessageDict, StreamResponseDict]


async def subscribe_kline(
        _obj: Any,
        _info: GraphQLResolveInfo,
        symbols: Sequence[str],
        interval: KLineInterval
) -> AsyncIterator[KLineEventDict]:

    if not symbols:
        return

    url = to_stream_url(symbols, 'kline_' + interval)

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


def resolve_kline_subscription(
        root: KLineEventDict,
        _info: GraphQLResolveInfo,
        symbols: Sequence[str],
        interval: KLineInterval
) -> dict[str, str | int | float | Numeric | datetime]:
    obj = root['k']
    return {
        'startTime': to_datetime(obj['t']),
        'closeTime': to_datetime(obj['T']),
        'symbol': obj['s'],
        'interval': obj['i'],
        'firstTradeId': obj['f'],
        'lastTradeId': obj['L'],
        'open': Numeric(obj['o']),
        'close': Numeric(obj['c']),
        'high': Numeric(obj['h']),
        'low': Numeric(obj['l']),
        'volume': Numeric(obj['v']),
        'tradeCount': obj['n'],
        'isClosed': obj['x'],
        'quoteAssetVolume': Numeric(obj['q']),
        'takerBuyBaseAssetVolume': Numeric(obj['V']),
        'takerBuyQuoteAssetVolume': Numeric(obj['Q']),
    }


def _to_kline(
        open_time: int,
        open_price: str,
        high_price: str,
        low_price: str,
        close_price: str,
        volume: str,
        close_time: int,
        quote_asset_volume: str,
        number_of_trades: int,
        taker_buy_base_asset_volume: str,
        taker_buy_quote_asset_volume: str,
        _unused_field: Any
) -> Dict[str, str | int | Numeric | datetime]:
    return {
        'openTime': to_datetime(open_time),
        'open': Numeric(open_price),
        'high': Numeric(high_price),
        'low': Numeric(low_price),
        'close': Numeric(close_price),
        'volume': Numeric(volume),
        'closeTime': to_datetime(close_time),
        'quoteAssetVolume': Numeric(quote_asset_volume),
        'tradeCount': number_of_trades,
        'takerBuyBaseAssetVolume': Numeric(taker_buy_base_asset_volume),
        'takerBuyQuoteAssetVolume': Numeric(taker_buy_quote_asset_volume),
    }


async def resolve_klines(
        _obj: dict[str, str | int | float],
        _info: GraphQLResolveInfo,
        symbol: str,
        interval: KLineInterval,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        limit: Optional[int],
) -> list[dict[str, Any]]:
    LOGGER.debug("Fetching trades for %s", symbol)
    url = f"{BINANCE_HTtP_URL}/api/v3/klines?symbol={symbol}&interval={interval}"
    if start_time is not None:
        url += f'&startTime={from_datetime(start_time)}'
    if end_time is not None:
        url += f'&endTime={from_datetime(end_time)}'
    if limit is not None:
        url += f'&limit={limit}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        klines = json.loads(response.content)
        return [
            _to_kline(*line)
            for line in klines
        ]
