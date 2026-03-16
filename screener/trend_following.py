class TrendFollowing:
    def __init__(self):
        pass

    def screen(self, df):
        """
        Strategi: 
        1. Trend: MA20 > MA50 > MA100
        2. Trend: Close > MA20
        3. Breakout MA20: previous close < MA20 < Close
        4. Volume: Spike > 1.5x average volume 20d
        5. Momentum: Close > Previous Close (naik dari kemarin)
        6. Power: Close > Open * 1.04 (naik minimal 4% hari ini)
        7. Liquidity: Turnover > 5 Miliar
        """
        try:
            # Avoid modifying the original dataframe
            df = df.copy()
            
            # 1. Hitung Moving Averages
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            df['MA100'] = df['Close'].rolling(window=100).mean()

            # 2. Ambil data terbaru dan data sebelumnya
            latest = df.iloc[-1]
            previous = df.iloc[-2]

            # 3. Kondisi MA Bertumpuk (Trend)
            ma_condition = (
                previous['MA20'] > previous['Close']
                and latest['Close'] > latest['MA20']
                and latest['MA20'] > latest['MA50']
                and latest['MA50'] > latest['MA100']
            )

            # 4. Kondisi Volume Spike (Volume > 1.5x rata-rata 20 hari)
            avg_volume = df['Volume'].rolling(window=20).mean().iloc[-1]
            volume_spike = latest['Volume'] > (avg_volume * 1.5)
                
            # 5. Kondisi Momentum Baru (User Request)
            is_higher_than_yesterday = latest['Close'] > previous['Close']
                
            # Close > Open * 1.04 (Min. kenaikan 4% dari harga buka hari ini)
            is_strong_bullish = latest['Close'] > (latest['Open'] * 1.04)

            # 6. Kondisi Turnover > 5 Miliar
            turnover = latest['Close'] * latest['Volume']
            is_liquid = turnover > 5_000_000_000

            return (
                ma_condition 
                and volume_spike 
                and is_higher_than_yesterday 
                and is_strong_bullish
                and is_liquid
            )
        except Exception as e:
            return False
