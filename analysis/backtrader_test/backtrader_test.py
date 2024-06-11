import backtrader as bt
import datetime
from strategies import BasicTestStrategy, MaTestStrategy


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.optstrategy(MaTestStrategy, maperiod=range(10, 31))

    # Create a Data Feeds
    data = bt.feeds.YahooFinanceCSVData(
        dataname='oracle.csv',
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.broker.setcommission(commission=0.00)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # cerebro.plot()
