import requests
import json
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

class DiscordNotifier:
    def __init__(self):
      self.webhook_config = {
        "trend_following": os.getenv("WEBHOOK_TREND_FOLLOWING"),
        "macd_cross_up": os.getenv("WEBHOOK_MACD_CROSS"),
        "rising_three": os.getenv("WEBHOOK_RISING_THREE"),
        "breakout_20_days": os.getenv("WEBHOOK_BREAKOUT_20_DAYS"),
        "bb_breakout_volume": os.getenv("WEBHOOK_BB_BREAKOUT_VOLUME")
      }

    def send_notification(self, strategy, matches):
      webhook_url = self.webhook_config.get(strategy)
      if not webhook_url: return

      wib = pytz.timezone('Asia/Jakarta')
      now = datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S")
      url_repo = "https://github.com/mamuncloud/bot-idx-screener-py"
        
      # Tentukan warna (Decimal) & Icon berdasarkan strategi
      if strategy == "macd_cross_up":
          color = 3066993 # Cyan/Green
          icon = "📈"
      elif strategy == "rising_three":
          color = 15158332 # Gold
          icon = "🔥"
      elif strategy == "trend_following":
          color = 3447003 # Royal Blue
          icon = "🚀"
      elif strategy == "breakout_20_days":
          color = 10181046 # Purple
          icon = "⚡"
      elif strategy == "bb_breakout_volume":
          color = 16711680 # Red
          icon = "⚡"
      else:
          color = 15158332 # Default Gold
          icon = "🔍"

      if not matches:
        embed = {
          "title": f"{icon} IDX Screener: {strategy.upper()}",
          "description": "Tidak ada saham yang memenuhi kriteria saat ini.",
          "color": 15158332, # Kuning/Oranye jika kosong
          "footer": {"text": f"Executed at {now}"}
        }
      else:
        def format_number(n):
            if n >= 1_000_000_000_000:
                return f"{n / 1_000_000_000_000:.2f}T"
            elif n >= 1_000_000_000:
                return f"{n / 1_000_000_000:.2f}B"
            elif n >= 1_000_000:
                return f"{n / 1_000_000:.2f}M"
            else:
                return f"{n:,.0f}"

        ticker_lines = [
            f"**{m['symbol']}** | Price: `{m['price']:,.0f}` | Vol: `{format_number(m['volume'])}` | Val: `{format_number(m['value'])}`"
            for m in matches
        ]

        ticker_list = ""
        for line in ticker_lines:
            if len(ticker_list) + len(line) + 15 > 1024: # Buffer for "...and more"
                ticker_list += "\n*...and more*"
                break
            ticker_list += line + "\n"
        
        embed = {
          "title": f"{icon} New Signal: {strategy.upper()}",
          "description": f"Ditemukan **{len(matches)}** saham yang masuk kriteria.",
          "color": color,
          "fields": [
            {
              "name": "✅ Tickers Detected",
              "value": ticker_list.strip(),
              "inline": False
            },
            {
              "name": "🛠️ System Info",
              "value": f"[GitHub Repository]({url_repo})",
              "inline": False
            }
          ],
          "footer": {
            "text": f"IDX Trading Bot • {now}",
            "icon_url": "https://cdn-icons-png.flaticon.com/512/2502/2502160.png"
          }
        }

        # Mengirim sebagai 'embeds' bukan 'content' biasa
        payload = {"embeds": [embed]}
        
        try:
          response = requests.post(
            webhook_url, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
          )
          response.raise_for_status()
        except Exception as e:
          print(f"❌ Gagal mengirim notifikasi: {e}")