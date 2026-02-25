import yfinance as yf
import re
import pandas as pd

from screener.screener import StockScreener
from notification.discord_bot import DiscordNotifier

class Command:
    def __init__(self, ticker_path="ticker.csv"):
        self.ticker_path = ticker_path
        self.symbols = []
        self.screener = StockScreener()
        self.notifier = DiscordNotifier()
        
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
            period="200d", 
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
                    found = self.screener.is_macd_golden_cross_up(df)
                elif strategy == "rising_three":
                    found = self.screener.is_rising_three_method(df)
                elif strategy == "trend_following":
                    found = self.screener.is_trend_following(df)
                elif strategy == "breakout_20_days":
                    found = self.screener.is_breakout_20_days(df)
                elif strategy == "bb_breakout_volume":
                    found = self.screener.is_bb_breakout_volume(df)
                elif strategy == "before_rising_three_method_with_volume":
                    found = self.screener.is_before_rising_three_method_with_volume(df)
                
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
            self.notifier.send_notification(strategy, matches)
        

        print(f"\nFINISHED: Found {len(matches)} stocks.")