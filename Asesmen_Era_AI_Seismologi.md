# Mengukur Pemahaman Nyata di Kelas Berbantuan AI
## Rancangan milestone kuantitatif — Seismologi `PAGF262413` (71 mahasiswa) + Praktikum `PAGF262412`

---

## 1. Diagnosis: yang rusak bukan mahasiswanya, tapi alat buktinya

Selama puluhan tahun kita memakai satu asumsi diam-diam:

> *Kalau mahasiswa bisa menghasilkan laporan yang benar, berarti dia paham.*

Asumsi itu bekerja karena dulu **satu-satunya jalan** menuju laporan yang benar adalah melewati proses berpikirnya. Artefak adalah bukti, karena artefak mahal diproduksi tanpa pemahaman.

AI memutus rantai itu. Sekarang artefak murah dan pemahaman mahal. **Laporan sempurna tidak lagi menjadi bukti apa pun** — bukan bukti paham, bukan juga bukti tidak paham. Nilainya sebagai alat ukur mendekati nol.

Konsekuensinya penting: masalahnya **bukan** "bagaimana mendeteksi AI". Itu jalan buntu (§7). Masalahnya adalah **membangun ulang alat bukti** — memindahkan asesmen ke hal-hal yang bantuan AI tidak bisa menggantikannya.

Kabar baiknya: sekali Anda menerima ini, Anda justru bisa membuka AI selebar-lebarnya seperti yang Anda inginkan. Karena yang dinilai bukan lagi artefaknya.

---

## 2. Prinsip inti: pisahkan **produk** dari **bukti**

| | Produk | Bukti |
|:--|:--|:--|
| Contoh | Laporan praktikum, notebook, esai, kode | Kuis tanpa bantuan, viva, prediksi terkunci, hasil numerik atas data unik |
| Boleh pakai AI? | **Ya, sebebasnya** — bahkan diwajibkan didokumentasikan | Tidak, atau tidak relevan |
| Bobot nilai | Kecil (gerbang) | Besar (penentu) |
| Fungsi | Media belajar | Alat ukur |

**Perubahan struktural tunggal yang paling berdampak:**

> Jadikan produk berbantuan AI sebagai **syarat masuk bernilai kecil (25%)**, dan jadikan verifikasi tanpa bantuan sebagai **penentu nilai (75%)** — pada konstruk yang sama.

Begitu bobotnya dibalik, insentif menyuruh AI mengerjakan tugas runtuh dengan sendirinya. Tugas berubah fungsi menjadi latihan, bukan setoran. Mahasiswa yang menyerahkan pekerjaan AI tanpa memahaminya akan **gagal di verifikasi 75%-nya sendiri** — tanpa perlu tuduhan, tanpa perlu detektor, tanpa perlu konfrontasi.

Ini juga adil: mahasiswa yang memakai AI untuk *benar-benar belajar* akan lolos verifikasi dengan mudah. Persis perilaku yang ingin Anda dorong.

---

## 3. Enam instrumen ukur

Diurutkan dari yang paling kuat. Kolom **Tahan-AI** menilai seberapa sulit bantuan AI menggantikan kognisi mahasiswa; **Biaya** dihitung untuk 71 mahasiswa.

| # | Instrumen | Tahan-AI | Biaya |
|:--:|:--|:--:|:--|
| 1 | Data unik per mahasiswa | ★★★★★ | Rendah (skrip sekali, pakai berkali-kali) |
| 2 | Verifikasi tanpa bantuan (*unassisted check*) | ★★★★★ | Rendah (20 menit di kelas) |
| 3 | Viva terpicu | ★★★★★ | Sedang (hanya untuk yang tertandai) |
| 4 | Prediksi terkunci sebelum hitung | ★★★★☆ | Rendah |
| 5 | Perburuan galat pada keluaran AI | ★★★★☆ | Sedang (menyiapkan galat) |
| 6 | Kalibrasi ketidakpastian | ★★★★☆ | Rendah |

---

### Instrumen 1 — Data unik per mahasiswa
**Ini keunggulan tak adil bidang seismologi. Manfaatkan habis-habisan.**

