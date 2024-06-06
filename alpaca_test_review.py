import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus

load_dotenv();

api_key = os.getenv('PAPER_API_KEY')
api_secret = os.getenv('PAPER_API_SECRET')

trading_client = TradingClient(api_key, api_secret)

def get_positions():
    positions = trading_client.get_all_positions(); # can close current positions
    print(positions);

def get_orders():
    request_params = GetOrdersRequest(
            status = QueryOrderStatus.OPEN
    )

    orders = trading_client.get_orders(request_params);
    print(orders);
    return orders;
    
def cancel_orders():
    orders = get_orders();
    
    for order in orders:
        trading_client.cancel_order_by_id(order.id) # method exists to cancel all orders
    

get_orders();
cancel_orders();

