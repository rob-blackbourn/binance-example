"""Entry pint for starting the service"""

import logging

from binance_server import start_server


def main():
    start_server()
    logging.shutdown()


if __name__ == '__main__':
    main()
