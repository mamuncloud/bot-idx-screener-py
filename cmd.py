import yfinance as yf
import re

from screener.breakout_20_days import Breakout20Days
from screener.trend_following import TrendFollowing
from screener.macd_cross import MacdCross
from screener.rising_three import RisingThree
from screener.bb_breakout import BbBreakout

from notification.discord_bot import DiscordNotifier

class Command:
    def __init__(self, ticker_path="ticker.csv"):
        self.ticker_path = ticker_path
        self.symbols = []
        self.notifier = DiscordNotifier()
        
        # Initialize strategy classes
        self.breakout_20_days = Breakout20Days()
        self.trend_following = TrendFollowing()
        self.macd_cross = MacdCross()
        self.rising_three = RisingThree()
        self.bb_breakout = BbBreakout()
        
        try:
            with open(self.ticker_path, 'r') as f:
                content = f.read()
                self.symbols = re.findall(r"[\w\.]+", content)
                
            if not self.symbols:
                raise ValueError("No tickers found in the CSV file.")
            
            self.symbols = [s.strip("',\" ") for s in self.symbols]
            self.symbols = [s if s.endswith(".JK") else f"{s}.JK" for s in self.symbols]
            
            print(f"Loaded {len(self.symbols)} tickers successfully.")
            
        except FileNotFoundError:
            print(f"Error: {self.ticker_path} not found.")
        except Exception as e:
            print(f"Error loading tickers: {e}")

    def run(self, strategy):
        if not self.symbols:
            print("No symbols to screen.")
            return

        print(f"\n--- Starting Screening: {strategy} ---")
        
        all_data = yf.download(
            self.symbols, 
            period="300d", 
            interval="1d", 
            group_by='ticker', 
            progress=True
        )
        
        matches = []
        
        for symbol in self.symbols:
            try:
                if len(self.symbols) > 1:
                    if symbol not in all_data.columns.levels[0]:
                        continue
                    df = all_data[symbol].dropna()
                else:
                    df = all_data.dropna()
                
                if df.empty or len(df) < 5: 
                    continue

                latest_close = df['Close'].iloc[-1]
                latest_volume = df['Volume'].iloc[-1]
                latest_value = latest_close * latest_volume
                
                found = False
                if strategy == "macd_cross_up":
                    found = self.macd_cross.screen(df)
                elif strategy == "rising_three":
                    found = self.rising_three.screen(df)
                elif strategy == "trend_following":
                    found = self.trend_following.screen(df)
                elif strategy == "breakout_20_days":
                    found = self.breakout_20_days.screen(df)
                elif strategy == "bb_breakout_volume":
                    found = self.bb_breakout.screen(df)
                elif strategy == "before_rising_three_method_with_volume":
                    found = self.rising_three.screen_anticipation(df)
                
                if found:
                    log = f" [MATCH] {symbol} | Price: {latest_close:,.0f}\t\t"
                    log += f"| Vol: {latest_volume:,.0f}\t\t"
                    log += f"| Val: {latest_value:,.0f}\t\t"
                    print(log)
                    
                    matches.append({
                        "symbol": symbol,
                        "price": latest_close,
                        "volume": latest_volume,
                        "value": latest_value
                    })
                    
            except Exception as e:
                print(f" Error processing {symbol}: {e}")
                continue

        # --- Bagian Pengiriman Notifikasi ---
        print("\n")
        if self.notifier:
            if matches:
                matches.sort(key=lambda x: x['value'], reverse=True)
                matches = matches[:3]
            self.notifier.send_notification(strategy, matches)
        

        print(f"\nFINISHED: Found {len(matches)} stocks.")