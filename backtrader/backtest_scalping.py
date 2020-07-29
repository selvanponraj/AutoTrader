"""
Perform backtest using a scalping strategy
"""
# pylint: disable=invalid-name
import math
import glob
import os

from tqdm import tqdm
from pandas.plotting import register_matplotlib_converters
import pandas as pd
import matplotlib.pyplot as plt
register_matplotlib_converters()

SYMBOLS = ["AAPL"]

DATADIR = os.path.join('..', 'historical-market-data') # download directory for the data
MAX_INVESTMENT = 1000

# track or accumulated profit or losses among many SYMBOLS
acum_market = 0
acum_wallet = 0

# calculate a buy&hold profit to compare against the scalping strategy
profit_buy_and_hold = {}
for symbol in tqdm(SYMBOLS, desc="Symbols"):
    path = f'{DATADIR}/{symbol}-2016-*.csv'
    days = glob.glob(path)

    if len(days) < 245:
        tqdm.write('Not enough days')
        continue

    # profit for `symbol` with a buy and hold strategy
    first_day = pd.read_csv(days[0])
    last_day = pd.read_csv(days[-1])

    last_price = last_day.iloc[-1]["close"]
    initial_price = first_day.iloc[-1]["close"]
    profit_buy_and_hold[symbol] = last_price / initial_price

    # if we own the position or not
    owned = False

    # count how many transaction total made for the symbol
    num_transactions = 0

    # BUY or SELL prices
    buy_price = None
    sell_price = None

    # we reset out `wallet` with a default investment of `MAX_INVESTMENT`
    wallet = initial_wallet = MAX_INVESTMENT

    # this is for the dataframe of the previous day
    df_prev = None

    # where to plot transactions prices/transactiona/mavg of the day
    plot_day = False

    # list to store the transaction profits
    profits = []

    for d, day in enumerate(tqdm(days, desc=f"{symbol:4} days")):
        # we save all BUYs and SELLs in a list, so we can later plot them
        purchases_day = []
        sells_day = []

        df = pd.read_csv(day)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True, drop=False)
        df = df.between_time('09:30', '16:00')

        if df_prev is None:
            df_prev = df
            continue

        # rolling 10m average standard deviation of the previous day
        prev_open_stddev = df_prev['open'].rolling(10).std().mean()

        # moving average of the current day close price
        avg_window = 4
        df['mavg'] = df['close'].rolling(avg_window).mean()

        # we need to force sell on the last minute of the last day
        force_sell = False

        # we need to reset the dataframe's index to have numerical indexes
        #   so we can easily reference things like "two steps back"
        df.reset_index(inplace=True, drop=True)
        for i, row in df.iterrows():
            open_price = row["open"]

            # if it's the last minute of the last day, we force sell
            if day == days[-1] and row.timestamp == df.iloc[-1].timestamp:
                final_price = row["close"]
                if owned is True:
                    force_sell = True
                    tqdm.write('forced sell')


            # numerical index of "two steps back"
            lookback = i - 2
            if lookback < 0 or math.isnan(df.iloc[lookback]['mavg']):
                continue


            if owned is False:

                # algo buys if previous minute's close price
                #   just passed the average on the previous minute
                buy_signal = (
                    df.iloc[i - 2]['close'] < df.iloc[i - 2]['mavg'] - prev_open_stddev
                    and df.iloc[i - 1]['close'] > df.iloc[i - 1]['mavg']
                )

                if buy_signal:
                    price = open_price
                    buy_price = price

                    # we buy as much as we possibly can
                    qty = int(wallet / price)

                    # decrease wallet by amount bought
                    amount = qty * price
                    wallet -= amount

                    # increase transaction counter
                    num_transactions += 1

                    # add transaction to our list
                    purchases_day.append([row['timestamp'], price])

                    # change the owned flag to True
                    owned = True

            elif owned is True:

                # algo sells if current open_price > buy_price,
                # or if forced_sell is True
                sell_signal = (
                    open_price > buy_price + prev_open_stddev
                    or force_sell is True
                )

                # uncomment this to plot unusual price drops
                # this is a moment to consider overall market health
                # if buy_price - open_price > 50 * prev_open_stddev:
                #     s = 1
                #     plot_day = True
                # else:
                #     plot_day = False


                if sell_signal:
                    price = open_price
                    sell_price = price
                    amount = qty * sell_price
                    wallet += amount
                    num_transactions += 1
                    sells_day.append([row['timestamp'], price])
                    profits.append([row['timestamp'], price])
                    owned = False

        df_prev = df

        # set to True if you want to plot of the day
        plot_day = False
        if plot_day:
            legend = []
            plt.plot(df["timestamp"], df["open"],'.-')
            legend.append('open')
            plt.plot(df["timestamp"], df["mavg"],'.-')
            legend.append('average')
            if purchases_day:
                plt.plot(*list(zip(*purchases_day)),'o')
                legend.append('purchases_day')
            if sells_day:
                plt.plot(*list(zip(*sells_day)),'o')
                legend.append('sells_day')
            plt.legend(legend)
            plt.title(f"Profit: {(wallet/initial_wallet)*100-100:.2f}%")
            plt.show()

    wallet_change_pc = wallet / initial_wallet
    acum_market += profit_buy_and_hold[symbol]
    acum_wallet += wallet_change_pc
    tqdm.write(f"{symbol} - market change %: {profit_buy_and_hold[symbol]:.3f}")
    tqdm.write(f"{symbol} - wallet change %: {wallet_change_pc:.3f}")
    tqdm.write(f"{symbol} - num_transactions: {num_transactions}")