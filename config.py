# Use you API key and secret
api_key = 'PK5RZN11XAH8ZZFDUPNT'
api_secret = 'L1AofM3BeGLGCRnRvUTUu8h1MVHSS16YOAoh6ixs'
base_url = 'https://paper-api.alpaca.markets/v2'  # Use paper trading base URL for testing

from alpaca.trading.client import TradingClient
client = TradingClient(api_key, api_secret)