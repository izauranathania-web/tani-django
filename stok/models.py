from django.db import models


class KategoriStok(models.TextChoices):
    BIBIT  = 'bibit',  'Bibit'
    PUPUK  = 'pupuk',  'Pupuk'
    LAINNYA = 'lainnya', 'Lainnya'


class Stok(models.Model):
    nama      = models.CharField(max_length=150)
    kategori  = models.CharField(max_length=20, choices=KategoriStok.choices)
    satuan    = models.CharField(max_length=30, help_text='contoh: kg, liter, batang, karung')
    stok      = models.FloatField(default=0)
    harga_beli = models.FloatField(default=0, help_text='Harga beli per satuan (Rp)')
    keterangan = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['kategori', 'nama']

    def __str__(self):
        return f"{self.nama} ({self.get_kategori_display()})"


class MutasiStok(models.Model):
    JENIS_CHOICES = [('masuk', 'Masuk'), ('keluar', 'Keluar')]

    stok       = models.ForeignKey(Stok, on_delete=models.CASCADE, related_name='mutasi')
    jenis      = models.CharField(max_length=10, choices=JENIS_CHOICES)
    jumlah     = models.FloatField()
    harga_sat  = models.FloatField(default=0, help_text='Harga per satuan saat mutasi')
    tanggal    = models.DateField()
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal', '-id']

    def total_nilai(self):
        return self.jumlah * self.harga_sat
