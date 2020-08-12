"""A Simple Strategy Trading Two Stocks

Original code: https://blog.csdn.net/qq_26948675/article/details/80016633
Modified based on: https://www.backtrader.com/blog/posts/2018-04-22-improving-code/improving-code.html

Replaced the local CSV files with online data from IEX.

Unfortunately, this strategy is not profitable for the two stocks picked.
"""

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import pandas as pd
# Import the backtrader platform
import backtrader as bt
import logging
logging.getLogger('matplotlib').disabled = True
logging.getLogger('matplotlib.font_manager').disabled = True

class TestStrategy(bt.Strategy):
    params = (
        # Standard MACD Parameters
        ('period', 252),
        ('prepend_constant', True),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose_x = self.datas[0].close
        self.dataclose_y = self.datas[1].close
        ma1 = bt.indicators.SMA(
            self.data0, period=self.p.period)
        ma2 = bt.indicators.SMA(
            self.data1, period=self.p.period)
        # Use a built-in indicator
        ma1_pct = bt.ind.PctChange(ma1, period=1)  # The ma1 percentage part
        ma2_pct = bt.ind.PctChange(ma2, period=1)  # The ma2 percentage part
        # # Use line delay notation (-x) to get a ref to the -1 point
        # ma1_pct = ma1 / ma1(-1) - 1.0  # The ma1 percentage part
        # ma2_pct = ma2 / ma2(-1) - 1.0  # The ma2 percentage part
        self.buy_sig = ma1_pct > ma2_pct  # buy signal
        self.sell_sig = ma1_pct <= ma2_pct  # sell signal
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_cashvalue(self, cash, value):
        self.log('Cash %s Value %s' % (cash, value))

    def notify_order(self, order):
        print(type(order), 'Is Buy ', order.isbuy())
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose_x[0])
        self.log('Close, %.2f' % self.dataclose_y[0])
        # Check if we are in the market
        if not self.getposition(self.datas[1]):
            # Not yet ... we MIGHT BUY if ...
            if self.buy_sig:
                    # if sma[0]<top[-5]:
                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE,{},{}'.format(
                    self.dataclose_y[0], self.dataclose_x[0]))
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(self.datas[0])
                self.order = self.sell(self.datas[1])

        else:
            # Already in the market ... we might sell
            if self.sell_sig:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('BUY CREATE,{},{}'.format(
                    self.dataclose_y[0], self.dataclose_x[0]))
                # Keep track of the created order to avoid a 2nd order
                self.log('Pos size %s' % self.position.size)
                self.order = self.close(self.datas[1])
                self.order = self.close(self.datas[0])


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=True)  # I don't want the default plot objects
    cerebro.addstrategy(TestStrategy)

    # Create a Data Feed
    start = datetime.datetime(2016, 1, 1)
    end = datetime.datetime(2018, 7, 6)

    # create the data
    usestore = True

    storekwargs = dict(
        host='127.0.0.1', port=7497,
        clientId=None, timeoffset=False,
        reconnect=3, timeout=3.0,
        notifyall=False, _debug=False
    )
    ibstore = bt.stores.IBStore(**storekwargs)
    print("Using IBstore")

    broker = ibstore.getbroker()
    IBDataFactory = ibstore.getdata if usestore else bt.feeds.IBData
    dtfmt = '%Y-%m-%dT%H:%M:%S.%f'
    datakwargs = dict(
        timeframe=bt.TimeFrame.TFrame("Days"), compression=1,
        historical=True, fromdate=start, todate=end,  ## mod todate here
        rtbar=False,
        qcheck=0.5,
        what=None,
        backfill_start=True,
        backfill=False,
        latethrough=False,
        tz=None,
        useRTH=True
    )

    data_1 = IBDataFactory(dataname='AAPL-STK-SMART-USD', **datakwargs)
    data_2 = IBDataFactory(dataname='DPZ-STK-SMART-USD', **datakwargs)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data_1)
    cerebro.adddata(data_2)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
