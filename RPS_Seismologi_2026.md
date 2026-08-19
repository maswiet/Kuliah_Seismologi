# Rencana Pembelajaran Semester — Seismologi (PAGF262413)

**Program Studi Sarjana Geofisika, Departemen Fisika, FMIPA UGM · Kurikulum 2026**
Semester IV (wajib) · 2 SKS · Senin 07:15–08:55, Ruang Kelas 209
Prasyarat: Gelombang (`PADF262208`) dan Mekanika Medium Kontinu (`PAGF262307`)
Ko-rekuisit: Praktikum Seismologi (`PAGF262412`, 1 SKS)

Dokumen ini membedah 8 pokok bahasan silabus Kurikulum 2026 menjadi **14 minggu materi + 2 minggu ujian**, dengan bacaan primer dari Shearer (2019) dan Stein & Wysession (2003), diperkuat sumber daring.

---

## 1. Kalibrasi kedalaman — baca ini dulu

Kedua buku acuan **ditulis untuk jenjang di atas Semester IV S1**. Shearer menyasar pascasarjana; Stein & Wysession menyasar *advanced undergraduate* dan pascasarjana tahun pertama. Karena itu penugasan bacaan di bawah bersifat **selektif per subbab**, bukan per bab, dengan aturan:

| Peran | Buku | Cara pakai |
|:--|:--|:--|
| **Naratif utama** | Stein & Wysession | Bacaan wajib mahasiswa. Gaya penyajiannya lebih landai, banyak gambar dan konteks tektonik. |
| **Ketegasan matematis** | Shearer | Rujukan penurunan rumus dan latihan. Diberikan sebagai bacaan wajib hanya pada subbab yang ditandai. |
| **Data dan praktik terkini** | Sumber daring | Menutup materi yang tidak ada di kedua buku (lihat §6). |

**Subbab bertanda † di Shearer dilewati seluruhnya** — penulisnya sendiri menandainya sebagai materi lanjut. Ini mencakup 3.7 (metode komputasi seismogram sintetik), 6.5 (propagator matrix), 6.6.3–6.6.4 (absorption band, standard linear solid), 7.7.1 (adjoint operator), dan 9.6.1.

Tiga bab Shearer juga **di luar cakupan MK ini** dan sebaiknya diarahkan ke MK lanjutan: Bab 7 (Reflection Seismology) → *Metode Seismik I & II*; Bab 13 (Anisotropy) dan 5.5 (tomografi 3-D) → topik skripsi atau S2.

> Akses legal kedua buku: koleksi Perpustakaan FMIPA/UGM dan langganan e-book Perpustakaan UGM.

---

## 2. Peta CPL → CPMK

Kurikulum 2026 memakai 4 Pilar CPL. Lima **CPMK** berikut menerjemahkannya ke tingkat mata kuliah:

| CPMK | Rumusan | Menopang CPL | Bloom | Minggu |
|:--|:--|:--|:--|:--|
| **CPMK1** | Menjelaskan konsep tegangan–regangan dan elastisitas, serta menurunkan persamaan gelombang seismik dan membedakan karakter gelombang badan (P, S) dan permukaan (Love, Rayleigh) | CPL2.3, CPL2.4 | C2–C3 | 2, 3, 5 |
| **CPMK2** | Menganalisis perambatan gelombang seismik dalam medium berlapis dan bumi berbentuk bola, serta mengidentifikasi fase seismik gempa lokal, regional, dan teleseismik | CPL2.3, CPL2.4 | C4 | 4, 6, 7 |
| **CPMK3** | Menjelaskan prinsip kerja dan fungsi respons instrumen seismik, serta arsitektur jaringan seismik modern termasuk DAS | CPL2.3, CPL4.1.4 | C2–C3 | 9, 10 |
| **CPMK4** | Menghitung parameter sumber gempa (lokasi, magnitudo, energi, intensitas) dari data seismogram riil dan menafsirkan mekanisme sumbernya | CPL3.1, CPL3.2, CPL4.1.5 | C3–C4, P4 | 11, 12, 13, 14 |
| **CPMK5** | Mengevaluasi statistika dan risiko kegempaan serta peran sistem monitoring dan peringatan dini bagi mitigasi bencana di Indonesia | CPL1.2, CPL2.6, CPL3.4 | C5, A4–A5 | 1, 15 |

