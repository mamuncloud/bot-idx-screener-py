
# 🚀 IDX Stock Screener with Discord Notification

Bot screener saham otomatis untuk Bursa Efek Indonesia (IDX) yang menggunakan berbagai strategi analisis teknikal. Hasil screening dikirimkan secara real-time ke channel Discord yang berbeda berdasarkan strategi, lengkap dengan detail harga, volume, value transaksi, dan link chart.

## ✨ Fitur Utama
- **Multi-Strategy**: Mendukung 6 strategi teknikal (MACD, Bollinger Bands, Breakout 20 Hari, Trend Following, Rising Three, dan Before Rising Three).
- **Rich Notifications**: Notifikasi Discord yang informatif mencakup:
    - 💰 Harga Close terakhir.
    - 📊 Volume & Value transaksi (Turnover) yang sudah diformat (T/B/M).
    - 📈 Link langsung ke Chartbit Stockbit untuk setiap emiten.
- **Multi-Channel Discord**: Setiap strategi dapat dikirim ke Webhook yang berbeda.
- **Automated**: Terintegrasi dengan GitHub Actions untuk screening otomatis sesuai jam bursa.
- **Batch Processing**: Mengambil data massal via `yfinance` untuk kecepatan maksimal.

## 🛠️ Strategi Screening
Berikut adalah daftar strategi yang diimplementasikan di `screener/screener.py`:

| Strategi | Deskripsi |
|----------|-----------|
| `macd_cross_up` | MACD Golden Cross dengan konfirmasi Volume Spike (2x rata-rata). |
| `rising_three` | Pola candlestick trend continuation *Rising Three Methods* (C5 Breakout). |
| `before_rising_three_method_with_volume` | **Antisipasi** pola Rising Three (C1 Bullish, C2-C4 Bearish di dalam range C1) dengan "Dying Volume". |
| `trend_following` | Moving Average bertumpuk (MA20 > MA50 > MA100) dengan Volume Spike. |
| `breakout_20_days` | Harga menembus High 20 hari terakhir dengan Volume Spike. |
| `bb_breakout_volume` | Harga menembus Upper Bollinger Band dengan lonjakan volume & Likuiditas. |

*Filter Likuiditas: Secara default menyaring saham dengan turnover > 5 Miliar.*

## 🚀 Cara Penggunaan

### 1. Setup Environment
Buat file `.env` di root folder dan tambahkan Webhook URL untuk masing-masing strategi:
```env
WEBHOOK_TREND_FOLLOWING=...
WEBHOOK_MACD_CROSS=...
WEBHOOK_RISING_THREE=...
WEBHOOK_BREAKOUT_20_DAYS=...
WEBHOOK_BB_BREAKOUT_VOLUME=...
```
*(Catatan: `before_rising_three_method_with_volume` menggunakan webhook yang sama dengan `rising_three`)*

### 2. Instalasi
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Manual
```bash
# Contoh menjalankan strategi breakout 20 hari
python main.py --strategy breakout_20_days
```

## 📂 Struktur Proyek
```
.
├── .github/workflows/    # File konfigurasi automasi (GitHub Actions)
├── notification/
│   └── discord_bot.py    # Logika pengiriman notifikasi Discord
├── screener/
│   └── screener.py       # Algoritma strategi screening
├── cmd.py                # Logic utama pemrosesan data
├── main.py               # Entry point program
├── ticker.csv            # Daftar ticker IDX
└── requirements.txt      # Library yang dibutuhkan
```

## 🤖 Otomasi (GitHub Actions)
Screener berjalan otomatis setiap hari bursa (Senin-Jumat) dengan jadwal:

1.  **Breakout 20 Days & BB Breakout**: 
    - 10:00, 13:00, 14:00, 15:00 WIB
2.  **MACD, Trend Following, & Rising Three**:
    - 11:00, 15:00 WIB

---
*Disclaimer: Gunakan bot ini sebagai alat bantu. Selalu lakukan analisis fundamental dan teknikal mandiri sebelum mengambil keputusan investasi.*