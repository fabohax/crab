# STRATO
Freqtrade trading strategy with Bollinger Bands, MACD & Stochastic RSI.

![Buy/Sell signals](/preview.png)

## Buy
* When price is oversold and losing momentum at Stochastic RSI and MACD signal is below 0.
* When price is lower than Lower Bollinger Band since 14 Periods.

## Sell
* When price is overbought and crossing above 80 Stochastic RSI value.
* When MACD signal is above MACD histogram.
* When price is higher than Higher Bollinger Band whith 2.7 Standard Deviation.

## ROI
* Yes

## Stoploss 
* Yes

## Trailing-Stoploss
* No
