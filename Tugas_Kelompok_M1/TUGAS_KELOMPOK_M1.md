# Tugas Kelompok Asinkron — Materi Minggu 2–5 (RPS)
### Pelaksanaan Milestone **M1** (diperluas ke M2)
**Mata Kuliah Seismologi · Program Studi Geofisika UGM · Semester Ganjil 2026/2027**

> Kuliah tatap muka Senin, 7 September 2026 (07.15) **ditiadakan** karena saya mendapat tugas mengikuti
> *management walkthrough* proyek SP-ERT Geothermal di Tomohon, Sulawesi Utara.
> Sebagai gantinya, tiga pertemuan (7, 14, 21 September) dijalankan **asinkron berbasis proyek
> kelompok**, dan **pertemuan 14 dan 21 September dipakai penuh untuk kuis tanpa bantuan,
> diskusi, dan ujian lisan (viva) per individu.**

**Cakupan materi** — empat pokok bahasan RPS sekaligus:

| Minggu RPS | Materi | Berkas materi |
|---|---|---|
| 2 | Tegangan, regangan, dan elastisitas | [`Minggu02_Tegangan_Regangan.md`](../Minggu02_Tegangan_Regangan.md) |
| 3 | Persamaan gelombang seismik; gelombang P dan S | [`Minggu03_Persamaan_Gelombang.md`](../Minggu03_Persamaan_Gelombang.md) |
| 4 | Hukum Snell, jalur sinar, dan *head wave* | [`Minggu04_Snell_Jalur_Sinar.md`](../Minggu04_Snell_Jalur_Sinar.md) |
| 5 | Koefisien refleksi–transmisi; gelombang permukaan dan dispersi | [`Minggu05_Permukaan_Dispersi.md`](../Minggu05_Permukaan_Dispersi.md) |

**Aturan asesmen yang berlaku:** [`Asesmen_Era_AI_Seismologi.md`](../Asesmen_Era_AI_Seismologi.md) —
produk berbantuan AI berbobot kecil (**A, 25%**), verifikasi tanpa bantuan menjadi penentu
(**U, 75%**), dengan rasio **R = U/A** sebagai pemicu viva.

---

## 1. Capaian pembelajaran yang harus tercapai

Setelah menyelesaikan tugas ini setiap **individu** (bukan hanya kelompok) harus mampu:

| Kode | Capaian |
|---|---|
| CP-1 | Menjelaskan dan memanipulasi tensor tegangan & regangan, serta menghubungkannya melalui hukum Hooke dan modulus elastik |
| CP-2 | Menurunkan persamaan gelombang elastik dan menjelaskan asal-usul serta sifat gelombang P dan S |
| CP-3 | Menerapkan hukum Snell untuk menentukan jalur sinar, refraksi kritis, dan menjelaskan pembentukan *head wave* |
| CP-4 | Menghitung koefisien refleksi–transmisi dan menjelaskan gelombang permukaan serta dispersinya |
| CP-5 | Mengomunikasikan hasil secara tertulis, lisan, dan memberi *peer review* ilmiah yang tajam namun santun |

Materi rujukan utama: Stein & Wysession (2003) *An Introduction to Seismology, Earthquakes,
and Earth Structure*; Shearer (2019) *Introduction to Seismology* (3rd ed.);
Aki & Richards (2002) *Quantitative Seismology*; Lay & Wallace (1995) *Modern Global Seismology*.

---

## 2. Struktur kelompok

- **71 mahasiswa → 18 kelompok** (17 kelompok berisi 4 orang, 1 kelompok berisi 3 orang).
- Ukuran sengaja dibuat kecil: dengan 4 orang dan 4 peran wajib, **tidak ada tempat untuk penumpang gelap** — setiap orang punya bab bernama sendiri di laporan.
- Pembagian anggota, peran, dan ketua **diacak oleh program** (`../skrip/buat_kelompok.py`,
  seed `20260907`) sehingga dapat diaudit dan diulang hasilnya. Tidak ada intervensi manual.
- Daftar lengkap: lihat [`kelompok.md`](kelompok.md). Di repositori publik ini NIM disamarkan menjadi tiga digit terakhir; daftar dengan NIM penuh ada di Google Classroom.
- **Tidak ada pertukaran kelompok/peran** kecuali dengan alasan akademik yang disetujui dosen.

### 2.1 Peran individu (wajib, setiap orang tepat satu)