Bobot pilar (mengikuti analisis korelasi Kurikulum 2026): teori kuat pada **CPL2**, sedang pada **CPL1** dan **CPL3**, lemah pada **CPL4.1** — beban CPL4.1 dipikul praktikum.

---

## 3. Peta 16 minggu

| Mg | Tema | PB | CPMK | Bloom |
|:--:|:--|:--:|:--:|:--:|
| 1 | Ruang lingkup, sejarah, dan peran seismologi | 1 | 5 | C2, A4 |
| 2 | Tegangan, regangan, dan elastisitas | 1→2 | 1 | C2–C3 |
| 3 | Persamaan gelombang seismik; gelombang P dan S | 2 | 1 | C3 |
| 4 | Hukum Snell, jalur sinar, dan *head wave* | 2 | 2 | C3–C4 |
| 5 | Koefisien refleksi–transmisi; gelombang permukaan dan dispersi | 2 | 1 | C3–C4 |
| 6 | Struktur dalam bumi dan fase seismik global | 3 | 2 | C4 |
| 7 | Gempa lokal–regional–teleseismik; atenuasi dan mikroseismik | 3 | 2 | C4 |
| **8** | **Ujian Tengah Semester** | 1–3 | 1, 2, 5 | C2–C4 |
| 9 | Seismometer sebagai osilator harmonik teredam | 4 | 3 | C3 |
| 10 | Jaringan seismik, perekaman digital, dan DAS | 4 | 3 | C2–C3 |
| 11 | Anatomi seismogram dan pemrosesan sinyal digital | 5 | 4 | C4, P4 |
| 12 | Penentuan episenter dan hiposenter | 6 | 4 | C3–C4, P4 |
| 13 | Magnitudo, momen, energi, dan intensitas | 6 | 4 | C3–C4 |
| 14 | Mekanisme sumber: bidang sesar, *first motion*, *beach ball* | 7 | 4 | C4 |
| 15 | Tensor momen, statistika gempa, monitoring dan mitigasi | 7→8 | 4, 5 | C5, A5 |
| **16** | **Ujian Akhir Semester** | 4–8 | 3, 4, 5 | C3–C5 |

PB = pokok bahasan silabus Kurikulum 2026 (1 Pendahuluan · 2 Gelombang Seismik · 3 Perambatan & Kejadian Gempa · 4 Instrumentasi · 5 Seismogram dan Anatominya · 6 Parameter Sumber · 7 Mekanisme Sumber · 8 Mitigasi Bencana).

---

## 4. Rincian mingguan

Singkatan: **[Sh]** = Shearer (2019, ed. ke-3) · **[SW]** = Stein & Wysession (2003), nomor halaman mengikuti TOC aslinya.

---

### Minggu 1 — Ruang lingkup, sejarah, dan peran seismologi
**PB 1 · CPMK5 · C2, A4**

Definisi dan ruang lingkup seismologi; posisinya dalam geofisika; sejarah perkembangan teori elastisitas dan instalasi seismograf; model dalam seismologi (maju vs balik); peran seismologi dalam kebencanaan, eksplorasi, pemantauan uji nuklir, dan pembangunan berkelanjutan.

