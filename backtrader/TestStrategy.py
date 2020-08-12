from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

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
    # params = (
    #     ('maperiod', 30),  # Tuple of tuples containing any variable settings required by the strategy.
    #     ('maperiod_1', 24)
    #
    # )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose_0 = self.datas[0].close
        self.dataopen_0 = self.datas[0].open

        self.dataopen = self.datas[-1].open
        self.datahigh = self.datas[-1].high
        self.datalow = self.datas[-1].low
        self.dataclose = self.datas[-1].close

        bt.indicators.RelativeStrengthIndex
        bt.indicators
        # self.st2_24 = bt.indicators.StochasticFast(self.datas[-1], period=24, period_dfast=1)
        # self.st1_30 = bt.indicators.StochasticFast(self.datas[-1], period=30, period_dfast=1)

        #
        # # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #
        # # # Add a MovingAverageSimple indicator
        # # self.sma = bt.indicators.SimpleMovingAverage(
        # #     self.datas[0], period=self.params.maperiod)
        #
        # # # Indicators for the plotting show
        # # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        # #                                     subplot=True)
        # # bt.indicators.StochasticSlow(self.datas[0])
        #

        #
        # # bt.indicators.MACDHisto(self.datas[0])
        # # rsi = bt.indicators.RSI(self.datas[0])
        # # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # # bt.indicators.ATR(self.datas[0], plot=False)

    # def notify_order(self, order):
    #     date = self.data.datetime.datetime().date()
    #
    #     if order.status == order.Accepted:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('Order Accepted')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #
    #     if order.status == order.Completed:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('Order Completed')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #         print('Created: {} Price: {} Size: {}'.format(bt.num2date(order.created.dt), order.created.price,
    #                                                       order.created.size))
    #         print('-' * 80)
    #
    #     if order.status == order.Canceled:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('Order Canceled')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #
    #     if order.status == order.Rejected:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('WARNING! Order Rejected')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #         print('-' * 80)
    #
    # def notify_trade(self, trade):
    #     date = self.data.datetime.datetime()
    #     if trade.isclosed:
    #         print('-' * 32, ' NOTIFY TRADE ', '-' * 32)
    #         print('{}, Close Price: {}, Profit, Gross {}, Net {}'.format(
    #             date,
    #             trade.price,
    #             round(trade.pnl, 2),
    #             round(trade.pnlcomm, 2)))
    #         print('-' * 80)

    def logdata(self):
        txt = []
        txt.append("{}".format(self.data._name))
        txt.append("{}".format(len(self)))
        txt.append("{}".format(self.data.datetime.datetime(0)))
        txt.append("{:.2f}".format(self.data.open[0]))
        txt.append("{:.2f}".format(self.data.high[0]))
        txt.append("{:.2f}".format(self.data.low[0]))
        txt.append("{:.2f}".format(self.data.close[0]))
        print(", ".join(txt))

    def next(self):
        self.logdata()
        # # Simply log the closing price of the series from the reference
        # self.log('Open, %.2f Close, %.2f' % (self.dataopen_0[0],self.dataclose_0[0]))

        # date = self.data.datetime.datetime()
        # open = self.data.open[0]
        # close = self.data.close[0]
        # print('{}: Open: ${}, Close: ${}, Position Size: {}'.format(date, open, close, self.position.size))
        #
        # self.my_signal_24 = (80 > self.st2_24[0] > 40) or (80 > self.st2_24[0] > 40)
        # self.my_signal_30 = (80 > self.st1_30[0] > 40) or (80 > self.st1_30[0] > 40)
        #
        # self.sip = self.dataclose[0] + (self.dataclose[0] - self.datalow[0])
        #
        # # if self.data.datetime.date() != self.data.datetime.date(-1):
        # #     print("EOD Closing Position")
        # #     if self.position.size > 0:
        # #         self.sell(size=1, price=self.dataclose[0])
        # #     elif self.position.size < 0:
        # #         self.buy(size=1, price=self.dataclose[0])
        #
        # # Check if we are in the market
        # if datetime.time(9, 29) < self.data.datetime.time() < datetime.time(15, 00):
        #     if not self.position:
        #         # Not yet ... we MIGHT BUY if ...
        #         if (self.my_signal_30 or self.my_signal_24):
        #
        #
        #             if self.data.open[0] > self.sip:
        #                 self.entry_price = self.sip + 30
        #                 self.smart_stop = self.datalow[0] - ((self.datahigh[0] - self.datalow[0]) / 2)
        #                 # BUY, BUY, BUY!!! (with all possible default parameters)
        #                 self.log('BUY CREATE, %.2f, st_30: %.2f, st_24 %.2f' % (self.entry_price,self.st1_30[0], self.st2_24[0]))
        #                 # self.order = self.buy(price=self.entry_price)
        #                 self.order = self.buy_bracket(
        #                     exectype=bt.Order.Limit,
        #                     price=self.entry_price,
        #                     stopprice=self.smart_stop,
        #                     limitexec=None,
        #                     valid=bt.Order.T_Close
        #                     )
        #             elif self.data.open[0] < self.sip:
        #                 self.entry_price = self.sip - 30
        #                 self.smart_stop = self.sip + 30
        #                 self.log('SELL CREATE, %.2f, st_30: %.2f, st_24 %.2f' % (
        #                 self.entry_price, self.st1_30[0], self.st2_24[0]))
        #                 # self.order = self.buy(price=self.entry_price)
        #                 self.order = self.sell_bracket(
        #                     price=self.entry_price,
        #                     stopprice=self.smart_stop,
        #                     limitexec=None,
        #                     valid=bt.Order.T_Close
        #                 )
        #
        # if self.data.datetime.time() > datetime.time(15, 00):
        #
        #     if self.position.size > 0:
        #         print("EOD Closing BUY Position")
        #         self.sell(size=1, price=self.dataclose[0])
        #     elif self.position.size < 0:
        #         print("EOD Closing SELL Position")
        #         self.buy(size=1, price=self.dataclose[0])


    def stop(self):
        print("End of the day")

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)
    # strats = cerebro.optstrategy(
    #     TestStrategy,
    #     maperiod=range(24, 30),
    #     maperiod_1=range(10, 24))

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere

    homepath = os.getenv('HOME')

    # # data = bt.feeds.YahooFinanceCSVData(
    # #     dataname=datapath,
    # #     fromdate=datetime.datetime(2019, 1, 1),
    # #     todate=datetime.datetime(2019, 12, 31),
    # #     reverse=False)
    # data = bt.feeds.YahooFinanceData(dataname='^NSEI',  fromdate=datetime.datetime(2018, 1, 1),
    #         todate=datetime.datetime(2019, 12, 31))

    datapath = os.path.join(homepath,'Desktop/History_Data/ES/2020/IBUS30_CFD.csv')
    data = MyHLOC(dataname=datapath)


    # # Add the Data Feed to Cerebro
    # cerebro.adddata(data)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)

    # # Set our desired cash start
    # cerebro.broker.setcash(100000.0)
    #
    # # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    #
    # # Set the commission
    # cerebro.broker.setcommission(commission=0.001)
    # # # 0.1% ... divide by 100 to remove the %
    # # cerebro.broker.setcommission(commission=0.001)
    #
    # # Print out the starting conditions
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # # Print out the final result
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    #
    # # Plot the result
    # cerebro.plot()