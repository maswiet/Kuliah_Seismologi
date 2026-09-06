"""
Minggu 4 — simulasi perambatan gelombang pada model dua lapis mendatar.

Menghasilkan seismogram sintetik 24 geofon untuk latihan seismik refraksi:
gelombang langsung, gelombang pantul, dan gelombang kepala (head wave) muncul
bersama dalam satu rekaman, lalu dibandingkan dengan hitungan Hukum Snell.

Skema acuan mata kuliah ini adalah SPECFEM2D (lihat skrip/w04_specfem2d/).
Berkas ini adalah **pengganti mandiri** berbasis beda-hingga akustik 2-D supaya
seluruh kelas tetap dapat mengerjakan latihan tanpa memasang SPECFEM2D lebih
dulu. Fisika yang diuji sama: satu persamaan gelombang, dua lapis, sumber di
permukaan, 24 geofon di permukaan.

    Beda-hingga: orde 2 dalam waktu, orde 4 dalam ruang, akustik rapat-tetap.
    Permukaan atas = permukaan bebas (tekanan nol); tiga sisi lain diredam.
    Geofon merekam simpul pertama di bawah permukaan bebas, sehingga yang
    tercatat sebanding dengan gradien tekanan vertikal — analog gerak partikel
    vertikal yang direkam geofon sungguhan.

Jalankan dari akar repo:
    python3 skrip/w04_gelombang_dua_lapis.py

Keluaran:
    data/W04_seismogram_dua_lapis.npz   rekaman 24 geofon + metadata
    data/W04_model_sejati.json          model sejati (kunci, untuk pengajar)
    Gambar/w04_model_dan_sinar.png
    Gambar/w04_snapshot_muka_gelombang.png
    Gambar/w04_rekaman_dan_kurva.png
"""
import json, os, time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- model sejati
V1, V2, H = 1000.0, 2500.0, 30.0        # m/s, m/s, m  (pelapukan di atas batuan dasar)
XMAX, ZMAX, DX = 280.0, 140.0, 0.5      # m (0,5 m -> ~8 titik per panjang gelombang terpendek)
F0, TMAX = 100.0, 0.24                  # Hz, s  (100 Hz: lambda1 = 10 m << h = 30 m)
XSRC, ZSRC = 20.0, 2.0                  # sumber tepat di bawah permukaan
XG0, DXG, NG = 28.0, 8.0, 24            # 24 geofon, offset 8 m sampai 192 m
GZ = 2                                  # simpul rekam, tepat di bawah permukaan bebas
SNAP_MS = [35, 60, 85, 105]            # snapshot, ms sejak WAKTU ASAL sumber

OUT_DATA, OUT_FIG = "data", "Gambar"


def hitung_teori(offs):
    """Waktu tempuh analitik ketiga fase, dari Hukum Snell."""
    ti = 2 * H * np.sqrt(V2**2 - V1**2) / (V1 * V2)      # intercept time
    return dict(
        langsung=offs / V1,
        pantul=np.sqrt(offs**2 + 4 * H**2) / V1,
        kepala=np.where(offs >= 2 * H * V1 / np.sqrt(V2**2 - V1**2),
                        offs / V2 + ti, np.nan),
        ti=ti,
        xc=2 * H * np.sqrt((V2 + V1) / (V2 - V1)),        # crossover
        ic=np.degrees(np.arcsin(V1 / V2)),                # sudut kritis
    )


