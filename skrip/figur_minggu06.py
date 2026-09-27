"""
Figur Minggu 6 — struktur dalam bumi, fase inti, dan inti terdalam (IMIC).

Menghasilkan dua PNG di Gambar/. Jalankan dari akar repo:
    python3 skrip/figur_minggu06.py

Lintasan sinar dan radius titik balik dihitung sungguhan dengan obspy.taup
(model iasp91), bukan sketsa tangan.

CATATAN KEJUJURAN GAMBAR 2b. Kurva anisotropi pada panel itu adalah **skema**,
bukan salinan koefisien terbitan. Ia dibangun dari bentuk baku transversal
isotropik d(v)/v = a cos^2(xi) + b cos^4(xi), dengan a dan b dipilih agar
memenuhi dua ciri yang dilaporkan Pham & Tkalcic (2023):
  - IMIC : arah paling lambat pada xi ~ 50 derajat dari sumbu rotasi,
           dengan beda ~4% terhadap arah kutub;
  - kulit luar inti dalam : arah paling lambat di bidang ekuator, lebih lemah.
Yang harus dibaca mahasiswa dari panel itu adalah **perbedaan orientasi**
sumbu lambatnya, bukan nilai persen yang presisi.

Rujukan:
  Pham & Tkalcic (2023), Nat. Commun. 14, 754, doi:10.1038/s41467-023-36074-2
  Ishii & Dziewonski (2002), PNAS 99, 14026, doi:10.1073/pnas.172508499
"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from obspy.taup import TauPyModel

OUT = "Gambar"
R_BUMI = 6371.0
R_CMB = 3480.0          # batas inti-mantel
R_ICB = 1221.5          # batas inti luar - inti dalam
R_IMIC = 650.0          # Pham & Tkalcic (2023)
R_IMIC_2002 = 300.0     # usulan awal Ishii & Dziewonski (2002)

MODEL = TauPyModel("iasp91")

FASE = [                # (nama, jarak derajat, warna, keterangan)
    ("P",     60,  "#1f77b4", "P — menembus mantel"),
    ("PcP",   40,  "#2ca02c", "PcP — pantul di CMB"),
    ("SKS",  110,  "#9467bd", "SKS — S lalu P di inti luar"),
    ("PKP",  150,  "#ff7f0e", "PKP — lewat inti luar"),
    ("PKIKP", 175, "#d62728", "PKIKP — menembus inti dalam"),
]


def gambar_lintasan():
    fig = plt.figure(figsize=(13, 6.2))
    ax = fig.add_subplot(1, 2, 1, projection="polar")
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)

    for r, gaya, lw in [(R_BUMI, "-", 1.4), (R_BUMI - 410, ":", .8),
                        (R_BUMI - 660, ":", .8), (R_CMB, "-", 1.2),
                        (R_ICB, "-", 1.2), (R_IMIC, "--", 1.6)]:
        th = np.linspace(0, 2 * np.pi, 400)
        ax.plot(th, np.full_like(th, r), gaya, color="0.35" if r != R_IMIC else "crimson",
                lw=lw, zorder=1)

    for nama, dist, warna, _ in FASE:
        arr = MODEL.get_ray_paths(source_depth_in_km=0, distance_in_degree=dist,
                                  phase_list=[nama])
        if not arr:
            print(f"  ! {nama} tidak ada pada {dist} derajat"); continue
        p = arr[0].path
        ax.plot(p["dist"], R_BUMI - p["depth"], color=warna, lw=2, zorder=3,
                label=f"{nama} ({dist}°)")
    ax.plot(0, R_BUMI, "k*", ms=16, zorder=5)

    ax.set_rmax(R_BUMI * 1.02); ax.set_rticks([]); ax.set_xticks([])
    ax.grid(False); ax.spines["polar"].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, -.14), ncol=3, fontsize=8.5,
              frameon=False)
    ax.set_title("(a) Lintasan sinar fase global (iasp91)", fontsize=11)
    # label batas ditaruh di separuh kiri yang tidak dilewati sinar mana pun,
    # masing-masing pada sudut berbeda agar tidak saling menimpa
    for th_deg, r, nama, warna in [(270, R_BUMI, "permukaan", "0.35"),
                                   (252, R_BUMI - 535, "410 & 660 km", "0.45"),
                                   (270, R_CMB, "CMB · 2891 km", "0.3"),
                                   (238, R_ICB, "ICB · 5150 km", "0.3"),
                                   (302, R_IMIC, "IMIC · r = 650 km", "crimson")]:
        ax.text(np.radians(th_deg), r, nama, fontsize=8.5, color=warna,
                ha="center", va="center", zorder=6,
                bbox=dict(fc="w", ec="none", alpha=.85, pad=1.5))

    # ---- panel kanan: radius titik balik PKIKP terhadap jarak -----------------
    ax2 = fig.add_subplot(1, 2, 2)
    d = np.arange(150, 180.5, 0.5)
    rb = []
    for x in d:
        a = MODEL.get_ray_paths(0, float(x), phase_list=["PKIKP"])
        rb.append(R_BUMI - a[0].path["depth"].max() if a else np.nan)
    rb = np.array(rb)

    ax2.axhspan(0, R_IMIC, color="crimson", alpha=.12)
    ax2.axhspan(R_IMIC, R_ICB, color="steelblue", alpha=.10)
    ax2.plot(d, rb, "k-", lw=2.2)
    ax2.axhline(R_IMIC, color="crimson", ls="--", lw=1.6)
    ax2.axhline(R_IMIC_2002, color="crimson", ls=":", lw=1.4)

    d_imic = float(np.interp(-R_IMIC, -rb, d))          # rb menurun terhadap d
    d_2002 = float(np.interp(-R_IMIC_2002, -rb, d))
    ax2.axvline(d_imic, color="crimson", ls="--", lw=1.0)
    ax2.plot([d_imic], [R_IMIC], "o", color="crimson", ms=7, zorder=5)

    ax2.text(151, R_IMIC + 40, f"IMIC 2023: r = {R_IMIC:.0f} km  "
                               f"→ butuh Δ ≳ {d_imic:.0f}°", color="crimson", fontsize=9)
    ax2.text(151, R_IMIC_2002 + 35, f"IMIC 2002: r = {R_IMIC_2002:.0f} km  "
                                    f"→ butuh Δ ≳ {d_2002:.0f}°", color="crimson",
             fontsize=8.5, alpha=.8)
    ax2.text(178.6, 900, "kulit luar\ninti dalam", color="steelblue", fontsize=9,
             ha="right", va="center")

    ax2.set(xlabel="jarak episentral Δ (derajat)",
            ylabel="radius titik balik PKIKP (km)",
            xlim=(150, 180.5), ylim=(0, 1100))
    ax2.grid(alpha=.25)
    ax2.set_title("(b) Sinar PKIKP mana yang benar-benar menyentuh\n"
                  "inti terdalam — hanya yang hampir antipodal", fontsize=10.5)

    fig.tight_layout()
    fig.savefig(f"{OUT}/w06_lintasan_fase_inti.png", dpi=150)
    plt.close(fig)
    print(f"  IMIC 650 km tersentuh mulai Δ = {d_imic:.1f}°; "
          f"IMIC 300 km mulai Δ = {d_2002:.1f}°")
    return d_imic, d_2002


def _anisotropi(xi_deg, xi_lambat_deg, beda_persen):
    """d(v)/v skema: a cos^2 + b cos^4, minimum pada xi_lambat, amplitudo diatur."""
    u_min = np.cos(np.radians(xi_lambat_deg))**2
    b = 1.0
    a = -2 * b * u_min                      # syarat turunan nol di u_min
    u = np.cos(np.radians(xi_deg))**2
    f = a * u + b * u**2
    f0, fmin = a + b, a * u_min + b * u_min**2
    return f * (beda_persen / (f0 - fmin))


def gambar_imic():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5.8))

    # ---- kiri: skema dua kulit inti dalam -----------------------------------
    th = np.linspace(0, 2 * np.pi, 400)
    a1.fill(R_ICB * np.sin(th), R_ICB * np.cos(th), color="steelblue", alpha=.20)
    a1.fill(R_IMIC * np.sin(th), R_IMIC * np.cos(th), color="crimson", alpha=.25)
    a1.plot(R_ICB * np.sin(th), R_ICB * np.cos(th), color="steelblue", lw=1.8)
    a1.plot(R_IMIC * np.sin(th), R_IMIC * np.cos(th), color="crimson", lw=1.8, ls="--")

    a1.annotate("", xy=(0, R_ICB * 1.33), xytext=(0, -R_ICB * 1.33),
                arrowprops=dict(arrowstyle="<->", color="k", lw=1.3))
    a1.text(70, R_ICB * 1.36, "sumbu rotasi bumi", fontsize=9, ha="left")

    # arah paling lambat: kulit luar = bidang ekuator
    a1.annotate("", xy=(R_ICB * .97, 0), xytext=(R_IMIC * 1.04, 0),
                arrowprops=dict(arrowstyle="->", color="steelblue", lw=2.6))
    a1.annotate("kulit luar inti dalam:\npaling lambat di ekuator",
                xy=(R_ICB * .95, 0), xytext=(R_ICB * 1.12, R_ICB * .62),
                color="steelblue", fontsize=9, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color="steelblue", lw=1.1))

    # arah paling lambat IMIC: ~50 derajat dari sumbu rotasi
    xi = np.radians(50)
    a1.annotate("", xy=(R_IMIC * .95 * np.sin(xi), R_IMIC * .95 * np.cos(xi)),
                xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="crimson", lw=2.6))
    a1.plot([0, 0], [0, R_IMIC * .95], color="crimson", lw=.9, ls=":")
    a1.annotate("inti terdalam (IMIC):\npaling lambat ~50° dari sumbu",
                xy=(R_IMIC * .55 * np.sin(xi), R_IMIC * .55 * np.cos(xi)),
                xytext=(-R_ICB * 1.45, R_ICB * .78),
                color="crimson", fontsize=9, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color="crimson", lw=1.1))
    a1.text(R_IMIC * .16, R_IMIC * .55, "ξ ≈ 50°", color="crimson", fontsize=9)
    a1.text(0, -R_ICB * 1.52, f"inti dalam r = {R_ICB:.0f} km   ·   "
                              f"inti terdalam r ≈ {R_IMIC:.0f} km",
            fontsize=9, ha="center", color="0.25")
    a1.set_aspect("equal"); a1.axis("off")
    a1.set_xlim(-R_ICB * 1.55, R_ICB * 2.05); a1.set_ylim(-R_ICB * 1.68, R_ICB * 1.62)
    a1.set_title("(a) Dua kulit dengan orientasi anisotropi berbeda", fontsize=11)

    # ---- kanan: kecepatan terhadap sudut xi ---------------------------------
    xs = np.linspace(0, 90, 400)
    a2.plot(xs, _anisotropi(xs, 90, 2.0), color="steelblue", lw=2.4,
            label="kulit luar inti dalam (lambat di ekuator)")
    a2.plot(xs, _anisotropi(xs, 50, 4.0), color="crimson", lw=2.4,
            label="inti terdalam / IMIC (lambat pada ~50°)")
    a2.axvline(50, color="crimson", ls=":", lw=1.2)
    a2.axvline(90, color="steelblue", ls=":", lw=1.2)
    a2.axhline(0, color="0.5", lw=.8)
    a2.set(xlabel="sudut ξ sinar terhadap sumbu rotasi (derajat)",
           ylabel="simpangan laju P terhadap rata-rata (%)", xlim=(0, 90))
    a2.set_xticks([0, 15, 30, 45, 50, 60, 75, 90])
    a2.grid(alpha=.25); a2.legend(fontsize=9, loc="upper right")
    a2.set_title("(b) SKEMA — yang penting perbedaan letak titik minimumnya,\n"
                 "bukan nilai persennya", fontsize=11)
    a2.text(1.5, 0.18, "arah kutub", fontsize=8.5, color="0.4")
    a2.text(88, 0.18, "bidang\nekuator", fontsize=8.5, color="0.4", ha="right")

    fig.tight_layout()
    fig.savefig(f"{OUT}/w06_imic_anisotropi.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Menggambar lintasan fase inti ...")
    gambar_lintasan()
    print("Menggambar skema anisotropi inti terdalam ...")
    gambar_imic()
    print("Selesai: 2 PNG di Gambar/.")
