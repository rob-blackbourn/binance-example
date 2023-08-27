"""Utilities"""

import asyncio
from asyncio import Event, Task
from datetime import datetime, date
from decimal import Decimal
import json
import platform
import signal
from types import FrameType
from typing import Any, Optional


class JSONEncodeEX(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + ('Z' if not o.tzinfo else '')
        elif isinstance(o, date):
            return o.isoformat() + 'T00:00:00Z'
        elif isinstance(o, Decimal):
            return float(
                str(
                    o.quantize(Decimal(1))
                    if o == o.to_integral()
                    else o.normalize()
                )
            )
        else:
            return super(JSONEncodeEX, self).default(o)


def dumps_ex(obj: Any) -> str:
    return json.dumps(obj, cls=JSONEncodeEX, allow_nan=True)


class CancellationEvent(Event):

    def __init__(self) -> None:
        super().__init__()

        loop = asyncio.get_event_loop()

        self._windows_task: Optional[Task] = None
        if platform.system() == "Windows":
            self._windows_task = asyncio.create_task(
                self._windows_signal_support()
            )

        def _signal_handler(sig_value: int, _from: Optional[FrameType]) -> None:
            print(f"Received signal {signal.Signals(sig_value).name}")
            self.set()

        for signal_name in {"SIGINT", "SIGTERM", "SIGBREAK"}:
            if hasattr(signal, signal_name):
                sig_value = getattr(signal, signal_name)
                try:
                    loop.add_signal_handler(sig_value, _signal_handler)
                except NotImplementedError:
                    signal.signal(sig_value, _signal_handler)

    async def wait_exit(self) -> None:
        if self._windows_task is not None:
            await self._windows_task

    async def _windows_signal_support(self) -> None:
        while not self.is_set():
            try:
                await asyncio.wait_for(self.wait(), 1)
            except asyncio.TimeoutError:
                pass
