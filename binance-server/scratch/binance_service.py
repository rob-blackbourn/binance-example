"""Binance service"""

import asyncio

import websockets


async def main() -> None:
    url1 = 'wss://stream.binance.com:9443/stream?streams=BTCUSDT@trade/ETHUSDT@trade'
    url2 = "wss://stream.binance.com:9443/stream?streams=btcusdt@bookTicker/ethusdt@bookTicker"
    async with websockets.connect("wss://stream.binance.com:9443/stream?streams=btcusdt@bookTicker/ethusdt@bookTicker") as ws:
        async for msg in ws:
            print(msg)

if __name__ == '__main__':
    asyncio.run(main())
