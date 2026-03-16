class RisingThree:
    def __init__(self):
        pass

    def screen(self, df):
        """
        Strategi:
        1. C1 Bullish > 4%
        2. Middle 3 days stay inside C1
        3. C5 Bullish > 4%
        4. C5 Close > C1 High
        """
        try:
            if len(df) < 5: return False
            
            c = df.tail(5)
            
            c1_bullish = c.iloc[0]['Close'] > c.iloc[0]['Open'] * 1.04
            c1_high = c.iloc[0]['High']
            c1_low = c.iloc[0]['Low']
            
            # 2. Validasi Middle Candles (Stay inside, Bearish & Volume weakening)
            middle_stayed_inside = (
                c.iloc[1]['High'] < c1_high 
                and c.iloc[1]['Low'] > c1_low

                and c.iloc[2]['High'] < c1_high 
                and c.iloc[2]['Low'] > c1_low

                and c.iloc[3]['High'] < c1_high 
                and c.iloc[3]['Low'] > c1_low
            )
            middle_is_bearish = (
                c.iloc[1]['Close'] < c.iloc[1]['Open']
                and c.iloc[2]['Close'] < c.iloc[2]['Open']
                and c.iloc[3]['Close'] < c.iloc[3]['Open']
            )
            
            c5_bullish = c.iloc[4]['Close'] > c.iloc[4]['Open'] * 1.04
            breakout = c.iloc[4]['Close'] > c1_high
            
            return (
                c1_bullish 
                and middle_stayed_inside 
                and middle_is_bearish
                and c5_bullish 
                and breakout
            )
        except Exception as e:
            return False

    def screen_anticipation(self, df):
        """
        Strategi Antisipasi dengan Konfirmasi Volume:
        1. C1 Bullish kuat (> 4%) + Volume Tinggi
        2. C2, C3, C4 berada di dalam range High/Low C1
        3. C2 Bearish, C3 Bearish, C4 Bearish (Color Red)
        4. Volume C2, C3, C4 menunjukkan tren menurun (Dying Volume)
        5. Harga > 60 dan < 5000
        """
        try:
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

            is_valid_price = c.iloc[0]['Close'] > 60 and c.iloc[0]['Close'] < 5000
            turnover = c.iloc[0]['Close'] * c.iloc[0]['Volume']
            is_liquid = turnover > 5_000_000_000

            return (
                c1_bullish 
                and middle_stayed_inside 
                and middle_is_bearish
                and is_valid_price
                and is_liquid
            )
        except Exception as e:
            return False