| Kode | Peran | Luaran individu yang dinilai |
|---|---|---|
| **P1** | **Teori & Derivasi** | Turunan matematis lengkap topik kelompok, langkah demi langkah, semua asumsi disebut eksplisit (≥ 2 halaman, boleh tulis tangan yang dipindai asalkan terbaca) |
| **P2** | **Komputasi & Numerik** | Notebook Python (`.ipynb`) yang menghitung/mensimulasikan topik dan dapat dijalankan ulang; minimal 1 verifikasi terhadap solusi analitik atau nilai literatur |
| **P3** | **Data & Studi Kasus** | Penerapan pada kasus nyata (data seismik/parameter batuan Indonesia bila memungkinkan) + ringkasan kritis ≥ 3 pustaka primer |
| **P4** | **Visualisasi, Sintesis & Soal** | 2–3 gambar orisinal berlabel lengkap, ringkasan 1 halaman "peta konsep", dan **3 soal latihan + kunci jawaban** untuk kelompok lain |

Kelompok beranggota 3 orang memakai peran P1, P2, dan **P34** (Data, Studi Kasus & Visualisasi gabungan).

### 2.2 Tugas ketua kelompok (dipilih acak, tercantum di `kelompok.md`)

Ketua **bukan** yang mengerjakan paling banyak, melainkan yang **memastikan semua bekerja**:

1. Membuat grup koordinasi dan jadwal internal dalam 12 jam pertama.
2. Menetapkan tenggat internal yang lebih awal dari tenggat resmi.
3. Mengisi **Logbook Kontribusi** ([`template/logbook_kontribusi.md`](template/logbook_kontribusi.md)) —
   siapa mengerjakan apa, kapan, berapa lama. Ditandatangani (paraf digital/nama) oleh **semua** anggota.
4. Mengompilasi laporan akhir menjadi satu dokumen yang runtut (bukan tempelan 4 berkas).
5. Melaporkan anggota yang tidak berkontribusi **sebelum** tenggat, bukan sesudah. Laporan menyusul setelah tenggat tidak mengubah nilai siapa pun.
6. Memimpin penyusunan *peer review* untuk 2 kelompok yang menjadi tanggung jawabnya.

Ketua mendapat **bobot koordinasi 10%** pada komponen nilai individunya (lihat rubrik).

---

## 3. Topik per kelompok

Setiap kelompok memperoleh **topik yang berbeda**, dirancang agar saling melengkapi sehingga
*peer review* silang memaksa mahasiswa membaca materi di luar topiknya sendiri.

| Klaster (materi minggu) | Kelompok | Topik |
|---|---|---|
| **A. Tegangan, regangan, elastisitas** (Minggu RPS 2) | K01–K05 | A1 tensor tegangan & Mohr · A2 tensor regangan & dilatasi · A3 hukum Hooke isotropik & batas ν · A4 anisotropi & parameter Thomsen · A5 modulus → Vp, Vs, Vp/Vs batuan Indonesia |
| **B. Persamaan gelombang, P & S, gelombang badan** (Minggu RPS 3) | K06–K10 | B1 persamaan Navier & dekomposisi Helmholtz · B2 polarisasi P–SV–SH & gerak partikel · B3 eikonal & *geometrical spreading* · B4 pola radiasi *double-couple* · B5 atenuasi Q, t*, dispersi fisik |
| **C. Snell, jalur sinar, head wave** (Minggu RPS 4) | K11–K14 | C1 hukum Snell & parameter sinar p, konversi mode · C2 jalur sinar medium berlapis/bergradien & kurva T(X) · C3 *head wave* & seismik refraksi (crossover, intercept) · C4 sinar dalam bumi bola: *shadow zone*, triplikasi, PcP/PKP |
| **D. Refleksi–transmisi, gelombang permukaan & dispersi** (Minggu RPS 5) | K15–K18 | D1 koefisien R/T insiden normal & seismogram konvolusi · D2 Zoeppritz & aproksimasi AVO · D3 gelombang Rayleigh pada *half-space* · D4 gelombang Love & inversi kurva dispersi → profil Vs |

Judul lengkap tiap topik ada di [`kelompok.md`](kelompok.md).

### 3.1 Pertanyaan pemandu (wajib dijawab di laporan)

Selain uraian topik, **setiap** kelompok wajib menjawab empat pertanyaan berikut dari sudut pandang topiknya:

1. **Fisis:** besaran fisis apa yang sebenarnya "bergerak"/berubah, dan apa satuannya?
2. **Asumsi:** asumsi apa yang membuat rumus utama topik ini berlaku, dan kapan asumsi itu gugur?
3. **Numerik:** berikan satu contoh berangka dengan parameter realistis (sebutkan sumber angkanya).
4. **Kaitan:** bagaimana topik ini dipakai dalam praktik nyata (eksplorasi geotermal, mitigasi gempa, tomografi, atau survei teknik sipil)?

