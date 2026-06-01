from django.db import models


class PengeluaranLain(models.Model):
    """Pengeluaran operasional selain pembelian stok dan gaji."""
    KATEGORI_CHOICES = [
        ('operasional', 'Operasional'),
        ('peralatan',   'Peralatan'),
        ('transport',   'Transport'),
        ('lainnya',     'Lainnya'),
    ]

    tanggal    = models.DateField()
    kategori   = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='operasional')
    deskripsi  = models.CharField(max_length=200)
    jumlah     = models.FloatField()
    keterangan = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal', '-id']

    def __str__(self):
        return f"{self.deskripsi} - Rp {self.jumlah:,.0f}"
