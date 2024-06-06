import os
from dotenv import load_dotenv

from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient, StockTradesRequest

load_dotenv();

api_key = os.getenv('PAPER_API_KEY')
api_secret = os.getenv('PAPER_API_SECRET')

trading_client = TradingClient(api_key, api_secret)
print(trading_client.get_account().account_number);
print(trading_client.get_account().buying_power);

data_client = StockHistoricalDataClient(api_key, api_secret)

request_params = StockTradesRequest(
        symbol_or_symbols="AAPL",
        start=datetime(2024, 6, 6, 14, 30),
        end=datetime(2024, 6, 6, 14, 45)
)

trades = data_client.get_stock_trades(request_params)

for trade in trades.data["AAPL"]:
    print(trade)
    break;

