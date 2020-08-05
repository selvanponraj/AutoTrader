#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-e

from __future__ import absolute_import, division, print_function, unicode_literals
import backtrader as bt
import datetime


class St(bt.Strategy):

    def __init__(self):
        self.st_24 = bt.indicators.StochasticFast(self.data, period=24, period_dfast=1)
        self.st_30 = bt.indicators.StochasticFast(self.data, period=30, period_dfast=1)

        self.sip = 0
        self.smart_stop = 0
        self.slippage = 30

        self.order = None

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

    def logsignaldata(self):
        txt = []
        txt.append("{}".format(self.data._name))
        txt.append("{}".format(len(self)-1))
        txt.append("{}".format(self.data.datetime.datetime(-1)))
        txt.append("{:.2f}".format(self.data.open[-1]))
        txt.append("{:.2f}".format(self.data.high[-1]))
        txt.append("{:.2f}".format(self.data.low[-1]))
        txt.append("{:.2f}".format(self.data.close[-1]))
        print(", ".join(txt))

    # def notify_order(self, order):
    #     date = self.data.datetime.datetime().date()
    #
    #     if order.status == order.Accepted:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('Order Accepted')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #
    #     if order.status == order.Completed:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('Order Completed')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #         print('Created: {} Price: {} Size: {}'.format(bt.num2date(order.created.dt), order.created.price,
    #                                                       order.created.size))
    #         print('-' * 80)
    #
    #     if order.status == order.Canceled:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('Order Canceled')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #
    #     if order.status == order.Rejected:
    #         print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
    #         print('WARNING! Order Rejected')
    #         print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
    #             date,
    #             order.status,
    #             order.ref,
    #             order.size,
    #             'NA' if not order.price else round(order.price, 5)
    #         ))
    #         print('-' * 80)
    #
    # def notify_trade(self, trade):
    #     date = self.data.datetime.datetime()
    #     if trade.isclosed:
    #         print('-' * 32, ' NOTIFY TRADE ', '-' * 32)
    #         print('{}, Close Price: {}, Profit, Gross {}, Net {}'.format(
    #             date,
    #             trade.price,
    #             round(trade.pnl, 2),
    #             round(trade.pnlcomm, 2)))
    #         print('-' * 80)


    def next(self):
        self.logdata()
        # date = self.data.datetime.date()
        # st_24_1 = round(self.st_24[-1], 2)
        # st_24_2 = round(self.st_24[-2],2)
        #
        # st_30_1 = round(self.st_30[-1], 2)
        # st_30_2 = round(self.st_30[-2], 2)
        #
        # self.my_signal_24_P1 = (st_24_2 > 80 > st_24_1 > 40)
        # self.my_signal_30_P1 = (st_30_2 > 80 > st_30_1 > 40)
        #
        # self.my_signal_24_P2 = (st_24_2 > 40 > st_24_1 > 20)
        # self.my_signal_30_P2 = (st_30_2 > 40 > st_30_1 > 20)
        #
        # self.my_signal_24_P3 = (st_24_2 > 20 > st_24_1 > 0)
        # self.my_signal_30_P3 = (st_30_2 > 20 > st_30_1 > 0)
        #
        # self.my_signal_24_P4 = (st_24_2 < 40 < st_24_1)
        # self.my_signal_30_P4 = (st_30_2 < 40 < st_30_1)
        #
        # self.my_signal_24_P5 = (st_24_2 < 90 < st_24_1 < 98)
        # self.my_signal_30_P5 = (st_30_2 < 90 < st_30_1 < 98)
        #
        # self.my_signal_24_P6 = (st_24_2 < 98 < st_24_1)
        # self.my_signal_30_P6 = (st_30_2 < 98 < st_30_1)
        #
        # # PATTERN1
        # if self.my_signal_24_P1 or self.my_signal_30_P1:
        #     print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
        #     self.logsignaldata()
        #     self.logdata()
        #     print('P1-CROSSDOWN80 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
        #
        #     self.sip = round(self.data.close[-1] + (self.data.close[-1] - self.data.low[-1]), 2)
        #     self.smart_stop = round(self.data.low[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
        #
        #     self.slippage = round((self.sip * 30) / 12000)
        #
        #     print('P1 -Setup1 - Buy: T-DAYOPEN {} > SIP {}: BUY:{}~{}, STOP: {}'.format(self.data.open[0],self.sip,self.sip,self.sip+self.slippage, self.smart_stop))
        #     # if self.data.open[0] > self.sip:
        #     #     self.order = self.buy_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.sip,
        #     #         stopprice=self.smart_stop,
        #     #         limitexec=None,
        #     #         valid=bt.Order.DAY,
        #     #         transmit=False,
        #     #     )
        #
        #     print('P1 - Setup2 - Sell: T-DAYOPEN {} < SIP {}: SELL {}~{}, STOP: {}'.format(self.data.open[0],self.sip,self.sip,self.sip-self.slippage,
        #                                                                 self.sip+self.slippage ))
        #     # if self.data.open[0] < self.sip:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.sip,
        #     #         stopprice=self.sip+self.slippage,
        #     #         limitexec=None,
        #     #         valid=bt.Order.DAY
        #     #     )
        #     print('*** Manual P1 - Setup3 Buy (Only If Setup2 Stopped) : BUY: {}, STOP: {}'.format(self.sip+self.slippage,self.smart_stop))
        # # PATTERN2
        # if self.my_signal_24_P2 or self.my_signal_30_P2:
        #     print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
        #     self.logsignaldata()
        #     self.logdata()
        #     print('P2-CROSSDOWN40 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2,st_24_1, st_30_2,st_30_1))
        #     self.slippage = round((self.data.close[-1] * 40) / 12000)
        #     self.smart_stop = round((self.data.high[-1] + self.data.low[-1]) / 2,2)
        #     print('P2 - Setup1 - Sell: T-DAYOPEN {} < LOW {}: SELL: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],self.data.open[0],
        #                                                                                              self.data.close[-1]-self.slippage,self.smart_stop))
        #     # if self.data.open[0] < self.data.low[-1]:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.open[0],
        #     #         stopprice=self.smart_stop,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        #     sip_sell = round((self.data.close[-1] + self.data.high[-1]) / 2,2)
        #     sip_buy = round((self.data.close[-1] + self.data.low[-1]) / 2,2)
        #
        #     self.slippage = round((self.data.high[-1] * 40) / 12000)
        #     p2_slip = round((self.data.close[-1] * 10) / 12000)
        #     print('P2 - Setup2 - Sell: T-DAYOPEN {} > LOW {}: SELL: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],sip_sell,sip_sell-p2_slip,self.data.high[-1]+self.slippage))
        #     # if self.data.open[0] > self.data.low[-1]:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=sip_sell,
        #     #         stopprice=self.data.high[-1]+self.slippage,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #     print("OR - Cancel one after order triggered")
        #     self.slippage = round((self.data.low[-1] * 40) / 12000)
        #     print('P2 - Setup2 -  Buy: T-DAYOPEN {} > LOW {}: BUY: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1], sip_buy,sip_buy+p2_slip,self.data.low[-1]-self.slippage))
        #     # if self.data.open[0] > self.data.low[-1]:
        #     #     self.order = self.buy_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=sip_buy,
        #     #         stopprice=self.data.low[-1]-self.slippage,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        # # PATTERN3
        # if self.my_signal_24_P3 or self.my_signal_30_P3:
        #     print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
        #     self.logsignaldata()
        #     self.logdata()
        #     print('P3-CROSSDOWN20 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
        #     self.slippage = round((self.data.low[-1] * 30) / 12000)
        #     self.smart_stop = round((self.data.high[-1] +self.data.low[-1]) / 2,2)
        #     print('P3 - Setup1 - Sell: T-DAYOPEN {} < LOW {}: SELL: {}~{}, STOP: {}'.format(self.data.open[0],self.data.low[-1],self.data.open[0],self.data.low[-1]-self.slippage, self.smart_stop))
        #
        #     # if self.data.open[0] < self.data.low[-1]:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.open[0],
        #     #         stopprice=self.smart_stop,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        #     self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
        #     print('P3 - Setup2 - Buy:  T-DAYOPEN {} > CLOSE {}: BUY: {}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))
        #
        #     # if self.data.open[0] > self.data.close[-1]:
        #     #     self.order = self.buy_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.close[-1],
        #     #         stopprice=self.smart_stop,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        #     self.sip = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2),2)
        #     self.slippage = round((self.sip * 30) / 12000)
        #     tp = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2),2)
        #     print('P3 - Setup3 - Buy: CLOSE {} > T-DAYOPEN {} < LOW {} : BUY: {}, STOP: {}, TP: Atclose or {}'.format(self.data.close[-1],self.data.open[0],self.data.low[-1], self.sip,self.sip-self.slippage, tp))
        #
        #     # if self.data.close[-1] > self.data.open[0] < self.data.low[-1]:
        #     #     self.order = self.buy_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.sip,
        #     #         stopprice=self.sip-self.slippage,
        #     #         limitprice=tp,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        # #PATTERN 4
        # if self.my_signal_24_P4 or self.my_signal_30_P4:
        #     print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
        #     print('P4-CROSSOVER40 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2,st_24_1, st_30_2,st_30_1))
        #     self.logsignaldata()
        #     self.logdata()
        #
        #     self.sip = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
        #     sip_buy = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
        #
        #     self.slippage = round((self.sip * 40) / 12000)
        #     print("Pre Conditions : Trade - On Pre P2 Long Success")
        #     print('P4 - Setup1 - Buy: T-DAYOPEN {} > SIP {}: BUY: {}, STOP: {}'.format(self.data.open[0],self.sip,self.sip,self.data.close[-1]))
        #     print('P4 - Setup1 - Buy: T-DAYOPEN {} < SIP {}: BUY: {}, STOP: {}'.format(self.data.open[0],self.sip,sip_buy,sip_buy-self.slippage))
        #
        #     self.slippage = round((self.data.open[0] * 30) / 12000)
        #     p4_slip = round((self.data.close[-1] * 20) / 12000)
        #     p4_avoid = round((self.data.close[-1] * 80) / 12000)
        #     p4_avoid_1 = round((self.data.close[-1] * 100) / 12000)
        #
        #     print("Pre Conditions : Trade - On Pre P2 Long Failure")
        #     print("Pre Conditions : Avoid - T-DAYOPEN {}~{} points Gap Down ".format(p4_avoid,p4_avoid_1))
        #     print('P4 - Setup2 - Sell: T-DAYOPEN {} < CLOSE {}: SELL: {}~{}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.open[0],self.data.close[-1]-self.slippage,self.data.close[-1]+p4_slip))
        #
        #     self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
        #     print('P4 - Setup3 - Sell: T-DAYOPEN {} > HIGH {}: SELL: {}, STOP: {}'.format(self.data.open[0],self.data.high[-1],self.data.close[0],self.smart_stop))
        #
        # #PATTERN 5
        # if self.my_signal_24_P5 or self.my_signal_30_P5:
        #     print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
        #     print('P5-CROSSOVER90 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
        #     self.logsignaldata()
        #     self.logdata()
        #
        #     self.slippage = round((self.data.open[0] * 20) / 12000)
        #     print('P5 - Setup1 - Sell: T-DAYOPEN {} < CLOSE {}: SELL: {}~{}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.open[0],self.data.open[0]-self.slippage, self.data.high[-1]))
        #
        #     # if self.data.open[0] < self.data.close[-1]:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.open[0],
        #     #         stopprice=self.data.high[-1],
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        #     self.slippage = round((self.data.close[-1] * 45) / 12000)
        #     self.sip = round(self.data.close[-1] +self.slippage, 2)
        #
        #     self.slippage = round((self.data.close[-1] * 40) / 12000)
        #     self.smart_stop =round(self.data.close[-1] - self.slippage,2)
        #     print('P5 - Setup2 - Buy:  SIP {} > T-DAYOPEN {} > CLOSE {}: BUY: {}, STOP: {}'.format(self.sip,self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))
        #
        #     # if self.sip > self.data.open[0] > self.data.close[-1]:
        #     #     self.order = self.buy_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.close[-1],
        #     #         stopprice=self.smart_stop,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        #     self.slippage = round((self.data.close[-1] * 45) / 12000)
        #     self.sip = round(self.data.close[-1] + self.slippage, 2)
        #     p5_slip = round((self.data.open[0] * 40) / 12000)
        #     print('P5 - Setup3 - Sell:  T-DAYOPEN {} > SIP {} : SELL: {}, STOP: {}'.format(self.data.open[0],self.sip,self.data.open[0], self.data.open[0]+p5_slip))
        #
        #     # if self.data.open[0] > self.sip:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.open[0],
        #     #         stopprice=self.data.open[0]+p5_slip,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #
        # #PATTERN 6
        # if self.my_signal_24_P6 or self.my_signal_30_P6:
        #     print('-' * 32, ' TRADINGPLAN FOR {}'.format(date), '-' * 32)
        #     print('P6-CROSSOVER98 - ST24: {} -> {}, ST30: {} -> {}'.format(st_24_2, st_24_1, st_30_2, st_30_1))
        #     self.logsignaldata()
        #     self.logdata()
        #
        #     self.smart_stop = round(self.data.close[-1] - ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
        #     self.sip = round(self.data.close[-1] + ((self.data.high[-1] - self.data.low[-1]) / 2), 2)
        #     self.slippage = round((self.data.close[-1] * 20) / 12000)
        #     print('P6 - Setup1 - Buy: T-DAYOPEN {} > CLOSE {}: BUY: {}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.close[-1],self.smart_stop))
        #     # if self.data.open[0] > self.data.close[-1]:
        #     #     self.order = self.buy_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.close[-1],
        #     #         stopprice=self.smart_stop,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )
        #     print('P6 - Setup2 - Sell: T-DAYOPEN {} < CLOSE {}: SELL: {}~{}, STOP: {}'.format(self.data.open[0],self.data.close[-1],self.data.open[0],self.data.close[-1]-self.slippage,self.sip))
        #     # if self.data.open[0] < self.data.close[-1]:
        #     #     self.order = self.sell_bracket(
        #     #         exectype=bt.Order.Limit,
        #     #         price=self.data.open[0],
        #     #         stopprice=self.sip,
        #     #         limitexec=None,
        #     #         valid=bt.Order.T_Close
        #     #     )

