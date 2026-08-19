# Minggu 2 — Tegangan, Regangan, dan Elastisitas

**Seismologi `PAGF262413`** · Senin 07:15–08:55, Ruang Kelas 209
Pokok Bahasan 1→2 · **CPMK1** · Bloom **C2–C3**

> **Sasaran.** Mahasiswa dapat (a) menuliskan tensor tegangan dan menjelaskan makna tiap komponennya, (b) menghitung sumbu utama tegangan, (c) menghubungkan tegangan dan regangan lewat Hukum Hooke serta menyebut modulus elastik yang berlaku, dan (d) menjelaskan mengapa tegangan geser maksimum menentukan di mana batuan pecah.

**Kuis diagnostik 10 menit di awal kelas.** Materi ini bersambung langsung dengan prasyarat Mekanika Medium Kontinu (`PAGF262307`). Ukur dulu apa yang masih tersisa sebelum melanjutkan — jangan berasumsi.

---

## 0 · Pembuka: mengapa bumi bisa mengantarkan gelombang · 10 menit

Air tidak mengantarkan gelombang S. Batuan bisa. Perbedaannya satu: batuan melawan **perubahan bentuk**, bukan hanya perubahan volume.

Seluruh seismologi berdiri di atas satu sifat itu. Dan untuk menyatakannya secara kuantitatif, kita memerlukan tensor.

*Tanyakan sebelum menjelaskan:* mengapa gelombang S tidak menembus inti luar bumi? Jawabannya sudah ada di kalimat pertama — dan mereka akan memakainya lagi di Minggu 6.

---

## 1 · Tensor tegangan · 25 menit

Gaya per satuan luas pada suatu bidang bergantung pada **arah bidang itu**. Karena itu tegangan bukan skalar dan bukan vektor, melainkan **tensor orde dua** dengan sembilan komponen:

24973\sigma_{ij} = \begin{pmatrix} \sigma_{11} & \sigma_{12} & \sigma_{13} \\ \sigma_{21} & \sigma_{22} & \sigma_{23} \\ \sigma_{31} & \sigma_{32} & \sigma_{33} \end{pmatrix}24973

Indeks pertama menyatakan **normal bidang**, indeks kedua menyatakan **arah gaya**. Diagonalnya tegangan normal, sisanya tegangan geser. Kesetimbangan momen memaksa $\sigma_{ij} = \sigma_{ji}$, sehingga hanya **enam** komponen yang bebas.

### Traksi

Vektor traksi pada bidang bernormal $\hat{n}$ adalah $T_i = \sigma_{ij} n_j$. Inilah yang benar-benar dirasakan bidang itu.

### Sumbu utama

Selalu ada orientasi di mana seluruh komponen geser lenyap. Arah itu adalah **vektor eigen** dari $\sigma_{ij}$, dan nilai eigennya adalah tegangan utama $\sigma_1 \ge \sigma_2 \ge \sigma_3$.

Ini bukan latihan aljabar. Sumbu utama itulah yang menentukan **orientasi sesar** yang akan terbentuk — dan di Minggu 14 kalian akan membacanya kembali dari bola fokal.

### Tegangan deviatorik

24973\sigma_{ij}^{\text{dev}} = \sigma_{ij} - \frac{1}{3}\sigma_{kk}\,\delta_{ij}24973

Bagian isotropiknya menekan batuan tanpa mengubah bentuk; bagian deviatoriknya yang membuatnya pecah. Pada kedalaman 10 km tekanan litostatik sekitar 270 MPa, sedangkan *stress drop* gempa hanya 1–10 MPa (Minggu 13). **Gempa adalah riak kecil di atas tekanan yang jauh lebih besar.**

---

## 2 · Tensor regangan · 20 menit

24973\varepsilon_{ij} = \frac{1}{2}\left( \frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i} \right)24973

Simetrisasi itu penting: bagian antisimetrik dari gradien perpindahan adalah **rotasi benda tegar**, yang tidak menegangkan apa pun.

