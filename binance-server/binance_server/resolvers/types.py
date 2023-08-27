"""Types"""

from typing import Any, Generic, TypedDict, TypeVar

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
