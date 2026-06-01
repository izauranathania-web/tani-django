from django.db import models
from stok.models import Stok


class Pembelian(models.Model):
    tanggal    = models.DateField()
    no_faktur  = models.CharField(max_length=60, unique=True)
    supplier   = models.CharField(max_length=150, blank=True, default='')
    total      = models.FloatField(default=0)
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal', '-id']

    def __str__(self):
        return f"Pembelian {self.no_faktur} - {self.tanggal}"


class ItemPembelian(models.Model):
    pembelian  = models.ForeignKey(Pembelian, on_delete=models.CASCADE, related_name='items')
    stok       = models.ForeignKey(Stok, on_delete=models.PROTECT, null=True, blank=True)
    nama_item  = models.CharField(max_length=150)
    jumlah     = models.FloatField()
    satuan     = models.CharField(max_length=30)
    harga_sat  = models.FloatField()

    def subtotal(self):
        return self.jumlah * self.harga_sat


class Penjualan(models.Model):
    tanggal    = models.DateField()
    no_faktur  = models.CharField(max_length=60, unique=True)
    pembeli    = models.CharField(max_length=150, blank=True, default='')
    total      = models.FloatField(default=0)
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal', '-id']

    def __str__(self):
        return f"Penjualan {self.no_faktur} - {self.tanggal}"


class ItemPenjualan(models.Model):
    penjualan  = models.ForeignKey(Penjualan, on_delete=models.CASCADE, related_name='items')
    stok       = models.ForeignKey(Stok, on_delete=models.PROTECT, null=True, blank=True)
    nama_item  = models.CharField(max_length=150)
    jumlah     = models.FloatField()
    satuan     = models.CharField(max_length=30)
    harga_sat  = models.FloatField()
    harga_beli = models.FloatField(default=0, help_text='HPP saat dijual')

    def subtotal(self):
        return self.jumlah * self.harga_sat

    def hpp(self):
        return self.jumlah * self.harga_beli
