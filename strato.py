# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy


class strato(IStrategy):
    """
    Default Strategy provided by freqtrade bot.
    Please do not modify this strategy, it's  intended for internal use only.
    Please look at the SampleStrategy in the user_data/strategy directory
    or strategy repository https://github.com/freqtrade/freqtrade-strategies
    for samples and inspiration.
    """
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy
    minimal_roi = {
         "0": 0.01, "4": 0.0075, "7": 0.005, "9": 0.0025, "15": 0
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.0022
    

    # Optimal ticker interval for the strategy
    ticker_interval = '1m'

    # Optional order type mapping
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 20

    # Optional time in force for orders
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc',
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # Bollinger bands
        bollinger21 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.1)
        dataframe['bb_low21'] = bollinger21['lower']
        dataframe['bb_mid21'] = bollinger21['mid']
        dataframe['bb_high21'] = bollinger21['upper']

        bollinger27 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.7)
        dataframe['bb_low27'] = bollinger27['lower']
        dataframe['bb_mid27'] = bollinger27['mid']
        dataframe['bb_high27'] = bollinger27['upper']

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        #RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=21)

        #STOCH_RSI
        period = 21
        smoothD = 3
        smoothK = 3
        stochrsi  = (dataframe['rsi'] - dataframe['rsi'].rolling(period).min()) / (dataframe['rsi'].rolling(period).max() - dataframe['rsi'].rolling(period).min())
        dataframe['fastk'] = stochrsi.rolling(smoothK).mean() * 100
        dataframe['fastd'] = dataframe['fastk'].rolling(smoothD).mean()

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
               ((dataframe['macdsignal']<0) &
               (dataframe['fastk']<20) &
               ((dataframe['fastd']-dataframe['fastk'])<3)) |
               (((dataframe['close']+dataframe['low'])/2) < dataframe['bb_low21'])
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
               (dataframe['macdsignal']>dataframe['macdhist']) |
               (dataframe['high'] > dataframe['bb_high27']) |
               (qtpylib.crossed_below(dataframe['fastk'],80))
            ),
            'sell'] = 1
        return dataframe

