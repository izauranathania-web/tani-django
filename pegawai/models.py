from django.db import models


class Pegawai(models.Model):
    STATUS_CHOICES = [('aktif', 'Aktif'), ('nonaktif', 'Nonaktif')]

    nama        = models.CharField(max_length=150)
    jabatan     = models.CharField(max_length=100, blank=True, default='')
    no_hp       = models.CharField(max_length=20, blank=True, default='')
    alamat      = models.TextField(blank=True, default='')
    gaji_pokok  = models.FloatField(default=0)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aktif')
    tanggal_masuk = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['nama']

    def __str__(self):
        return self.nama


class Penggajian(models.Model):
    pegawai     = models.ForeignKey(Pegawai, on_delete=models.CASCADE, related_name='penggajian')
    periode     = models.CharField(max_length=7, help_text='Format: YYYY-MM')
    gaji_pokok  = models.FloatField()
    tunjangan   = models.FloatField(default=0)
    potongan    = models.FloatField(default=0)
    total_gaji  = models.FloatField()
    keterangan  = models.TextField(blank=True, default='')
    tanggal_bayar = models.DateField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-periode', '-id']
        unique_together = ['pegawai', 'periode']

    def __str__(self):
        return f"{self.pegawai.nama} - {self.periode}"