**Besaran regangan pada gelombang seismik sangat kecil.** Untuk gempa jauh, regangannya berorde $10^{-9}$ sampai $10^{-6}$. Di rentang itu batuan berperilaku **linear sempurna** — dan itulah izin yang memungkinkan seluruh kerangka konvolusi di Minggu 11 berlaku.

---

## 3 · Hukum Hooke dan modulus elastik · 25 menit

24973\sigma_{ij} = c_{ijkl}\,\varepsilon_{kl}24973

Tensor $c_{ijkl}$ punya 81 komponen, tetapi simetri menguranginya menjadi 21, dan untuk medium **isotropik** hanya tersisa **dua**: parameter Lamé $\lambda$ dan $\mu$.

| Modulus | Lambang | Melawan |
|:--|:--|:--|
| Geser | $\mu$ | Perubahan bentuk |
| Ruah (*bulk*) | $K = \lambda + \tfrac{2}{3}\mu$ | Perubahan volume |
| Young | $E$ | Peregangan sepanjang satu sumbu |
| Nisbah Poisson | $\sigma$ | Penyempitan melintang |

**Ini muara Minggu 2.** Minggu depan kedua parameter itu akan muncul kembali sebagai kecepatan:

24973V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}, \qquad V_S = \sqrt{\frac{\mu}{\rho}}24973

Perhatikan: $V_S$ hanya memuat $\mu$. Pada zat cair $\mu = 0$, sehingga $V_S = 0$ — gelombang S tidak ada. Pertanyaan pembuka tadi baru saja terjawab dengan rumus.

Di Minggu 12 mahasiswa mengukur $V_P/V_S = 1{,}80$ dari data Yogyakarta, yang berarti $\sigma = 0{,}276$. Angka itu bukan hafalan; ia hasil pengukuran mereka sendiri.

---

## 4 · Tegangan geser maksimum dan pensesaran · 15 menit

Tegangan geser maksimum bekerja pada bidang **45°** terhadap $\sigma_1$ dan besarnya $(\sigma_1-\sigma_3)/2$. Namun sesar nyata di batuan biasanya terbentuk pada sudut **25°–35°** terhadap $\sigma_1$, bukan 45°, karena gesekan ikut menentukan (kriteria Mohr–Coulomb).

Konsekuensi yang dipakai Minggu 14: **dari orientasi sesar, arah tegangan utama daerah itu dapat disimpulkan** — dan sebaliknya.

---

## Tugas

**T2.1 Prediksi terkunci.** (a) Berapa besar regangan pada gelombang seismik dari gempa jauh? Beri selang. (b) Kalau $\mu$ suatu batuan nol, gelombang apa yang masih bisa lewat? (c) Tekanan litostatik pada 10 km kira-kira berapa MPa?

**T2.2 Hitungan.** Kerjakan latihan Bab 2 Shearer, khususnya perhitungan sumbu utama. Kerjakan dengan tangan lebih dulu, baru periksa dengan `numpy.linalg.eigh`.

**T2.3 Bacaan.** Shearer 2.1–2.3 · Stein & Wysession 2.3.1–2.3.10 (h. 38–51), terutama 2.3.5 *Maximum shear stress and faulting*.

---

## Catatan waktu

| Bagian | Menit | Kumulatif |
|:--|:--:|:--:|
| Kuis diagnostik prasyarat | 10 | 10 |
| 0 · Pembuka | 5 | 15 |
| 1 · Tensor tegangan | 25 | 40 |
| 2 · Tensor regangan | 20 | 60 |
| 3 · Hukum Hooke dan modulus | 25 | 85 |
| 4 · Tegangan geser dan pensesaran | 15 | 100 |

**Minggu depan:** kedua parameter Lamé menjadi dua kecepatan gelombang, dan Poisson 1828 terbukti.

<sub>Seismologi PAGF262413 · Program Studi Sarjana Geofisika FMIPA UGM · Kurikulum 2026</sub>
