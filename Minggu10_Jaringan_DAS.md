# Minggu 10 — Jaringan Seismik, Perekaman Digital, dan DAS

**Seismologi `PAGF262413`** · Senin 07:15–08:55, Ruang Kelas 209
Pokok Bahasan 4 · **CPMK3** · Bloom **C2–C3**

> **Sasaran.** Mahasiswa dapat (a) membedakan jenis jaringan seismik dan menjelaskan untuk apa masing-masing dirancang, (b) menyebutkan standar data dan metadata yang dipakai secara internasional, (c) menjelaskan jaringan pemantauan Indonesia, dan (d) menjelaskan prinsip kerja **DAS** beserta kelebihan dan keterbatasannya.

---

## 0 · Pembuka: satu alat tidak berarti apa-apa · 10 menit

Sepanjang tujuh minggu terakhir mahasiswa sudah bertemu kesimpulan yang sama berulang kali dengan wajah berbeda:

| Minggu | Batas yang ditemukan |
|:--|:--|
| 12 | Gap azimut buruk membuat galat lokasi **berarah** |
| 12 | Kedalaman tidak tertentukan tanpa stasiun dekat |
| 14 | Lima polaritas tidak cukup untuk satu mekanisme |

Semuanya bermuara pada satu hal: **bukan alatnya yang membatasi, melainkan di mana alat itu berada.** Hari ini kita bicara tentang bagaimana jaringan dirancang.

---

## 1 · Jenis jaringan · 20 menit

| Jenis | Rentang | Dirancang untuk |
|:--|:--|:--|
| **Global** | Seluruh dunia | Struktur bumi, gempa besar, pemantauan nuklir. Contoh: GSN, GEOFON, GEOSCOPE |
| **Regional** | Satu negara/wilayah | Katalog gempa, peringatan dini. Contoh: jaringan BMKG |
| **Lokal** | Puluhan km | Gunung api, panas bumi, gempa mikro. Contoh: jaringan YK Yogyakarta 2006 |
| **Array** | Ratusan meter–km | Beamforming, arah datang, pemantauan nuklir. Contoh: ASAR, WRA |

**Array bekerja berbeda dari jaringan biasa.** Ia memperlakukan banyak sensor sebagai satu alat besar: dengan menggeser dan menjumlahkan rekaman (*beamforming*), sinyal lemah yang datang dari satu arah dapat diperkuat sementara derau saling meniadakan. Ini penerapan langsung *stacking* dari Minggu 11 — perbaikan SNR sebanding $\sqrt{N}$.

**Jaringan YK yang dipakai sepanjang mata kuliah ini** adalah jaringan lokal sementara: 17 stasiun, dipasang beberapa pekan setelah gempa Yogyakarta 2006 untuk merekam gempa susulan. Rentang gap azimutnya yang lebar (53°–304°) adalah akibat langsung geometri pemasangannya — dan itulah yang mahasiswa ukur akibatnya di Minggu 12.

---

## 2 · Standar data dan metadata · 20 menit

Seismologi adalah salah satu bidang ilmu kebumian yang paling awal menyeragamkan formatnya, dan itulah sebabnya data dari mana pun dapat dipakai bersama.

| Standar | Isi |
|:--|:--|
| **miniSEED** | Deret waktu terkompresi; format baku dunia |
| **StationXML** | Metadata stasiun dan **respons instrumen** (Minggu 9) |
| **QuakeML** | Katalog gempa, pick, mekanisme sumber |
| **FDSN web service** | Antarmuka baku untuk mengunduh data dari server mana pun |
| **Kode jaringan FDSN** | Dua huruf unik: `GE` GEOFON, `IA` Indonesia, `YK` jaringan sementara Yogyakarta |

**Data tanpa metadata tidak berguna.** Rekaman berisi *count*; hanya StationXML yang mengubahnya menjadi m/s. Sebuah arsip seismik yang kehilangan metadatanya kehilangan hampir seluruh nilainya.

