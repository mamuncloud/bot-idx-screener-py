
# IDX Stock Screener with Discord Notification 🚀

Bot screener saham otomatis untuk Bursa Efek Indonesia (IDX) yang menggunakan analisis teknikal (MACD & Candlestick Pattern) dan mengirimkan notifikasi secara real-time ke channel Discord yang berbeda berdasarkan strategi.

## ✨ Fitur Utama
- **Multi-Strategy**: Mendukung `MACD Golden Cross` dengan Volume Spike dan pattern `Rising Three Methods`.
- **Multi-Channel Discord**: Notifikasi dikirim ke channel spesifik sesuai strategi yang dipilih.
- **Batch Processing**: Menggunakan download data massal via `yfinance` untuk performa maksimal.
- **Security**: Integrasi file `.env` untuk menyembunyikan Webhook URL dan path sensitif.
- **Flexible Ticker**: Mampu membaca format CSV list ticker baik dalam bentuk kolom maupun baris.


## Direktori

```
.
├── README.md
├── cmd.py
├── main.py
├── notification
│   └── discord_bot.py
├── requirements.txt
├── screener
│   └── screener.py
└── ticker.csv
```