import pandas as pd
from config import *
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

class Gateway:
    """Gateway follows the Singleton design pattern"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create a new one
        if cls._instance is None:
            cls._instance = super(Gateway, cls).__new__(cls)
            cls._instance.logs = []  # Initialize the logs list for the first instance
        return cls._instance
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.subscribers = []  # List of observers
        self.stock_client = StockHistoricalDataClient(api_key=api_key, secret_key=api_secret)
        request_params = StockBarsRequest(symbol_or_symbols=symbol,
                                          timeframe=TimeFrame.Hour,
                                          start='2024-11-23',
                                          end = '2024-11-30')
        
        symbol_data = self.stock_client.get_stock_bars(request_params=request_params)
        if isinstance(symbol_data, dict):  # Si plusieurs symboles sont récupérés, prendre celui qui nous intéresse
            data = symbol_data[self.symbol].df
        else:  # Sinon, directement accéder au DataFrame
            data = symbol_data.df
        print(data)
        # Nettoyer et préparer les données
        data.dropna(inplace=True)  # Supprimer les lignes avec des valeurs manquantes
        data.sort_index(inplace=True)  # Trier les données par index (timestamp)
        
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
            
            