*Aktivitas:* unduh data satu gempa dari [IRIS/EarthScope DMC](https://ds.iris.edu/ds/nodes/dmc/) memakai `obspy` FDSN client, beserta inventarisnya, lalu terapkan `remove_response()`.

---

## 3 · Jaringan Indonesia · 20 menit

**BMKG** mengoperasikan jaringan seismik nasional dengan ratusan stasiun, mendukung katalog gempa dan **InaTEWS** (*Indonesia Tsunami Early Warning System*) yang dibangun setelah bencana 2004.

Katalog BMKG yang dipakai di Minggu 13 memuat **217.807 gempa** periode 1998–2024 — salah satu katalog terpadat di dunia, konsekuensi langsung dari posisi tektonik Indonesia.

Rantai peringatan dini tsunami menuntut kecepatan yang ekstrem: deteksi, penentuan lokasi, estimasi magnitudo, dan keputusan peringatan harus selesai dalam **hitungan menit**, karena tsunami dari sumber dekat dapat mencapai pantai dalam 20–30 menit. Setiap keterlambatan berarti nyawa.

> Ini menghubungkan seluruh mata kuliah: kecepatan itu hanya mungkin kalau penentuan lokasi (Minggu 12) dan magnitudo (Minggu 13) dapat diotomatisasi dengan andal — dan keandalannya dibatasi oleh geometri jaringan.

---

## 4 · DAS: kabel yang menjadi ribuan sensor · 25 menit

**Bagian paling mutakhir dalam mata kuliah ini — dan tidak dibahas di kedua buku acuan**, karena Stein & Wysession terbit 2003 dan Shearer 2019.

### Prinsipnya

Serat optik biasa memuat ketaksempurnaan mikroskopik yang menghamburkan balik sebagian cahaya (**hamburan Rayleigh**). Kalau pulsa laser dikirim dan cahaya balik itu dianalisis fasanya, **regangan sepanjang serat** dapat diukur.

Satu interogator pada ujung kabel sepanjang puluhan kilometer menghasilkan **ribuan titik ukur** berjarak beberapa meter.

### Mengapa ini penting

| Kelebihan | Keterbatasan |
|:--|:--|
| Kerapatan spasial luar biasa (jarak meteran) | Hanya **satu komponen** — regangan sepanjang serat |
| Dapat memakai **serat gelap** telekomunikasi yang sudah terpasang | Peka pada arah datang gelombang |
| Menjangkau tempat yang mustahil dipasangi seismometer: dasar laut, lubang bor, perkotaan padat | Kalibrasi ke satuan fisis lebih rumit |
| Tahan lingkungan ekstrem | Volume data sangat besar |

Bagi Indonesia potensinya besar: kabel telekomunikasi bawah laut melintasi zona subduksi yang selama ini nyaris tidak terpantau, karena memasang seismometer dasar laut sangat mahal.

### Bacaan wajib

- Zhan, Z. (2020). *Distributed acoustic sensing turns fiber-optic cables into sensitive seismic antennas.* **Seismological Research Letters** 91(1).
- Lindsey, N. J., & Martin, E. R. (2021). *Fiber-optic seismology.* **Annual Review of Earth and Planetary Sciences** 49.

---

## Tugas

**T10.1 Prediksi terkunci.** (a) Berapa banyak titik ukur pada kabel DAS 40 km berjarak 10 m? (b) Kalau satu stasiun menghasilkan 3 komponen × 100 Hz, berapa banyak data DAS itu dibandingkan satu stasiun? (c) Mengapa DAS tidak menggantikan seismometer?

**T10.2 Praktik.** Unduh data satu gempa dari FDSN beserta inventarisnya, terapkan dekonvolusi respons, dan laporkan amplitudo puncak dalam satuan fisis.

**T10.3 Bacaan.** Stein & Wysession 6.6.6–6.6.9 (h. 407–410) · Zhan (2020) · Lindsey & Martin (2021).

**Daring:** [daftar jaringan FDSN](https://www.fdsn.org/networks/) · [InaTEWS BMKG](https://inatews.bmkg.go.id/)

---

## Catatan waktu

| Bagian | Menit | Kumulatif |
|:--|:--:|:--:|
| 0 · Pembuka: bukan alatnya, tempatnya | 10 | 10 |
| 1 · Jenis jaringan | 20 | 30 |
| 2 · Standar data dan metadata | 20 | 50 |
| 3 · Jaringan Indonesia dan InaTEWS | 20 | 70 |
| 4 · DAS | 25 | 95 |
| Penutup | 5 | 100 |

**Minggu depan:** anatomi seismogram dan pemrosesan sinyal digital — dan mulai di sana, mahasiswa bekerja dengan data nyata mereka sendiri.

<sub>Seismologi PAGF262413 · Program Studi Sarjana Geofisika FMIPA UGM · Kurikulum 2026</sub>
