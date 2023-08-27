"""Types"""

from decimal import Decimal
from typing import Any, Generic, Literal, TypedDict, TypeVar

TData = TypeVar('TData')


class DataStreamDict(TypedDict, Generic[TData]):
    stream: str
    data: TData


class ErrorMessageDict(TypedDict):
    code: int
    msg: str


class StreamResponseDict(TypedDict):
    result: Any
    id: int


Numeric = Decimal
# Numeric = str

KLineInterval = Literal[
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
    "1M",
]
