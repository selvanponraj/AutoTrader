import datetime
import os.path
import sys
import backtrader as bt
import matplotlib.pyplot as pl

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
class SmartPattern1(bt.Strategy):
    def __init__(self):
        self.dataopen = self.data.open(-1)
        self.datahigh = self.data.high(-1)
        self.datalow = self.data.low(-1)
        self.dataclose = self.data.close(-1)

        self.st1_30 = bt.indicators.StochasticFast(self.datas[-1], period=30, period_dfast=1)
        self.st2_24 = bt.indicators.StochasticFast(self.datas[-1], period=24, period_dfast=1)



        self.order = None  # Property to keep track of pending orders.  There are no orders when the strategy is initialized.
        self.buyprice = None
        self.buycomm = None

    def log(self, txt, dt=None):
        # Logging function for the strategy.  'txt' is the statement and 'dt' can be used to specify a specific datetime
        dt = dt or self.datas[0].datetime.datetime(0)
        print('{0},{1}'.format(dt.isoformat(), txt))

    def notify_order(self, order):
        # 1. If order is submitted/accepted, do nothing
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {0:8.2f}, Size: {1:8.2f} Cost: {2:8.2f}, Comm: {3:8.2f}'.format(
                    order.executed.price,
                    order.executed.size,
                    order.executed.value,
                    order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, {0:8.2f}, Size: {1:8.2f} Cost: {2:8.2f}, Comm{3:8.2f}'.format(
                    order.executed.price,
                    order.executed.size,
                    order.executed.value,
                    order.executed.comm))

            self.bar_executed = len(self)  # when was trade executed
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))

    def next(self):

        if self.order:  # check if order is pending, if so, then break out
            return
        self.my_signal_24 = (80 > self.st2_24[0] > 40) or (80 > self.st2_24[0] > 40)
        self.my_signal_30 = (80 > self.st1_30[0] > 40) or (80 > self.st1_30[0] > 40)

        if datetime.time(9, 29) < self.data.datetime.time() < datetime.time(15, 29):
            if not self.position:  # not in the market
                if (self.my_signal_30 or self.my_signal_24) and self.data.open[0] > self.sip:
                    o1 = self.buy(size=1,
                                  exectype=bt.Order.Market,
                                  price=self.entry_price,
                                  valid=bt.Order.DAY,
                                  transmit=True)

                    print('{}: Oref {} / Buy at {}'.format(
                        self.datetime.datetime(), o1.ref, self.entry_price))

                    o2 = self.sell(size=1,
                                   exectype=bt.Order.Stop,
                                   price=self.smart_stop,
                                   valid=bt.Order.DAY,
                                   parent=o1)

                    print('{}: Oref {} / Sell Stop at {}'.format(
                        self.datetime.datetime(), o2.ref, self.smart_stop))

        if  self.position.size != 0 and self.data.datetime.time() > datetime.time(15, 31):
            print("EOD Closing Position")
            self.close(exectype=bt.Order.Market, size=1)
            print("Position : " , self.position)


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
    cerebro.addstrategy(SmartPattern1)

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
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.001)
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
