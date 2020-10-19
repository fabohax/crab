from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

import talib.abstract as ta  # noqa
import freqtrade.vendor.qtpylib.indicators as qtpylib


class hyperstrato(IHyperOpt):

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2.7)
        dataframe['bblow'] = bollinger['lower']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=2)
        dataframe['bbmid'] = bollinger2['mid']

        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=21, stds=3)
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

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []
            # GUARDS AND TRENDS
            if 'k-enabled' in params and params['k-enabled']:
                conditions.append(dataframe['srsi_k'] < params['buy_k'])
            if 'd-enabled' in params and params['d-enabled']:
                conditions.append(dataframe['srsi_d'] < params['buy_d'])

            # TRIGGERS
            if 'buy-trigger' in params:
                if params['buy-trigger'] == 'bb_lower':
                    conditions.append(dataframe['close'] < ((params['bbbuy']/10000)*dataframe['bblow']))

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:

        return [
            Categorical(['bb_lower'], name='buy-trigger'),
            Integer(9900, 10000, name='bbbuy'),
            Integer(0, 5, name='buy_k'),
            Integer(0, 25, name='buy_d'),
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []
            # GUARDS AND TRENDS
            if 'sell-k-enabled' in params and params['sell-k-enabled']:
                conditions.append(dataframe['srsi_k'] > params['sell_k'])

            if 'sell-d-enabled' in params and params['sell-d-enabled']:
                conditions.append(dataframe['srsi_d'] > params['sell_d'])

            # TRIGGERS
            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'bb_hi':
                    conditions.append(
                        qtpylib.crossed_above(dataframe['open'], ((params['sell']/10000) * dataframe['bbhi']))
                    )

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:

        return [
            Categorical(['bb_hi'], name='sell-trigger'),
            Integer(9900, 12000, name='sell'),
            Integer(50, 100, name='sell_k'),
            Integer(50, 100, name='sell_d')
        ]

    @staticmethod
    def stoploss_space() -> List[Dimension]:

        return [
            Real(-0.05, -0.015, name='stoploss'),
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (
                    (dataframe['low'] < (dataframe['bblow'])) &
                    (dataframe['macdsignal'] < 0) &
                    (dataframe['srsi_d'] < 21 )
                )|
                (
                    (dataframe['macdsignal'] < dataframe['macdhist']) &
                    (dataframe['srsi_k'] < 5) &
                    (dataframe['srsi_d'] < 10) &
                    ((dataframe['srsi_d'] > dataframe['srsi_k']))
                )|
                (
                    (dataframe['macdsignal'] < dataframe['macdhist']) &
                    (dataframe['srsi_d'] < 35) &
                    (dataframe['srsi_k'] > 20) &
                    ((dataframe['srsi_d'] > dataframe['srsi_k']))
                )
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['bbmid'], dataframe['open']))
                | (dataframe['macdsignal'] > dataframe['macdhist'])
                | (dataframe['high']) > dataframe['bbhi']
                | (dataframe['close']>dataframe['bbhi21']) 
                | (dataframe['srsi_k']==100 & dataframe['srsi_d']==100) 
            ),
            'sell'] = 1
        return dataframe
