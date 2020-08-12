import backtrader as bt
from datetime import datetime

from backtrader.indicators.supertrend import SuperTrend


class MyStrategy(bt.Strategy):
    params = (('period', 10), ('multiplier', 3))

    def __init__(self):
        self.myind = SuperTrend(period = self.p.period, multiplier = self.p.multiplier)

    def next(self):
        if self.data[0] > self.myind.l.super_trend[0]:
            self.buy()
        elif self.data[0] < self.myind.l.super_trend[0]:
            self.sell()

def run():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(1337.0)
    cerebro.broker.setcommission(commission=0.001)

    data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                     fromdate=datetime(2020, 1, 1),
                                     todate=datetime(2020, 8, 31))
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()


if __name__ == "__main__":
    run()