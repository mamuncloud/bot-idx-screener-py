class MacdCross:
    def __init__(self):
        pass

    def screen(self, df):
        """
        Strategi:
        1. MACD Golden Cross Up
        2. Volume Spike > 2x average volume 20d
        3. Volume > Previous Volume
        4. Turnover > 5 Miliar
        """
        try:
            if len(df) < 30: return False
            
            # Avoid modifying original df
            df = df.copy()
            
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            
            cross_up = (macd.iloc[-1] > signal.iloc[-1]) and (macd.iloc[-2] <= signal.iloc[-2])
            
            vol_avg = df['Volume'].rolling(window=20).mean().iloc[-1]
            vol_spike = df['Volume'].iloc[-1] > (vol_avg * 2)
            vol_compare = df['Volume'].iloc[-1] > df['Volume'].iloc[-2]
            
            # Liquidity check
            latest_close = df['Close'].iloc[-1]
            latest_volume = df['Volume'].iloc[-1]
            turnover = latest_close * latest_volume
            is_liquid = turnover > 5_000_000_000
            
            return cross_up and vol_spike and vol_compare and is_liquid
        except Exception as e:
            return False
