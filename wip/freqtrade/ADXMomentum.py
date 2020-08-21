from datetime import datetime
import backtrader as bt
from live.MyIB import MyIB
import logging
import models
import setup_psql_environment
logging.getLogger('matplotlib').disabled = True
logging.getLogger('matplotlib.font_manager').disabled = True

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


class ADXMomentum(bt.Indicator):
    lines = ('adx', 'plus_di', 'minus_di', 'sar', 'mom')

    def __init__(self):
        self.lines.adx = bt.talib.ADX(self.datas[0].high, self.datas[0].low, self.datas[0].close, timeperiod=14)
        self.lines.plus_di = bt.talib.PLUS_DI(self.datas[0].high, self.datas[0].low, self.datas[0].close, timeperiod=25)
        self.lines.minus_di = bt.talib.MINUS_DI(self.datas[0].high, self.datas[0].low, self.datas[0].close,
                                                timeperiod=25)
        self.lines.sar = bt.talib.SAR(self.datas[0].high, self.datas[0].low)
        self.lines.mom = bt.talib.MOM(self.datas[0], timeperiod=14)


class MyStrategy(bt.Strategy):

    def __init__(self):
        self.myind = ADXMomentum()

    def logdata(self):
        txt = ["{}".format(self.data._name), "{}".format(len(self)), "{}".format(self.data.datetime.datetime(0)),
               "{:.2f}".format(self.data.high[0]), "{:.2f}".format(self.data.low[0]),
               "{:.2f}".format(self.data.open[0]), "{:.2f}".format(self.data.close[0])]
        print(", ".join(txt))

    def next(self):
        self.logdata()
        if self.myind.adx[0] > 25 and self.myind.mom[0] < 0 and self.myind.minus_di[0] > 25 and self.myind.plus_di[0] < \
                self.myind.minus_di[0]:
            self.buy()
        elif self.myind.adx[0] > 25 and self.myind.mom[0] > 0 and 25 < self.myind.minus_di[0] < self.myind.plus_di[
            0]:
             self.sell()

    # def next(self):
    #     if not self.position:
    #         if self.myind.adx[0] > 25 and self.myind.mom[0] < 0 and self.myind.minus_di[0] > 25 and self.myind.plus_di[
    #             0] < self.myind.minus_di[0]:
    #             self.buy()
    #     elif self.position:
    #         if self.myind.adx[0] > 25 and self.myind.mom[0] > 0 and 25 < self.myind.minus_di[0] < self.myind.plus_di[0]:
    #             self.sell()




if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.001)

    ib = MyIB(session=True)

    start = datetime(2020, 1, 1)
    end = datetime(2020, 8, 31)

    data=ib.getdata(start,end)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=60)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
