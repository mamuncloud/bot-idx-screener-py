class Breakout20Days:
    def __init__(self):
        pass

    def screen(self, df):
        """
        Strategi:
        1. Breakout: Harga Close hari ini > High tertinggi dalam 20 hari terakhir (tidak termasuk hari ini)
        2. Volume: Volume hari ini > 1.5x rata-rata volume 20 hari
        3. Momentum: Close > Open * 1.04 (Candle bullish naik minimal 4% hari ini)
        4. Liquidity: Turnover > 5 Miliar
        """
        try:
            if len(df) < 21:  # Butuh minimal 21 data untuk membandingkan dengan 20 hari sebelumnya
                return False
            
            # 1. Ambil data hari ini
            latest = df.iloc[-1]
            previous = df.iloc[-2]

            # 2. Cari harga tertinggi dari 20 hari ke belakang (tidak termasuk hari ini)
            # .iloc[-21:-1] mengambil index ke -21 sampai -2 (total 20 bar sebelum hari ini)
            lookback_period = df.iloc[-21:-1]
            max_high_20d = lookback_period['High'].max()

            # 3. Hitung Volume Spike
            avg_volume_20d = df['Volume'].rolling(window=20).mean().iloc[-1]
            volume_spike = latest['Volume'] > (avg_volume_20d * 1.5)

            # 4. Kondisi Breakout
            # Harga tutup harus menembus titik tertinggi 20 hari
            is_breakout = latest['Close'] > max_high_20d

            # Tambahan: Pastikan candle hari ini bullish (Close > Open)
            is_bullish = latest['Close'] > latest['Open'] * 1.04

            is_higher_than_yesterday = latest['Close'] > previous['Close']

            # 5. Kondisi Turnover > 5 Miliar (Price * Volume)
            turnover = latest['Close'] * latest['Volume']
            is_liquid = turnover > 5_000_000_000
            
            return is_breakout and volume_spike and is_bullish and is_liquid and is_higher_than_yesterday
        except Exception as e:
            print(f"Error pada screening breakout: {e}")
            return False
