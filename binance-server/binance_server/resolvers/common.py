"""Common code"""

from datetime import datetime, timezone
from typing import Sequence

BINANCE_WS_URL = "wss://stream.binance.com:9443"
BINANCE_HTtP_URL = "https://api.binance.com"


def to_datetime(value: int) -> datetime:
    return datetime.fromtimestamp(value/1000, tz=timezone.utc)


def from_datetime(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def to_stream_url(symbols: Sequence[str], variable: str) -> str:
    streams = [f'{symbol.lower()}@{variable}' for symbol in symbols]
    query_string = f"streams={'/'.join(streams)}"
    url = f"{BINANCE_WS_URL}/stream?{query_string}"
    return url
