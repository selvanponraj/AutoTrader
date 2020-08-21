# https://community.backtrader.com/topic/2341/crossover-indicator-doesn-t-plot-as-expected/10
import datetime

import backtrader as bt


class ADX(bt.Indicator):
    lines = ('adx', 'fast', 'slow')
    params = (
        ('pfast', 10),
        ('pslow', 30)
    )

    def __init__(self):
        self.lines.adx = bt.talib.ADX(
            self.data.high, self.data.low, self.data.close)
        self.lines.fast = bt.ind.SMA(self.lines.adx, period=self.p.pfast)
        self.lines.slow = bt.ind.SMA(self.lines.adx, period=self.p.pslow)


class SMACross(bt.Strategy):

    params = (
        ('pfast', 10),
        ('pslow', 30),
    )

    def __init__(self):
        self.sma_fast = bt.talib.SMA(
            self.datas[0].close, timeperiod=self.p.pfast)
        self.sma_slow = bt.talib.SMA(
            self.datas[0].close, timeperiod=self.p.pslow)
        self.sma_crossover = bt.ind.CrossOver(self.sma_fast, self.sma_slow)

        self.adx = ADX(self.datas[0])
        self.adx_crossover = bt.ind.CrossOver(
            self.adx.fast, self.adx.slow, subplot=True)

    def next(self):
        if not self.position:
            if self.sma_crossover > 0:
                self.buy()
        elif self.position:
            if self.sma_crossover < 0:
                self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SMACross)
    datapath = '/Users/sponraj/auto_trade/local/backtrader/datas/orcl-1995-2014.txt'

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(2000, 12, 31),
        # Do not pass values after this date
        reverse=False)

    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot()
