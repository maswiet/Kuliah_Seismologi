#!/usr/bin/env python3
"""Menyiapkan Par_file SPECFEM2D untuk latihan refraksi dua lapis Minggu 4.

Format Par_file berbeda antar versi SPECFEM2D, jadi skrip ini **tidak** menulis
Par_file dari nol. Ia menyunting Par_file bawaan instalasi kalian sendiri dan
hanya mengganti kunci-kunci yang relevan, sehingga tetap cocok dengan versi yang
kalian pasang.

    python3 siapkan_par_file.py $SPECFEM2D/DATA/Par_file  -o Par_file

Kunci yang tidak ditemukan akan dilaporkan, bukan didiamkan — periksa manual
versi kalian bila ada yang muncul di daftar itu.
"""
import argparse, re, sys

# model dua lapis: pelapukan 30 m di atas batuan dasar
NILAI = {
    "title":                    "Refraksi dua lapis - Seismologi PAGF262413 Minggu 4",
    "NPROC":                    "1",
    "SIMULATION_TYPE":          "1",
    "NOISE_TOMOGRAPHY":         "0",
    "SAVE_FORWARD":             ".false.",
    "AXISYM":                   ".false.",
    "P_SV":                     ".true.",       # ada P dan SV, bukan SH saja
    "NSTEP":                    "8000",
    "DT":                       "4.0d-5",       # 8000 x 4e-5 = 0,32 s rekaman
    "time_stepping_scheme":     "1",
    "seismotype":               "2",            # 2 = kecepatan partikel, seperti geofon
    "NTSTEP_BETWEEN_OUTPUT_SEISMOS": "10000",
    "save_ASCII_seismograms":   ".true.",
    "save_binary_seismograms_single": ".false.",
    "save_binary_seismograms_double": ".false.",
    "SU_FORMAT":                ".false.",
    "use_existing_STATIONS":    ".true.",       # pakai berkas STATIONS kita
    "nreceiversets":            "0",
    "read_external_mesh":       ".false.",
    "interfacesfile":           "interfaces_dua_lapis.dat",
    "xmin":                     "0.d0",
    "xmax":                     "280.d0",
    "nx":                       "112",          # elemen 2,5 m
    "STACEY_ABSORBING_CONDITIONS": ".true.",
    "PML_BOUNDARY_CONDITIONS":  ".false.",
    "absorbbottom":             ".true.",
    "absorbright":              ".true.",
    "absorbleft":               ".true.",
    "absorbtop":                ".false.",      # PERMUKAAN BEBAS - jangan diserap
    "nbmodels":                 "2",
    "nbregions":                "2",
    "NSTEP_BETWEEN_OUTPUT_IMAGES": "400",
    "output_color_image":       ".true.",
    "output_postscript_snapshot": ".false.",
}

# blok yang harus ditulis utuh, bukan sekadar satu kunci
BLOK_MODEL = """\
# nomor 1 rho Vp Vs 0 0 QKappa Qmu 0 0 0 0 0 0
1 1 2000.d0 2500.d0 1445.d0 0 0 9999 9999 0 0 0 0 0 0
2 1 1800.d0 1000.d0  578.d0 0 0 9999 9999 0 0 0 0 0 0
"""
BLOK_REGION = """\
# nxmin nxmax nzmin nzmax nomor_model
1 112  1 44 1
1 112 45 56 2
"""


def sunting(teks):
    hilang = list(NILAI)
    out = []
    for baris in teks.split("\n"):
        m = re.match(r"^(\s*)([A-Za-z_][A-Za-z_0-9]*)(\s*=\s*)(.*)$", baris)
        if m and m.group(2) in NILAI:
            k = m.group(2)
            komentar = ""
            sisa = m.group(4)
            if "#" in sisa:
                komentar = "  " + sisa[sisa.index("#"):]
            out.append(f"{m.group(1)}{k}{m.group(3)}{NILAI[k]}{komentar}")
            if k in hilang:
                hilang.remove(k)
        else:
            out.append(baris)
    return "\n".join(out), hilang


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("par_file", help="Par_file bawaan instalasi SPECFEM2D kalian")
    ap.add_argument("-o", "--keluaran", default="Par_file")
    o = ap.parse_args()

    teks = open(o.par_file, encoding="utf-8", errors="replace").read()
    baru, hilang = sunting(teks)
    open(o.keluaran, "w", encoding="utf-8").write(baru)

    print(f"Ditulis: {o.keluaran}  ({len(NILAI)-len(hilang)}/{len(NILAI)} kunci diganti)")
    if hilang:
        print("\nTIDAK ditemukan di Par_file kalian — periksa manual versi kalian:")
        for k in hilang:
            print(f"  {k:34s} seharusnya = {NILAI[k]}")
    print("\nBlok model dan region harus disalin manual ke Par_file, "
          "menggantikan blok bawaannya:\n")
    print(BLOK_MODEL)
    print(BLOK_REGION)
    print("Lalu jalankan dari direktori kerja SPECFEM2D:")
    print("  ./bin/xmeshfem2D && ./bin/xspecfem2D")
    print("Seismogram ASCII keluar di OUTPUT_FILES/AA.S00NN.BXZ.semv")


if __name__ == "__main__":
    sys.exit(main())