def simulasi(snapshot_ms=()):
    nx, nz = int(XMAX / DX) + 1, int(ZMAX / DX) + 1
    c = np.full((nz, nx), V1)
    c[int(H / DX):, :] = V2

    dt = 0.4 * DX / c.max()                      # syarat CFL
    nt = int(TMAX / dt) + 1
    t = np.arange(nt) * dt
    t0 = 1.4 / F0                                # puncak wavelet Ricker
    a = (np.pi * F0 * (t - t0))**2
    src = (1 - 2 * a) * np.exp(-a)

    # peredam sederhana di kiri, kanan, bawah; permukaan atas dibiarkan bebas
    npml, r = 30, 0.90
    w = np.ones((nz, nx))
    for i in range(npml):
        f = r + (1 - r) * (i / npml)
        w[:, i] = np.minimum(w[:, i], f)
        w[:, nx - 1 - i] = np.minimum(w[:, nx - 1 - i], f)
        w[nz - 1 - i, :] = np.minimum(w[nz - 1 - i, :], f)

    isx, isz = int(XSRC / DX), int(ZSRC / DX)
    gx = ((XG0 + np.arange(NG) * DXG) / DX).astype(int)
    seis = np.zeros((nt, NG))
    snaps, want = [], [int((ms / 1e3 + t0) / dt) for ms in snapshot_ms]

    p0 = np.zeros((nz, nx)); p1 = np.zeros((nz, nx))
    k = (c * dt / DX)**2
    c4a, c4b, c4c = -1 / 12, 4 / 3, -5 / 2

    tic = time.time()
    for it in range(nt):
        lap = (c4a * (np.roll(p1, 2, 1) + np.roll(p1, -2, 1)
                      + np.roll(p1, 2, 0) + np.roll(p1, -2, 0))
               + c4b * (np.roll(p1, 1, 1) + np.roll(p1, -1, 1)
                        + np.roll(p1, 1, 0) + np.roll(p1, -1, 0))
               + 2 * c4c * p1)
        p2 = 2 * p1 - p0 + k * lap
        p2[isz, isx] += k[isz, isx] * src[it]
        p2[0, :] = 0.0                            # permukaan bebas
        p2 *= w; p1 *= w
        p0, p1 = p1, p2
        seis[it] = p1[GZ, gx]
        if it in want:
            snaps.append((it * dt - t0, p1.copy()))   # waktu fisis, bukan waktu grid

    print(f"  grid {nx}x{nz}, dt = {dt*1e3:.3f} ms, {nt} langkah, {time.time()-tic:.1f} s")
    return dict(seis=seis, dt=dt, t0=t0, offs=gx * DX - XSRC, c=c, snaps=snaps)


# ------------------------------------------------------------------ pemetikan
def petik(seis, dt, t0, f0=F0, frac=0.01):
    """First break tiap jejak: ambang amplitudo lalu dinaikkan ke puncak wavelet.

    Rekaman ini bebas derau, jadi ambang sederhana 1% amplitudo maksimum sudah
    cukup dan jauh lebih mudah dijelaskan daripada STA/LTA. Pada data lapangan
    yang berderau, ambang setetap ini akan gagal — di sana dipakai STA/LTA atau
    AIC. Ambang harus tetap rendah karena **gelombang kepala amplitudonya kecil**;
    itu sifat fisisnya, bukan cacat simulasi.
    """
    t = np.arange(seis.shape[0]) * dt - t0
    naik = int(0.7 / f0 / dt)
    out = []
    for i in range(seis.shape[1]):
        a = np.abs(seis[:, i].astype(float))
        j = int(np.argmax(a > frac * a.max()))
        out.append(t[j + int(np.argmax(a[j:j + naik]))])
    return np.array(out)


def inversi(offs, pick, xc_tebakan):
    """Dua garis -> V1, V2, h. Statik dihapus dari intersep garis langsung.

    Geofon di sekitar crossover sengaja dibuang: di sana gelombang langsung dan
    gelombang kepala tiba nyaris bersamaan dan saling mengganggu, sehingga
    pick-nya tidak mewakili cabang mana pun.
    """
    dekat, jauh = offs < xc_tebakan - 15, offs > xc_tebakan + 10
    _, statik = np.polyfit(offs[dekat], pick[dekat], 1)
    pk = pick - statik
    s1, _ = np.polyfit(offs[dekat], pk[dekat], 1)
    s2, ti = np.polyfit(offs[jauh], pk[jauh], 1)
    v1, v2 = 1 / s1, 1 / s2
    h = ti / 2 * v1 * v2 / np.sqrt(v2**2 - v1**2)
    return dict(V1=v1, V2=v2, h=h, ti=ti, statik=statik,
                ic=np.degrees(np.arcsin(v1 / v2)),
                xc=2 * h * np.sqrt((v2 + v1) / (v2 - v1)))


