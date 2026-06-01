from django.urls import path
from . import views

urlpatterns = [
    path('laba-rugi/',            views.laba_rugi,          name='laba_rugi'),
    path('pengeluaran/',          views.list_pengeluaran,   name='list_pengeluaran'),
    path('pengeluaran/tambah/',   views.tambah_pengeluaran, name='tambah_pengeluaran'),
    path('pengeluaran/<int:pk>/hapus/', views.hapus_pengeluaran, name='hapus_pengeluaran'),
]
