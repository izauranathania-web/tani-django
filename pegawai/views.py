from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

from .models import Pegawai, Penggajian


@login_required
def list_pegawai(request):
    status = request.GET.get('status', '')
    qs = Pegawai.objects.all()
    if status:
        qs = qs.filter(status=status)
    return render(request, 'pegawai/list.html', {'pegawai_list': qs, 'status': status})


@login_required
def tambah_pegawai(request):
    if request.method == 'POST':
        nama    = request.POST.get('nama', '').strip()
        jabatan = request.POST.get('jabatan', '').strip()
        no_hp   = request.POST.get('no_hp', '').strip()
        alamat  = request.POST.get('alamat', '').strip()
        gaji    = float(request.POST.get('gaji_pokok', 0) or 0)
        tgl     = request.POST.get('tanggal_masuk') or None
        if not nama:
            messages.error(request, 'Nama pegawai wajib diisi.')
        else:
            Pegawai.objects.create(
                nama=nama, jabatan=jabatan, no_hp=no_hp,
                alamat=alamat, gaji_pokok=gaji, tanggal_masuk=tgl
            )
            messages.success(request, f'Pegawai "{nama}" ditambahkan.')
            return redirect('list_pegawai')
    return render(request, 'pegawai/form.html', {'judul': 'Tambah Pegawai'})


@login_required
def edit_pegawai(request, pk):
    p = get_object_or_404(Pegawai, pk=pk)
    if request.method == 'POST':
        p.nama    = request.POST.get('nama', p.nama).strip()
        p.jabatan = request.POST.get('jabatan', '').strip()
        p.no_hp   = request.POST.get('no_hp', '').strip()
        p.alamat  = request.POST.get('alamat', '').strip()
        p.gaji_pokok = float(request.POST.get('gaji_pokok', p.gaji_pokok) or 0)
        p.status  = request.POST.get('status', p.status)
        p.tanggal_masuk = request.POST.get('tanggal_masuk') or None
        p.save()
        messages.success(request, 'Data pegawai diperbarui.')
        return redirect('list_pegawai')
    return render(request, 'pegawai/form.html', {'judul': 'Edit Pegawai', 'pegawai': p})


@login_required
def hapus_pegawai(request, pk):
    p = get_object_or_404(Pegawai, pk=pk)
    if request.method == 'POST':
        p.delete()
        messages.success(request, 'Pegawai dihapus.')
    return redirect('list_pegawai')


@login_required
def penggajian(request):
    periode = request.GET.get('periode', datetime.date.today().strftime('%Y-%m'))
    list_gaji = Penggajian.objects.filter(periode=periode).select_related('pegawai')
    pegawai_aktif = Pegawai.objects.filter(status='aktif')
    return render(request, 'pegawai/penggajian.html', {
        'list_gaji': list_gaji,
        'pegawai_aktif': pegawai_aktif,
        'periode': periode,
    })


@login_required
def bayar_gaji(request):
    if request.method == 'POST':
        pegawai_id = request.POST.get('pegawai_id')
        periode    = request.POST.get('periode', '').strip()
        tunjangan  = float(request.POST.get('tunjangan', 0) or 0)
        potongan   = float(request.POST.get('potongan', 0) or 0)
        ket        = request.POST.get('keterangan', '').strip()
        tgl_bayar  = request.POST.get('tanggal_bayar') or str(datetime.date.today())

        p = get_object_or_404(Pegawai, pk=pegawai_id)
        total = p.gaji_pokok + tunjangan - potongan

        pg, created = Penggajian.objects.get_or_create(
            pegawai=p, periode=periode,
            defaults={
                'gaji_pokok': p.gaji_pokok,
                'tunjangan': tunjangan,
                'potongan': potongan,
                'total_gaji': total,
                'keterangan': ket,
                'tanggal_bayar': tgl_bayar,
            }
        )
        if not created:
            messages.warning(request, f'{p.nama} sudah digaji untuk periode {periode}.')
        else:
            messages.success(request, f'Gaji {p.nama} periode {periode} berhasil dicatat.')
    return redirect(f'/pegawai/penggajian/?periode={request.POST.get("periode", "")}')
