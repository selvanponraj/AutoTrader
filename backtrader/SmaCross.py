from datetime import datetime
import backtrader as bt
from user_data.strategies import *
from user_data.strategies.berlinguyinca import *
from pandas import DataFrame
import talib.abstract as ta
from user_data.strategies.berlinguyinca import *
import numpy as np  # noqa

def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe['maShort'] = ta.SMA(dataframe, timeperiod=25)
    dataframe['maMedium'] = ta.SMA(dataframe, timeperiod=60)
    return dataframe

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        params = (('n1', 10),('n2', 30))
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        # sma1,sma2 = bt.talib.SMA(self.data, timeperiod=10),  bt.talib.SMA(self.data, timeperiod=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data0 = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2011, 1, 1),
                                  todate=datetime(2012, 12, 31))
cerebro.adddata(data0)

cerebro.run()

cerebro.plot()