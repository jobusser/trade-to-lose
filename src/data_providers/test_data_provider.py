import os
from dotenv import load_dotenv
from datetime import datetime

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from interfaces.data_provider import DataProvider 

class TestDataProvider(DataProvider):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('PAPER_API_KEY')
        api_secret = os.getenv('PAPER_API_SECRET')
        
        self.client = StockHistoricalDataClient(api_key, api_secret)
        self.data = self._fetch_data()
        self.index = 0

    def _fetch_data(self):
        params = StockBarsRequest(
            symbol_or_symbols="AAPL",
            timeframe=TimeFrame.Minute,
            start=datetime(2024, 5, 1),
            end=datetime(2024, 5, 2)
        )
        bars = self.client.get_stock_bars(params)
        return bars.df

    def provide_data(self):
        if self.index < len(self.data):
            bar = self.data.iloc[self.index]
            self.index += 1
            return bar
        else:
            return None



