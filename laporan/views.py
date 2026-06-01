from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, FloatField, ExpressionWrapper
import datetime

from transaksi.models import Penjualan, Pembelian, ItemPenjualan
from pegawai.models import Penggajian
from .models import PengeluaranLain


@login_required
def laba_rugi(request):
    today = datetime.date.today()
    # Default: bulan ini
    start_default = today.replace(day=1).strftime('%Y-%m-%d')
    end_default   = today.strftime('%Y-%m-%d')

    start = request.GET.get('start', start_default)
    end   = request.GET.get('end', end_default)

    # ── PENDAPATAN ────────────────────────────────────────
    total_penjualan = Penjualan.objects.filter(
        tanggal__gte=start, tanggal__lte=end
    ).aggregate(t=Sum('total'))['t'] or 0

    # ── HPP ───────────────────────────────────────────────
    hpp_items = ItemPenjualan.objects.filter(
        penjualan__tanggal__gte=start,
        penjualan__tanggal__lte=end
    ).annotate(
        hpp_item=ExpressionWrapper(F('jumlah') * F('harga_beli'), output_field=FloatField())
    )
    total_hpp = hpp_items.aggregate(t=Sum('hpp_item'))['t'] or 0

    laba_kotor = total_penjualan - total_hpp

    # ── BEBAN OPERASIONAL ─────────────────────────────────
    # Gaji
    beban_gaji = Penggajian.objects.filter(
        tanggal_bayar__gte=start, tanggal_bayar__lte=end
    ).aggregate(t=Sum('total_gaji'))['t'] or 0

    # Pengeluaran lain per kategori
    pengeluaran_qs = PengeluaranLain.objects.filter(
        tanggal__gte=start, tanggal__lte=end
    )
    pengeluaran_per_kat = {}
    for pe in pengeluaran_qs:
        k = pe.get_kategori_display()
        pengeluaran_per_kat[k] = pengeluaran_per_kat.get(k, 0) + pe.jumlah
    total_pengeluaran_lain = pengeluaran_qs.aggregate(t=Sum('jumlah'))['t'] or 0

    total_beban = beban_gaji + total_pengeluaran_lain
    laba_bersih = laba_kotor - total_beban

    # ── DETAIL PENJUALAN ──────────────────────────────────
    penjualan_detail = Penjualan.objects.filter(
        tanggal__gte=start, tanggal__lte=end
    ).prefetch_related('items').order_by('-tanggal')

    # ── PEMBELIAN (informasi) ─────────────────────────────
    total_pembelian = Pembelian.objects.filter(
        tanggal__gte=start, tanggal__lte=end
    ).aggregate(t=Sum('total'))['t'] or 0

    context = {
        'start': start,
        'end':   end,
        # Pendapatan
        'total_penjualan': total_penjualan,
        # HPP & Laba Kotor
        'total_hpp':    total_hpp,
        'laba_kotor':   laba_kotor,
        # Beban
        'beban_gaji':   beban_gaji,
        'pengeluaran_per_kat': pengeluaran_per_kat,
        'total_pengeluaran_lain': total_pengeluaran_lain,
        'total_beban':  total_beban,
        # Laba Bersih
        'laba_bersih':  laba_bersih,
        # Info tambahan
        'total_pembelian': total_pembelian,
        'penjualan_detail': penjualan_detail,
    }
    return render(request, 'laporan/laba_rugi.html', context)


# ── PENGELUARAN LAIN ──────────────────────────────────────

@login_required
def list_pengeluaran(request):
    qs = PengeluaranLain.objects.all()
    return render(request, 'laporan/list_pengeluaran.html', {'list': qs})


@login_required
def tambah_pengeluaran(request):
    if request.method == 'POST':
        tanggal  = request.POST.get('tanggal') or str(datetime.date.today())
        kategori = request.POST.get('kategori', 'operasional')
        deskripsi = request.POST.get('deskripsi', '').strip()
        jumlah   = float(request.POST.get('jumlah', 0) or 0)
        ket      = request.POST.get('keterangan', '').strip()
        if not deskripsi or jumlah <= 0:
            messages.error(request, 'Deskripsi dan jumlah wajib diisi.')
        else:
            PengeluaranLain.objects.create(
                tanggal=tanggal, kategori=kategori,
                deskripsi=deskripsi, jumlah=jumlah, keterangan=ket
            )
            messages.success(request, 'Pengeluaran dicatat.')
            return redirect('list_pengeluaran')
    return render(request, 'laporan/form_pengeluaran.html')


@login_required
def hapus_pengeluaran(request, pk):
    from .models import PengeluaranLain
    from django.shortcuts import get_object_or_404
    pe = get_object_or_404(PengeluaranLain, pk=pk)
    if request.method == 'POST':
        pe.delete()
        messages.success(request, 'Pengeluaran dihapus.')
    return redirect('list_pengeluaran')
