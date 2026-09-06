# Latihan SPECFEM2D — refraksi dua lapis (Minggu 4)

Berkas masukan untuk memodelkan gelombang langsung, pantul, dan **kepala**
(*head wave*) pada model dua lapis mendatar, lalu membandingkan waktu tibanya
dengan hitungan Hukum Snell.

## Model

| Besaran | Nilai |
|:--|--:|
| Kecepatan lapisan pelapukan $V_1$ | 1000 m/s |
| Kecepatan batuan dasar $V_2$ | 2500 m/s |
| Tebal lapisan lapuk $h$ | 30 m |
| Sudut kritis $i_c=\arcsin(V_1/V_2)$ | 23,58° |
| *Intercept time* $t_i$ | 54,99 ms |
| *Crossover distance* $X_c$ | 91,7 m |
| Sumber | palu di permukaan, $x$ = 20 m, Ricker 40 Hz |
| Penerima | 24 geofon, $x$ = 28…212 m (offset 8…192 m, spasi 8 m) |
| Domain | 280 m × 140 m, elemen 2,5 m |

Nilai $i_c$, $t_i$, dan $X_c$ **jangan dilihat dulu** sebelum kalian
menghitungnya sendiri dari seismogram. Itu inti latihannya.

## Berkas

| Berkas | Isi |
|:--|:--|
| `interfaces_dua_lapis.dat` | tiga antarmuka: dasar, batas lapisan, permukaan bebas |
| `SOURCE` | gaya vertikal di permukaan, Ricker 40 Hz |
| `STATIONS` | 24 geofon di permukaan |
| `siapkan_par_file.py` | menyunting `Par_file` bawaan instalasi kalian |

## Menjalankan

```bash
cd $SPECFEM2D                       # direktori instalasi kalian
mkdir -p latihan_w04/DATA latihan_w04/OUTPUT_FILES
cp <repo>/skrip/w04_specfem2d/{SOURCE,STATIONS,interfaces_dua_lapis.dat} latihan_w04/DATA/
python3 <repo>/skrip/w04_specfem2d/siapkan_par_file.py DATA/Par_file -o latihan_w04/DATA/Par_file
# salin blok model & region yang dicetak skrip ke Par_file, lalu:
cd latihan_w04 && $SPECFEM2D/bin/xmeshfem2D && $SPECFEM2D/bin/xspecfem2D
```

Seismogram ASCII muncul di `OUTPUT_FILES/AA.S00NN.BXZ.semv` — dua kolom,
waktu dan kecepatan partikel vertikal.

> **Peringatan versi.** Nama kunci di `Par_file` berubah antar rilis SPECFEM2D.
> Berkas ini ditulis untuk SPECFEM2D 8.x. `siapkan_par_file.py` sengaja hanya
> menyunting Par_file milik kalian sendiri dan **melaporkan kunci yang tidak
> ditemukan** — periksa daftar itu terhadap manual versi kalian sebelum
> menjalankan. Belum diuji-jalan pada mesin pengampu, jadi laporkan bila ada
> kunci yang meleset supaya berkas ini diperbaiki untuk angkatan berikutnya.

## Kalau SPECFEM2D belum terpasang

Jangan berhenti. Jalankan pengganti mandiri berbasis beda-hingga yang
menghasilkan eksperimen yang sama:

```bash
python3 skrip/w04_gelombang_dua_lapis.py
```

Seluruh analisis di `Minggu04_Praktik.ipynb` memakai keluaran itu, sehingga
latihan tetap dapat diselesaikan tanpa memasang apa pun.
