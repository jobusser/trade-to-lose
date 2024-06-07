import os
from dotenv import load_dotenv

from datetime import date, datetime

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame

load_dotenv();

api_key = os.getenv('PAPER_API_KEY')
api_secret = os.getenv('PAPER_API_SECRET')


client = StockHistoricalDataClient(api_key, api_secret)

def get_guotes():
    multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY", "GLD", "TLT"])
    latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)
    gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
    spy_latest_ask_price = latest_multisymbol_quotes["SPY"].ask_price
    
    for quote in latest_multisymbol_quotes:
        print(quote)

    print('\n\n\n')
    print(gld_latest_ask_price)
    print(spy_latest_ask_price)

def get_historical_data():
    params = StockBarsRequest(
            symbol_or_symbols="AAPL",
            timeframe=TimeFrame.Minute,
            start=datetime(2024, 5, 1),
            end=datetime(2024, 5, 2)
    )

    bars = client.get_stock_bars(params)

    print(bars.df)


get_historical_data()


