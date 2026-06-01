# 🌱 TaniApp — Sistem Manajemen Pertanian
Django v1.0 · 2026

## Fitur
- 🔐 Login admin
- 🌿 Stok bibit & pupuk (dengan mutasi masuk/keluar)
- 🛒 Pembelian (update stok otomatis)
- 💰 Penjualan (kurangi stok otomatis)
- 👨‍🌾 Data pegawai & penggajian per periode
- 📤 Pengeluaran operasional
- 📈 Laporan Laba/Rugi otomatis (bisa filter periode)

## Struktur
```
tani_django/
├── manage.py
├── tani_project/         # Settings & routing utama
├── accounts/             # Login, logout, dashboard
├── stok/                 # Stok bibit & pupuk
├── transaksi/            # Pembelian & penjualan
├── pegawai/              # Data pegawai & gaji
├── laporan/              # Laba/rugi & pengeluaran
└── templates/            # Semua HTML template
```

## Cara Menjalankan

### 1. Install Django
```bash
pip install django
```

### 2. Buat database
```bash
python manage.py migrate
```

### 3. Buat akun admin
```bash
python manage.py buat_admin
# Username: admin | Password: admin123
```

### 4. Jalankan server
```bash
python manage.py runserver
```

### 5. Buka browser
```
http://localhost:8000
```

---

## Cara Kerja Laporan Laba/Rugi

```
Pendapatan
  + Total Penjualan
─────────────────────
Dikurangi HPP
  - Harga beli × jumlah terjual
= Laba Kotor

Dikurangi Beban Operasional
  - Gaji pegawai
  - Pengeluaran lain (transport, peralatan, dll)
= LABA / RUGI BERSIH
```

## Tips
- Harga beli stok akan otomatis dipakai sebagai HPP saat penjualan dicatat
- Backup: salin file `tani.db` ke tempat lain secara berkala
- Ganti password admin lewat: `python manage.py changepassword admin`
