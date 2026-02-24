class StockScreener:
    def __init__(self):
      return

    def is_breakout_20_days(self, df):
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

        # 5. Kondisi Turnover > 3 Miliar (Price * Volume)
        # Di Bursa Efek Indonesia, Volume di yfinance biasanya dalam lembar saham
        turnover = latest['Close'] * latest['Volume']
        is_liquid = turnover > 5_000_000_000
        
        return is_breakout and volume_spike and is_bullish and is_liquid and is_higher_than_yesterday
      except Exception as e:
        print(f"Error pada screening breakout: {e}")
        return False

    def is_trend_following(self, df):
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
        # Close > Prev Close
        is_higher_than_yesterday = latest['Close'] > previous['Close']
            
        # Close > Open * 1.04 (Min. kenaikan 4% dari harga buka hari ini)
        is_strong_bullish = latest['Close'] > (latest['Open'] * 1.04)

        # 6. Kondisi Turnover > 3 Miliar (Price * Volume)
        # Di Bursa Efek Indonesia, Volume di yfinance biasanya dalam lembar saham
        turnover = latest['Close'] * latest['Volume']
        is_liquid = turnover > 5_000_000_000

        # Return True jika semua kondisi terpenuhi
        return (
          ma_condition 
          and volume_spike 
          and is_higher_than_yesterday 
          and is_strong_bullish
          and is_liquid
        )
      except Exception as e:
        return False

    def is_macd_golden_cross_up(self, df):
        """
        Strategi:
        1. MACD Golden Cross Up
        2. Volume Spike > 2x average volume 20d
        3. Volume > Previous Volume
        4. Turnover > 5 Miliar
        """
        if len(df) < 30: return False
        
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        cross_up = (macd.iloc[-1] > signal.iloc[-1]) and (macd.iloc[-2] <= signal.iloc[-2])
        
        vol_avg = df['Volume'].rolling(window=20).mean().iloc[-1]
        vol_spike = df['Volume'].iloc[-1] > (vol_avg * 2)
        vol_compare = df['Volume'].iloc[-1] > df['Volume'].iloc[-2]
        
        return cross_up and vol_spike and vol_compare

    def is_rising_three_method(self, df):
      """
        Strategi:
        1. C1 Bullish > 4%
        2. Middle 3 days stay inside C1
        3. C5 Bullish > 4%
        4. C5 Close > C1 High
      """
      if len(df) < 5: return False
        
      c = df.tail(5)
        
      c1_bullish = c.iloc[0]['Close'] > c.iloc[0]['Open'] * 1.04
      c1_high = c.iloc[0]['High']
      c1_low = c.iloc[0]['Low']
        
      middle_stayed_inside = True
      for i in range(1, 4):
        if c.iloc[i]['High'] > c1_high or c.iloc[i]['Low'] < c1_low:
          middle_stayed_inside = False
          break
        
      c5_bullish = c.iloc[4]['Close'] > c.iloc[4]['Open'] * 1.04
      breakout = c.iloc[4]['Close'] > c1_high
      
      return (
        c1_bullish 
        and middle_stayed_inside 
        and c5_bullish 
        and breakout
      )

    def is_before_rising_three_method_with_volume(self, df):
      """
      Strategi Antisipasi dengan Konfirmasi Volume:
      1. C1 Bullish kuat (> 4%) + Volume Tinggi
      2. C2, C3, C4 berada di dalam range High/Low C1
      3. C2 Bearish, C3 Bearish, C4 Bearish (Color Red)
      4. Volume C2, C3, C4 menunjukkan tren menurun (Dying Volume)
      """
      if len(df) < 4: return False
      
      c = df.tail(4)
      
      # 1. Validasi Candle 1 (Bullish & Base High/Low)
      c1_bullish = c.iloc[0]['Close'] > c.iloc[0]['Open'] * 1.06
      c1_high = c.iloc[0]['High']
      c1_low = c.iloc[0]['Low']
      
      # 2. Validasi Middle Candles (Stay inside, Bearish & Volume weakening)
      middle_stayed_inside = (
        c.iloc[1]['Close'] < c1_high 
        and c.iloc[1]['Close'] > c1_low

        and c.iloc[2]['Close'] < c1_high 
        and c.iloc[2]['Close'] > c1_low

        and c.iloc[3]['Close'] < c1_high 
        and c.iloc[3]['Close'] > c1_low
      )
      middle_is_bearish = (
        c.iloc[1]['Close'] < c.iloc[1]['Open']
        and c.iloc[2]['Close'] < c.iloc[2]['Open']
        and c.iloc[3]['Close'] < c.iloc[3]['Open']
      )

      return (
          c1_bullish 
          and middle_stayed_inside 
          and middle_is_bearish
      )
    
    def is_bb_breakout_volume(self, df):
      """
        Strategi:
        0. Close sebelumnya < Upper Bollinger Band (Belum breakout)
        1. Close sekarang > Upper Bollinger Band (Breakout)
        2. Volume sekarang > 2x Rata-rata Volume 20 hari
        3. Turnover > 5 Miliar
      """
      if len(df) < 20: return False
        
      # 1. Hitung Bollinger Bands (Standar deviasi 2, Periode 20)
      ma_20 = df['Close'].rolling(window=20).mean()
      std_20 = df['Close'].rolling(window=20).std()
      upper_bb = ma_20 + (2 * std_20)
      
      # 2. Cek Kondisi Breakout (Current vs Previous)
      # Indeks -1 adalah data terbaru, -2 adalah data sebelumnya
      prev_breakout = df['Close'].iloc[-2] < upper_bb.iloc[-2]
      curr_breakout = df['Close'].iloc[-1] > upper_bb.iloc[-1]
        
      # 3. Cek Volume Spike
      vol_avg = df['Volume'].rolling(window=20).mean().iloc[-1]
      vol_spike = df['Volume'].iloc[-1] > (vol_avg * 2)

      turnover = df['Close'].iloc[-1] * df['Volume'].iloc[-1]
      is_liquid = turnover > 5_000_000_000
        
      return prev_breakout and curr_breakout and vol_spike and is_liquid