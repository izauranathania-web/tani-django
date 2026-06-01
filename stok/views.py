from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import datetime

from .models import Stok, MutasiStok


@login_required
def list_stok(request):
    kategori = request.GET.get('kategori', '')
    qs = Stok.objects.all()
    if kategori:
        qs = qs.filter(kategori=kategori)
    return render(request, 'stok/list.html', {'stok_list': qs, 'kategori': kategori})


@login_required
def tambah_stok(request):
    if request.method == 'POST':
        nama      = request.POST.get('nama', '').strip()
        kategori  = request.POST.get('kategori', '')
        satuan    = request.POST.get('satuan', '').strip()
        harga     = float(request.POST.get('harga_beli', 0) or 0)
        keterangan = request.POST.get('keterangan', '').strip()
        if not nama or not kategori or not satuan:
            messages.error(request, 'Nama, kategori, dan satuan wajib diisi.')
        else:
            Stok.objects.create(nama=nama, kategori=kategori, satuan=satuan,
                                harga_beli=harga, keterangan=keterangan)
            messages.success(request, f'Stok "{nama}" ditambahkan.')
            return redirect('list_stok')
    return render(request, 'stok/form.html', {'judul': 'Tambah Stok Baru'})


@login_required
def edit_stok(request, pk):
    stok = get_object_or_404(Stok, pk=pk)
    if request.method == 'POST':
        stok.nama      = request.POST.get('nama', stok.nama).strip()
        stok.kategori  = request.POST.get('kategori', stok.kategori)
        stok.satuan    = request.POST.get('satuan', stok.satuan).strip()
        stok.harga_beli = float(request.POST.get('harga_beli', stok.harga_beli) or 0)
        stok.keterangan = request.POST.get('keterangan', '').strip()
        stok.save()
        messages.success(request, 'Data stok diperbarui.')
        return redirect('list_stok')
    return render(request, 'stok/form.html', {'judul': 'Edit Stok', 'stok': stok})


@login_required
def hapus_stok(request, pk):
    stok = get_object_or_404(Stok, pk=pk)
    if request.method == 'POST':
        stok.delete()
        messages.success(request, 'Stok dihapus.')
    return redirect('list_stok')


@login_required
def mutasi_stok(request, pk):
    stok = get_object_or_404(Stok, pk=pk)
    if request.method == 'POST':
        jenis    = request.POST.get('jenis', '')
        jumlah   = float(request.POST.get('jumlah', 0) or 0)
        harga    = float(request.POST.get('harga_sat', stok.harga_beli) or 0)
        tanggal  = request.POST.get('tanggal') or str(datetime.date.today())
        ket      = request.POST.get('keterangan', '').strip()
        if jumlah <= 0:
            messages.error(request, 'Jumlah harus lebih dari 0.')
        else:
            with transaction.atomic():
                MutasiStok.objects.create(
                    stok=stok, jenis=jenis, jumlah=jumlah,
                    harga_sat=harga, tanggal=tanggal, keterangan=ket
                )
                if jenis == 'masuk':
                    stok.stok += jumlah
                else:
                    stok.stok = max(0, stok.stok - jumlah)
                stok.save()
            messages.success(request, f'Mutasi stok "{stok.nama}" berhasil dicatat.')
            return redirect('list_stok')
    riwayat = stok.mutasi.order_by('-tanggal', '-id')[:20]
    return render(request, 'stok/mutasi.html', {'stok': stok, 'riwayat': riwayat})
