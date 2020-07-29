from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
# Import the backtrader platform
import backtrader as bt

class MyHLOC(bt.feeds.GenericCSVData):
  # datetime, O, H, L, C, V, OI, WAP
  params = (
      # ('fromdate', datetime.datetime(2020, 4, 1)),
      # ('todate', datetime.datetime(2020, 4, 2)),
      ('nullvalue', 0.0),
      # ('dtformat', ('%Y-%m-%d')),
      # ('tmformat', ('%H.%M.%S')),
      ('timeframe', bt.TimeFrame.Minutes),
      ('datetime', 0),
      ('open', 1),
      ('high', 2),
      ('low', 3),
      ('close', 4),
      ('volume', 5),
      ('openinterest', 6)
)


# Create a Stratey
class TestStrategy(bt.Strategy):

    params = dict(
        smaperiod=5,
        trade=False,
        stake=1,
        exectype=bt.Order.Market,
        stopafter=0,
        valid=None,
        cancel=0,
        donotsell=False,
        stoptrail=False,
        stoptraillimit=False,
        trailamount=None,
        trailpercent=None,
        limitoffset=None,
        oca=False,
        bracket=False,
    )


    def logdata(self):
        # txt = []
        # txt.append("{}".format(self.data._name))
        # txt.append("{}".format(len(self)))
        # txt.append("{}".format(self.data.datetime.datetime(0)))
        # txt.append("{:.2f}".format(self.data.line))
        # txt.append("{:.2f}".format(self.data.high[0]))
        # txt.append("{:.2f}".format(self.data.low[0]))
        # txt.append("{:.2f}".format(self.data.close[0]))
        # txt.append("{:.2f}".format(self.data.volume[0]))
        # print(", ".join(txt))
        print (self.data.line.to_string())

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # # Write down: no pending order
        # self.order = None

    def __init__(self):
        self.highest = 0
        self.lowest = 0

        print('I am in init')



    def next(self):
        print('I am in next')
        if self.data.datetime.time() < datetime.time(9, 45, 0):
            if self.data.datetime.date() != self.data.datetime.date(-1):
                print("\n")
                self.highest = self.datas[0].high[0]
                self.lowest = self.datas[0].low[0]

            self.highest = max(self.datas[0].high[0], self.highest)
            self.lowest = min(self.datas[0].low[0], self.lowest)

            self.log(f"highest (high) {self.highest:7.2f} ({self.datas[0].high[0]:7.2f}), "
                     f"lowest (low) {self.lowest:7.2f} ({self.datas[0].low[0]:7.2f})")
        pass




if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')
    datapath = '/Users/sponraj/Desktop/History_Data/ES/2020/04_ESU2020_FUT.csv'

    # Create a Data Feed datetime,O,H,L,C,V,OI,WAP
    data0 = MyHLOC(dataname=datapath)
    # cerebro.adddata(data0)
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Minutes, compression=15)

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # store = bt.stores.IBStore(port=7497)
    # stockkwargs = dict(
    #     timeframe=bt.TimeFrame.Minutes,
    #     rtbar=False,  # use RealTime 5 seconds bars
    #     historical=True,  # only historical download
    #     qcheck=0.5,  # timeout in seconds (float) to check for events
    #     fromdate=datetime.datetime(2019, 9, 24),  # get data from..
    #     todate=datetime.datetime(2019, 9, 25),  # get data from..
    #     latethrough=False,  # let late samples through
    #     tradename=None  # use a different asset as order target
    # )
    # data0 = store.getdata(dataname="AAPL-STK-SMART-USD", **stockkwargs)
    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