---

## 4. Luaran yang dikumpulkan

### 4.1 Individu (unggah sendiri, tidak boleh diwakilkan ketua)
1. **Prediksi terkunci** — `K##_NIM_prediksi.md`, **diunggah paling lambat Selasa 8 Sep 21.00,
   sebelum menghitung apa pun**. Berisi tebakan angka untuk 3 besaran topik Anda beserta alasan
   fisisnya. Setelah tenggat tidak dapat diubah. Yang dinilai **alasannya**, bukan ketepatan
   angkanya: meleset dengan penalaran masuk akal bernilai penuh, tepat tanpa alasan bernilai setengah.
2. **Berkas peran** sesuai tabel 2.1 → `K##_NIM_Nama_P#.pdf` (atau `.ipynb` untuk P2).
3. **Refleksi 1 halaman**: apa yang semula tidak dipahami, bagaimana akhirnya dipahami, dan satu pertanyaan yang masih mengganjal.

> **Aturan angka (berlaku untuk semua luaran):** setiap besaran dilaporkan sebagai **selang
> keyakinan 80%**, bukan titik tunggal — misalnya `α = 5,8 ± 0,4 km/s (80%)`. Yang dinilai adalah
> **laju cakupan**: seberapa sering selang Anda benar-benar memuat nilai rujukan literatur.
> Selang sempit-tapi-salah dinilai lebih buruk daripada selang lebar-tapi-benar.

### 4.2 Kelompok (diunggah ketua)
1. **Laporan gabungan** 10–15 halaman (A4, 11 pt, spasi 1.15), memakai
   [`template/laporan_kelompok.md`](template/laporan_kelompok.md). Wajib memuat kontribusi keempat peran dengan **nama penulis di setiap subbab**.
2. **Notebook** yang dapat dijalankan ulang + berkas data (atau tautannya).
3. **Video penjelasan 8 menit** — **setiap anggota wajib bicara ≥ 90 detik** dan wajah/nama tampak. Unggah ke Drive/YouTube tidak-terdaftar, cantumkan tautannya.
4. **Poster A1 satu halaman** (PDF) untuk dipajang saat diskusi kelas.
5. **Logbook kontribusi** bertanda tangan semua anggota.
6. **3×4 = 12 soal latihan + kunci** (gabungan dari peran P4 dan anggota lain).

### 4.3 Peer review silang (kelompok)
Setiap kelompok me-review **2 kelompok lain** dan di-review oleh **2 kelompok lain**
(pasangan tercantum di `kelompok.md`; pola geser +6 dan +13 agar reviewer selalu berasal dari klaster materi yang berbeda).

Gunakan [`template/formulir_peer_review.md`](template/formulir_peer_review.md). Review yang baik berisi:
- 1 kesalahan/kelemahan **teknis** yang spesifik (sebut halaman/persamaan),
- 1 saran perbaikan yang dapat langsung dikerjakan,
- 1 pertanyaan tingkat ujian lisan untuk kelompok yang di-review,
- percobaan menjalankan ulang notebook mereka: berhasil / gagal, dan di mana gagalnya.

Review "bagus, sudah lengkap, lanjutkan" **dinilai nol**.

---

## 5. Linimasa

| Tanggal | Kegiatan | Tenggat |
|---|---|---|
| **Sen, 7 Sep** | Rilis tugas (asinkron). Ketua membentuk koordinasi & membagi jadwal internal | 19.00 |
| Sel, 8 Sep | Ketua mengunggah rencana kerja kelompok (½ hal.) · **setiap individu mengunggah prediksi terkunci** | 21.00 |
| **Rab, 9 Sep** | **Berkas individu (P1–P4) diunggah masing-masing** | 23.59 |
| **Jum, 11 Sep** | **Laporan kelompok + notebook + video + poster + logbook** | 23.59 |
| **Min, 13 Sep** | **Peer review silang untuk 2 kelompok** diunggah | 20.00 |
| **Sen, 14 Sep · 07.15** | **Kelas 1: kuis tanpa bantuan 20 mnt + diskusi + viva gelombang I** — klaster A & B (K01–K10) | — |
| Kam, 18 Sep | Revisi laporan berdasarkan peer review + tanggapan tertulis kepada reviewer | 23.59 |
| **Sen, 21 Sep · 07.15** | **Kelas 2: diskusi + viva gelombang II** — klaster C & D (K11–K18) | — |

