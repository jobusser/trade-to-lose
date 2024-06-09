
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from interfaces.data_provider import DataProvider

class HistoricalStockDataProvider(DataProvider):
    def __init__(self, symbol: str, timeframe: TimeFrame, start_date: datetime, end_date: datetime):
        """
        Initialize the data provider with specific parameters.
        
        Args:
            symbol (str): The stock symbol (e.g., 'AAPL', 'TSLA').
            timeframe (TimeFrame): The time frame for the data (e.g., TimeFrame.Minute, TimeFrame.Hour, TimeFrame.Day).
            start_date (datetime): The start date for the data fetching.
            end_date (datetime): The end date for the data fetching.
        """
        load_dotenv()
        api_key = os.getenv('PAPER_API_KEY')
        api_secret = os.getenv('PAPER_API_SECRET')
        
        self.client = StockHistoricalDataClient(api_key, api_secret)
        self.symbol = symbol
        self.timeframe = timeframe
        self.start_date = start_date
        self.end_date = end_date
        self.data = self._fetch_data()
        self.index = 0

    def _fetch_data(self):
        params = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=self.timeframe,
            start=self.start_date,
            end=self.end_date
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



