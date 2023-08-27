"""Server"""

import asyncio
import logging
import logging.config

from bareasgi import Application
from hypercorn.asyncio import serve
from hypercorn.config import Config

from .app import make_application


async def _start_http(app: Application):
    config = Config()
    config.bind = ["192.168.86.216:9009"]

    await serve(app, config)  # type: ignore


def start_server():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            'binance_server': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False
            },
        },
        'root': {
            'level': 'WARNING',
            'handlers': ['console']
        }
    })
    app = make_application()
    asyncio.run(_start_http(app))
