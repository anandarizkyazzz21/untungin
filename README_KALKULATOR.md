# 💰 **Kalkulator Untung Rugi Bisnis**

Aplikasi sederhana untuk menghitung keuntungan atau kerugian bisnis apapun menggunakan Tkinter GUI.

## ✨ **Fitur Utama**

### 📊 **Dashboard**
- **Total Modal**: Jumlah semua modal yang diinvestasikan
- **Total Pengeluaran**: Semua biaya operasional
- **Total Pemasukan**: Semua pendapatan dari penjualan
- **Total Biaya**: Modal + Pengeluaran
- **Keuntungan/Rugi**: Pemasukan - Total Biaya
- **Status**: UNTUNG 🎉 / RUGI 😞 / BALANCE ⚖️

### ➕ **Input Data**
- **Modal**: Input modal awal atau tambahan
- **Pengeluaran**: Biaya operasional (gaji, sewa, listrik, dll)
- **Pemasukan**: Pendapatan dari penjualan

### 📋 **History**
- **Modal**: Riwayat semua input modal
- **Pengeluaran**: Riwayat semua pengeluaran
- **Pemasukan**: Riwayat semua pemasukan

### 📊 **Export Excel**
- **4 Sheet**: Summary, Modal, Pengeluaran, Pemasukan
- **Laporan Lengkap**: Semua data keuangan dalam format Excel

---

## 🚀 **Cara Menggunakan**

### **1. Persiapan**
```bash
# Install dependencies (jika belum)
pip install pandas openpyxl

# Jalankan aplikasi
python run_kalkulator.py
```

### **2. Input Modal Awal**
1. Pilih tab **"➕ Input Data"**
2. **Jenis**: Pilih `modal`
3. **Tanggal**: Pilih tanggal input
4. **Deskripsi**: "Modal awal usaha" atau "Tambahan modal"
5. **Jumlah**: Masukkan jumlah modal (contoh: 5000000)
6. Klik **"💾 Simpan"**

### **3. Input Pengeluaran**
1. **Jenis**: Pilih `pengeluaran`
2. **Kategori**: Pilih dari dropdown:
   - Gaji, Sewa, Listrik, Transport
   - Bahan Baku, Pemasaran, Lainnya
3. **Deskripsi**: Detail pengeluaran (opsional)
4. **Jumlah**: Masukkan jumlah pengeluaran
5. Klik **"💾 Simpan"**

### **4. Input Pemasukan**
1. **Jenis**: Pilih `pemasukan`
2. **Kategori**: Pilih dari dropdown:
   - Penjualan, Jasa, Komisi, Lainnya
3. **Deskripsi**: Detail pemasukan (opsional)
4. **Jumlah**: Masukkan jumlah pemasukan
5. Klik **"💾 Simpan"**

### **5. Monitor Dashboard**
- Lihat **tab "📊 Dashboard"** untuk ringkasan real-time
- **Keuntungan/Rugi** otomatis terhitung
- **Status** menunjukkan kondisi bisnis

### **6. Lihat History**
- Tab **"📋 History"** memiliki 3 sub-tab:
  - **💰 Modal**: Riwayat semua modal
  - **💸 Pengeluaran**: Riwayat semua biaya
  - **💵 Pemasukan**: Riwayat semua pendapatan

### **7. Export Laporan**
- Klik **"📊 Export Excel"** di Dashboard
- Pilih lokasi penyimpanan file
- File Excel akan berisi 4 sheet lengkap

---

## 📊 **Contoh Penggunaan**

### **Bisnis Warung Makan:**
```
Modal Awal: Rp 10,000,000
Pengeluaran:
- Sewa tempat: Rp 2,000,000/bulan
- Bahan baku: Rp 3,000,000/bulan
- Gaji karyawan: Rp 1,500,000/bulan
- Listrik: Rp 500,000/bulan

Pemasukan:
- Penjualan harian: Rp 1,500,000/hari
- Total pemasukan bulan: Rp 45,000,000

Perhitungan:
Total Biaya = 10,000,000 + (2M + 3M + 1.5M + 0.5M) = 17,000,000
Keuntungan = 45,000,000 - 17,000,000 = 28,000,000
Status: UNTUNG 🎉
```

