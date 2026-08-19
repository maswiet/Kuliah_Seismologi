# Minggu 5 — Koefisien Refleksi–Transmisi; Gelombang Permukaan dan Dispersi

**Seismologi `PAGF262413`** · Senin 07:15–08:55, Ruang Kelas 209
Pokok Bahasan 2 · **CPMK1** · Bloom **C3–C4**

> **Sasaran.** Mahasiswa dapat (a) menjelaskan pembagian energi pada batas dan menghitung koefisien refleksi–transmisi untuk kasus sederhana, (b) menjelaskan bagaimana gelombang Love dan Rayleigh terbentuk serta di komponen mana keduanya muncul, dan (c) membedakan kecepatan fase dari kecepatan grup serta menjelaskan mengapa dispersi membawa informasi struktur.

---

## 0 · Pembuka: gelombang yang datang paling akhir dan paling merusak · 10 menit

Pada seismogram gempa jauh, kedatangan terbesar hampir selalu **bukan** P dan bukan S, melainkan gelombang yang merambat di permukaan — datang paling akhir, beramplitudo paling besar, dan bertahan paling lama.

Untuk bangunan tinggi, gelombang inilah yang paling berbahaya, karena periodanya panjang dan bisa beresonansi dengan gedung.

---

## 1 · Energi di batas: koefisien refleksi dan transmisi · 25 menit

Ketika gelombang menumbuk batas, energinya terbagi. Untuk kasus paling sederhana — SH pada batas datar — koefisiennya bergantung pada **impedansi** $Z = \rho V$:

25044R = \frac{Z_1 - Z_2}{Z_1 + Z_2}, \qquad T = \frac{2Z_1}{Z_1 + Z_2}25044

Tiga hal yang layak digarisbawahi:

- Kalau $Z_1 = Z_2$, tidak ada pantulan — **meski kecepatannya berbeda.** Yang dilihat gelombang adalah impedansi, bukan kecepatan.
- Kalau $Z_2 > Z_1$, koefisien pantulnya **negatif**: polaritas gelombang pantul terbalik.
- Untuk P–SV kasusnya jauh lebih rumit karena terjadi **konversi jenis** — P datang menghasilkan P dan SV sekaligus.

Konversi itu bukan kerumitan yang mengganggu; ia justru dimanfaatkan. **Fungsi penerima** (*receiver function*) — salah satu alat utama memetakan Moho — seluruhnya bertumpu pada gelombang P yang terkonversi jadi S di batas kerak–mantel.

---

## 2 · Gelombang permukaan · 25 menit

### Rayleigh

Terbentuk dari perpaduan P dan SV yang terperangkap di dekat permukaan bebas. Gerak partikelnya **elips retrograd** pada bidang vertikal yang memuat arah rambat. Muncul di komponen **Z dan R**, tidak di T. Kecepatannya sekitar $0{,}92\,V_S$ pada medium homogen.

### Love

Terbentuk dari SH yang terperangkap dalam **lapisan** di atas medium berkecepatan lebih tinggi — jadi ia **tidak ada** pada medium homogen. Gerak partikelnya mendatar, tegak lurus arah rambat. Muncul **hanya** di komponen T.

> Di sinilah rotasi ZNE → ZRT yang diperkenalkan Minggu 11 menemukan gunanya yang paling tegas: rotasi itu **memisahkan Love dari Rayleigh secara fisis**, bukan sekadar mengganti sistem koordinat.

---

## 3 · Dispersi: kecepatan yang bergantung frekuensi · 25 menit

Gelombang permukaan berperioda panjang menjangkau lebih dalam, sehingga merasakan batuan yang lebih cepat. Akibatnya **kecepatannya bergantung perioda** — inilah dispersi.

| | Definisi | Yang diamati |
|:--|:--|:--|
| **Kecepatan fase** $c$ | $\omega/k$ | Laju rambat satu puncak gelombang |
| **Kecepatan grup** $U$ | $d\omega/dk$ | Laju rambat paket energi |

Hubungannya $U = c - \lambda \dfrac{dc}{d\lambda}$.

**Mengapa ini penting.** Kurva dispersi terukur adalah **cetak biru struktur kecepatan terhadap kedalaman**. Membalikkannya menghasilkan profil $V_S(z)$ — dan itulah dasar metode MASW serta tomografi *ambient noise* yang dipakai luas untuk mikrozonasi kota, termasuk di Yogyakarta.

*Bahan diskusi:* tsunami juga terdispersi (Stein & Wysession 2.8.4, h. 99). Mengapa gelombang tsunami berperioda panjang tiba lebih dulu, dan apa artinya bagi sistem peringatan dini?

---

## 4 · Mode normal · 10 menit

Untuk gempa sangat besar, seluruh bumi berdenting seperti lonceng pada frekuensi diskretnya sendiri — **mode normal**. Pertama kali teramati dengan jelas setelah gempa Chile M9,5 tahun 1960, seperti tercatat di garis waktu Minggu 1.

Mode normal memberi kendala pada struktur bumi **secara global dan sekaligus**, melengkapi gelombang badan yang hanya menyampel sepanjang lintasannya.

---

## Tugas

**T5.1 Prediksi terkunci.** (a) Batuan dengan $\rho$ berbeda tetapi $\rho V$ sama — adakah pantulan? (b) Gelombang mana yang lebih dulu tiba, Love atau Rayleigh? (c) Perioda panjang menjangkau lebih dalam atau lebih dangkal?

**T5.2 Bacaan.** Shearer 6.1–6.3, 8.1–8.3 (**lewati 6.5†**) · Stein & Wysession 2.6.1–2.6.6 (h. 75–81), 2.7.2–2.7.4 (h. 87–91), 2.8.1–2.8.2 (h. 93–94).

**T5.3 Pengayaan opsional.** Stein & Wysession 2.8.4 *Tsunami dispersion* (h. 99) — relevansi tinggi untuk Indonesia; cocok dijadikan topik studi kasus Minggu 15.

---

## Catatan waktu

| Bagian | Menit | Kumulatif |
|:--|:--:|:--:|
| 0 · Pembuka | 10 | 10 |
| 1 · Koefisien refleksi–transmisi | 25 | 35 |
| 2 · Gelombang Love dan Rayleigh | 25 | 60 |
| 3 · Dispersi, fase vs grup | 25 | 85 |
| 4 · Mode normal | 10 | 95 |
| Penutup | 5 | 100 |

**Minggu depan:** dari kerak ke seluruh planet — fase seismik global dan struktur dalam bumi.

<sub>Seismologi PAGF262413 · Program Studi Sarjana Geofisika FMIPA UGM · Kurikulum 2026</sub>
