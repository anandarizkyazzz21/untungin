# UNTUNGIN - Aplikasi Perhitungan Untung/Rugi Pedagang

Aplikasi desktop untuk menghitung untung/rugi pedagang menggunakan Python dan Tkinter.

## Struktur Proyek

```
untungin/
├── main.py              # Entry point aplikasi
├── app/
│   ├── controller.py    # Logika bisnis dan kalkulasi
│   ├── model.py         # Pengelolaan data CSV
│   └── view.py          # Antarmuka pengguna Tkinter
├── data/
│   └── transaksi.csv    # File penyimpanan data transaksi
└── test_untungin.py     # Script testing
```

## Fitur

- **Dashboard**: Form input untuk menghitung untung/rugi produk
- **Riwayat**: Tabel transaksi dengan statistik total untung/rugi
- **Ekspor CSV**: Ekspor data transaksi ke file CSV
- **Hapus Semua**: Hapus semua data transaksi

## Cara Menjalankan

1. Pastikan Python 3.x terinstall
2. Install dependencies jika diperlukan (tkinter biasanya sudah included)
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## Logika Bisnis

- **Kalkulasi**: total_modal = modal * qty, total_jual = jual * qty, untung_rugi = total_jual - total_modal, margin_pct = (untung_rugi / total_modal) * 100
- **Status**: UNTUNG (untung_rugi > 0), RUGI (untung_rugi < 0), BEP (untung_rugi = 0)
- **Validasi**: Input harus angka positif > 0

## Data Schema

CSV columns: id, nama_produk, kategori, harga_modal, harga_jual, jumlah, total_modal, total_jual, untung_rugi, margin_pct, tanggal

## Testing

Jalankan test script:
```bash
python test_untungin.py
```