### **Bisnis Online Shop:**
```
Modal: Rp 5,000,000 (stok awal)
Pengeluaran:
- Iklan Facebook: Rp 1,000,000
- Ongkir: Rp 500,000
- Biaya marketplace: Rp 300,000

Pemasukan:
- Penjualan produk: Rp 8,000,000

Keuntungan = 8,000,000 - (5,000,000 + 1,000,000 + 500,000 + 300,000)
           = 8,000,000 - 6,800,000 = 1,200,000
Status: UNTUNG 🎉
```

---

## 🎨 **Interface**

### **Tab Dashboard**
```
📊 Dashboard
├── Total Modal: Rp 10,000,000
├── Total Pengeluaran: Rp 5,000,000
├── Total Pemasukan: Rp 15,000,000
├── Total Biaya: Rp 15,000,000
├── Keuntungan/Rugi: Rp 0
└── Status: BALANCE ⚖️
```

### **Tab Input Data**
```
➕ Input Data
├── Tanggal: [YYYY-MM-DD]
├── Jenis: [modal ▼] [pengeluaran ▼] [pemasukan ▼]
├── Kategori: [dropdown - muncul jika pilih pengeluaran/pemasukan]
├── Deskripsi: [text input]
├── Jumlah: [number input]
└── [💾 Simpan] [🗑️ Clear Form]
```

### **Tab History**
```
📋 History
├── 💰 Modal
│   ├── ID | Tanggal | Deskripsi | Jumlah
│   └── [Data modal yang diinput]
├── 💸 Pengeluaran
│   ├── ID | Tanggal | Kategori:Deskripsi | Jumlah
│   └── [Data pengeluaran]
└── 💵 Pemasukan
    ├── ID | Tanggal | Kategori:Deskripsi | Jumlah
    └── [Data pemasukan]
```

---

## 📁 **File Database**

File `profit_calculator.db` menyimpan:
- **Tabel modal**: id, tanggal, deskripsi, jumlah
- **Tabel pengeluaran**: id, tanggal, kategori, deskripsi, jumlah
- **Tabel pemasukan**: id, tanggal, kategori, deskripsi, jumlah

---

## 🔧 **Fitur Tambahan**

### **Reset Data**
- Tombol **"🗑️ Reset Semua Data"** di Dashboard
- **Konfirmasi**: Pastikan sebelum menghapus semua data
- **Warning**: Tindakan tidak dapat dibatalkan

### **Real-time Update**
- Semua perhitungan otomatis update
- Status berubah warna: Hijau (Untung), Merah (Rugi), Biru (Balance)

### **Data Validation**
- Tanggal wajib diisi
- Jumlah harus angka positif
- Kategori wajib dipilih untuk pengeluaran/pemasukan

---

## 🚀 **Menjalankan Aplikasi**

### **Opsi 1: Launcher (Recommended)**
```bash
python run_kalkulator.py
```

### **Opsi 2: Direct Run**
```bash
python kalkulator_untung_rugi.py
```

### **Testing**
```bash
python test_kalkulator.py
```

---

## 📋 **File Yang Dibuat**

```
D:\rizkya_py\testpy\
├── kalkulator_untung_rugi.py    ← Aplikasi utama
├── run_kalkulator.py            ← Launcher script
├── test_kalkulator.py           ← Testing script
├── profit_calculator.db         ← Database SQLite
└── README_KALKULATOR.md         ← Dokumentasi ini
```

---

## 💡 **Tips Penggunaan**

1. **Input Berkala**: Masukkan data setiap hari/minggu
2. **Backup Data**: Export Excel secara berkala
3. **Kategori Konsisten**: Gunakan kategori yang sama untuk tracking
4. **Monitor Status**: Perhatikan status UNTUNG/RUGI
5. **Analisis**: Gunakan Excel untuk analisis mendalam

---

**🎉 Aplikasi Kalkulator Untung Rugi siap membantu bisnis Anda!**