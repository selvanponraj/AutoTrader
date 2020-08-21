from datetime import datetime
import backtrader as bt
from live.MyIB import MyIB
import logging
logging.getLogger('matplotlib').disabled = True
logging.getLogger('matplotlib.font_manager').disabled = True

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=20)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(1337.0)
    cerebro.broker.setcommission(commission=0.001)

    ib = MyIB()
    start = datetime(2020, 1, 1)
    # end = datetime(2020, 8, 19)
    end = datetime.today()
    data = ib.getdata(start, end)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
