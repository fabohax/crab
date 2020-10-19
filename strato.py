# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy

class strato(IStrategy):

    INTERFACE_VERSION = 2

    minimal_roi = {
        "0": 0.0438,
        "25": 0.022,
        "39": 0.0107,
        "137": 0
    }

    stoploss = -0.0021

    timeframe = '3m'

    order_types = {
        'buy': 'market',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    startup_candle_count: int = 20

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
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=3.3)
        dataframe['bblow'] = bollinger['lower']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2)
        dataframe['bbmid'] = bollinger2['mid']

        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.1)
        dataframe['bbhi'] = bollinger3['upper']

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

        # dataframe_5m = resample_to_interval(dataframe, 5)
        # dataframe_5m['rsi']=ta.RSI(dataframe_5m, timeperiod=14)
        # stochrsi_5m = (dataframe_5m['rsi'] - dataframe_5m['rsi'].rolling(period).min()) / (dataframe_5m['rsi'].rolling(period).max() - dataframe_5m['rsi'].rolling(period).min())
        # dataframe_5m['srsik']= stochrsi_5m.rolling(SmoothK).mean() * 100
        # dataframe_5m['srsid'] = dataframe_5m['srsi_k'].rolling(smoothD).mean()   
        
        # dataframe = resampled_merge(dataframe, dataframe_5m, fill_na=True)     


        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (
                    (dataframe['low'] < dataframe['bblow']) &
                    (dataframe['macdsignal'] < 0) &
                    (dataframe['srsi_d'] < 21)
                )|
                (
                    (dataframe['macdsignal'] < dataframe['macdhist']) &
                    (dataframe['srsi_k'] < 6) &
                    (dataframe['srsi_d'] < 12) &
                    (dataframe['srsi_d'] > dataframe['srsi_k'])
                )
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['bbmid'], dataframe['open']))
                | (dataframe['macdsignal'] > dataframe['macdhist'])
                | (dataframe['close'] > dataframe['bbhi']) 
                | (dataframe['srsi_d']==100)
            ),
            'sell'] = 1
        return dataframe




