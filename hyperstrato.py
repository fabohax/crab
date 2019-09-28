# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from functools import reduce
from math import exp
from typing import Any, Callable, Dict, List
from datetime import datetime

import numpy as np# noqa F401
import talib.abstract as ta
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


class hyperstrato(IHyperOpt):
    """
    This is a sample hyperopt to inspire you.
    Feel free to customize it.

    More information in https://github.com/freqtrade/freqtrade/blob/develop/docs/hyperopt.md

    You should:
    - Rename the class name to some unique name.
    - Add any methods you want to build your hyperopt.
    - Add any lib you need to build your hyperopt.

    You must keep:
    - The prototypes for the methods: populate_indicators, indicator_space, buy_strategy_generator.

    The roi_space, generate_roi_table, stoploss_space methods are no longer required to be
    copied in every custom hyperopt. However, you may override them if you need the
    'roi' and the 'stoploss' spaces that differ from the defaults offered by Freqtrade.

    This sample illustrates how to override these methods.
    """
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:

        #STOCHRSI
        stoch_rsi = ta.STOCHRSI(dataframe)
        dataframe['fastd_rsi'] = stoch_rsi['fastd']
        dataframe['fastk_rsi'] = stoch_rsi['fastk']
        # Bollinger bands
        bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband1'] = bollinger1['lower']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_upperband2'] = bollinger2['upper']

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by hyperopt
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use
            """
            conditions = []
            # GUARDS AND TRENDS
            
            if 'fastk_rsi-enabled' in params and params['fastk_rsi-enabled']:
                conditions.append(dataframe['fastk_rsi'] < params['fastk_rsi-value'])
            if 'fastd_rsi-enabled' in params and params['fastd_rsi-enabled']:
                conditions.append(dataframe['fastd_rsi'] < params['fastd_rsi-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'bb_lower1':
                    conditions.append(dataframe['close'] < (0.999*dataframe['bb_lowerband1']))          

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching strategy parameters
        """
        return [
            Integer(0, 5, name='fastk_rsi-value'),
            Integer(0, 25, name='fastd_rsi-value'),
            Categorical(['bb_lower1','bb_lower2','bb_lower3'], name='trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by hyperopt
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use
            """
            # print(params)
            conditions = []
            # GUARDS AND TRENDS
            if 'sell-fastk_rsi-enabled' in params and params['sell-fastk_rsi-enabled']:
                conditions.append(dataframe['fastk_rsi'] > params['sell-fastk_rsi-value'])

            if 'sell-fastd_rsi-enabled' in params and params['sell-fastd_rsi-enabled']:
                conditions.append(dataframe['fastd_rsi'] > params['sell-fastd_rsi-value'])

            # TRIGGERS
            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'sell-bb_upper2':
                    conditions.append(qtpylib.crossed_above(
                        dataframe.open,(0.994*dataframe['bb_upperband2']
                        )))

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters
        """
        return [
            Integer(90, 100, name='sell-fastk_rsi-value'),
            Integer(65, 100, name='sell-fastd_rsi-value'),
            Categorical(['sell-bb_upper2'], name='sell-trigger')
        ]

    @staticmethod
    def generate_roi_table(params: Dict) -> Dict[int, float]:
        """
        Generate the ROI table that will be used by Hyperopt

        This implementation generates the default legacy Freqtrade ROI tables.

        Change it if you need different number of steps in the generated
        ROI tables or other structure of the ROI tables.

        Please keep it aligned with parameters in the 'roi' optimization
        hyperspace defined by the roi_space method.
        """
        roi_table = {}
        roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
        roi_table[params['roi_t3']] = params['roi_p1'] + params['roi_p2']
        roi_table[params['roi_t3'] + params['roi_t2']] = params['roi_p1']
        roi_table[params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

        return roi_table

    @staticmethod
    def roi_space() -> List[Dimension]:
        """
        Values to search for each ROI steps

        Override it if you need some different ranges for the parameters in the
        'roi' optimization hyperspace.

        Please keep it aligned with the implementation of the
        generate_roi_table method.
        """
        return [
            Integer(10, 120, name='roi_t1'),
            Integer(10, 60, name='roi_t2'),
            Integer(10, 40, name='roi_t3'),
            Real(0.01, 0.04, name='roi_p1'),
            Real(0.01, 0.07, name='roi_p2'),
            Real(0.01, 0.20, name='roi_p3'),
        ]

    @staticmethod
    def stoploss_space() -> List[Dimension]:
        """
        Stoploss Value to search

        Override it if you need some different range for the parameter in the
        'stoploss' optimization hyperspace.
        """
        return [
            Real(-0.6, 0, name='stoploss'),
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of from strategy
        must align to populate_indicators in this file
        Only used when --spaces does not include buy
        """
        dataframe.loc[
            (
                (dataframe.close<dataframe['bb_lowerband']) &
                (dataframe['fastd_rsi']<24) &
                (dataframe['fastk_rsi']<3)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of from strategy
        must align to populate_indicators in this file
        Only used when --spaces does not include sell
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe.open,(0.994*dataframe['bb_upperband']))) &
                (dataframe['fastd_rsi']>67) &
                (dataframe['fastk_rsi']>92)
            ),
            'sell'] = 1
        return dataframe
