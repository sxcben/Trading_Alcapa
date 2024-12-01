from gateway import Gateway
from strategies import MovingAverageStrategy 
from order_manager import OrderManager
from alpaca.trading.client import TradingClient
from config import *


if __name__ == '__main__':
    client = TradingClient(api_key, api_secret)
    gateway = Gateway('AAPL')
    order_manager = OrderManager(client, 1000000)
    ma_strategy = MovingAverageStrategy('AAPL', order_manager)
    print(ma_strategy.order_manager)
    gateway.subscribe(ma_strategy)

    gateway.live_feed()

    order_manager.export_logs()