import pandas as pd
class Gateway:
    """Gateway follows the Singleton design pattern"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create a new one
        if cls._instance is None:
            cls._instance = super(Gateway, cls).__new__(cls)
            cls._instance.logs = []  # Initialize the logs list for the first instance
        return cls._instance
    
    def __init__(self, symbol, file):
        self.symbol = symbol
        self.subscribers = []  # List of observers
        data = pd.read_csv(file)
        data.dropna(inplace=True)  # Remove any rows with missing values
        data['Datetime'] = data['Datetime'].str.replace('-04:00', '')
        data.set_index('Datetime', inplace=True)  # Set Datetime as index
        data.sort_index(inplace=True)  # Sort by datetime
        self.data = data

    def subscribe(self, subscriber):
        """Add an observer to the list."""
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        """Remove an observer from the list."""
        self.subscribers.remove(subscriber)

    def notify(self, time, price, quantity):
        """Notify all subscribers of a price update."""
        for subscriber in self.subscribers:
            subscriber.update(time, price, quantity)
    
    def live_feed(self):
        for index, row in self.data.iterrows():
            self.notify(index, float(row['Adj Close']), int(row['Volume']))