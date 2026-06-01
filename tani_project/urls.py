from django.urls import path, include

urlpatterns = [
    path('',          include('accounts.urls')),
    path('stok/',     include('stok.urls')),
    path('transaksi/',include('transaksi.urls')),
    path('pegawai/',  include('pegawai.urls')),
    path('laporan/',  include('laporan.urls')),
]
