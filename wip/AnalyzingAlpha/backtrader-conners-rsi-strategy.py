from datetime import datetime
import backtrader as bt
import pandas as pd
import sqlalchemy
# import setup_psql_environment
# from models import Security, SecurityPrice
from live.MyIB import MyIB
import logging
logging.getLogger('matplotlib').disabled = True
logging.getLogger('matplotlib.font_manager').disabled = True

class Streak(bt.ind.PeriodN):
    '''
    Keeps a counter of the current upwards/downwards/neutral streak
    '''
    lines = ('streak',)
    params = dict(period=2)  # need prev/cur days (2) for comparisons

    curstreak = 0

    def next(self):
        d0, d1 = self.data[0], self.data[-1]

        if d0 > d1:
            self.l.streak[0] = self.curstreak = max(1, self.curstreak + 1)
        elif d0 < d1:
            self.l.streak[0] = self.curstreak = min(-1, self.curstreak - 1)
        else:
            self.l.streak[0] = self.curstreak = 0


class ConnorsRSI(bt.Indicator):
    '''
    Calculates the ConnorsRSI as:
        - (RSI(per_rsi) + RSI(Streak, per_streak) + PctRank(per_rank)) / 3
    '''
    lines = ('crsi',)
    params = dict(prsi=3, pstreak=2, prank=100)

    def __init__(self):
        # Calculate the components
        rsi = bt.ind.RSI(self.data, period=self.p.prsi)
        streak = Streak(self.data)
        rsi_streak = bt.ind.RSI(streak.data, period=self.p.pstreak)
        prank = bt.ind.PercentRank(self.data, period=self.p.prank)

        # Apply the formula
        self.l.crsi = (rsi + rsi_streak + prank) / 3.0


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.myind = ConnorsRSI()

    def logdata(self):
        txt = ["{}".format(self.data._name), "{}".format(len(self)), "{}".format(self.data.datetime.datetime(0)),
               "{:.2f}".format(self.data.high[0]), "{:.2f}".format(self.data.low[0]),
               "{:.2f}".format(self.data.open[0]), "{:.2f}".format(self.data.close[0])]
        print(", ".join(txt))

    def next(self):
        self.logdata()

        if self.myind.crsi[0] <= 10:
            self.buy()
        elif self.myind.crsi[0] >= 90:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.001)

    ib = MyIB()
    start = datetime(2020, 1, 1)
    # end = datetime(2020, 8, 19)
    end =datetime.today()
    data = ib.getdata(start, end)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