# ------------------------------------------------------------------ penyajian
def gambar_model(sim):
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.imshow(sim["c"], extent=[0, XMAX, ZMAX, 0], cmap="Blues", aspect="auto",
              vmin=800, vmax=2700)
    ax.axhline(H, color="k", lw=1.6)
    ax.plot(XSRC, 0, "r*", ms=18, label="sumber")
    ax.plot(XG0 + np.arange(NG) * DXG, np.zeros(NG), "kv", ms=6, label="24 geofon")

    ic = np.radians(np.degrees(np.arcsin(V1 / V2)))
    xa = XSRC + H * np.tan(ic)
    xb = XSRC + 170
    ax.plot([XSRC, xa], [0, H], "r-", lw=1.4)                       # turun kritis
    ax.plot([xa, xb], [H, H], "r-", lw=1.4)                         # merayap di batas
    ax.plot([xb, xb + H * np.tan(ic)], [H, 0], "r-", lw=1.4,
            label="gelombang kepala")
    ax.plot([XSRC, XSRC + 150], [0, 0], "g-", lw=1.4, label="gelombang langsung")
    ax.plot([XSRC, XSRC + 45, XSRC + 90], [0, H, 0], "m--", lw=1.4,
            label="gelombang pantul")
    ax.annotate(f"$i_c$ = {np.degrees(ic):.1f}°", (xa - 6, H / 2), color="r", fontsize=10)
    ax.text(XMAX - 8, H / 2, f"$V_1$ = {V1:.0f} m/s", ha="right", fontsize=11)
    ax.text(XMAX - 8, H + 45, f"$V_2$ = {V2:.0f} m/s", ha="right", fontsize=11)
    ax.set(xlabel="jarak (m)", ylabel="kedalaman (m)", ylim=(120, -12),
           title=f"Model dua lapis: h = {H:.0f} m, tiga lintasan sinar")
    ax.legend(loc="lower left", fontsize=9, ncol=2)
    fig.tight_layout(); fig.savefig(f"{OUT_FIG}/w04_model_dan_sinar.png", dpi=150)
    plt.close(fig)


def gambar_snapshot(sim):
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 6.2))
    for n, (ax, (tt, p)) in enumerate(zip(axes.ravel(), sim["snaps"])):
        v = 0.10 * np.abs(p[:110, :230]).max()
        ax.imshow(p, extent=[0, XMAX, ZMAX, 0], cmap="seismic",
                  vmin=-v, vmax=v, aspect="auto", interpolation="bilinear")
        ax.axhline(H, color="k", lw=1.2)
        ax.plot(XSRC, 0, "k*", ms=11)
        ax.plot(XG0 + np.arange(NG) * DXG, np.full(NG, 1.5), "kv", ms=3)
        ax.set(xlim=(0, 235), ylim=(115, -4), xlabel="x (m)", ylabel="z (m)")
        ax.set_title(f"t = {tt*1e3:.0f} ms", fontsize=10)
        # Muka gelombang kepala: garis lurus bersudut i_c terhadap BIDANG BATAS,
        # ujung bawahnya menempel pada muka bias yang berlari di batas.
        ic = np.arcsin(V1 / V2)
        t_turun = H / (V1 * np.cos(ic))              # satu tungkai turun kritis
        if tt > t_turun:
            xb = XSRC + H * np.tan(ic) + V2 * (tt - t_turun)   # muka bias di batas
            xs_ = xb - H / np.tan(ic)                          # potong permukaan
            if xb < 232 and xs_ > XSRC:
                ax.plot([xb, xs_], [H, 0], "g--", lw=2.4)
                ax.annotate("gelombang kepala", xy=((xb + xs_) / 2, H / 2),
                            xytext=(0.80, 0.88), textcoords="axes fraction",
                            fontsize=9, color="darkgreen", ha="center",
                            arrowprops=dict(arrowstyle="->", color="darkgreen", lw=1.5))
    fig.suptitle("Muka gelombang: yang melengkung = gelombang langsung dan bias;\n"
                 "tungkai lurus yang menghubungkannya ke permukaan = gelombang kepala",
                 fontsize=10.5)
    fig.tight_layout(); fig.savefig(f"{OUT_FIG}/w04_snapshot_muka_gelombang.png", dpi=150)
    plt.close(fig)