Berbeda dengan esai atau soal buku teks, seismologi punya persediaan **tak terbatas soal yang tiap jawabannya berbeda dan ground-truth-nya publik**. Beri tiap mahasiswa event ID berlainan dari katalog USGS/ISC/BMKG. AI bisa menjelaskan *metodenya*, tapi tidak bisa mengetahui angka *milik dia*.

Yang diukur: **galat absolut terhadap katalog rujukan.**

| Besaran | Toleransi lulus | Catatan |
|:--|:--|:--|
| Episenter (metode lingkaran, ≥4 stasiun) | ≤ 30 km | Longgar — metode grafis memang kasar |
| Episenter (inversi Geiger) | ≤ 15 km | |
| Waktu asal | ≤ 3 s | |
| Kedalaman | dinilai lewat kalibrasi (Instrumen 6) | Paling tidak terkendala pada jaringan sempit |
| Magnitudo $M_L$ | ± 0,3 | Standar praktik |
| Tipe mekanisme sesar | benar (kategorik) | Naik / turun / geser — wajib benar |
| *Strike*, *rake* | ± 25° | Solusi *first-motion* memang berketidakpastian besar |
| Residual *picking* P (lokal) | RMS ≤ 0,5 s | |

**Kunci pelaksanaan:** siapkan satu skrip Python penilai yang menarik nilai katalog via FDSN web service dan membandingkan dengan CSV setoran mahasiswa. Investasi ± 1 hari, lalu 71 mahasiswa terkoreksi dalam hitungan detik, tiap semester.

**Bonus:** mahasiswa boleh dan sebaiknya memakai AI untuk membantu koding. Yang dinilai kebenaran angka atas datanya sendiri — dan untuk sampai ke sana dia harus paham apa yang dilakukan kodenya.

---

### Instrumen 2 — Verifikasi tanpa bantuan
**Inti dari seluruh rancangan.**

Tiap milestone punya dua pengukuran atas konstruk yang sama:

- **A** = skor produk berbantuan (tugas rumah, AI bebas, wajib didokumentasikan)
- **U** = skor verifikasi tanpa bantuan (20 menit di kelas, tanpa perangkat, kertas)

Soal U **lebih sederhana** dari A, tetapi menguji inti penalaran yang sama. Kalau A-nya mengerjakan inversi hiposenter 6 stasiun, U-nya cukup: *"Diberikan tiga lingkaran ini, tandai episenternya dan jelaskan mengapa kedalaman lebih sulit ditentukan daripada posisi lateral."*

**Metrik diagnostik — Rasio Retensi:**

$$R = \frac{U}{A}$$

| $R$ | Tafsir | Tindakan |
|:--|:--|:--|
| ≥ 0,80 | Terinternalisasi | — |
| 0,60 – 0,79 | Sebagian | Umpan balik tertulis |
| < 0,60 | **Tertandai** | Picu viva (Instrumen 3) |

**$R$ bukan nilai dan bukan tuduhan.** $R$ adalah pemicu percakapan. Nilai tetap datang dari $0{,}25A + 0{,}75U$.

Mengapa rasio, bukan selisih? Selisih $A-U$ menghukum mahasiswa berskor tinggi (A=95, U=75 → selisih 20) sementara memaafkan yang berskor rendah (A=60, U=40 → selisih 20) padahal yang kedua justru lebih mengkhawatirkan. Rasio menormalkan ini: 0,79 vs 0,67.

---

### Instrumen 3 — Viva terpicu (bukan menyeluruh)

Viva menyeluruh untuk 71 mahasiswa mustahil: 3 menit × 71 = 3,5 jam per putaran. Karena itu **viva hanya dijalankan pada sampel terpicu**:

- semua mahasiswa dengan $R < 0{,}60$, **ditambah**
- 15% sampel acak dari sisanya

Sampel acak itu penting: tanpanya, dipanggil viva = tuduhan. Dengan sampel acak, dipanggil viva = hal biasa.

**Format:** 5 menit, 3 pertanyaan diambil acak dari bank soal publik, **semuanya tentang pekerjaannya sendiri**:

> "Mengapa Anda memilih *corner frequency* penapis di 1 Hz?"
> "Kalau stasiun terjauh Anda dibuang, apa yang terjadi pada elips galat — membesar ke arah mana?"
> "Angka kedalaman Anda 42 km. Yakin? Apa yang paling membatasi keyakinan itu?"

