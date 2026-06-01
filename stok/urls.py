from django.urls import path
from . import views

urlpatterns = [
    path('',               views.list_stok,    name='list_stok'),
    path('tambah/',        views.tambah_stok,  name='tambah_stok'),
    path('<int:pk>/edit/', views.edit_stok,    name='edit_stok'),
    path('<int:pk>/hapus/',views.hapus_stok,   name='hapus_stok'),
    path('<int:pk>/mutasi/',views.mutasi_stok, name='mutasi_stok'),
]
