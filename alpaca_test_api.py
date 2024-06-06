import os
from dotenv import load_dotenv

from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient, StockTradesRequest

load_dotenv();

api_key = os.getenv('PAPER_API_KEY')
api_secret = os.getenv('PAPER_API_SECRET')

trading_client = TradingClient(api_key, api_secret)

print(trading_client.get_account().account_number)
print(trading_client.get_account().buying_power)
print(trading_client.get_account())
