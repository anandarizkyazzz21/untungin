# 💰 Untungin - Toko Baju Management (Tkinter Version)

Aplikasi manajemen toko baju lengkap dengan interface GUI menggunakan Tkinter. Aplikasi ini dibuat sebagai alternatif dari versi KivyMD yang mengalami masalah layar hitam.

## ✨ Fitur Utama

### 📊 Dashboard
- **Total Modal**: Total harga beli semua produk × stok
- **Total Laba Potensial**: Potensi keuntungan dari semua produk
- **Total Penjualan**: Total pendapatan dari transaksi
- **Total Produk**: Jumlah produk dalam inventory
- **Produk Stok Rendah**: Produk dengan stok < 5 (ditampilkan merah)

### 📦 Inventory Management
- **Lihat Produk**: Tampilan tabel semua produk dengan status stok
- **Tambah Produk**: Form dialog untuk menambah produk baru
- **Edit Produk**: Update informasi produk existing
- **Hapus Produk**: Menghapus produk dari database
- **Warning Stok Rendah**: Produk dengan stok < 5 ditampilkan merah

### 💰 Kasir (Point of Sale)
- **Pilih Produk**: Listbox produk dengan stok tersedia
- **Keranjang Belanja**: Treeview untuk item yang dipilih
- **Input Jumlah**: Field untuk menentukan quantity
- **Checkout**: Proses transaksi dan update stok otomatis

### 📋 History Transaksi
- **Riwayat Penjualan**: Tampilan semua transaksi terbaru
- **Detail Transaksi**: Produk, jumlah, total, dan timestamp
- **Auto Refresh**: Data terupdate otomatis

### 📊 Export Excel
- **3 Sheet Excel**: Summary, Products, Transactions
- **Data Lengkap**: Semua informasi bisnis dalam format Excel
- **Save Dialog**: Pilih lokasi penyimpanan file

## 🗄️ Database SQLite

### Tabel Produk
```sql
CREATE TABLE produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga_beli REAL NOT NULL,
    harga_jual REAL NOT NULL,
    stok INTEGER NOT NULL DEFAULT 0
);
```

### Tabel Transaksi
```sql
CREATE TABLE transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produk_id INTEGER,
    jumlah INTEGER NOT NULL,
    total REAL NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (produk_id) REFERENCES produk (id)
);
```

## 🚀 Instalasi & Menjalankan

### Prerequisites
```bash
pip install pandas openpyxl
```

### Menjalankan Aplikasi
```bash
# Dari direktori project
python untungin_tkinter.py
```

### Testing
```bash
# Jalankan test untuk memverifikasi semua komponen
python test_tkinter.py
```

## 📁 Struktur File

```
D:\rizkya_py\testpy\
├── untungin_tkinter.py    # Aplikasi utama Tkinter
├── test_tkinter.py        # Script testing
├── database.py            # Database operations (opsional)
├── untungin.db           # Database SQLite
├── requirements.txt      # Dependencies
└── README.md             # Dokumentasi ini
```

## 🎯 Cara Penggunaan

### 1. Dashboard
- Lihat ringkasan bisnis secara real-time
- Klik "Export ke Excel" untuk laporan lengkap

### 2. Inventory
- **Tambah Produk**: Klik "➕ Tambah Produk" → isi form → Simpan
- **Edit Produk**: Pilih produk → klik "✏️ Edit Produk" → update → Update
- **Hapus Produk**: Pilih produk → klik "🗑️ Hapus Produk" → konfirmasi

### 3. Kasir
- Pilih produk dari list → masukkan jumlah → "➕ Tambah ke Keranjang"
- Lihat keranjang di sebelah kanan
- Klik "💳 Checkout" untuk proses transaksi

### 4. History
- Lihat semua transaksi yang sudah dilakukan
- Klik "🔄 Refresh History" untuk update data

## 🔧 Troubleshooting

### Masalah: Aplikasi tidak bisa dijalankan
**Solusi**: Pastikan semua dependencies terinstall
```bash
pip install pandas openpyxl
```

### Masalah: Database error
**Solusi**: Hapus file `untungin.db` dan jalankan ulang aplikasi untuk membuat database baru

### Masalah: Stok tidak update
**Solusi**: Pastikan transaksi berhasil diproses di tab Kasir

## 📊 Sample Data

Aplikasi dilengkapi dengan 8 produk sample:
- Kemeja Formal (Rp 150,000)
- Kemeja Kasual (Rp 120,000)
- Kaos Polos (Rp 75,000)
- Jaket Denim (Rp 250,000)
- Blouse Wanita (Rp 95,000)
- Sweater (Rp 180,000)
- Hoodie (Rp 200,000)
- Tank Top (Rp 65,000)

## 🎨 Interface

- **Modern GUI**: Menggunakan ttk untuk tampilan yang clean
- **Color Coding**: Produk stok rendah ditampilkan merah
- **Responsive**: Window dapat di-resize
- **Intuitive**: Tab-based navigation yang mudah digunakan

## 💡 Keunggulan Tkinter Version

✅ **Stable**: Tidak ada masalah layar hitam seperti KivyMD
✅ **Lightweight**: Dependencies minimal
✅ **Native**: Menggunakan komponen OS native
✅ **Compatible**: Bekerja di Windows, Linux, macOS
✅ **Feature Complete**: Semua fitur lengkap seperti yang diminta

---

**Dibuat dengan ❤️ untuk manajemen toko baju yang lebih untung!**