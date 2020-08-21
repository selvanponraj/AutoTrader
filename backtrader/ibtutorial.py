#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2018 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import datetime


class St(bt.Strategy):
    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))
        txt.append('{}'.format(self.data.datetime.datetime(0).isoformat()))
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    data_live = False
    trade_open = None

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True
            self.trade_open = self.datas[0].open[0]

    def notify_order(self, order):
        if order.status == order.Completed:
            buysell = 'BUY ' if order.isbuy() else 'SELL'
            txt = '{} {}@{}'.format(buysell, order.executed.size,
                                    order.executed.price)
            print(txt)

    bought = 0
    sold = 0

    def next_open(self):
        # self.logdata()
        pass

    def next(self):

        self.logdata()

        # if not self.data_live:
        #     return
        #
        # if not self.bought:
        #     self.bought = len(self)  # keep entry bar
        #     self.buy()
        # elif not self.sold:
        #     if len(self) == (self.bought + 3):
        #         self.sell()


def run(args=None):
    cerebro = bt.Cerebro(stdstats=False, cheat_on_open=True)
    store = bt.stores.IBStore(port=7497)

    # data = store.getdata(dataname='NIFTY-FUT-SGX-USD-202007', timeframe=bt.TimeFrame.Ticks)
    # data = store.getdata(dataname='IBUS30-CFD-SMART', timeframe=bt.TimeFrame.Minutes, tz='EST5EDT')
    # data = store.getdata(dataname='ES-202009-GLOBEX',
    #                      timeframe=bt.TimeFrame.Ticks,
    #                      tz='EST5EDT')
    dataname = "IBGB100-CFD-SMART"
    tz = 'UTC'
    sessionstart = datetime.time(7, 00, 00)
    sessionend = datetime.time(15, 00, 00)
    dataname = "IBGB100-CFD-SMART"
    # dataname = 'NIFTY-202008-SGX'
    dataname='ES-202009-GLOBEX'
    # dataname = 'NQ-202009-GLOBEX'
    # dataname = 'YM-202009-ECBOT'
    # dataname = 'GXBT'
    # dataname = 'NIFTY-202008-SGX'
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 8, 19)
    stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        tz=None,
        rtbar=True,  # use RealTime 5 seconds bars
        historical=True,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        fromdate=start,  # get data from..
        todate=end,  # get data till..
        # todate=datetime.datetime.today(),  # get data till..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target,
        useRTH=True,
        # sessionstart=sessionstart,
        # sessionend=sessionend
    )

    # data = store.getdata(dataname=dataname, timeframe=bt.TimeFrame.Minutes, compression=1, rtbar=True,
    #                        qcheck=1.0, latethrough=False,
    #                        tz=None, tzinput=None, useRTH=True)

    data0 = bt.feeds.IBData(dataname='AAPL-STK-SMART-USD', **stockkwargs)
    print(data0.lines)
    data0.addfilter(bt.filters.SessionFilter)
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Days, compression=1)

    # # LIVE
    # stockkwargs = dict(
    #     timeframe=bt.TimeFrame.Minutes,
    #     tz=None,
    #     rtbar=False,  # use RealTime 5 seconds bars
    #     historical=True,  # only historical download
    #     qcheck=0.5,  # timeout in seconds (float) to check for events
    #     # fromdate=datetime.datetime(2020, 6, 1),  # get data from..
    #     # todate=datetime.datetime(2020, 12, 31),  # get data till..
    #     # todate=datetime.datetime.today(),  # get data till..
    #     latethrough=False,  # let late samples through
    #     tradename=None,  # use a different asset as order target,
    #     useRTH=True,
    #     sessionstart=sessionstart,
    #     sessionend=sessionend,
    #     backfill=False
    # )

    # data1 = store.getdata(dataname=dataname, **stockkwargs)
    # cerebro.resampledata(data1, timeframe=bt.TimeFrame.Minutes, compression=1)

    cerebro.addstrategy(St)
    cerebro.run()


if __name__ == '__main__':
    run()