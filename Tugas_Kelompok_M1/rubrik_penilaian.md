# Rubrik Penilaian — Tugas Kelompok Minggu 2–5 (Milestone M1 diperluas)

Rubrik ini **mengikuti** kerangka [`Asesmen_Era_AI_Seismologi.md`](../Asesmen_Era_AI_Seismologi.md),
bukan menggantikannya. Prinsip yang sama berlaku:

> Produk berbantuan AI = **gerbang bernilai kecil (A, 25%)**.
> Verifikasi tanpa bantuan = **penentu nilai (U, 75%)** pada konstruk yang sama.

Tugas ini menjadi pelaksanaan **M1** (elastisitas, persamaan gelombang, P vs S — Minggu 3)
yang diperluas sampai menyentuh **M2** (Snell, jalur sinar, fase seismik), dengan tambahan
instrumen 4 (prediksi terkunci) dan 6 (kalibrasi ketidakpastian).

---

## 1. Struktur nilai

### A — Skor produk berbantuan (bobot **25%**)
Boleh memakai AI sebebasnya, **wajib dideklarasikan** (Lampiran C laporan).

| Komponen A | Porsi dari A |
|---|---|
| A1 Berkas peran individu (P1–P4) + refleksi | 40 |
| A2 Laporan kelompok + notebook + poster + video | 40 |
| A3 Peer review yang diberikan ke 2 kelompok lain | 20 |

A2 dan A3 dikalikan **faktor kontribusi individu *f*** (§3).

### U — Skor tanpa bantuan (bobot **75%**)
Dikerjakan di kelas atau di hadapan dosen. Tanpa AI, tanpa catatan kecuali disebut boleh.

| Komponen U | Porsi dari U | Kapan |
|---|---|---|
| U1 **Ujian lisan individu** 4–5 menit | 45 | 14 & 21 Sep di kelas |
| U2 **Kuis tanpa bantuan** 20 menit, tutup buku | 27 | 14 Sep, awal kelas |
| U3 **Presentasi penyaji-acak** + kualitas pertanyaan dalam diskusi | 14 | 14 & 21 Sep |
| U4 **Prediksi terkunci** (instrumen 4) + **kalibrasi ketidakpastian** (instrumen 6) | 14 | dikumpulkan 9 Sep, dinilai setelahnya |

**Nilai akhir individu** = 0,25·A + 0,75·U.

### R — rasio pemicu viva
$R = U / A$. Ambang seperti pada dokumen asesmen: **R ≥ 0,60**.

- R < 0,60 → **viva tambahan terpicu** (bukan tuduhan, hanya verifikasi lanjutan).
- Mahasiswa yang **tidak dapat menjelaskan berkas yang ia unggah sendiri** → U1 = 0 dan *f* ≤ 0,6.
- A bagus + U rendah adalah pola yang justru paling ingin ditangkap sistem ini. Tidak perlu detektor AI.

**Gerbang:** A < 40 → tidak boleh mengikuti U1/U2 sebelum melengkapi setoran. Produk itu syarat masuk.

---

## 2. Rubrik per komponen

### U1 — Ujian lisan individu (45% dari U)
4 dimensi, masing-masing 0–25.

| Dimensi | 22–25 | 15–21 | 8–14 | 0–7 |
|---|---|---|---|---|
| **Penguasaan konsep** | Menjelaskan makna fisis tanpa catatan; tahu mengapa rumus berbentuk demikian | Konsep benar, sesekali ragu | Hafal rumus, makna fisis kabur | Tidak dapat menjelaskan |
| **Derivasi** | Menurunkan ulang langkah kunci di papan dengan benar | Menurunkan dengan sedikit bantuan | Hanya menyebut hasil akhir | Salah / tidak dapat |
| **Asumsi & batas berlaku** | Menyebut asumsi spontan, tahu kapan gugur | Menyebut bila ditanya | Sebagian | Tidak sadar ada asumsi |
| **Kaitan lintas topik** | Menghubungkan ke topik kelompok yang ia review dan ke aplikasi nyata | Satu arah | Terbatas topik sendiri | Tidak ada |

Komposisi pertanyaan: 2 dari topik sendiri + 1 dari topik kelompok yang ia review. Semua diambil
dari [`bank_soal_oral_exam.md`](bank_soal_oral_exam.md) yang sudah dipublikasikan.

### U2 — Kuis tanpa bantuan (27% dari U)
20 menit, tutup buku, di kelas 14 September. Isi: 4 soal pendek — satu per klaster A/B/C/D — yang
menuntut **penurunan singkat atau penalaran fisis**, bukan hafalan definisi. Soal ditarik dari
konstruk yang sama dengan tugas, sehingga U dan A benar-benar mengukur hal yang sama.

### U3 — Presentasi penyaji-acak & partisipasi (14% dari U)
Penyaji **ditunjuk dosen di tempat**. Nilai penyaji menjadi nilai seluruh anggota kelompok — inilah
pengaman paling langsung terhadap anggota yang menumpang. Dinilai: kejelasan alur, penguasaan saat
ditanya, dan **kualitas pertanyaan yang diajukan ke kelompok lain**.

### U4 — Prediksi terkunci & kalibrasi ketidakpastian (14% dari U)

**Prediksi terkunci (instrumen 4).** Sebelum menghitung apa pun, setiap mahasiswa mengunggah
`prediksi_terkunci.md` berisi tebakan angka untuk 3 besaran topiknya (misal: Vp/Vs batuan yang
dipilih, sudut kritis, crossover distance, kecepatan Rayleigh) **beserta alasan fisisnya**.
Dikumpulkan 9 September dan tidak dapat diubah.