**Rubrik: 0–3 per pertanyaan, total 0–9**

| Skor | Kriteria |
|:--:|:--|
| 3 | Menjelaskan sebab, mengaitkan ke fisika, sadar keterbatasan |
| 2 | Menjelaskan benar tetapi prosedural, tanpa sebab |
| 1 | Mengenali istilah, tidak bisa menjelaskan |
| 0 | Tidak mengenali pekerjaannya sendiri |

Ambang: **≥ 6 dari 9**. Di bawah itu, nilai produk (25%) dinolkan dan diberi kesempatan mengulang — bukan sanksi akademik.

**Estimasi beban nyata:** jika 20% tertandai, ± 14 orang + 10 sampel acak = 24 × 5 menit ≈ **2 jam per milestone**. Jalankan hanya pada 3 milestone besar → ± 6 jam per semester. Bisa dibagi dengan asisten praktikum.

---

### Instrumen 4 — Prediksi terkunci sebelum menghitung

Sebelum boleh menjalankan kode apa pun, mahasiswa menyetorkan prediksi numerik bertanda waktu:

> "Menurut saya beda waktu tiba S−P akan sekitar ___ detik, jadi jaraknya ± ___ km. Amplitudo di stasiun terjauh akan lebih ___ karena ___."

Lalu hitung, lalu jelaskan selisihnya.

**Metrik: Skor Kalibrasi** = proporsi prediksi yang jatuh dalam toleransi yang diumumkan.
Target milestone: **≥ 60% prediksi dalam toleransi** pada akhir semester (mulai dari ~30% di awal — kenaikannya itulah bukti belajar).

Mengapa tahan-AI: yang dinilai adalah intuisi *sebelum* alat bantu menyentuh soal. AI boleh dipakai sesudahnya untuk menjelaskan mengapa prediksinya meleset — itu justru pemakaian AI terbaik.

---

### Instrumen 5 — Perburuan galat pada keluaran AI

Berikan notebook analisis yang **dihasilkan AI dan sengaja mengandung galat masuk akal**. Tugasnya: temukan, perbaiki, jelaskan.

Contoh galat yang bisa ditanam di seismologi:
- Nyquist dilanggar — *resampling* tanpa *anti-alias filter*
- Respons instrumen tidak didekonvolusi sebelum menghitung magnitudo
- Fase yang salah dilabeli — Pn ditandai sebagai Pg
- Model kecepatan berbeda dipakai antara *forward* dan *inverse*
- Sudut *rake* memakai konvensi berbeda dari konvensi *strike*-nya
- Lingkaran jarak digambar dengan $v_P$ padahal datanya S−P

**Metrik:** $\text{Skor} = \dfrac{\text{galat ditemukan}}{\text{galat ditanam}} - 0{,}5 \times \text{(laporan galat palsu)}$

Ambang: **≥ 0,60**. Penalti positif palsu penting — mencegah strategi asal menuduh semua baris salah.

Instrumen ini istimewa: ia **sekaligus** mengukur pemahaman **dan** melatih keterampilan yang paling dibutuhkan di era AI, yaitu mengaudit keluaran mesin. Ini yang paling selaras dengan niat Anda memanfaatkan AI seluas-luasnya.

---

### Instrumen 6 — Kalibrasi ketidakpastian

Tiap angka wajib dilaporkan sebagai selang, bukan titik: "kedalaman 42 ± 12 km (selang keyakinan 80%)".

**Metrik: Laju Cakupan** = proporsi selang 80% mahasiswa yang benar-benar memuat nilai katalog.

| Laju cakupan | Tafsir |
|:--|:--|
| ± 0,80 | Terkalibrasi baik |
| ≫ 0,80 | Terlalu hati-hati — selangnya kelewat lebar |
| ≪ 0,80 | **Terlalu percaya diri** — pola khas jawaban AI yang ditelan mentah |

