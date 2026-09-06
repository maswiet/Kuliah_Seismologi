# Paket Kelas Asinkron — Milestone M1 (materi Minggu 2–5)

Paket tugas kelompok asinkron untuk mata kuliah **Seismologi `PAGF262413`**. Menggantikan pertemuan
tatap muka **Senin, 7 September 2026 (07.15)** dan menyiapkan kuis tanpa bantuan, diskusi, serta
viva pada **14 dan 21 September 2026**.

Mencakup empat pokok bahasan RPS sekaligus — Minggu 2 (tegangan, regangan, elastisitas), Minggu 3
(persamaan gelombang, P dan S), Minggu 4 (Snell, jalur sinar, head wave), Minggu 5
(refleksi–transmisi, gelombang permukaan dan dispersi) — dan menjadi pelaksanaan **Milestone M1**
menurut [`Asesmen_Era_AI_Seismologi.md`](../Asesmen_Era_AI_Seismologi.md).

## Isi

| Berkas | Untuk siapa | Keterangan |
|---|---|---|
| [`TUGAS_KELOMPOK_M1.md`](TUGAS_KELOMPOK_M1.md) | Mahasiswa | Petunjuk tugas lengkap: capaian, peran, luaran, linimasa, aturan |
| [`kelompok.md`](kelompok.md) | Mahasiswa & dosen | 18 kelompok, topik, peran individu, ketua, pasangan peer review (NIM disamarkan) |
| [`rubrik_penilaian.md`](rubrik_penilaian.md) | Mahasiswa & dosen | Kerangka A/U/R 25–75, rubrik tiap komponen, faktor kontribusi |
| [`bank_soal_oral_exam.md`](bank_soal_oral_exam.md) | Mahasiswa | 66 pertanyaan viva, dipublikasikan sejak awal |
| [`PENGUMUMAN_CLASSROOM.md`](PENGUMUMAN_CLASSROOM.md) | Dosen | Teks siap tempel ke Google Classroom |
| [`template/`](template/) | Mahasiswa | Kerangka laporan, logbook kontribusi, formulir peer review |
| [`../skrip/buat_kelompok.py`](../skrip/buat_kelompok.py) | Dosen | Pengacak kelompok & ketua (reproducible) |

## Rancangan singkat

- **71 mahasiswa → 18 kelompok** (17 × 4 orang + 1 × 3 orang). Kelompok sengaja kecil: dengan
  4 peran wajib dan bab bernama di laporan, tidak ada ruang untuk penumpang gelap.
- **18 topik berbeda** dalam 4 klaster yang memetakan materi Minggu 2–4:
  tegangan–regangan–elastisitas · persamaan gelombang, P & S · Snell, jalur sinar, head wave ·
  refleksi–transmisi, gelombang permukaan & dispersi.
- **Peer review silang** dengan pola geser **+6 dan +13 (mod 18)**: setiap kelompok me-review 2
  kelompok dari klaster materi yang berbeda dan di-review oleh 2 kelompok lain. Efeknya, setiap
  mahasiswa terpaksa menguasai materi di luar topiknya sendiri.
- **Bobot 25 / 75** sesuai kerangka asesmen mata kuliah: produk berbantuan AI (A) 25%,
  verifikasi tanpa bantuan (U) 75%, dengan **R = U/A** sebagai pemicu viva pada ambang 0,60.
- **Instrumen tambahan** dari dokumen asesmen: prediksi terkunci sebelum menghitung (instrumen 4)
  dan pelaporan setiap angka sebagai selang keyakinan 80% (instrumen 6).
- **Pengaman anti-penumpang gelap** berlapis: peran individu bernama, logbook kontribusi
  bertanda tangan, penyaji ditunjuk acak saat presentasi, faktor kontribusi individu, dan
  komponen U 75% yang tidak dapat diwakilkan.

## Menjalankan ulang pengacakan

```bash
python3 ../skrip/buat_kelompok.py
```

Seed tetap `20260907`, sehingga hasilnya identik setiap kali dijalankan dan dapat diaudit
oleh mahasiswa mana pun. Mengubah seed akan mengubah seluruh pembagian — jangan lakukan
setelah tugas dirilis.

Sumber data peserta: `List_Peserta_Kuliah_Seismology.xls` (ekspor sistem akademik), disimpan
**hanya di komputer dosen**. Berkas itu dan `kelompok.csv` memuat nomor telepon serta surel
mahasiswa sehingga **tidak pernah di-commit** (lihat `.gitignore`).
