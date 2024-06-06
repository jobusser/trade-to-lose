import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv();

api_key = os.getenv('PAPER_API_KEY')
api_secret = os.getenv('PAPER_API_SECRET')

trading_client = TradingClient(api_key, api_secret)

def buy():
    market_order_data = MarketOrderRequest(
            symbol = "SPY",
            qty = 1,
            side = OrderSide.BUY,
            time_in_force = TimeInForce.DAY
    )

    market_order = trading_client.submit_order(market_order_data);
    print(market_order);

def buy_limit_order():
    # buy at a specified price limit
    # price is far too low, order will sit and will not be filled i.e. executed
    limit_order_data = LimitOrderRequest(
            symbol = "SPY",
            qty = 1,
            side = OrderSide.BUY,
            time_in_force = TimeInForce.DAY,
            limit_price = 400.00
    )

    limit_order = trading_client.submit_order(limit_order_data);
    print(limit_order);

buy_limit_order();

