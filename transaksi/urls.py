from django.urls import path
from . import views

urlpatterns = [
    path('pembelian/',               views.list_pembelian,   name='list_pembelian'),
    path('pembelian/tambah/',        views.tambah_pembelian, name='tambah_pembelian'),
    path('pembelian/<int:pk>/hapus/',views.hapus_pembelian,  name='hapus_pembelian'),
    path('penjualan/',               views.list_penjualan,   name='list_penjualan'),
    path('penjualan/tambah/',        views.tambah_penjualan, name='tambah_penjualan'),
    path('penjualan/<int:pk>/hapus/',views.hapus_penjualan,  name='hapus_penjualan'),
]
