import backtrader as bt
import datetime

class MyIB():
    index_list = ['IBGB100', 'IBDE30', 'IBUS30', 'IBUS500', 'IBUST100', 'IBAU200','ES', 'NQ', 'DOW', 'SPY']

    # create the data
    usestore = True
    storekwargs = dict(
        host='127.0.0.1', port=7497,
        clientId=None, timeoffset=False,
        reconnect=3, timeout=3.0,
        notifyall=False, _debug=False
    )
    ibstore = bt.stores.IBStore(**storekwargs)
    print("Using IBstore")
    broker = ibstore.getbroker()
    IBDataFactory = ibstore.getdata if usestore else bt.feeds.IBData

    tz = 'UTC'
    dtfmt = '%Y-%m-%dT%H:%M:%S.%f'
    sessionstart = None
    sessionend = None

    tradename = None
    what='TRADES'


    def __init__(self, session=False):
        self.session = session

    def getdata(self, start, end):
        print("Available Index:")
        for i, index in enumerate(self.index_list, start=1):
            print('{}. {}'.format(i, index))
        while True:
            try:
                selected = int(input('Select a index (1-{}): '.format(i)))
                index = self.index_list[selected - 1]
                print('You have selected {}'.format(index))
                break
            except (ValueError, IndexError):
                print('This is not a valid selection. Please enter number between 1 and {}!'.format(i))

        if index in ('IBGB100'):
            dataname = "IBGB100-CFD-SMART"
            dataname = "AAPL-STK-SMART-USD"
            self.sessionstart = datetime.time(7, 00, 00)
            self.sessionend = datetime.time(15, 00, 00)
            self.what = 'TRADES'
        elif index in ('IBDE30'):
            dataname = 'IBDE30-CFD-SMART-EUR'
            self.sessionstart = datetime.time(7, 00, 00)
            self.sessionend = datetime.time(15, 30, 00)
            self.what = 'MIDPOINT'
        elif index in ('IBUS30'):
            dataname = "IBUS30-CFD-SMART"
            self.sessionstart = datetime.time(13, 30, 00)
            self.sessionend = datetime.time(20, 00, 00)
            self.what = 'MIDPOINT'
        elif index in ('IBUS500'):
            dataname = "IBUS500-CFD-SMART"
            self.sessionstart = datetime.time(13, 30, 00)
            self.sessionend = datetime.time(20, 00, 00)
            self.what = 'MIDPOINT'
        elif index in ('IBUST100'):
            dataname = "IBUST100-CFD-SMART"
            self.sessionstart = datetime.time(13, 30, 00)
            self.sessionend = datetime.time(20, 00, 00)
            self.what = 'MIDPOINT'
        elif index in ('IBAU200'):
            dataname = "IBAU200-CFD-SMART"
            # self.sessionstart = datetime.time(13, 30, 00)
            self.sessionend = datetime.time(6, 00, 00)
            self.what = 'MIDPOINT'
        elif index in ('ES'):
            dataname = "ES-202009-GLOBEX"
        elif index in ('NQ'):
            dataname = "NQ-202009-GLOBEX"
        elif index in ('DOW'):
            dataname = "YM-202009-ECBOT"
        elif index in ('SPY'):
            dataname = "SPY-STK-SMART-USD"
            tradename = "SPY-CFD-SMART-USD"
        datakwargs = dict(
            timeframe=bt.TimeFrame.Minutes,
            tz=self.tz,
            rtbar=False,  # use RealTime 5 seconds bars
            historical=True,  # only historical download
            qcheck=0.5,  # timeout in seconds (float) to check for events
            fromdate=start,
            todate = end,
            latethrough=False,  # let late samples through
            tradename=self.tradename,  # use a different asset as order target,
            useRTH=True,
            sessionstart=self.sessionstart,
            sessionend=self.sessionend,
            what=self.what
        )
        data = self.IBDataFactory(dataname=dataname, **datakwargs)
        if self.session:
            data.addfilter(bt.filters.MySessionFilter)
        return data