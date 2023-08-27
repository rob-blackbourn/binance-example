"""Common code"""

from datetime import datetime, timezone

BINANCE_WS_URL = "wss://stream.binance.com:9443"
BINANCE_HTtP_URL = "https://api.binance.com"


def to_datetime(value: int) -> datetime:
    return datetime.fromtimestamp(value/1000, tz=timezone.utc)


def from_datetime(value: datetime) -> int:
    return int(value.timestamp() * 1000)
