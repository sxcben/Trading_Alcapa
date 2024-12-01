from gateway import Gateway
from strategies import MovingAverageStrategy 
from order_manager import OrderManager
from alpaca.trading.client import TradingClient
from config import *


if __name__ == '__main__':
    client = TradingClient(api_key, api_secret)
    print(client.get_account())
    gateway = Gateway('AAPL', start_date=start_date, end_date=end_date)
    order_manager = OrderManager(client)
    ma_strategy = MovingAverageStrategy('AAPL', order_manager)
    gateway.subscribe(ma_strategy)

    gateway.live_feed()
    print('finished')
    # order_manager.export_logs()