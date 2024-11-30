from abc import ABC, abstractmethod
import pandas as pd
print('hello')
from order import Order

class Strategy(ABC):
    def __init__(self, symbol, order_manager):
        self.order_manager = order_manager
        self.symbol = symbol
        self.data = pd.DataFrame(data=[], columns=['Adj Close', 'Volume'])
        self.nb_data_points = 0 # the number of data points in our price+volume time series

    def update(self, time, price, quantity):
        """ feeds updated price to the strategy """
        self.data.loc[time] = [price, quantity]
        self.nb_data_points += 1
        self.generate_signal()

    @abstractmethod
    def generate_signal(self):
        pass


class MovingAverageStrategy(Strategy):
    def __init__(self, symbol, order_manager, short_window = 50, long_window = 200):
        super().__init__(symbol, order_manager)
        self.short_window = short_window
        self.long_window = long_window
        self.signal = [0]

    def generate_signal(self):
        short_mavg = self.get_moving_average(self.short_window)
        long_mavg = self.get_moving_average(self.long_window)
        prev_signal = self.signal[-1]
        if self.nb_data_points >= self.long_window:
            if short_mavg > long_mavg:
                self.signal.append(1)
            else:
                self.signal.append(0)
            if self.signal[-1] != prev_signal:
                if self.signal[-1] < prev_signal: # sell signal
                    side = 'ASK'
                elif self.signal[-1] > prev_signal: # buy signal
                    side = 'BID'
                order = Order(side, self.data.iloc[-1]['Adj Close'], 1) # quantity = 1 : to improve
            else:
                order = None
            self.order_manager.send_order(order)

    def get_moving_average(self, window):
        return self.data.iloc[self.nb_data_points-window:]['Adj Close'].mean()