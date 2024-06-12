import os
from datetime import datetime, time, timedelta, date
from backtrader import backtrader
import requests

from dotenv import load_dotenv

import pandas as pd
import bs4 as bs

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

load_dotenv();
api_key = os.getenv('PAPER_API_KEY')
api_secret = os.getenv('PAPER_API_SECRET')
client = StockHistoricalDataClient(api_key, api_secret)

def get_spy_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        if ticker == 'FB':
            ticker = 'META'
        tickers.append(ticker)
    return tickers


def get_opening_data(ticker, start_date, end_date):
    ''' 
    Get minute candles of opening hour for each trading day in range 
    '''
    current_date = start_date
    all_data = pd.DataFrame()

    while current_date <= end_date:
        if current_date.weekday() < 5:
            params = StockBarsRequest(
                symbol_or_symbols=ticker,
                timeframe=TimeFrame.Minute,
                start=datetime(current_date.year, current_date.month, current_date.day, 13, 30),
                end=datetime(current_date.year, current_date.month, current_date.day, 14, 31)
            )

            bars = client.get_stock_bars(params)
            if not bars.df.empty:
                all_data = pd.concat([all_data, bars.df])

        current_date += timedelta(days=1)

    all_data = all_data.reset_index(level='symbol', drop=True)

    all_data.sort_index(inplace=True)
    return all_data


class OpeningRangeBreakout(backtrader.Strategy):
    params = dict(
            num_opening_bars = 15
    )

    def __init__(self):
        self.opening_range_low = 0
        self.opening_range_high = 0
        self.opening_range = 0
        self.bought_today = False
        self.order = None

    def log(self, txt, dt=None):
        if dt is None:
            dt = self.datas[0].datetime.datetime()

        print('%s, %s' % (dt, txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        current_bar_datetime = self.data.num2date(self.data.datetime[0])
        previous_bar_datetime = self.data.num2date(self.data.datetime[-1])

        if current_bar_datetime.date() != previous_bar_datetime.date():
            self.opening_range_low = self.data.low[0]
            self.opening_range_high = self.data.high[0]
            self.bought_today = False

        opening_range_start_time = time(13, 30, 0)
        dt = datetime.combine(date.today(), opening_range_start_time) + timedelta(minutes=self.p.num_opening_bars)
        opening_range_end_time = dt.time()

        if current_bar_datetime.time() >= opening_range_start_time and current_bar_datetime.time() < opening_range_end_time:
            self.opening_range_high = max(self.data.high[0], self.opening_range_high)
            self.opening_range_low = min(self.data.low[0], self.opening_range_low)
            self.opening_range = self.opening_range_high - self.opening_range_low

        else:
            if self.order:
                return
            
            if self.position and (self.data.close[0] > (self.opening_range_high + self.opening_range)):
                self.close()

            if self.data.close[0] > self.opening_range_high and not self.position and not self.bought_today:
                self.order = self.buy()
                self.bought_today = True

            if self.position and (self.data.close[0] < (self.opening_range_high - self.opening_range)):
                self.order = self.close()

            if self.position and current_bar_datetime.time() >= time(14, 30, 0):
                self.log("RUNNING OUT OF TIME - LIQUIDIATING POSITION")
                self.close()

    def stop(self):
        self.log('(Num opening bars %2d) Ending value %.2f' % (self.params.num_opening_bars, self.broker.getvalue()))

        if self.broker.getvalue() > 130000: 
            self.log('*** BIG WINNER ***')
        elif self.broker.getvalue() < 70000:
            self.log('*** MAJOR LOSER ***')



if __name__ == '__main__':

    tickers = ['AAPL']
    start_date = datetime(2024, 5, 1)
    end_date = datetime(2024, 5, 31)




    for ticker in tickers:

        print(f'=== TESTING {ticker} ===')

        cerebro = backtrader.Cerebro()
        cerebro.broker.setcash(100000)


        historical_data = get_opening_data(ticker, start_date, end_date)
        data = backtrader.feeds.PandasData(dataname=historical_data)

        cerebro.adddata(data)

        cerebro.addstrategy(OpeningRangeBreakout)
        cerebro.addsizer(backtrader.sizers.PercentSizer, percents=95)

        cerebro.run()

        cerebro.plot()







