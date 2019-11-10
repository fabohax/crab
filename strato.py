import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.indicator_helpers import fishers_inverse
from freqtrade.strategy.interface import IStrategy


class Strato(IStrategy):

    minimal_roi = {
        "0":   0.041010101010101010,
        "25":  0.022010101010101010,
        "39":  0.010101010101010101,
        "137": 0
    }
    stoploss = -0.566053026840454
    ticker_interval = '5m'
    order_types = {
        'buy': 'market',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc',
    }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Bollinger bands
        bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband1'] = bollinger1['lower']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_upperband2'] = bollinger2['upper']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['close']<(0.999*dataframe['bb_lowerband1']))
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['open'],(0.994*dataframe['bb_upperband2'])))
            ),
            'sell'] = 1
        return dataframe


# Best result:

#   2322/5000:    378 trades. Avg profit  0.18%. Total profit  697.97824604 USDT (  69.80Σ%). Avg duration 117.2 mins. Objective: 1.69246

# Buy hyperspace params:
# {'fastd_rsi-value': 24, 'fastk_rsi-value': 3, 'trigger': 'bb_lower1'}
# Sell hyperspace params:
# {   'sell-fastd_rsi-value': 67,
#     'sell-fastk_rsi-value': 92,
#     'sell-trigger': 'sell-bb_upper2'}
# ROI table:
# {   0: 0.043830430840248555,
#     25: 0.022071662190063887,
#     39: 0.01079222321562015,
#     137: 0}
# Stoploss: -0.566053026840454