def gambar_rekaman(sim):
    seis, dt, t0, offs = sim["seis"], sim["dt"], sim["t0"], sim["offs"]
    t = np.arange(seis.shape[0]) * dt - t0
    th = hitung_teori(offs)
    pick = petik(seis, dt, t0)
    inv = inversi(offs, pick, th["xc"])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6.5))

    # -- kiri: rekaman + pick --------------------------------------------------
    sc, gain = 0.6 * DXG, (1 + 6 * np.maximum(t, 0))       # kuatkan tiba awal
    for i, off in enumerate(offs):
        tr = seis[:, i] * gain
        tr = tr / np.abs(tr).max()
        a1.plot(off + sc * tr, t * 1e3, "k-", lw=0.6)
        a1.fill_betweenx(t * 1e3, off, off + sc * tr, where=tr > 0,
                         color="k", alpha=0.55, lw=0)
    a1.plot(offs, pick * 1e3, "o", ms=5, mfc="yellow", mec="r", mew=1.2,
            label="first break terpetik")
    a1.axvline(th["xc"], color="b", ls=":", lw=1.5)
    a1.text(th["xc"] - 3, -18, f"crossover {th['xc']:.0f} m", color="b",
            fontsize=9, ha="right", va="center")
    a1.set(xlabel="offset (m)", ylabel="waktu terhadap waktu asal (ms)",
           ylim=(185, -25), title="(a) Seismogram sintetik 24 geofon")
    a1.legend(loc="lower left", fontsize=9); a1.grid(alpha=0.25)

    # -- kanan: kurva waktu tempuh --------------------------------------------
    pk = (pick - inv["statik"]) * 1e3
    a2.plot(offs, pk, "o", ms=6, mfc="yellow", mec="r", label="pick (statik dihapus)")
    a2.plot(offs, th["langsung"] * 1e3, "g-", lw=2, label="teori langsung  $X/V_1$")
    a2.plot(offs, th["kepala"] * 1e3, "r-", lw=2, label="teori kepala  $X/V_2+t_i$")
    a2.plot(offs, th["pantul"] * 1e3, "m--", lw=1.5,
            label=r"teori pantul  $\sqrt{X^2+4h^2}/V_1$")
    xs = np.array([0, offs.max()])
    a2.plot(xs, xs / inv["V1"] * 1e3, "g:", lw=1.6)
    a2.plot(xs, (xs / inv["V2"] + inv["ti"]) * 1e3, "r:", lw=1.6,
            label="garis cocokan mahasiswa")
    a2.axvline(th["xc"], color="b", ls=":", lw=1.5)
    a2.set(xlabel="offset (m)", ylabel="waktu (ms)", xlim=(0, offs.max() * 1.03),
           ylim=(0, 200), title="(b) Kurva waktu tempuh dan hasil inversi dua garis")
    a2.legend(loc="upper left", fontsize=9); a2.grid(alpha=0.25)
    a2.text(0.98, 0.04,
            f"$V_1$ = {inv['V1']:.0f} m/s (sejati {V1:.0f})\n"
            f"$V_2$ = {inv['V2']:.0f} m/s (sejati {V2:.0f})\n"
            f"$h$  = {inv['h']:.1f} m (sejati {H:.0f})\n"
            f"$i_c$ = {inv['ic']:.1f}° (sejati {th['ic']:.1f}°)",
            transform=a2.transAxes, ha="right", va="bottom", fontsize=10,
            bbox=dict(fc="w", ec="0.6"))

    fig.tight_layout(); fig.savefig(f"{OUT_FIG}/w04_rekaman_dan_kurva.png", dpi=150)
    plt.close(fig)
    return inv


def main():
    os.makedirs(OUT_DATA, exist_ok=True); os.makedirs(OUT_FIG, exist_ok=True)
    print("Simulasi beda-hingga dua lapis ...")
    sim = simulasi(SNAP_MS)
    th = hitung_teori(sim["offs"])
    print(f"  sudut kritis {th['ic']:.2f}°, intercept {th['ti']*1e3:.2f} ms, "
          f"crossover {th['xc']:.1f} m")

    np.savez_compressed(
        f"{OUT_DATA}/W04_seismogram_dua_lapis.npz",
        seis=sim["seis"].astype(np.float32), dt=sim["dt"], t0=sim["t0"],
        offs=sim["offs"], f0=F0,
        catatan="24 geofon, sumber di permukaan; t sudah relatif waktu asal "
                "setelah dikurangi t0. Model sejati sengaja tidak disertakan.")
    json.dump(dict(V1=V1, V2=V2, h=H, sudut_kritis_deg=th["ic"],
                   intercept_s=th["ti"], crossover_m=th["xc"]),
              open(f"{OUT_DATA}/W04_model_sejati.json", "w"), indent=2)

    gambar_model(sim); gambar_snapshot(sim)
    inv = gambar_rekaman(sim)
    print(f"  uji-silang inversi: V1={inv['V1']:.0f} ({100*(inv['V1']-V1)/V1:+.1f}%)  "
          f"V2={inv['V2']:.0f} ({100*(inv['V2']-V2)/V2:+.1f}%)  "
          f"h={inv['h']:.1f} m ({100*(inv['h']-H)/H:+.1f}%)  "
          f"statik={inv['statik']*1e3:+.1f} ms")
    print("Selesai: 1 npz, 1 json kunci, 3 PNG.")


if __name__ == "__main__":
    main()
