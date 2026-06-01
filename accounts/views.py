from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from stok.models import Stok
from transaksi.models import Pembelian, Penjualan
from pegawai.models import Pegawai, Penggajian
from laporan.models import PengeluaranLain

import datetime


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Username atau password salah.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    today = datetime.date.today()
    bulan_ini = today.strftime('%Y-%m')

    # Stok
    stok_bibit = Stok.objects.filter(kategori='bibit').count()
    stok_pupuk = Stok.objects.filter(kategori='pupuk').count()
    stok_menipis = Stok.objects.filter(stok__lte=10).count()

    # Transaksi bulan ini
    total_pembelian = Pembelian.objects.filter(
        tanggal__year=today.year, tanggal__month=today.month
    ).aggregate(t=Sum('total'))['t'] or 0

    total_penjualan = Penjualan.objects.filter(
        tanggal__year=today.year, tanggal__month=today.month
    ).aggregate(t=Sum('total'))['t'] or 0

    # Gaji bulan ini
    total_gaji = Penggajian.objects.filter(periode=bulan_ini).aggregate(
        t=Sum('total_gaji')
    )['t'] or 0

    # Pengeluaran lain bulan ini
    total_pengeluaran_lain = PengeluaranLain.objects.filter(
        tanggal__year=today.year, tanggal__month=today.month
    ).aggregate(t=Sum('jumlah'))['t'] or 0

    # Laba/Rugi bulan ini (sederhana)
    from transaksi.models import ItemPenjualan
    hpp_bulan = ItemPenjualan.objects.filter(
        penjualan__tanggal__year=today.year,
        penjualan__tanggal__month=today.month
    ).aggregate(t=Sum('harga_beli'))['t'] or 0
    # HPP total = jumlah * harga_beli per item
    from django.db.models import F, FloatField, ExpressionWrapper
    hpp_total = ItemPenjualan.objects.filter(
        penjualan__tanggal__year=today.year,
        penjualan__tanggal__month=today.month
    ).annotate(
        hpp_item=ExpressionWrapper(F('jumlah') * F('harga_beli'), output_field=FloatField())
    ).aggregate(t=Sum('hpp_item'))['t'] or 0

    laba_kotor = total_penjualan - hpp_total
    total_beban = total_gaji + total_pengeluaran_lain
    laba_bersih = laba_kotor - total_beban

    # Transaksi terbaru
    pembelian_terbaru = Pembelian.objects.order_by('-tanggal', '-id')[:5]
    penjualan_terbaru = Penjualan.objects.order_by('-tanggal', '-id')[:5]
    pegawai_aktif = Pegawai.objects.filter(status='aktif').count()

    context = {
        'stok_bibit': stok_bibit,
        'stok_pupuk': stok_pupuk,
        'stok_menipis': stok_menipis,
        'total_pembelian': total_pembelian,
        'total_penjualan': total_penjualan,
        'total_gaji': total_gaji,
        'laba_bersih': laba_bersih,
        'pembelian_terbaru': pembelian_terbaru,
        'penjualan_terbaru': penjualan_terbaru,
        'pegawai_aktif': pegawai_aktif,
        'bulan_ini': today.strftime('%B %Y'),
    }
    return render(request, 'accounts/dashboard.html', context)
