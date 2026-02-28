import pandas as pd
import pandas_ta as ta

class Strategy:
    def __init__(self, symbol):
        self.symbol = symbol

    def analyze(self, data):
        """
        Input: List of dicts (OHLCV) from Delta API.
        Output: 'buy', 'sell', or 'hold'
        """
        if not data or len(data) < 40:
            return 'hold'

        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Pine Script Logic Components
        # len = 34, SMA
        df['sma34'] = ta.sma(df['close'], length=34)
        
        # EMA 13, EMA 21
        df['ema13'] = ta.ema(df['close'], length=13)
        df['ema21'] = ta.ema(df['close'], length=21)
        
        # Hull MA (HMA) - (hma_base_length=8 + hma_length_scalar=5 * 6) = 38
        # Actually in script: hullma(hma_src, hma_base_length+hma_length_scalar*6)
        # = hullma(close, 8 + 30) = hullma(close, 38)
        df['hma38'] = ta.hma(df['close'], length=38)

        # Signal Generator logic:
        # longCondition = crossover(close, open)
        # shortCondition = crossunder(close, open)
        
        # Crossover(close, open) check:
        # Current: close > open
        # Previous: close <= open
        curr_close = df['close'].iloc[-1]
        curr_open = df['open'].iloc[-1]
        prev_close = df['close'].iloc[-2]
        prev_open = df['open'].iloc[-2]

        is_long = (prev_close <= prev_open) and (curr_close > curr_open)
        is_short = (prev_close >= prev_open) and (curr_close < curr_open)

        if is_long:
            return 'buy', df.iloc[-1].to_dict()
        elif is_short:
            return 'sell', df.iloc[-1].to_dict()
        else:
            return 'hold', df.iloc[-1].to_dict()