Poin pentingnya: selang yang sempit-tapi-salah **lebih buruk** daripada selang lebar-tapi-benar. Mahasiswa yang menyalin angka AI tanpa paham cenderung melaporkan selang sempit, karena ia tidak tahu apa yang tidak ia ketahui. Instrumen ini menangkap persis kondisi itu — dan mengajarkan sikap ilmiah yang benar sekaligus.

---

## 4. Tujuh milestone semester

Terikat pada CPMK yang sudah ditetapkan di `RPS_Seismologi_2026.md`.

| M | Minggu | CPMK | Fokus | Instrumen | Ambang lulus |
|:--:|:--:|:--:|:--|:--|:--|
| **M1** | 3 | 1 | Elastisitas, persamaan gelombang, P vs S | 2, 4 | $U \ge 60$ · $R \ge 0{,}60$ |
| **M2** | 7 | 2 | Snell, jalur sinar, fase seismik | 1, 2 | $U \ge 60$ · identifikasi fase ≥ 70% benar |
| **M3** | 8 | 1, 2, 5 | **UTS** — integratif | 2 (murni) | $\ge 60$ |
| **M4** | 10 | 3 | Respons instrumen, jaringan, DAS | 2, 5 | $U \ge 60$ · perburuan galat ≥ 0,60 |
| **M5** | 12 | 4 | Lokasi episenter–hiposenter | **1**, 2, 3, 6 | Episenter ≤ 30 km · $R \ge 0{,}60$ · viva ≥ 6/9 |
| **M6** | 14 | 4 | Magnitudo & mekanisme sumber | **1**, 2, 3, 6 | $M_L$ ± 0,3 · tipe sesar benar · viva ≥ 6/9 |
| **M7** | 15 | 5 | Statistika, monitoring, mitigasi | 3, 5 | Presentasi + viva ≥ 6/9 |
| — | 16 | 3, 4, 5 | **UAS** — integratif | 2 (murni) | $\ge 60$ |

**M5 dan M6 adalah milestone terpenting** — di sanalah data unik, viva, dan kalibrasi bertemu. Kalau waktu Anda terbatas, jalankan penuh hanya pada dua ini.

---

## 5. Papan pantau kuantitatif

Satu baris per mahasiswa, satu blok kolom per milestone. Semuanya angka, semuanya bisa di-*sort*.

| Kolom | Isi | Kegunaan |
|:--|:--|:--|
| `A` | Skor produk berbantuan (0–100) | Bobot 25% |
| `U` | Skor tanpa bantuan (0–100) | Bobot 75% |
| `R` | $U/A$ | **Pemicu viva** |
| `err_km` | Galat episenter (km) | Ketepatan objektif |
| `err_mag` | Galat magnitudo | Ketepatan objektif |
| `cal` | Laju cakupan selang | Deteksi percaya diri berlebih |
| `pred` | Skor kalibrasi prediksi | Pertumbuhan intuisi |
| `bug` | Skor perburuan galat | Kemampuan audit |
| `viva` | 0–9 | Verifikasi akhir |

**Tiga sinyal agregat yang layak Anda pantau tiap milestone:**

1. **Median $R$ kelas.** Turun tajam antar-milestone → tugasnya terlalu mudah di-*outsource*, bukan mahasiswanya memburuk.
2. **Korelasi $A$ dengan $U$.** Kelas sehat: $r \approx 0{,}6$–$0{,}8$. Kalau $r \to 0$, artefak Anda sudah **berhenti mengukur apa pun** — itu alarm paling penting di seluruh sistem.
3. **Tren `cal` dan `pred`.** Keduanya harus naik sepanjang semester. Inilah bukti kuantitatif paling jujur bahwa pemahaman benar-benar tumbuh.

Sinyal ke-2 patut digarisbawahi: ia mengukur kesehatan **instrumen Anda**, bukan mahasiswa. Tidak ada rancangan asesmen yang awet tanpa pemeriksaan diri semacam ini.

---

## 6. Anggaran waktu nyata (71 mahasiswa)

| Kegiatan | Persiapan | Pelaksanaan/semester |
|:--|:--|:--|
| Skrip penilai data unik | ± 8 jam sekali | ~0 (otomatis) |
| 6 kuis tanpa bantuan | 6 × 1 jam | 6 × 20 mnt kelas = 2 jam |
| Notebook bergalat (2 buah) | 2 × 3 jam | ~0 (otomatis) |
| Viva terpicu (3 putaran) | 2 jam bank soal | 3 × 2 jam = 6 jam |
| Papan pantau | 3 jam sekali | 6 × 30 mnt = 3 jam |
| **Total** | **± 25 jam (sekali)** | **± 11 jam/semester** |

