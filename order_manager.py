
import time
class OrderManager:
    """OrderManager follows the Singleton design pattern"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create a new one
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
            cls._instance.logs = []  # Initialize the logs list for the first instance
        return cls._instance
    
    def __init__(self, client):
        self.client = client
        self.capital = [int(client.get_account().cash)]
        self.nb_shares = [0] # number of shares owned
        self.logs = []
        

    def risk_management_decorator(func):
        def wrapper(self, order, price):
            if order is None:
               return func(self, order, price) 
            
            elif order.side.value == 'buy':
                if price*order.qty <= self.capital[-1]:
                    return func(self, order, price)
                else:
                    self.log('Order canceled : insufficient capital')
                    return func(self, None, price)
            elif order.side.value == 'sell':
                if order.qty <= self.nb_shares[-1]:
                    return func(self, order, price)
                else:
                    self.log('Order canceled : insufficient number of shares')
                    return func(self, None, price)
                
        return wrapper

    @risk_management_decorator
    def send_order(self, order, price):
        print(order)
        if order is None:
            self.capital.append(self.capital[-1])
            self.nb_shares.append(self.nb_shares[-1])
        else:
            print('order send')
            self.client.submit_order(order)


            time.sleep(1)  # Poll every second
            if order.side.value == 'buy':
                self.capital.append(self.capital[-1] - price*order.qty)
                self.nb_shares.append(self.nb_shares[-1] + order.qty)
            elif order.side.value == 'sell':
                self.capital.append(self.capital[-1] + price*order.qty)
                self.nb_shares.append(self.nb_shares[-1] - order.qty)
            