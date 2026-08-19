# Perkakas Milestone M5

Dua skrip yang mengubah rancangan asesmen di [`Asesmen_Era_AI_Seismologi.md`](../Asesmen_Era_AI_Seismologi.md) menjadi sesuatu yang benar-benar dapat dijalankan untuk 71 mahasiswa.

| Skrip | Fungsi |
|:--|:--|
| [`m5_siapkan_dataset.py`](m5_siapkan_dataset.py) | Membuat paket soal **unik per mahasiswa** + kunci jawaban privat |
| [`m5_koreksi.py`](m5_koreksi.py) | Mengoreksi setoran, menulis papan pantau, daftar viva, dan ringkasan mutu |

---

## 1 · Menyiapkan soal

```bash
python3 skrip/m5_siapkan_dataset.py --peserta peserta.csv --keluaran dataset_m5
```

`peserta.csv` cukup berkolom `nim,nama`.

Tiap mahasiswa menerima **tiga soal W11** (potongan rekaman 60 detik untuk *picking*) dan **tiga soal W12** (waktu tiba banyak stasiun untuk penentuan lokasi) — masing-masing satu soal mudah, satu sedang, satu sulit.

**Pembagian berjenjang itu bukan hiasan.** Tanpa stratifikasi, ambang nilai tetap akan menghukum mahasiswa yang kebetulan mendapat soal berat. Dengan stratifikasi, semua orang menghadapi campuran kesulitan yang sebanding.

Ukuran nyata untuk 71 mahasiswa:

| | |
|:--|:--|
| Waktu jalan | ± 7 detik |
| Ukuran keluaran | 6,7 MB |
| Keunikan soal W12 | 213 dari 213 — tidak ada yang berbagi |
| Offset P pada W11 | diacak 12–45 detik, tidak bisa dihafal |

### Yang perlu diperhatikan

- **Folder `_kunci/` jangan pernah di-commit.** Skrip menulis `.gitignore` otomatis, tapi periksa sendiri sebelum push.
- **Ganti `--garam` tiap semester** agar soal tidak berulang dari angkatan sebelumnya.
- Undian di-seed dari NIM memakai SHA-256, jadi menjalankan ulang menghasilkan paket yang sama persis. `hash()` bawaan Python sengaja tidak dipakai karena nilainya diacak tiap proses.
- Ada **lantai SNR ≥ 4** pada soal W11. Rekaman yang lebih buruk dari itu tidak dapat di-*pick* oleh siapa pun; "sulit" harus berarti menuntut, bukan mustahil.

---

## 2 · Mengoreksi

```bash
python3 skrip/m5_koreksi.py \
    --kunci dataset_m5/_kunci/kunci_m5.csv \
    --setoran setoran/ \
    --skor skor_AU.csv \
    --keluaran hasil_m5
```

`skor_AU.csv` berisi `nim,A,U` — skor tugas berbantuan dan skor verifikasi tanpa bantuan, diisi pengajar. Boleh dilewati; metrik ketepatan tetap dihitung.

### Keluaran

| Berkas | Isi |
|:--|:--|
| `papan_pantau.csv` | Satu baris per mahasiswa: `dt_P`, `err_km`, `cal`, `A`, `U`, `R`, `nilai`, status viva |
| `daftar_viva.csv` | Siapa yang dipanggil dan mengapa |
| `ringkasan_mutu.txt` | Ketepatan kelas, kalibrasi, retensi, dan **kesehatan instrumen** |

### Pemicu viva

Viva dipanggil bila `R < 0,60`, atau `dt_P > 0,5 s`, atau `err_km > 15 km`, atau setoran tidak lengkap — **ditambah sampel acak 15%** dari yang tidak tertandai.

Sampel acak itu penting secara sosial, bukan statistik: tanpanya, dipanggil viva sama dengan dituduh. Dengan sampel acak, dipanggil viva adalah hal biasa.

### Metrik yang mengawasi soal Anda sendiri

Ringkasan melaporkan **korelasi A dengan U**. Kelas sehat berada di sekitar 0,6–0,8. Bila runtuh mendekati nol, artefak yang Anda kumpulkan sudah berhenti mengukur pemahaman — dan yang perlu diperbaiki rancangan tugasnya, bukan mahasiswanya. Korelasi tidak dilaporkan bila n < 15, karena pada sampel sekecil itu angkanya didominasi derau.

---

## 3 · Format setoran

Sel setoran pada [`Minggu11_Praktik.ipynb`](../Minggu11_Praktik.ipynb) dan [`Minggu12_Praktik.ipynb`](../Minggu12_Praktik.ipynb) sudah menghasilkan format ini.

**W11** — `nim, soal, P_detik, S_detik, pita_lo, pita_hi, P_selang_bawah, P_selang_atas`
**W12** — `nim, soal, lat, lon, kedalaman_km, kedalaman_selang_bawah, kedalaman_selang_atas`

Pengoreksi mengenali beberapa nama kolom alternatif, dan melaporkan berkas yang tidak terbaca beserta sebabnya alih-alih diam-diam melewatinya.

---

## 4 · Batas yang harus disampaikan ke mahasiswa

**Pick rujukan berasal dari EqTransformer, bukan analis manusia.** Ia rujukan yang konsisten, bukan kebenaran mutlak. Nilai `dt_P` yang besar memicu percakapan, bukan sanksi — dan mahasiswa yang dapat menunjukkan bahwa pick-nya lebih baik daripada rujukan layak diberi nilai lebih, bukan kurang.

Hal yang sama berlaku untuk katalog lokasi: ia keluaran NonLinLoc dengan model kecepatan tertentu, dan membawa sidik jari model itu.

---

## 5 · Alur satu semester

```
Minggu 11  siapkan dataset  ->  bagikan paket  ->  mahasiswa mengerjakan notebook
Minggu 12  verifikasi tanpa bantuan di kelas (20 menit)  ->  isi skor_AU.csv
           jalankan pengoreksi  ->  baca ringkasan_mutu.txt
           panggil daftar_viva.csv  ->  catat skor viva
```

Semester pertama sebaiknya dipakai untuk **kalibrasi tanpa konsekuensi nilai**. Ambang 0,60 pada rasio retensi adalah tebakan awal, bukan hasil penelitian — sebaran kelas Anda sendiri yang akan memberi tahu angka yang benar.
