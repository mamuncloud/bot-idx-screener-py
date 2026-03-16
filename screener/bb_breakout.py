class BbBreakout:
    def __init__(self):
        pass

    def screen(self, df):
        """
        Strategi:
        0. Close sebelumnya < Upper Bollinger Band (Belum breakout)
        1. Close sekarang > Upper Bollinger Band (Breakout)
        2. Volume sekarang > 2x Rata-rata Volume 20 hari
        3. Turnover > 5 Miliar
        4. Harga > 60 dan < 5000
        5. Volume > Previous Volume
        6. MA20 > MA50
        """
        try:
            if len(df) < 50: return False
            
            # Avoid modifying original df
            df = df.copy()
            
            # 1. Hitung Bollinger Bands (Standar deviasi 2, Periode 20)
            ma_20 = df['Close'].rolling(window=20).mean()
            ma_50 = df['Close'].rolling(window=50).mean()
            std_20 = df['Close'].rolling(window=20).std()
            upper_bb = ma_20 + (2 * std_20)
            
            # 2. Cek Kondisi Breakout (Current vs Previous)
            prev_breakout = df['Close'].iloc[-2] < upper_bb.iloc[-2]
            curr_breakout = df['Close'].iloc[-1] > upper_bb.iloc[-1]
            
            # 3. Cek Volume Spike
            vol_prev = df['Volume'].iloc[-1] > df['Volume'].iloc[-2]
            vol_avg = df['Volume'].rolling(window=20).mean().iloc[-1]
            vol_spike = df['Volume'].iloc[-1] > (vol_avg * 2)

            turnover = df['Close'].iloc[-1] * df['Volume'].iloc[-1]
            is_liquid = turnover > 5_000_000_000

            is_valid_price = (
                df['Close'].iloc[-1] > 60 
                and df['Close'].iloc[-1] < 5000
            )
            
            return (
                prev_breakout 
                and curr_breakout 
                and vol_prev 
                and vol_spike 
                and is_liquid
                and is_valid_price
                and ma_20.iloc[-1] > ma_50.iloc[-1]
            )
        except Exception as e:
            return False