- **[SW]** 1.1.1 *Overview* (h. 1), 1.1.2 *Models in seismology* (h. 5), 1.2 *Seismology and society* (h. 9) — khususnya 1.2.1 bahaya & risiko, 1.2.5 *forecasting*, 1.2.6 *prediction*, 1.2.7 *real-time warnings*, 1.2.8 pemantauan nuklir
- **[Sh]** 1.1 *A Brief History of Seismology*, 1.1.1 *Recent Advances*
- **Daring**: peta gempa waktu-nyata [USGS](https://earthquake.usgs.gov/earthquakes/map/) dan [BMKG](https://www.bmkg.go.id/); materi kelas [EarthScope](https://www.iris.edu/hq/inclass/search)

*Aktivitas*: diskusi pembuka — mahasiswa menelusuri satu gempa merusak di Indonesia dan mengidentifikasi peran seismologi di setiap fase bencana (pra, saat, pasca). Menanamkan CPL1.2 sejak pertemuan pertama.

---

### Minggu 2 — Tegangan, regangan, dan elastisitas
**PB 1→2 · CPMK1 · C2–C3**

Tensor tegangan dan traksi; sumbu utama; tegangan deviatorik; tensor regangan; hubungan tegangan–regangan linear (Hukum Hooke); modulus elastik dan satuannya; tegangan geser maksimum dan kaitannya dengan pensesaran.

- **[Sh]** 2.1 *The Stress Tensor* (termasuk contoh 2.1.1, 2.1.3), 2.2 *The Strain Tensor* (2.2.2 contoh regangan untuk gelombang seismik), 2.3 *The Linear Stress–Strain Relationship*
- **[SW]** 2.3.1–2.3.10 (h. 38–51), terutama 2.3.5 *Maximum shear stress and faulting* (h. 43) dan 2.3.9 *Constitutive equations* (h. 48)

*Aktivitas*: Latihan Shearer Bab 2. Ini titik sambung langsung dengan prasyarat Mekanika Medium Kontinu — buka dengan kuis diagnostik singkat untuk mengukur retensi.

---

### Minggu 3 — Persamaan gelombang seismik; gelombang P dan S
**PB 2 · CPMK1 · C3**

Persamaan momentum; penurunan persamaan gelombang seismik; potensial skalar dan vektor (dekomposisi Helmholtz); gelombang bidang dan gelombang bola; polarisasi gelombang P dan S; kecepatan gelombang sebagai fungsi sifat medium; energi dalam gelombang bidang.

- **[Sh]** 3.1 *Introduction: The Wave Equation*, 3.2 *The Momentum Equation*, 3.3 *The Seismic Wave Equation* + 3.3.1 *Potentials*, 3.4 *Plane Waves*, 3.5 *Polarizations of P- and S-Waves*, 3.6 *Spherical Waves* — **lewati 3.7†**
- **[SW]** 2.2 *Waves on a string* (h. 29, analogi 1-D pengantar), 2.4.1 *The seismic wave equation* (h. 53), 2.4.4 *P and S waves* (h. 56), 2.4.5 *Energy in a plane wave* (h. 61)

*Aktivitas*: demonstrasi Python — animasi polarisasi P vs S. Bahan siap pakai di [Seismo-Live](https://seismo-live.github.io/).

---

### Minggu 4 — Hukum Snell, jalur sinar, dan *head wave*
**PB 2 · CPMK2 · C3–C4**

Hukum Snell dan sudut kritis; parameter sinar dan *slowness*; jalur sinar dalam model berlapis mendatar; kurva waktu tempuh $T(X)$ dan fungsi $\tau(p)$; *low-velocity zone*; gelombang kepala (*head wave*) dan dasar seismik refraksi; prinsip Fermat dan Huygens; pemandu gelombang (*waveguide*).

- **[Sh]** 4.1 *Snell's Law*, 4.2 *Ray Paths for Laterally Homogeneous Models* (+ contoh 4.2.1), 4.3 *Travel Time Curves and Delay Times* (4.3.2 fungsi $\tau(p)$, 4.3.4 *Low-Velocity Zones*), 4.4 *Summary of 1-D Ray Tracing Equations* — **lewati 4.6†**
- **[SW]** 2.5.3–2.5.10 (h. 65–72): sudut datang, hukum Snell, sudut kritis, parameter sinar & *slowness*, *waveguide*, Fermat, Huygens & difraksi; 3.2.1 *Flat layer method* (h. 120) untuk *head wave*

*Aktivitas*: hitung kedalaman Moho dari kurva waktu tempuh refraksi dua lapis — jembatan langsung ke Praktikum Acara 2.

---

### Minggu 5 — Koefisien refleksi–transmisi; gelombang permukaan dan dispersi
**PB 2 · CPMK1 · C3–C4**

Energi gelombang seismik dan penyebaran geometris; koefisien refleksi dan transmisi SH; insidensi vertikal; ketergantungan pada sudut sinar; gelombang Rayleigh pada *halfspace* homogen; gelombang Love pada lapisan di atas *halfspace*; dispersi, kecepatan fase vs kecepatan grup.

- **[Sh]** 6.1 *Energy in Seismic Waves*, 6.2 *Geometrical Spreading in 1-D Velocity Models*, 6.3.1–6.3.5 koefisien refleksi/transmisi; 8.1 *Love Waves* (+ 8.1.2 contoh dispersi Love), 8.2 *Rayleigh Waves*, 8.3 *Dispersion* — **lewati 6.5†**
- **[SW]** 2.6.1–2.6.6 (h. 75–81), 2.7.2 *Rayleigh waves* (h. 87), 2.7.3 *Love waves* (h. 90), 2.7.4 *Love wave dispersion* (h. 91), 2.8.1 *Phase and group velocity* (h. 93), 2.8.2 *Dispersive signals* (h. 94)

*Pengayaan opsional*: 2.8.4 *Tsunami dispersion* (h. 99) — relevansi tinggi untuk Indonesia, cocok jadi topik tugas.

---

### Minggu 6 — Struktur dalam bumi dan fase seismik global
**PB 3 · CPMK2 · C4**

Penjejakan sinar dalam bumi bola dan transformasi *earth-flattening*; distribusi kecepatan dan inversi kurva waktu tempuh; tata nama fase seismik (fase kerak: Pg, Pn, PmP; fase bumi utuh: P, PP, PcP, PKP, S, SS, ScS); struktur mantel atas, mantel bawah, dan inti; model referensi PREM.

- **[Sh]** 4.5 *Spherical Earth Ray Tracing* + 4.5.1 *Earth-Flattening Transformation*, 4.7 *Ray Nomenclature* (4.7.1 fase kerak, 4.7.2 fase bumi utuh), 4.8 *Global Body Wave Observations*, Appendix A *The PREM Model*
- **[SW]** 3.4.1–3.4.3 (h. 157–161), 3.5.1 *Body wave phases* (h. 163), 3.5.2 *Core phases* (h. 166), 3.5.3 *Upper mantle structure* (h. 169), 3.5.4 *Lower mantle structure* (h. 171), 3.5.5 *Visualizing body waves* (h. 174)

*Aktivitas*: latihan pelabelan fase pada rekaman teleseismik riil. Unduh lewat [IRIS/EarthScope DMC](https://ds.iris.edu/ds/nodes/dmc/), plot kurva waktu tempuh dengan `obspy.taup`.

---

### Minggu 7 — Gempa lokal, regional, teleseismik; atenuasi dan mikroseismik
**PB 3 · CPMK2 · C4**

Pembedaan gempa lokal, regional, dan teleseismik dari jarak episentral dan tampilan seismogram; pengaruh struktur bumi terhadap sinyal; atenuasi intrinsik vs penyebaran geometris, hamburan, dan *multipathing*; faktor kualitas $Q$ dan $t^*$; gelombang mantel dan kanal; derau latar bumi dan mikroseismik.

- **[Sh]** 6.6 *Attenuation* (6.6.1 contoh, 6.6.2 $t^*$ dan dispersi kecepatan, 6.6.5 atenuasi bumi, 6.6.6 mengamati $Q$) — **lewati 6.6.3†, 6.6.4†**; 12.1 *Earth's Background Noise*, 12.2 *Cross-Correlation Analysis of Ambient Noise*
- **[SW]** 3.7.1 *Wave attenuation* (h. 185), 3.7.2 *Geometric spreading* (h. 187), 3.7.3 *Multipathing* (h. 187), 3.7.4 *Scattering* (h. 189), 3.7.5 *Intrinsic attenuation* (h. 190), 3.7.6 *Quality factor Q* (h. 192); 5.4.2 *Earthquakes in subducting slabs* (h. 312) sebagai konteks Indonesia

*Aktivitas*: bandingkan tiga seismogram — gempa lokal Yogyakarta, regional Jawa, dan teleseismik — dari stasiun yang sama.

---

### Minggu 8 — **UJIAN TENGAH SEMESTER**
Cakupan Minggu 1–7 (PB 1–3) · Menguji CPMK1, CPMK2, CPMK5 · Bobot **30%**

Kisi-kisi ada di §5.

---

### Minggu 9 — Seismometer sebagai osilator harmonik teredam
**PB 4 · CPMK3 · C3**

Seismometer sebagai sistem massa–pegas–peredam; persamaan gerak dan solusinya; perioda alami dan faktor redaman; fungsi respons instrumen dan kurva respons amplitudo–fase; kalibrasi; perbedaan seismograf perioda pendek, perioda panjang, dan *broadband*; masalah perioda dan seismograf modern.

- **[Sh]** 11.1 *Seismometer as Damped Harmonic Oscillator*, 11.2 *Short-Period and Long-Period Seismograms*, 11.3 *Modern Seismographs*
- **[SW]** 6.6.2 *The damped harmonic oscillator* (h. 398), 6.6.3 *Earth noise* (h. 400), 6.6.4 *Seismometers and seismographs* (h. 400), 6.6.5 *Digital recording* (h. 405)

*Aktivitas*: plot kurva respons instrumen dari file StationXML riil menggunakan ObsPy; tunjukkan efek dekonvolusi respons pada seismogram.

---

### Minggu 10 — Jaringan seismik, perekaman digital, dan DAS
**PB 4 · CPMK3 · C2–C3**

Jenis jaringan seismik: global, regional, lokal, dan *array*; standar data dan metadata (miniSEED, StationXML, kode jaringan FDSN); jaringan Indonesia (InaTEWS, InaSIS BMKG); teknologi mutakhir **DAS (*Distributed Acoustic Sensing*)** — prinsip hamburan Rayleigh pada serat optik, kelebihan (rapat spasial, memanfaatkan serat gelap) dan keterbatasannya (satu komponen, sensitif regangan sepanjang serat).

- **[SW]** 6.6.6 *Types of networks* (h. 407), 6.6.7 *Global networks* (h. 407), 6.6.8 *Arrays* (h. 409), 6.6.9 *Regional networks* (h. 410)
- **Daring wajib** — DAS tidak dibahas di kedua buku (lihat §6): Zhan (2020), *Distributed Acoustic Sensing Turns Fiber-Optic Cables into Sensitive Seismic Antennas*, **Seismological Research Letters** 91(1); Lindsey & Martin (2021), *Fiber-Optic Seismology*, **Annual Review of Earth and Planetary Sciences** 49
- **Daring**: [daftar jaringan FDSN](https://www.fdsn.org/networks/), [InaTEWS BMKG](https://inatews.bmkg.go.id/)

*Aktivitas*: kuliah tamu atau demonstrasi rekaman DAS. Materi paling "kekinian" dalam MK ini — pemicu minat riset yang baik.

---

### Minggu 11 — Anatomi seismogram dan pemrosesan sinyal digital
**PB 5 · CPMK4 · C4, P4**

Komponen seismogram Z, N, E dan rotasi ke R, T; identifikasi fase P, S, dan gelombang permukaan; karakteristik amplitudo, frekuensi, dan durasi sinyal; deret dan transformasi Fourier; sistem linear, konvolusi dan dekonvolusi; pencuplikan, aliasing, DFT dan FFT; penapisan (*filtering*); *stacking* dan nisbah sinyal–derau.

- **[SW]** 6.2 *Fourier analysis* (h. 369), 6.3.1 *Basic model* (h. 377), 6.3.2 *Convolution and deconvolution modeling* (h. 379), 6.3.4 *Correlation* (h. 383), 6.4.1 *Sampling of continuous data* (h. 385), 6.4.2 *The discrete Fourier transform* (h. 387), 6.4.4 *FFT* (h. 389), 6.4.5 *Digital convolution* (h. 390), 6.5 *Stacking* (h. 391)
- **[Sh]** Appendix E *Time Series and Fourier Transforms* (E.1 Konvolusi, E.2 Transformasi Fourier)
- **Rujukan khas**: Kulhánek, *Anatomy of Seismograms* — atlas fase; dan [NMSOP-2](https://gfzpublic.gfz.de/pubman/item/item_43728) Bab 11 tentang tata cara *picking*

*Aktivitas*: pertemuan paling terintegrasi dengan praktikum — sinkronkan dengan Acara 1 dan 2.

---

### Minggu 12 — Penentuan episenter dan hiposenter
**PB 6 · CPMK4 · C3–C4, P4**

Selisih waktu tiba S–P dan penentuan jarak episentral; **metode lingkaran** (grafis, tiga stasiun); formulasi masalah balik; **metode Geiger** dan inversi iteratif; matriks turunan parsial dan matriks kovariansi; sumber galat (model kecepatan, *pick*, geometri jaringan) dan elips kesalahan; *trade-off* kedalaman–waktu asal; metode lokasi relatif dan *double-difference*.

- **[SW]** 7.2.1 *Theory* (h. 416), 7.2.2 *Earthquake location for a homogeneous medium* (h. 419), 7.2.3 *Errors* (h. 420), 7.2.4 *Earthquake location for more complex geometries* (h. 422)
- **[Sh]** 5.6 *Earthquake Location*, 5.6.1 *Iterative Location Methods*, 5.6.2 *Relative Event Location Methods* — **lewati 5.5 (tomografi 3-D)**

*Aktivitas*: sinkron dengan Praktikum Acara 3. Bandingkan hasil hitungan mahasiswa dengan katalog [ISC](http://www.isc.ac.uk/) dan BMKG untuk gempa yang sama.

---

### Minggu 13 — Magnitudo, momen, energi, dan intensitas
**PB 6 · CPMK4 · C3–C4**

Skala magnitudo $M_L$, $m_b$, $M_S$, dan saturasinya; momen seismik $M_0$ dan magnitudo momen $M_W$; spektrum sumber, frekuensi sudut, dan hukum penskalaan diri-serupa; *stress drop*; energi seismik teradiasi dan efisiensi; skala intensitas (MMI, MMI-BMKG) serta hubungan intensitas–percepatan tanah dan dampak kerusakan.

- **[SW]** 4.6.1 *Magnitudes and moment* (h. 263), 4.6.2 *Source spectra and scaling laws* (h. 266), 4.6.3 *Stress drop and earthquake energy* (h. 269)
- **[Sh]** 9.5 *Stress Drop* (+ 9.5.1 contoh, 9.5.2 penskalaan diri-serupa), 9.6 *Radiated Seismic Energy* (**lewati 9.6.1†**), 9.7 *Earthquake Magnitude*, 9.7.3 *The Intensity Scale*

*Aktivitas*: sinkron dengan Praktikum Acara 4. Diskusi kritis — mengapa media dan sebagian instansi masih memakai "skala Richter" padahal $M_L$ jenuh di atas ~6,5?

---

### Minggu 14 — Mekanisme sumber: bidang sesar, *first motion*, dan *beach ball*
**PB 7 · CPMK4 · C4**

Geometri sesar (*strike*, *dip*, *rake*) dan tipe sesar; pola radiasi gelombang badan untuk sumber *double-couple*; polaritas gerakan awal (*first motion*) P; proyeksi stereografi bola fokal dan pembacaan *beach ball*; ambiguitas bidang sesar dan bidang bantu; fungsi Green dan pengantar tensor momen.

- **[SW]** 4.2.1 *Fault geometry* (h. 217), 4.2.2 *First motions* (h. 219), 4.2.3 *Body wave radiation patterns* (h. 220), 4.2.4 *Stereographic fault plane representation* (h. 222)
- **[Sh]** 9.1 *Green's Functions and the Moment Tensor* (pengantar saja), 9.2 *Earthquake Faults*, 9.3 *Radiation Patterns and Beach Balls* + 9.3.1 *Example: Plotting a Focal Mechanism*

*Aktivitas*: sinkron dengan Praktikum Acara 5. Bandingkan solusi manual mahasiswa dengan katalog [Global CMT](https://www.globalcmt.org/CMTsearch.html) dan [IRIS SPUD MT](https://ds.iris.edu/spud/momenttensor).

---

### Minggu 15 — Tensor momen, statistika gempa, monitoring dan mitigasi
**PB 7→8 · CPMK4, CPMK5 · C5, A5**

Tensor momen: gaya ekuivalen, *double couple*, komponen isotropik dan CLVD, penafsirannya; sumber non-*double-couple* (gempa vulkanik, ledakan); hubungan frekuensi–magnitudo Gutenberg–Richter dan nilai-$b$; hukum Omori dan gempa susulan; probabilitas kejadian gempa dan siklus gempa; sistem monitoring dan peringatan dini; studi kasus Indonesia.

- **[SW]** 4.4.1 *Equivalent forces* (h. 239), 4.4.4 *Double couples* (h. 242), 4.4.5 *Earthquake moment tensors* (h. 242), 4.4.6 *Isotropic and CLVD moment tensors* (h. 245), 4.4.8 *Interpretation of moment tensors* (h. 249); 4.7.1 *Frequency–magnitude relations* (h. 274), 4.7.2 *Aftershocks* (h. 277), 4.7.3 *Earthquake probabilities* (h. 278)
- **[Sh]** 9.2.1 *Non-Double-Couple Sources*, 9.7.1 *The b-Value* + 9.7.2 contoh; 10.1 *The Earthquake Cycle*, 10.2 *Earthquake Triggering*, 10.3 *Searching for Precursors*, 10.4 *Are Earthquakes Unpredictable?*
- **Daring**: [InaTEWS BMKG](https://inatews.bmkg.go.id/), [USGS ShakeAlert](https://earthquake.usgs.gov/), peta bahaya gempa nasional (Pusgen/PuSGeN, Kementerian PU)

*Aktivitas penutup*: presentasi kelompok studi kasus — Yogyakarta 2006, Palu–Donggala 2018, Lombok 2018, Cianjur 2022, atau Mentawai 2010. Tiap kelompok wajib menyertakan mekanisme sumber, statistik gempa susulan, dan evaluasi kinerja peringatan dini. Inilah asesmen utama untuk **CPL1.2 (A5)** dan **CPL3.4**.

---

### Minggu 16 — **UJIAN AKHIR SEMESTER**
Cakupan Minggu 9–15 (PB 4–8), dengan konsep PB 1–3 sebagai prasyarat · Menguji CPMK3, CPMK4, CPMK5 · Bobot **35%**

---

## 5. Kisi-kisi ujian

### UTS (Minggu 8) — 100 poin, 100 menit

| Bagian | Materi | CPMK | Bloom | Poin |
|:--|:--|:--:|:--:|:--:|
| A. Konseptual singkat | Ruang lingkup, sejarah, peran seismologi; definisi P/S/Love/Rayleigh | 5, 1 | C2 | 20 |
| B. Hitungan elastisitas | Tensor tegangan/regangan, sumbu utama, modulus elastik | 1 | C3 | 20 |
| C. Penjejakan sinar | Snell, parameter sinar, kurva $T(X)$, kedalaman lapis dari data refraksi | 2 | C3 | 25 |
| D. Analisis fase | Identifikasi fase pada seismogram teleseismik; penalaran dari kurva waktu tempuh | 2 | C4 | 25 |
| E. Esai integratif | Menghubungkan atenuasi/struktur bumi dengan tampilan seismogram di Indonesia | 2, 5 | C4 | 10 |

### UAS (Minggu 16) — 100 poin, 120 menit

| Bagian | Materi | CPMK | Bloom | Poin |
|:--|:--|:--:|:--:|:--:|
| A. Instrumentasi | Respons seismometer, redaman, jenis jaringan, DAS | 3 | C2–C3 | 20 |
| B. Sinyal digital | Fourier, aliasing/Nyquist, konvolusi–dekonvolusi, penapisan | 4 | C3 | 15 |
| C. Lokasi gempa | Metode lingkaran dan satu iterasi Geiger; analisis galat | 4 | C3–C4 | 25 |
| D. Magnitudo & energi | $M_0$, $M_W$, *stress drop*, saturasi skala magnitudo | 4 | C3–C4 | 15 |
| E. Mekanisme sumber | Membaca *beach ball*, menentukan tipe sesar, menafsirkan tensor momen | 4 | C4 | 15 |
| F. Esai mitigasi | Evaluasi nilai-$b$/gempa susulan dan kinerja peringatan dini pada satu kasus | 5 | C5 | 10 |

---

## 6. Sumber daring dan celah yang ditutupnya

Kedua buku acuan terbit 2003 dan 2019, sehingga ada materi Kurikulum 2026 yang **tidak tercakup** dan wajib diambil dari sumber daring:

| Celah | Ada di buku? | Sumber pengganti |
|:--|:--|:--|
| **DAS** (*Distributed Acoustic Sensing*) | Tidak, di keduanya | Zhan (2020) *SRL* 91(1); Lindsey & Martin (2021) *Annu. Rev. Earth Planet. Sci.* 49 |
| **Jaringan & data Indonesia** | Tidak | [BMKG](https://www.bmkg.go.id/), [InaTEWS](https://inatews.bmkg.go.id/) |
| **Standar data modern** (miniSEED, StationXML, FDSN web service) | Sebagian, sudah usang di [SW] | [FDSN](https://www.fdsn.org/networks/), [IRIS/EarthScope DMC](https://ds.iris.edu/ds/nodes/dmc/) |
| **Praktik observatori & tata cara *picking*** | Ringkas | [NMSOP-2](https://gfzpublic.gfz.de/pubman/item/item_43728), GFZ — akses terbuka |
| **Perangkat komputasi** | [Sh] Appendix D (Python) saja | [ObsPy](https://docs.obspy.org/), [Seismo-Live](https://seismo-live.github.io/) |
| **Katalog gempa & mekanisme** | Tidak | [USGS](https://earthquake.usgs.gov/earthquakes/map/), [ISC](http://www.isc.ac.uk/), [Global CMT](https://www.globalcmt.org/CMTsearch.html), [IRIS SPUD MT](https://ds.iris.edu/spud/momenttensor) |
| **Bahan ajar visual siap pakai** | — | [EarthScope Education](https://www.iris.edu/hq/inclass/search) |

---

## 7. Sistem penilaian

| Komponen | Bobot | CPMK yang diukur |
|:--|:--:|:--|
| Ujian Tengah Semester | 30% | CPMK1, CPMK2, CPMK5 |
| Ujian Akhir Semester | 35% | CPMK3, CPMK4, CPMK5 |
| Tugas dan kuis (min. 5 kali) | 20% | CPMK1–CPMK4 |
| Presentasi studi kasus (Minggu 15) | 10% | CPMK5 |
| Partisipasi dan keaktifan | 5% | CPL1.1 |

Nilai Praktikum Seismologi (`PAGF262412`) dihitung terpisah sebagai MK 1 SKS tersendiri.

**Titik sinkronisasi teori ↔ praktikum:**

| Acara Praktikum | Kuliah penopang |
|:--|:--|
| 1. Dasar seismogram & pemrosesan sinyal digital | Minggu 11 |
| 2. Identifikasi fase & waktu tiba | Minggu 6, 11 |
| 3. Episenter & hiposenter (lingkaran, inversi) | Minggu 12 |
| 4. Magnitudo & energi | Minggu 13 |
| 5. Mekanisme fokus | Minggu 14 |

Praktikum sebaiknya berjalan **1–2 minggu di belakang** kuliah teori pada topik yang sama, agar landasan konseptual sudah terbentuk sebelum pengolahan data riil.

---

## 8. Daftar acuan

**Wajib**

1. Shearer, P. M. (2019). *Introduction to Seismology* (3rd ed.). Cambridge University Press.
2. Stein, S., & Wysession, M. (2003). *An Introduction to Seismology, Earthquakes, and Earth Structure*. Blackwell Publishing.
3. Havskov, J., & Alguacil, G. (2016). *Instrumentation in Earthquake Seismology* (2nd ed.). Springer.
4. Kulhánek, O. (1990). *Anatomy of Seismograms*. Elsevier.

**Praktikum**

5. Bormann, P. (Ed.). (2012). *New Manual of Seismological Observatory Practice (NMSOP-2)*. GFZ.
6. Suryanto, W. (2026). *Modul Praktikum Seismologi*. Program Studi Geofisika FMIPA UGM.

**Pendukung**

7. Båth, M. (1979). *Introduction to Seismology*. Birkhäuser Verlag.
8. Zhan, Z. (2020). Distributed acoustic sensing turns fiber-optic cables into sensitive seismic antennas. *Seismological Research Letters*, 91(1).
9. Lindsey, N. J., & Martin, E. R. (2021). Fiber-optic seismology. *Annual Review of Earth and Planetary Sciences*, 49.

---

<sub>Disusun untuk Kurikulum 2026, Program Studi Sarjana Geofisika FMIPA UGM.</sub>
