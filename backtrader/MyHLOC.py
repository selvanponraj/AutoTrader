import backtrader.feeds as bt
class MyHLOC(bt.feeds.GenericCSVData):
  # datetime, O, H, L, C, V, OI, WAP
  params = (
      # ('fromdate', datetime.datetime(2020, 4, 1)),
      # ('todate', datetime.datetime(2020, 4, 2)),
      ('nullvalue', 0.0),
      # ('dtformat', ('%Y-%m-%d')),
      # ('tmformat', ('%H.%M.%S')),
      ('timeframe', bt.TimeFrame.Minutes),
      ('datetime', 0),
      ('open', 1),
      ('high', 2),
      ('low', 3),
      ('close', 4),
      ('volume', 5),
      ('openinterest', 6)
)
