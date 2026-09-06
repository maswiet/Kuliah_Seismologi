#!/usr/bin/env python3
"""Pembagian kelompok + pemilihan ketua secara acak (reproducible).

Sumber data : List_Peserta_Kuliah_Seismology.xls (ekspor SIMASTER/DSSDI)
Seed        : 20260907 (tanggal kuliah) -> hasil selalu sama bila diulang,
              sehingga pembagian dapat diaudit/dipertanggungjawabkan.
Keluaran    : kelompok.csv, kelompok.md
"""
import argparse, random, csv, sys
from pathlib import Path

import xlrd

SEED = 20260907
UKURAN = 4                      # target anggota per kelompok
ROOT = Path(__file__).resolve().parent.parent
XLS = ROOT / "List_Peserta_Kuliah_Seismology.xls"

TOPIK = [
    # (kode, klaster, judul)
    ("A1", "Tegangan–Regangan–Elastisitas", "Tensor tegangan: traksi Cauchy, komponen normal & geser, tegangan utama dan lingkaran Mohr"),
    ("A2", "Tegangan–Regangan–Elastisitas", "Tensor regangan infinitesimal: dekomposisi regangan–rotasi, dilatasi, regangan deviatorik"),
    ("A3", "Tegangan–Regangan–Elastisitas", "Hukum Hooke isotropik: hubungan λ, μ, K, E, ν dan batas fisis nilai Poisson"),
    ("A4", "Tegangan–Regangan–Elastisitas", "Anisotropi elastik: dari 21 konstanta ke VTI/HTI dan parameter Thomsen"),
    ("A5", "Tegangan–Regangan–Elastisitas", "Energi regangan & modulus batuan → Vp, Vs, Vp/Vs: nilai tipikal batuan Indonesia"),

    ("B1", "Persamaan Gelombang & Gelombang Badan", "Turunan persamaan gerak elastik (Navier) dan dekomposisi Helmholtz → gelombang P dan S"),
    ("B2", "Persamaan Gelombang & Gelombang Badan", "Solusi gelombang bidang: polarisasi P–SV–SH dan gerak partikel pada seismogram 3 komponen"),
    ("B3", "Persamaan Gelombang & Gelombang Badan", "Aproksimasi frekuensi tinggi: persamaan eikonal, muka gelombang, dan geometrical spreading"),
    ("B4", "Persamaan Gelombang & Gelombang Badan", "Sumber gempa double-couple: pola radiasi P dan S serta pembacaan beachball"),
    ("B5", "Persamaan Gelombang & Gelombang Badan", "Atenuasi anelastik Q, operator t*, dan dispersi fisik pada gelombang badan"),

    ("C1", "Snell, Jalur Sinar, Head Wave", "Hukum Snell dan parameter sinar p; konversi mode P→SV pada bidang batas"),
    ("C2", "Snell, Jalur Sinar, Head Wave", "Jalur sinar pada medium berlapis & bergradien: kurva travel-time T(X) dan refraksi kritis"),
    ("C3", "Snell, Jalur Sinar, Head Wave", "Head wave & seismik refraksi: crossover distance, intercept time, penentuan tebal lapisan"),
    ("C4", "Snell, Jalur Sinar, Head Wave", "Penjalaran sinar dalam bumi berlapis bola: shadow zone, triplikasi, fase PcP/PKP (IASP91/ak135)"),

    ("D1", "Refleksi–Transmisi & Gelombang Permukaan", "Koefisien refleksi–transmisi insiden normal: impedansi, polaritas, dan seismogram sintetik konvolusi"),
    ("D2", "Refleksi–Transmisi & Gelombang Permukaan", "Persamaan Zoeppritz & aproksimasi AVO (Aki–Richards/Shuey); sudut kritis"),
    ("D3", "Refleksi–Transmisi & Gelombang Permukaan", "Gelombang Rayleigh pada half-space: turunan, gerak elips retrograd, kedalaman penetrasi"),
    ("D4", "Refleksi–Transmisi & Gelombang Permukaan", "Gelombang Love & dispersi: kurva fase/grup dan inversi sederhana menjadi profil Vs (MASW)"),
]

PERAN4 = [
    ("P1", "Teori & Derivasi"),
    ("P2", "Komputasi & Numerik"),
    ("P3", "Data & Studi Kasus"),
    ("P4", "Visualisasi, Sintesis & Soal"),
]
PERAN3 = [
    ("P1", "Teori & Derivasi"),
    ("P2", "Komputasi & Numerik"),
    ("P34", "Data, Studi Kasus & Visualisasi"),
]


def baca_peserta():
    bk = xlrd.open_workbook(str(XLS), ignore_workbook_corruption=True)
    sh = bk.sheet_by_index(0)
    hdr = [str(sh.cell_value(3, c)).strip() for c in range(sh.ncols)]
    i_nim, i_nama, i_mail = hdr.index("NIM"), hdr.index("Nama"), hdr.index("Email")
    out = []
    for r in range(4, sh.nrows):
        nama = str(sh.cell_value(r, i_nama)).strip()
        if not nama:
            continue
        out.append({
            "nim": str(sh.cell_value(r, i_nim)).strip(),
            "nama": " ".join(w.title() if w.isupper() else w for w in nama.split()),
            "email": str(sh.cell_value(r, i_mail)).strip(),
        })
    return out


