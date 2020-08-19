# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy

"""
Strato Strategy
Designed by @fabohax
CC0 License
"""

class strato(IStrategy):
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy
    minimal_roi = {
         "0": 0.004, "12": 0.002, "24": 0.001, "48": 0
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.0021
    

    # Optimal ticker interval for the strategy
    ticker_interval = '3m'

    # Optional order type mapping
    order_types = {
        'buy': 'limit',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 21

    # Optional time in force for orders
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc',
    }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.1)
        dataframe['bbhigh'] = bollinger['upper']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.7)
        dataframe['bblow'] = bollinger2['lower']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        BUY
        """
        dataframe.loc[
            (
                ((dataframe['close']+dataframe['low'])/2) < dataframe['bblow']
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        SELL
        """
        dataframe.loc[
            (
                ((dataframe['close']+dataframe['high'])/2) > dataframe['bbhigh']
            ),
            'sell'] = 1
        return dataframe

