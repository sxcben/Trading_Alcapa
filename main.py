from gateway import Gateway
from strategies import MovingAverageStrategy 
from order_manager import OrderManager

if __name__ == '__main__':
    gateway = Gateway('DPZ', '../data/dominos_data.csv')
    order_manager = OrderManager(1000000)
    ma_strategy = MovingAverageStrategy('DPZ', order_manager)
    
    gateway.subscribe(ma_strategy)

    gateway.live_feed()

    order_manager.export_logs()