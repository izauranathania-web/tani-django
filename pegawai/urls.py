from django.urls import path
from . import views

urlpatterns = [
    path('',               views.list_pegawai,   name='list_pegawai'),
    path('tambah/',        views.tambah_pegawai, name='tambah_pegawai'),
    path('<int:pk>/edit/', views.edit_pegawai,   name='edit_pegawai'),
    path('<int:pk>/hapus/',views.hapus_pegawai,  name='hapus_pegawai'),
    path('penggajian/',    views.penggajian,     name='penggajian'),
    path('penggajian/bayar/', views.bayar_gaji,  name='bayar_gaji'),
]
