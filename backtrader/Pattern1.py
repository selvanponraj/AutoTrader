#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-e

from __future__ import absolute_import, division, print_function, unicode_literals
import backtrader as bt
import datetime


class St(bt.Strategy):
    IBUS_START=(13,30)
    IBUS_START = (8,1)
    IBGBP_START = (7, 00)
    IBGBP_START = (15, 1)

    def __init__(self):
        self.st_24 = bt.indicators.StochasticFast(self.data, period=24, period_dfast=1)
        self.st_30 = bt.indicators.StochasticFast(self.data, period=30, period_dfast=1)

        self.sip = 0
        self.smart_stop = 0
        self.slippage = 30

    def logdata(self):
        txt = []
        txt.append("{}".format(self.data._name))
        txt.append("{}".format(len(self)))
        txt.append("{}".format(self.data.datetime.date(0)))
        txt.append("{:.2f}".format(self.data.open[0]))
        txt.append("{:.2f}".format(self.data.high[0]))
        txt.append("{:.2f}".format(self.data.low[0]))
        txt.append("{:.2f}".format(self.data.close[0]))
        print(", ".join(txt))

    def next(self):
        # self.logdata()
        date = self.data.datetime.date()

        self.my_signal_24_P1 = (80 > self.st_24[0] > 40)
        self.my_signal_30_P1 = (80 > self.st_30[0] > 40)

        self.my_signal_24_P2 = (40 > self.st_24[0] > 20)
        self.my_signal_30_P2 = (40 > self.st_30[0] > 20)

        self.my_signal_24_P3 = (20 > self.st_24[0] > 0)
        self.my_signal_30_P3 = (20 > self.st_30[0] > 0)


        # if datetime.time(7, 00) < self.data.datetime.time() < datetime.time(15, 00):
        if self.my_signal_24_P1 or self.my_signal_30_P1:
            print('TRADING PLAN P1 FOR {}: ST24: {}, ST30: {}'.format(date, self.st_24[-1], self.st_30[-1]))
            self.logdata()

            self.slippage = round((self.data.close[-1] * 30) / 12000)
            self.sip = round(self.data.close[-1] + (self.data.close[-1] - self.data.low[-1]), 2)
            self.smart_stop = round(self.data.low[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)

            print('P1 -Setup1 - Buy: T-DAYOPEN {} > SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.sip,self.sip+self.slippage, self.smart_stop))
            print('P1 - Setup2 - Sell: T-DAYOPEN {} < SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.sip,self.sip-self.slippage,
                                                                        self.sip+self.slippage ))
            print('P1 - Setup3 Only If Setup2 Stopped - Buy: SIP: {}, STOP: {}'.format(self.sip+self.slippage,self.smart_stop))

        if self.my_signal_24_P2 or self.my_signal_30_P2:
            print('TRADING PLAN P2 FOR {}: ST24: {}, ST30: {}'.format(date, self.st_24[0], self.st_30[0]))
            self.logdata()

            self.slippage = round((self.data.close[-1] * 40) / 12000)

            self.smart_stop = round((self.data.high[-1] + self.data.low[-1]) / 2,2)
            print('P2 - Setup1 - Sell: T-DAYOPEN {} < {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],self.data.open[0],
                                                                                                     self.data.close[-1]-self.slippage,self.smart_stop))
            sip_sell = round((self.data.close[-1] + self.data.high[-1]) / 2,2)
            sip_buy = round((self.data.close[-1] + self.data.low[-1]) / 2,2)
            p2_slip = round((self.data.close[-1] * 10) / 12000)
            print('P2 - Setup2 - Sell: T-DAYOPEN {} > {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],sip_sell,sip_sell-p2_slip,self.data.high[-1]+self.slippage))
            print("OR - Cancel one after order triggered")
            print('P2 - Setup2 -  Buy: T-DAYOPEN {} > {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1], sip_buy,sip_buy+p2_slip,self.data.low[-1]-self.slippage))

        if self.my_signal_24_P3 or self.my_signal_30_P3:
            print('TRADING PLAN P3 FOR {}: ST24: {}, ST30: {}'.format(date, self.st_24[0], self.st_30[0]))
            self.logdata()
            self.slippage = round((self.data.close[-1] * 40) / 12000)
            self.smart_stop = round((self.data.high[-1] +self.data.low[-1]) / 2,2)
            print('P3 - Setup1 - Sell: T-DAYOPEN {} < {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],self.data.open[0],self.data.low[-1]-self.slippage, self.smart_stop))
            self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
            print('P3 - Setup2 - Buy:  T-DAYOPEN {} > {}: SIP: {}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))
            self.sip = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
            tp = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2),2)
            print('P3 - Setup3 - Buy: {} > T-DAYOPEN {} < {} : SIP: {}, STOP: {}, TP: Atclose or {}'.format(self.data.close[-1],self.data.open[0],self.data.low[-1], self.sip,self.sip-self.slippage, tp))

def run():
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(port=7497, clientId=1001)
    cerebro.broker = store.getbroker()

    # stockkwargs = dict(
    #     timeframe=bt.TimeFrame.Minutes,
    #     # tz='EST5EDT',
    #     rtbar=False,  # use RealTime 5 seconds bars
    #     historical=True,  # only historical download
    #     qcheck=0.5,  # timeout in seconds (float) to check for events
    #     fromdate=datetime.datetime(2020, 4, 28),  # get data from..
    #     todate=datetime.datetime(2020, 7, 30),  # get data from..
    #     latethrough=False,  # let late samples through
    #     tradename=None,  # use a different asset as order target,
    #     # sessionend = datetime.datetime(20, 00)
    # )
    # data0 = store.getdata(dataname="IBUS30-CFD-SMART", **stockkwargs)
    # cerebro.resampledata(data0, timeframe=bt.TimeFrame.Days, compression=1)

    data = bt.feeds.YahooFinanceData(dataname='^NSEI',  fromdate=datetime.datetime(2019, 5, 1),
            todate=datetime.datetime.now(datetime.timezone.utc))

    cerebro.adddata(data)
    cerebro.addstrategy(St)
    cerebro.run()


if __name__ == "__main__":
    run()