def bagi(mhs):
    rng = random.Random(SEED)
    mhs = sorted(mhs, key=lambda m: m["nim"])
    rng.shuffle(mhs)

    n = len(mhs)
    n_kel = -(-n // UKURAN)                      # jumlah kelompok (ceil)
    if n_kel > len(TOPIK):
        sys.exit(f"Topik kurang: butuh {n_kel}, tersedia {len(TOPIK)}")
    kelompok = [[] for _ in range(n_kel)]
    for i, m in enumerate(mhs):                  # round-robin -> ukuran seimbang
        kelompok[i % n_kel].append(m)

    hasil = []
    for k, anggota in enumerate(kelompok):
        peran = PERAN4 if len(anggota) >= 4 else PERAN3
        rng.shuffle(anggota)
        ketua_idx = rng.randrange(len(anggota))
        rows = []
        for j, m in enumerate(anggota):
            kode, judul = peran[j % len(peran)]
            rows.append({**m, "peran": kode, "peran_nama": judul,
                         "ketua": j == ketua_idx})
        hasil.append({"no": k + 1, "topik": TOPIK[k], "anggota": rows})
    return hasil


def peer(n):
    """Setiap kelompok me-review 2 kelompok lain, dan di-review oleh 2 kelompok."""
    return {i: ((i + 6) % n, (i + 13) % n) for i in range(n)}


def samar(nim):
    """24/500000/PA/20000 -> \u2026000  (untuk versi repositori publik)."""
    return "\u2026" + nim[-3:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publik", action="store_true",
                    help="tulis kelompok_publik.md dengan NIM disamarkan, tanpa CSV")
    opsi = ap.parse_args()

    mhs = baca_peserta()
    hasil = bagi(mhs)
    n = len(hasil)
    rev = peer(n)

    if opsi.publik:
        L = ["# Pembagian Kelompok — Tugas Kelompok M1", "",
             f"Jumlah mahasiswa: **{len(mhs)}** · Jumlah kelompok: **{n}** · "
             f"Diacak dengan `scripts/buat_kelompok.py` (seed `{SEED}`, hasil reproducible).", "",
             "Tanda **(K)** = ketua kelompok. NIM sengaja disamarkan menjadi tiga digit terakhir "
             "karena repositori ini publik; daftar lengkap ada di Google Classroom.", ""]
        for g in hasil:
            kode, klaster, judul = g["topik"]
            i = g["no"] - 1
            L += [f"## K{g['no']:02d} — Topik {kode}", "",
                  f"**Klaster:** {klaster}  ", f"**Judul:** {judul}  ",
                  f"**Me-review:** K{rev[i][0]+1:02d} dan K{rev[i][1]+1:02d}", "",
                  "| Peran | Nama | NIM | Tugas individu |", "|---|---|---|---|"]
            for a in g["anggota"]:
                nm = f"**{a['nama']} (K)**" if a["ketua"] else a["nama"]
                L.append(f"| {a['peran']} | {nm} | {samar(a['nim'])} | {a['peran_nama']} |")
            L.append("")
        (ROOT / "kelompok_publik.md").write_text("\n".join(L), encoding="utf-8")
        print(f"{len(mhs)} mahasiswa -> {n} kelompok · ditulis: kelompok_publik.md (NIM disamarkan)")
        return

    with open(ROOT / "kelompok.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Kelompok", "Kode Topik", "Judul Topik", "NIM", "Nama",
                    "Email", "Kode Peran", "Peran", "Ketua",
                    "Review Kelompok"])
        for g in hasil:
            t = g["topik"]
            r = f"K{rev[g['no']-1][0]+1:02d}, K{rev[g['no']-1][1]+1:02d}"
            for a in g["anggota"]:
                w.writerow([f"K{g['no']:02d}", t[0], t[2], a["nim"], a["nama"],
                            a["email"], a["peran"], a["peran_nama"],
                            "KETUA" if a["ketua"] else "", r])

    L = ["# Pembagian Kelompok — Kuliah Seismologi (Minggu 2–4)", "",
         f"Jumlah mahasiswa: **{len(mhs)}** · Jumlah kelompok: **{n}** · "
         f"Diacak dengan `scripts/buat_kelompok.py` (seed `{SEED}`, hasil reproducible).", "",
         "Tanda **(K)** = ketua kelompok.", ""]
    for g in hasil:
        kode, klaster, judul = g["topik"]
        i = g["no"] - 1
        L += [f"## K{g['no']:02d} — Topik {kode}", "",
              f"**Klaster:** {klaster}  ", f"**Judul:** {judul}  ",
              f"**Me-review:** K{rev[i][0]+1:02d} dan K{rev[i][1]+1:02d}", "",
              "| Peran | Nama | NIM | Tugas individu |",
              "|---|---|---|---|"]
        for a in g["anggota"]:
            nm = f"**{a['nama']} (K)**" if a["ketua"] else a["nama"]
            L.append(f"| {a['peran']} | {nm} | {a['nim']} | {a['peran_nama']} |")
        L.append("")
    (ROOT / "kelompok.md").write_text("\n".join(L), encoding="utf-8")
    print(f"{len(mhs)} mahasiswa -> {n} kelompok "
          f"(ukuran {min(len(g['anggota']) for g in hasil)}–{max(len(g['anggota']) for g in hasil)})")
    print("Ditulis: kelompok.csv, kelompok.md")


if __name__ == "__main__":
    main()