def run():
    cerebro = bt.Cerebro(stdstats=False)

    index_list = ['IBGB100','IBDE100', 'IBUS30', 'IBUS500','IBUST100', 'ES', 'NIFTY']

    print("Available Index:")
    for i, index in enumerate(index_list, start=1):
        print('{}. {}'.format(i, index))
    while True:
        try:
            selected = int(input('Select a index (1-{}): '.format(i)))
            index = index_list[selected - 1]
            print('You have selected {}'.format(index))
            break
        except (ValueError, IndexError):
            print('This is not a valid selection. Please enter number between 1 and {}!'.format(i))

    if index in('IBGB100'):
        tz='UTC'
        sessionstart = datetime.time(7, 00, 00)
        sessionend = datetime.time(15, 00, 00)
        dataname = "IBGB100-CFD-SMART"
    elif index in ('IBDE100'):
        tz = 'UTC'
        sessionstart = datetime.time(7, 00, 00)
        sessionend = datetime.time(15, 00, 00)
        dataname='IBDE30-CFD-SMART-EUR'
    elif index in ('IBUS30'):
        tz = 'EST5EDT'
        sessionstart = datetime.time(9, 30, 00)
        sessionend = datetime.time(16, 00, 00)
        dataname = "IBUS30-CFD-SMART"
    elif index in ('IBUS500'):
        tz = 'EST5EDT'
        sessionstart = datetime.time(9, 30, 00)
        sessionend = datetime.time(16, 00, 00)
        dataname = "IBUS500-CFD-SMART"
    elif index in ('IBUST100'):
        tz = 'EST5EDT'
        sessionstart = datetime.time(9, 30, 00)
        sessionend = datetime.time(16, 00, 00)
        dataname = "IBUST100-CFD-SMART"
    elif index in ('ES'):
        tz = 'EST5EDT'
        sessionstart=datetime.time(9, 30, 00)
        sessionend=datetime.time(16, 00, 00)
        dataname = "ES-202009-GLOBEX"
    elif index in 'NIFTY':
        tz = None
        sessionstart = datetime.time(9, 30, 00)
        sessionend = datetime.time(16, 00, 00)
        data = bt.feeds.YahooFinanceData(dataname='^NSEI', fromdate=datetime.datetime(2019, 1, 1),
                                         todate=datetime.datetime.today())
        cerebro.adddata(data)

    stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        tz=tz,
        rtbar=False,  # use RealTime 5 seconds bars
        # historical=True,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        # fromdate=datetime.datetime(2020, 6, 1),  # get data from..
        # todate=datetime.datetime(2020, 12, 31),  # get data till..
        # todate=datetime.datetime.today(),  # get data till..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target,
        useRTH=True,
        sessionstart=sessionstart,
        sessionend=sessionend
    )

    if index not in ('NIFTY'):
        store = bt.stores.IBStore(port=7497, clientId=1001)
        cerebro.broker = store.getbroker()
        data = store.getdata(dataname=dataname, **stockkwargs)
        data.addfilter(bt.filters.SessionFilter)
        cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=180)

    cerebro.addstrategy(St)

    # # Set our desired cash start
    # cerebro.broker.setcash(100000.0)
    #
    # # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    #
    # # Set the commission
    # # # 0.1% ... divide by 100 to remove the %
    # cerebro.broker.setcommission(commission=0.001)
    #
    # # Print out the starting conditions
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    # # Print out the final result
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == "__main__":
    run()