Skor = ketepatan arah penalaran, bukan ketepatan angka. Prediksi meleset dengan alasan yang masuk
akal bernilai penuh; prediksi tepat tanpa alasan bernilai setengah.

**Kalibrasi ketidakpastian (instrumen 6).** Setiap angka dalam laporan dilaporkan sebagai **selang
keyakinan 80%**, bukan titik: "α = 5,8 ± 0,4 km/s (80%)". Metrik: **laju cakupan** — proporsi selang
yang benar-benar memuat nilai rujukan literatur.

| Laju cakupan | Tafsir |
|---|---|
| ≈ 0,80 | Terkalibrasi baik |
| ≫ 0,80 | Terlalu hati-hati, selang kelewat lebar |
| ≪ 0,80 | **Terlalu percaya diri** — pola khas angka AI yang ditelan mentah |

Selang sempit-tapi-salah dinilai **lebih buruk** daripada selang lebar-tapi-benar.

### A1 — Berkas peran individu (40% dari A)

| Aspek | Bobot |
|---|---|
| Kelengkapan sesuai spesifikasi peran P1/P2/P3/P4 | 30 |
| Ketepatan teknis (derivasi benar, kode berjalan, sitasi tepat) | 35 |
| Kedalaman melampaui catatan kuliah (pustaka primer, contoh berangka sendiri) | 20 |
| Kerapian (notasi konsisten, gambar berlabel, satuan ditulis, selang keyakinan ada) | 10 |
| Refleksi 1 halaman yang jujur dan spesifik | 5 |

P2 khusus: notebook yang **gagal dijalankan ulang** oleh reviewer kehilangan seluruh 35 poin
ketepatan teknis, kecuali kegagalan terbukti karena kelalaian reviewer.

### A2 — Laporan & luaran kelompok (40% dari A)

| Aspek | Bobot |
|---|---|
| Menjawab keempat pertanyaan pemandu (§3.1 dokumen tugas) | 25 |
| Integrasi — terbaca sebagai satu tulisan, bukan 4 tempelan | 20 |
| Ketepatan teknis & konsistensi notasi antaranggota | 20 |
| Gambar orisinal, poster, dan 12 soal + kunci | 15 |
| Video 8 menit, semua anggota bicara ≥ 90 detik | 10 |
| Logbook lengkap & deklarasi AI benar | 10 |

### A3 — Kualitas peer review yang diberikan (20% dari A)

| Aspek | Bobot |
|---|---|
| Menemukan kelemahan teknis spesifik (rujuk halaman/persamaan) | 35 |
| Saran perbaikan yang langsung dapat dikerjakan | 25 |
| Pertanyaan setingkat ujian lisan yang tajam | 20 |
| Bukti mencoba menjalankan ulang notebook (berhasil/gagal + di mana) | 15 |
| Nada profesional: mengkritik karya, bukan orang | 5 |

Review generik ("sudah bagus, tinggal dirapikan") = **0**.

---

## 3. Faktor kontribusi individu (*f*)

Berlaku pada komponen kelompok A2 dan A3 saja — U tidak pernah dikalikan *f* karena U memang
sudah individual.

Sumber: **logbook kontribusi** (30%), **penilaian sejawat rahasia** dalam kelompok (40%, tiap orang
membagi 100 poin ke rekan-rekannya, bukan ke dirinya), dan **pengamatan dosen** saat ujian lisan (30%).

| *f* | Kriteria |
|---|---|
| 1,10 | Kontribusi jauh di atas porsi; menolong anggota lain memahami materi |
| 1,00 | Mengerjakan porsinya penuh dan tepat waktu (**default**) |
| 0,85 | Terlambat / perlu banyak diingatkan; hasil di bawah spesifikasi peran |
| 0,60 | Kontribusi minimal; tidak menguasai bagian yang diklaim |
| 0,00 | Hanya menempelkan nama |

Ketua: **+10 poin pada A1** bila logbook, koordinasi, dan kompilasi rapi; **−10** bila kelompok
berantakan karena koordinasi tidak berjalan. Ketua yang melapor anggota bermasalah **sebelum**
tenggat tidak dikenai penalti atas kegagalan anggota itu.

---

## 4. Papan pantau

Satu baris per mahasiswa, mengikuti format papan pantau di dokumen asesmen:

| Kolom | Isi |
|---|---|
| `A` | Skor produk berbantuan (0–100) |
| `U` | Skor tanpa bantuan (0–100) |
| `R` | U/A — pemicu viva bila < 0,60 |
| `cal` | Laju cakupan selang 80% |
| `pred` | Skor prediksi terkunci |
| `f` | Faktor kontribusi |
| `viva` | 0–9 bila terpicu |

Tiga sinyal kelas yang dipantau: median R, korelasi A–U (sehat bila r ≈ 0,6–0,8), dan tren `cal`/`pred`.
Korelasi A–U yang runtuh ke nol berarti **artefaknya berhenti mengukur apa pun** — alarm untuk
instrumennya, bukan untuk mahasiswanya.

---

## 5. Konversi nilai

| Skor akhir | Huruf |
|---|---|
| ≥ 80 | A |
| 75–79,9 | A− |
| 70–74,9 | B+ |
| 65–69,9 | B |
| 60–64,9 | B− |
| 55–59,9 | C+ |
| 50–54,9 | C |
| 40–49,9 | D |
| < 40 | E |

Keterlambatan setoran A: −10% per hari, ditolak setelah 3 hari. Komponen U tidak dapat diulang
kecuali dengan izin akademik resmi.
