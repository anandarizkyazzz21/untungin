# Advanced Profit Calculator - Kalkulator Untung Rugi Bisnis

Aplikasi kalkulator untung rugi yang komprehensif untuk pemilik bisnis dengan interface modern dan fitur analisis bisnis yang lengkap.

## ✨ Fitur Utama

### 📊 Dashboard Real-time
- **8 KPI Utama**: Modal, Penjualan, Pengeluaran, Keuntungan Kotor, ROI, Total Produk, Stok Rendah, dan Tren Penjualan
- **Visualisasi Data**: Chart penjualan bulanan dan analisis tren
- **Alert Otomatis**: Notifikasi untuk produk stok rendah

### 🏪 Manajemen Produk
- **CRUD Lengkap**: Tambah, edit, hapus, dan lihat produk
- **Kategori Produk**: Kelompokkan produk berdasarkan kategori
- **Stok Management**: Tracking stok otomatis dengan alert
- **Harga Dinamis**: Harga beli dan jual terpisah

### 🛒 Sistem POS (Point of Sale)
- **Pencatatan Penjualan**: Catat penjualan dengan detail produk dan jumlah
- **Kalkulasi Otomatis**: Hitung total penjualan dan keuntungan real-time
- **Riwayat Penjualan**: Lihat semua transaksi penjualan

### 💸 Tracking Pengeluaran
- **Kategori Pengeluaran**: Kelompokkan pengeluaran (Operational, Marketing, dll)
- **Detail Lengkap**: Deskripsi dan tanggal pengeluaran
- **Analisis Biaya**: Pantau pengeluaran berdasarkan kategori

### 📈 Laporan & Analisis
- **Laporan Komprehensif**: Export ke Excel dengan semua data
- **Analisis Tren**: Lihat performa penjualan dari waktu ke waktu
- **Top Products**: Identifikasi produk terlaris
- **ROI Calculation**: Hitung return on investment

### 🎨 Interface Modern
- **UI/UX Modern**: Desain profesional dengan tema gelap
- **Responsive**: Interface yang mudah digunakan
- **Real-time Updates**: Data terupdate otomatis

## 🚀 Instalasi & Setup

### Persyaratan Sistem
- Python 3.8+
- Tkinter (sudah termasuk dalam Python)
- Dependencies: pandas, openpyxl, matplotlib

### Instalasi Dependencies
```bash
pip install pandas openpyxl matplotlib
```

### Menjalankan Aplikasi
```bash
python advanced_profit_calculator.py
```

## 📖 Cara Penggunaan

### 1. Setup Awal
1. Jalankan aplikasi
2. Aplikasi akan membuat database otomatis
3. Masukkan modal awal di tab "Modal"

### 2. Menambah Produk
1. Buka tab "Produk"
2. Klik "Tambah Produk"
3. Isi detail: nama, kategori, harga beli, harga jual, stok awal, stok minimum
4. Klik "Simpan"

### 3. Mencatat Penjualan
1. Buka tab "Penjualan"
2. Pilih produk dari dropdown
3. Masukkan jumlah terjual
4. Klik "Catat Penjualan"

### 4. Mencatat Pengeluaran
1. Buka tab "Pengeluaran"
2. Pilih kategori
3. Masukkan deskripsi dan jumlah
4. Klik "Tambah Pengeluaran"

### 5. Melihat Laporan
1. Buka tab "Laporan"
2. Klik "Export Excel" untuk laporan lengkap
3. Lihat analisis di dashboard

## 📊 Struktur Database

### Tabel Utama
- `produk`: Data produk (nama, kategori, harga, stok)
- `penjualan`: Riwayat penjualan
- `pengeluaran`: Riwayat pengeluaran
- `modal`: Data modal/investasi

### File Database
- `advanced_profit.db`: SQLite database utama
- Backup otomatis saat export

## 🔧 Troubleshooting

### Masalah Umum
1. **Import Error**: Pastikan semua dependencies terinstall
   ```bash
   pip install pandas openpyxl matplotlib
   ```

2. **UI Tidak Muncul**: Pastikan Tkinter terinstall (biasanya sudah ada di Python)

3. **Database Error**: Hapus file `advanced_profit.db` dan jalankan ulang

### Testing
Jalankan script test untuk memverifikasi fungsionalitas:
```bash
python test_advanced_calculator.py
```

## 📈 Contoh Penggunaan

### Skenario Toko Baju
1. **Setup Produk**:
   - Kaos: Harga beli Rp 50.000, jual Rp 80.000, stok 20
   - Celana: Harga beli Rp 100.000, jual Rp 150.000, stok 15

2. **Penjualan**:
   - Jual 5 kaos: Keuntungan Rp 150.000
   - Jual 3 celana: Keuntungan Rp 150.000

3. **Pengeluaran**:
   - Sewa toko: Rp 2.000.000/bulan
   - Listrik: Rp 500.000/bulan

4. **ROI**: Hitung pengembalian investasi bulanan

## 🎯 Target Pengguna

- Pemilik UMKM/Toko
- Pengusaha retail
- Manajer bisnis kecil
- Freelancer yang ingin tracking keuangan

## 🔄 Update & Maintenance

- Database backup otomatis saat export
- Data persistent di SQLite
- Update real-time di dashboard

## 📞 Support

Untuk pertanyaan atau masalah:
1. Jalankan `python test_advanced_calculator.py` untuk diagnosis
2. Periksa log error di terminal
3. Pastikan semua dependencies terinstall

---

**Versi**: 2.0 Advanced
**Bahasa**: Bahasa Indonesia
**Framework**: Tkinter + SQLite
**Dependencies**: pandas, openpyxl, matplotlib