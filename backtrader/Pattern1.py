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
    def logsignaldata(self):
        txt = []
        txt.append("{}".format(self.data._name))
        txt.append("{}".format(len(self)))
        txt.append("{}".format(self.data.datetime.date(-1)))
        txt.append("{:.2f}".format(self.data.open[-1]))
        txt.append("{:.2f}".format(self.data.high[-1]))
        txt.append("{:.2f}".format(self.data.low[-1]))
        txt.append("{:.2f}".format(self.data.close[-1]))
        print(", ".join(txt))

    def next(self):
        # self.logdata()
        date = self.data.datetime.date()

        st_24_1 = round(self.st_24[-1], 2)
        st_24_2 = round(self.st_24[-2],2)

        st_30_1 = round(self.st_30[-1], 2)
        st_30_2 = round(self.st_30[-2], 2)

        self.my_signal_24_P1 = (st_24_2 > 80 > st_24_1 > 40)
        self.my_signal_30_P1 = (st_30_2 > 80 > st_30_1 > 40)

        self.my_signal_24_P2 = (st_24_2 > 40 > st_24_1 > 20)
        self.my_signal_30_P2 = (st_30_2 > 40 > st_30_1 > 20)

        self.my_signal_24_P3 = (st_24_2 > 20 > st_24_1 > 0)
        self.my_signal_30_P3 = (st_30_2 > 20 > st_30_1 > 0)

        self.my_signal_24_P4 = (st_24_2 < 40 < st_24_1)
        self.my_signal_30_P4 = (st_30_2 < 40 < st_30_1)

        self.my_signal_24_P5 = (st_24_2 < 90 < st_24_1 < 98)
        self.my_signal_30_P5 = (st_30_2 < 90 < st_30_1 < 98)

        self.my_signal_24_P6 = (st_24_2 < 98 < st_24_1)
        self.my_signal_30_P6 = (st_30_2 < 98 < st_30_1)

        # PATTERN1
        # if datetime.time(7, 00) < self.data.datetime.time() < datetime.time(15, 00):
        if self.my_signal_24_P1 or self.my_signal_30_P1:

            print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
            self.logsignaldata()
            self.logdata()
            print('P1-CROSSDOWN80 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
            self.slippage = round((self.data.close[-1] * 30) / 12000)
            self.sip = round(self.data.close[-1] + (self.data.close[-1] - self.data.low[-1]), 2)
            self.smart_stop = round(self.data.low[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)

            print('P1 -Setup1 - Buy: T-DAYOPEN {} > SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.sip,self.sip+self.slippage, self.smart_stop))
            print('P1 - Setup2 - Sell: T-DAYOPEN {} < SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.sip,self.sip-self.slippage,
                                                                        self.sip+self.slippage ))
            print('P1 - Setup3 Only If Setup2 Stopped - Buy: SIP: {}, STOP: {}'.format(self.sip+self.slippage,self.smart_stop))
        # PATTERN2
        if self.my_signal_24_P2 or self.my_signal_30_P2:
            print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
            print('P2-CROSSDOWN40 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2,st_24_1, st_30_2,st_30_1))
            self.logdata()
            self.slippage = round((self.data.close[-1] * 40) / 12000)
            self.smart_stop = round((self.data.high[-1] + self.data.low[-1]) / 2,2)
            print('P2 - Setup1 - Sell: T-DAYOPEN {} < LOW {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],self.data.open[0],
                                                                                                     self.data.close[-1]-self.slippage,self.smart_stop))
            sip_sell = round((self.data.close[-1] + self.data.high[-1]) / 2,2)
            sip_buy = round((self.data.close[-1] + self.data.low[-1]) / 2,2)
            p2_slip = round((self.data.close[-1] * 10) / 12000)
            print('P2 - Setup2 - Sell: T-DAYOPEN {} > LOW {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],sip_sell,sip_sell-p2_slip,self.data.high[-1]+self.slippage))
            print("OR - Cancel one after order triggered")
            print('P2 - Setup2 -  Buy: T-DAYOPEN {} > LOW {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1], sip_buy,sip_buy+p2_slip,self.data.low[-1]-self.slippage))
        # PATTERN3
        if self.my_signal_24_P3 or self.my_signal_30_P3:
            print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
            print('P3-CROSSDOWN20 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
            self.logdata()
            self.slippage = round((self.data.close[-1] * 40) / 12000)
            self.smart_stop = round((self.data.high[-1] +self.data.low[-1]) / 2,2)
            print('P3 - Setup1 - Sell: T-DAYOPEN {} < LOW {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],self.data.open[0],self.data.low[-1]-self.slippage, self.smart_stop))
            self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
            print('P3 - Setup2 - Buy:  T-DAYOPEN {} > CLOSE {}: SIP: {}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))
            self.sip = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
            tp = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2),2)
            print('P3 - Setup3 - Buy: CLOSE {} > T-DAYOPEN {} < LOW {} : SIP: {}, STOP: {}, TP: Atclose or {}'.format(self.data.close[-1],self.data.open[0],self.data.low[-1], self.sip,self.sip-self.slippage, tp))

        #PATTERN4
        # if previous PATTERN2 LONG is Success - Long Trade
        if self.my_signal_24_P4 or self.my_signal_30_P4:
            print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
            print('P4-CROSSOVER40 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2,st_24_1, st_30_2,st_30_1))
            self.logdata()
            self.sip = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
            sip_buy = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
            self.slippage = round((self.data.close[-1] * 40) / 12000)
            print('On Pre P2 Long Success P4 - Setup1 - Buy: T-DAYOPEN {} > SIP {}: SIP: {}, STOP: {}'.format(self.data.open[0],self.sip,self.sip,self.data.close[-1]))
            print('On Pre P2 Long Success P4 - Setup1 - Buy: T-DAYOPEN {} < SIP {}: SIP: {}, STOP: {}'.format(self.data.open[0],self.sip,sip_buy,sip_buy-self.slippage))
            self.slippage = round((self.data.close[-1] * 30) / 12000)
            p4_slip = round((self.data.close[-1] * 20) / 12000)
            print('On Pre P2 Long Failure P4 - Setup2 - Sell: T-DAYOPEN {} < CLOSE {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.open[0],self.data.close[-1]-self.slippage,self.data.close[-1]+p4_slip))
            self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
            print('On Pre P2 Long Failure P4 - Setup3 - Sell: T-DAYOPEN {} > HIGH {}: SIP: {}, STOP: {}'.format(self.data.open[0],self.data.high[-1],self.data.close[0],self.smart_stop))

        #PATTERN 5
        if self.my_signal_24_P5 or self.my_signal_30_P5:
            print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
            print('P5-CROSSOVER90 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
            self.logdata()

            self.slippage = round((self.data.close[-1] * 20) / 12000)
            print('P5 - Setup1 - Sell: T-DAYOPEN {} < CLOSE {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.open[0],self.data.open[0]-self.slippage, self.data.high[-1]))

            self.slippage = round((self.data.close[-1] * 45) / 12000)
            self.sip = round(self.data.close[-1] +self.slippage, 2)

            self.slippage = round((self.data.close[-1] * 40) / 12000)
            self.smart_stop =round(self.data.close[-1] - self.slippage,2)
            print('P5 - Setup2 - Buy:  SIP {} > T-DAYOPEN {} > CLOSE {}: SIP: {}, STOP: {}'.format(self.sip,self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))


            self.sip = round(self.data.close[-1] + self.slippage, 2)
            self.slippage = round((self.data.close[-1] * 40) / 12000)
            print('P5 - Setup3 - Sell:  T-DAYOPEN {} > SIP {} : SIP: {}, STOP: {}'.format(self.data.open[0],self.sip,self.data.open[0], self.data.open[0]+self.slippage))

        #PATTERN 6
        if self.my_signal_24_P6 or self.my_signal_30_P6:
            print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
            print('P6-CROSSOVER98 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
            self.logdata()
            self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
            self.sip = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
            self.slippage = round((self.data.close[-1] * 20) / 12000)
            print('P6 - Setup1 - Long: T-DAYOPEN {} > CLOSE {}: SIP: {}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))
            print('P6 - Setup2 - Sell: T-DAYOPEN {} < CLOSE {}: SIP: {}~{}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.open[0],self.data.close[-1]-self.slippage,self.sip))

def run():
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(port=7497, clientId=1001)
    cerebro.broker = store.getbroker()

    stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        # tz='EST5EDT',
        rtbar=False,  # use RealTime 5 seconds bars
        historical=True,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        fromdate=datetime.datetime(2020, 6, 1),  # get data from..
        todate=datetime.datetime.now(datetime.timezone.utc),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target,
        # sessionend = datetime.datetime(20, 00)
    )
    # data0 = store.getdata(dataname="IBUS500-CFD-SMART", **stockkwargs)
    #
    data0 = store.getdata(dataname='ES-202009-GLOBEX',**stockkwargs)
    #
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Days, compression=1)

    # data = bt.feeds.YahooFinanceData(dataname='^NSEI',  fromdate=datetime.datetime(2019, 1, 1),
    #                                  todate=datetime.datetime(2020, 1, 31))
    #
    #         # todate=datetime.datetime.now(datetime.timezone.utc))
    #
    # cerebro.adddata(data)
    cerebro.addstrategy(St)
    cerebro.run()


if __name__ == "__main__":
    run()