Beban persiapan terkonsentrasi di semester pertama dan hampir seluruhnya bisa dipakai ulang. Beban pelaksanaan ± 11 jam per semester wajar untuk MK 2 SKS berisi 71 mahasiswa — dan viva bisa dibagi dengan asisten praktikum.

---

## 7. Pagar keadilan — hal yang **jangan** dilakukan

**Jangan pakai detektor teks AI.** Tingkat positif palsunya tinggi dan biasnya sistematis terhadap penulis non-penutur asli bahasa Inggris — persis mahasiswa Anda ketika menulis laporan berbahasa Inggris. Detektor semacam ini akan menuduh mahasiswa jujur, dan sekali itu terjadi kepercayaan kelas hilang permanen. Seluruh rancangan di atas sengaja **tidak memerlukan deteksi sama sekali**.

**Jangan perlakukan $R$ rendah sebagai bukti kecurangan.** $R$ rendah punya banyak sebab sah: cemas ujian, sakit, tekanan waktu, kesulitan bahasa, atau memang belum paham dan butuh bantuan. $R$ hanya memicu **percakapan**; viva yang memutuskan, dan hasil viva menentukan nilai — bukan sanksi.

**Jangan sembunyikan aturannya.** Umumkan seluruh sistem — bobot 25/75, ambang $R$, keberadaan sampel acak — di pertemuan pertama. Transparansi mengubah perilaku jauh lebih efektif daripada pengawasan diam-diam, dan menghilangkan rasa dijebak.

**Jangan menghukum pemakaian AI.** Wajibkan pendokumentasiannya, lalu nilai pemahamannya. Mahasiswa yang memakai AI dengan cerdas akan lolos verifikasi dengan mudah, dan itulah yang ingin Anda hasilkan.

---

## 8. Rencana penerapan bertahap

**Semester 1 (Gasal 2026/2027) — kalibrasi, jangan menghukum.**
Jalankan M5 dan M6 saja secara penuh. Kumpulkan sebaran $R$ kelas. **Angka ambang 0,60 di dokumen ini adalah tebakan awal saya, bukan hasil penelitian** — kohort Anda sendiri yang akan memberi tahu ambang yang benar. Semester ini $R$ hanya untuk umpan balik, tidak berkonsekuensi nilai.

**Semester 2 — aktifkan penuh.**
Terapkan ambang hasil kalibrasi ke tujuh milestone. Bobot 25/75 mulai berlaku.

**Semester 3 — perluas.**
Bagikan skrip penilai dan bank soal viva ke MK lain di prodi. Rancangan ini tidak khas seismologi; yang khas hanya toleransi numeriknya.

---

## 9. Jawaban langsung atas kekhawatiran Anda

> *"Mereka kelihatan bisa menjawab semua, tugas sempurna, tapi sejatinya doing nothing dan know nothing."*

Dengan rancangan ini, keadaan tersebut menjadi **mustahil disembunyikan dan tidak perlu dituduhkan**:

- Tugasnya boleh sempurna — bobotnya cuma 25%.
- Verifikasi 20 menit tanpa perangkat akan menampakkannya, karena 75% nilainya ada di sana.
- Angka atas data uniknya tidak akan cocok dengan katalog, karena AI tidak tahu event mana miliknya.
- Selang ketidakpastiannya akan terlalu sempit, karena ia tidak tahu apa yang tidak ia ketahui.
- Dan pada viva, ia tidak akan bisa menjelaskan mengapa ia memilih *corner frequency* itu.

Anda tidak perlu menangkap siapa pun. Anda hanya perlu **berhenti menerima artefak sebagai bukti** — dan sistem ini yang menyediakan buktinya.

---

<sub>Disusun untuk Seismologi PAGF262413 dan Praktikum Seismologi PAGF262412, Program Studi Sarjana Geofisika FMIPA UGM, Kurikulum 2026.</sub>
