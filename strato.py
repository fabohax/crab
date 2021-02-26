# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy

class strato(IStrategy):

    INTERFACE_VERSION = 2

    minimal_roi = {
        "0": 0.0055,
        "30": 0
    }

    stoploss = -0.1


    timeframe = '1m'

    order_types = {
        'buy': 'limit',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    startup_candle_count: int = 20

    trailing_stop = True
    trailing_stop_positive = 0.13267
    trailing_stop_positive_offset = 0.22438
    trailing_only_offset_is_reached = True

    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc',
    }

    def informative_pairs(self):

        return []

    def get_ticker_indicator(self):
        return int(self.timeframe[:-1])

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.7)
        dataframe['bblo'] = bollinger['lower']
        dataframe['bbmi'] = bollinger['mid']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=1.1)
        dataframe['bbhi'] = bollinger2['upper']

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']     

        # #RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # #StochRSI 
        period = 14
        smoothD = 3
        SmoothK = 3
        stochrsi  = (dataframe['rsi'] - dataframe['rsi'].rolling(period).min()) / (dataframe['rsi'].rolling(period).max() - dataframe['rsi'].rolling(period).min())
        dataframe['srsi_k'] = stochrsi.rolling(SmoothK).mean() * 100
        dataframe['srsi_d'] = dataframe['srsi_k'].rolling(smoothD).mean()


        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['low'] < dataframe['bblo']) & (dataframe['srsi_d']<7) & (dataframe['macd']<0)
	        ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['high'] > dataframe['bbmi'])
            ),
            'sell'] = 1
        return dataframe