Keterlambatan: −10% per hari, ditolak setelah 3 hari. Berlaku per individu untuk luaran individu.

---

## 6. Diskusi kelas & ujian lisan (14 dan 21 September)

Format **14 September** (100 menit):

- **0–20** **Kuis tanpa bantuan**, tutup buku, tanpa AI: 4 soal pendek (satu per klaster A/B/C/D) yang menuntut penurunan singkat atau penalaran fisis. Inilah komponen U2.
- **20–35** Poster walk: semua poster dipajang, mahasiswa berkeliling dan menempel 1 pertanyaan pada poster kelompok lain.
- **35–70** Presentasi kilat 5 menit × kelompok terjadwal; **penyaji ditunjuk mendadak oleh dosen di tempat**, bukan ditentukan kelompok. Nilai presentasi menjadi nilai seluruh kelompok — inilah pengaman utama terhadap anggota yang tidak ikut bekerja.
- **70–95** **Viva individu** 4–5 menit per orang, pertanyaan diambil dari bank soal (§7) dan dari berkas peran orang tersebut. Rentang: 2 pertanyaan topik sendiri + 1 pertanyaan topik kelompok yang ia review.
- **95–100** Umpan balik dosen & penutup.

Format **21 September** sama, tanpa kuis: poster walk 0–15, presentasi 15–55, viva individu 55–90, umpan balik 90–100.

**Aturan tegas:** mahasiswa yang tidak dapat menjelaskan berkas peran yang ia unggah sendiri
memperoleh **U1 = 0** dan faktor kontribusi *f* ≤ 0,6, tanpa memandang nilai kelompoknya.
Karena U berbobot 75%, nilai kelompok tidak dapat menutupinya.

---

## 7. Bank pertanyaan oral exam

Lihat [`bank_soal_oral_exam.md`](bank_soal_oral_exam.md) — 66 pertanyaan terbuka. Semua pertanyaan
dipublikasikan sejak awal; yang diuji adalah pemahaman, bukan kejutan.

---

## 8. Rubrik penilaian

Lihat [`rubrik_penilaian.md`](rubrik_penilaian.md). Ringkas:

| Kelompok | Komponen | Bobot |
|---|---|---|
| **A — Produk berbantuan AI (25%)** | Berkas peran individu + refleksi | 10% |
| | Laporan & luaran kelompok | 10% |
| | Kualitas peer review yang diberikan | 5% |
| **U — Verifikasi tanpa bantuan (75%)** | Ujian lisan individu (14 & 21 Sep) | 34% |
| | Kuis tanpa bantuan 20 menit, tutup buku (14 Sep) | 20% |
| | Presentasi penyaji-acak + partisipasi diskusi | 10% |
| | Prediksi terkunci + kalibrasi ketidakpastian | 11% |

Rasio **R = U/A** dihitung untuk setiap mahasiswa. **R < 0,60 memicu viva tambahan** — bukan
tuduhan, hanya verifikasi lanjutan. Laporan sempurna dengan U rendah adalah persis pola yang
dirancang untuk tertangkap sistem ini, sehingga tidak diperlukan detektor AI apa pun.

**Gerbang:** skor A < 40 berarti setoran belum lengkap; mahasiswa wajib melengkapinya sebelum
boleh mengikuti komponen U.

**Faktor kontribusi individu** (0,5–1,1) dihitung dari logbook + penilaian sejawat dalam kelompok
+ pengamatan dosen saat oral exam, lalu dikalikan pada komponen kelompok. Artinya: menumpang nama
pada laporan kelompok tanpa bekerja akan menurunkan nilai secara langsung.

---

## 9. Integritas akademik

- **AI generatif (ChatGPT, Claude, dsb.) boleh digunakan** sebagai alat bantu, **wajib** dituliskan pada
  bagian "Pernyataan Penggunaan AI": alat apa, untuk bagian apa, prompt intinya. Penggunaan tanpa deklarasi
  diperlakukan sebagai pelanggaran integritas.
- Semua derivasi harus dapat dipertahankan secara lisan. Oral exam adalah penyaring utamanya.
- Menyalin laporan kelompok lain, atau menandatangani logbook yang tidak benar, dikenai sanksi
  akademik sesuai peraturan universitas bagi **seluruh** penanda tangan.

---

*Pertanyaan selama masa asinkron: ajukan lewat kolom komentar Google Classroom (agar terlihat semua),
bukan japri. Dosen menjawab pada malam hari selama penugasan lapangan.*
