from datetime import datetime

from alpaca.data.timeframe import TimeFrame

from data_providers.historical_stock_data_provider import HistoricalStockDataProvider



# Example usage
if __name__ == "__main__":
    provider = HistoricalStockDataProvider(
        symbol="AAPL",
        timeframe=TimeFrame.Minute,
        start_date=datetime(2024, 5, 1),
        end_date=datetime(2024, 5, 2)
    )

    for _ in range(5):  # Fetch the first 5 bars
        print(provider.provide_data())
