"""Resolvers for kline"""

from datetime import datetime
import json
import logging
from typing import (
    Any,
    Dict,
    Optional,
)

from graphql import GraphQLResolveInfo
import httpx

from .common import BINANCE_HTtP_URL, to_datetime, from_datetime
from .types import KLineInterval, Numeric

LOGGER = logging.getLogger(__name__)


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
