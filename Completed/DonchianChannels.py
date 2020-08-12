from datetime import datetime
import backtrader as bt
import datetime
import logging
logging.getLogger('matplotlib').disabled = True
logging.getLogger('matplotlib.font_manager').disabled = True

class DonchianChannels(bt.Indicator):
    '''
    Params Note:
      - `lookback` (default: -1)
        If `-1`, the bars to consider will start 1 bar in the past and the
        current high/low may break through the channel.
        If `0`, the current prices will be considered for the Donchian
        Channel. This means that the price will **NEVER** break through the
        upper/lower channel bands.
    '''

    alias = ('DCH', 'DonchianChannel',)

    lines = ('dcm', 'dch', 'dcl',)  # dc middle, dc high, dc low
    params = dict(
        period=20,
        lookback=-1,  # consider current bar or not
    )

    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(
        dcm=dict(ls='--'),  # dashed line
        dch=dict(_samecolor=True),  # use same color as prev line (dcm)
        dcl=dict(_samecolor=True),  # use same color as prev line (dch)
    )

    def __init__(self):
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        self.l.dch = bt.ind.Highest(hi, period=self.p.period)
        self.l.dcl = bt.ind.Lowest(lo, period=self.p.period)
        self.l.dcm = (self.l.dch + self.l.dcl) / 2.0  # avg of the above


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.myind = DonchianChannels()
        pass

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
        if self.data[0] > self.myind.dch[0]:
            self.buy()
        elif self.data[0] < self.myind.dcl[0]:
            self.sell()

class PropSizer(bt.Sizer):
    """A position sizer that will buy as many stocks as necessary for a certain proportion of the portfolio
       to be committed to the position, while allowing stocks to be bought in batches (say, 100)"""
    params = {"prop": 0.1, "batch": 100}

    def _getsizing(self, comminfo, cash, data, isbuy):
        """Returns the proper sizing"""

        if isbuy:  # Buying
            target = self.broker.getvalue() * self.params.prop  # Ideal total value of the position
            price = data.close[0]
            shares_ideal = target / price  # How many shares are needed to get target
            batches = int(shares_ideal / self.params.batch)  # How many batches is this trade?
            shares = batches * self.params.batch  # The actual number of shares bought

            if shares * price > cash:
                return 0  # Not enough money for this trade
            else:
                return shares

        else:  # Selling
            return self.broker.getposition(data).size  # Clear the position

if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats=True)  # I don't want the default plot objects
    cerebro.addstrategy(MyStrategy)

    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2017, 12, 31)

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

    data0 = IBDataFactory(dataname='AAPL-STK-SMART-USD', **datakwargs)
    data0.plotinfo.plotmaster = data0

    cerebro.adddata(data0)  # Give the data to cerebro

    # data = bt.feeds.YahooFinanceData(dataname='AAPL',
    #                                  fromdate=datetime.datetime(2017, 1, 1),
    #                                  todate=datetime.datetime(2017, 12, 31))
    # cerebro.adddata(data)

    print("Data added to cerebro")


    class AcctValue(bt.Observer):
        alias = ('Value',)
        lines = ('value',)

        plotinfo = {"plot": True, "subplot": True}

        def next(self):
            self.lines.value[0] = self._owner.broker.getvalue()  # Get today's account value (cash + stocks)


    cerebro.addobserver(AcctValue)
    # cerebro.addsizer(PropSizer)

    cerebro.broker.set_cash(1337)  # Set our starting cash to $1,000,000
    cerebro.broker.setcommission(0.001)

    cerebro.broker.getvalue()

    cerebro.run()
    cerebro.plot()