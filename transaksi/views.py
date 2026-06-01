from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import datetime, json

from .models import Pembelian, ItemPembelian, Penjualan, ItemPenjualan
from stok.models import Stok, MutasiStok


# ── PEMBELIAN ─────────────────────────────────────────────

@login_required
def list_pembelian(request):
    start = request.GET.get('start', '')
    end   = request.GET.get('end', '')
    qs    = Pembelian.objects.prefetch_related('items')
    if start: qs = qs.filter(tanggal__gte=start)
    if end:   qs = qs.filter(tanggal__lte=end)
    return render(request, 'transaksi/list_pembelian.html', {'list': qs})


@login_required
def tambah_pembelian(request):
    stok_list = Stok.objects.all().order_by('kategori', 'nama')
    if request.method == 'POST':
        tanggal   = request.POST.get('tanggal') or str(datetime.date.today())
        no_faktur = request.POST.get('no_faktur', '').strip()
        supplier  = request.POST.get('supplier', '').strip()
        ket       = request.POST.get('keterangan', '').strip()

        stok_ids   = request.POST.getlist('stok_id')
        nama_items = request.POST.getlist('nama_item')
        jumlahs    = request.POST.getlist('jumlah')
        satuans    = request.POST.getlist('satuan')
        harga_sats = request.POST.getlist('harga_sat')

        if not no_faktur or not nama_items:
            messages.error(request, 'No. faktur dan minimal 1 item wajib diisi.')
        else:
            items_data = list(zip(stok_ids, nama_items, jumlahs, satuans, harga_sats))
            total = sum(float(j) * float(h) for _, _, j, _, h in items_data)

            try:
                with transaction.atomic():
                    pb = Pembelian.objects.create(
                        tanggal=tanggal, no_faktur=no_faktur,
                        supplier=supplier, total=total, keterangan=ket
                    )
                    for sid, nama, jml, sat, hsat in items_data:
                        jml   = float(jml or 0)
                        hsat  = float(hsat or 0)
                        stok  = Stok.objects.filter(pk=sid).first() if sid else None
                        ItemPembelian.objects.create(
                            pembelian=pb, stok=stok, nama_item=nama,
                            jumlah=jml, satuan=sat, harga_sat=hsat
                        )
                        # Update stok otomatis
                        if stok:
                            MutasiStok.objects.create(
                                stok=stok, jenis='masuk', jumlah=jml,
                                harga_sat=hsat, tanggal=tanggal,
                                keterangan=f'Pembelian {no_faktur}'
                            )
                            stok.stok += jml
                            stok.harga_beli = hsat  # update harga beli terbaru
                            stok.save()
                messages.success(request, f'Pembelian {no_faktur} berhasil dicatat.')
                return redirect('list_pembelian')
            except Exception as e:
                messages.error(request, f'Gagal menyimpan: {e}')

    # Generate no faktur auto
    last = Pembelian.objects.order_by('-id').first()
    n = (last.id if last else 0) + 1
    auto_faktur = f"PB-{n:04d}"
    return render(request, 'transaksi/form_pembelian.html', {
        'stok_list': stok_list,
        'auto_faktur': auto_faktur,
    })


@login_required
def hapus_pembelian(request, pk):
    pb = get_object_or_404(Pembelian, pk=pk)
    if request.method == 'POST':
        pb.delete()
        messages.success(request, 'Pembelian dihapus.')
    return redirect('list_pembelian')


# ── PENJUALAN ─────────────────────────────────────────────

@login_required
def list_penjualan(request):
    start = request.GET.get('start', '')
    end   = request.GET.get('end', '')
    qs    = Penjualan.objects.prefetch_related('items')
    if start: qs = qs.filter(tanggal__gte=start)
    if end:   qs = qs.filter(tanggal__lte=end)
    return render(request, 'transaksi/list_penjualan.html', {'list': qs})


@login_required
def tambah_penjualan(request):
    stok_list = Stok.objects.all().order_by('kategori', 'nama')
    if request.method == 'POST':
        tanggal   = request.POST.get('tanggal') or str(datetime.date.today())
        no_faktur = request.POST.get('no_faktur', '').strip()
        pembeli   = request.POST.get('pembeli', '').strip()
        ket       = request.POST.get('keterangan', '').strip()

        stok_ids   = request.POST.getlist('stok_id')
        nama_items = request.POST.getlist('nama_item')
        jumlahs    = request.POST.getlist('jumlah')
        satuans    = request.POST.getlist('satuan')
        harga_sats = request.POST.getlist('harga_sat')

        if not no_faktur or not nama_items:
            messages.error(request, 'No. faktur dan minimal 1 item wajib diisi.')
        else:
            items_data = list(zip(stok_ids, nama_items, jumlahs, satuans, harga_sats))
            total = sum(float(j) * float(h) for _, _, j, _, h in items_data)

            try:
                with transaction.atomic():
                    pj = Penjualan.objects.create(
                        tanggal=tanggal, no_faktur=no_faktur,
                        pembeli=pembeli, total=total, keterangan=ket
                    )
                    for sid, nama, jml, sat, hsat in items_data:
                        jml  = float(jml or 0)
                        hsat = float(hsat or 0)
                        stok = Stok.objects.filter(pk=sid).first() if sid else None
                        harga_beli = stok.harga_beli if stok else 0
                        ItemPenjualan.objects.create(
                            penjualan=pj, stok=stok, nama_item=nama,
                            jumlah=jml, satuan=sat, harga_sat=hsat,
                            harga_beli=harga_beli
                        )
                        # Kurangi stok otomatis
                        if stok:
                            MutasiStok.objects.create(
                                stok=stok, jenis='keluar', jumlah=jml,
                                harga_sat=hsat, tanggal=tanggal,
                                keterangan=f'Penjualan {no_faktur}'
                            )
                            stok.stok = max(0, stok.stok - jml)
                            stok.save()
                messages.success(request, f'Penjualan {no_faktur} berhasil dicatat.')
                return redirect('list_penjualan')
            except Exception as e:
                messages.error(request, f'Gagal menyimpan: {e}')

    last = Penjualan.objects.order_by('-id').first()
    n = (last.id if last else 0) + 1
    auto_faktur = f"PJ-{n:04d}"
    return render(request, 'transaksi/form_penjualan.html', {
        'stok_list': stok_list,
        'auto_faktur': auto_faktur,
    })


@login_required
def hapus_penjualan(request, pk):
    pj = get_object_or_404(Penjualan, pk=pk)
    if request.method == 'POST':
        pj.delete()
        messages.success(request, 'Penjualan dihapus.')
    return redirect('list_penjualan')
