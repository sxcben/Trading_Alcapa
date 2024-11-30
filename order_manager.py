class OrderManager:
    """OrderManager follows the Singleton design pattern"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create a new one
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
            cls._instance.logs = []  # Initialize the logs list for the first instance
        return cls._instance
    
    def __init__(self, capital):
        self.capital = [capital]
        self.nb_shares = [0] # number of shares owned
        self.logs = []

    def risk_management_decorator(func):
        def wrapper(self, order):
            if order is None:
               return func(self, order) 
            elif order.side == 'BID':
                if order.price*order.quantity <= self.capital[-1]:
                    return func(self, order)
                else:
                    self.log('Order canceled : insufficient capital')
                    return func(self, None)
            elif order.side == 'ASK':
                if order.quantity <= self.nb_shares[-1]:
                    return func(self, order)
                else:
                    self.log('Order canceled : insufficient number of shares')
                    return func(self, None)
        return wrapper

    @risk_management_decorator
    def send_order(self, order):
        if order is None:
            self.capital.append(self.capital[-1])
            self.nb_shares.append(self.nb_shares[-1])
        else:
            status, quantity_executed = self.matching_engine.try_execute(order)
            if status == 0:
                self.log('Order filled : ' + str(order))
            elif status == 1:
                self.log('Order partially filled : (quantity filled = ' + str(quantity_executed) + ')' + str(order))
            else:
                self.log('Order canceled : ' + str(order))
            if order.side == 'BID':
                self.capital.append(self.capital[-1] - order.price*quantity_executed)
                self.nb_shares.append(self.nb_shares[-1] + quantity_executed)
            elif order.side == 'ASK':
                self.capital.append(self.capital[-1] + order.price*quantity_executed)
                self.nb_shares.append(self.nb_shares[-1] - quantity_executed)