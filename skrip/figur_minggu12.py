"""
Figur Minggu 12 — penentuan episenter dan hiposenter.
Seismologi PAGF262413, Program Studi Sarjana Geofisika FMIPA UGM.

Sumber data (arsip lokal, tidak disertakan di repo karena ukurannya):
  arrivals.csv, catalog_nll.csv, catalog_velest.csv, catalog_hypodd.csv,
  catalog_growclust.csv  dari pengolahan gempa susulan Yogyakarta 2006,
  serta station.dat berisi koordinat 17 stasiun jaringan YK.

CATATAN PENTING tentang data: kolom tt pada arrivals.csv adalah WAKTU TEMPUH
dari waktu asal, bukan waktu tiba absolut. Jadi t0 = 0 menurut konstruksi, dan
perpotongan garis Wadati yang bukan nol adalah ukuran penyimpangan anggapan
medium seragam terhadap bumi berlapis.

Menghasilkan lima PNG di Gambar/. Jalankan dari akar repo:
    python3 skrip/figur_minggu12.py
"""
import os
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

D    = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/full/")
STA  = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/hypodd/station.dat")
OUT  = "Gambar/"
EV   = 9101          # event contoh: 11 stasiun berpasangan P-S, gap 59 derajat
VP   = 5.5           # km/s, anggapan medium seragam
KM   = 111.19

sta = pd.read_csv(STA, sep=r"\s+", header=None, names=["sta","lat","lon"]).set_index("sta")
arr = pd.read_csv(D+"arrivals.csv")
nll = pd.read_csv(D+"catalog_nll.csv")

e = arr[arr.evid==EV].pivot_table(index="sta", columns="phase", values="tt")
e["SP"]  = e.S - e.P
e["epi"] = arr[arr.evid==EV].groupby("sta")["epi"].first()
d   = e.dropna(subset=["SP"]).copy()
ref = nll.iloc[EV]
slope, inter = np.polyfit(d.P, d.SP, 1)
vpvs = 1 + slope
poisson = ((vpvs**2)-2)/(2*((vpvs**2)-1))
k = VP/slope
d["dhyp"] = d.SP * k
d["dkat"] = np.sqrt(d.epi**2 + ref.depth**2)

# ------------------------------------------------------------------ 1. WADATI
t0 = -inter/slope
fig, ax = plt.subplots(1, 2, figsize=(13.2, 4.9))
ax[0].plot(d.P, d.SP, "o", ms=8, color="#0e7490")
for s_, r_ in d.iterrows():
    ax[0].annotate(s_, (r_.P, r_.SP), textcoords="offset points", xytext=(6,-3), fontsize=8)
xs = np.linspace(0, d.P.max()*1.1, 10)
ax[0].plot(xs, slope*xs+inter, "--", color="#dc2626", lw=1.5)
ax[0].plot([t0], [0], "*", ms=16, color="#dc2626")
ax[0].annotate(f"perpotongan {t0:+.2f} s\n(t$_0$ sejatinya 0 —\nselisihnya artefak\nmedium seragam)",
               (t0, 0), textcoords="offset points", xytext=(14,10), fontsize=8.5,
               color="#dc2626", fontweight="bold")
ax[0].axhline(0, color="#94a3b8", lw=.8); ax[0].grid(alpha=.25)
ax[0].set_xlabel("Waktu tempuh P (detik)"); ax[0].set_ylabel("S − P (detik)")
ax[0].set_title(f"A · Diagram Wadati — kemiringan {slope:.3f}  →  $V_P/V_S$ = {vpvs:.3f}",
                fontsize=11, fontweight="bold", loc="left")
ax[0].text(.03, .93, f"rasio Poisson σ = {poisson:.3f}", transform=ax[0].transAxes,
           fontsize=10, va="top", bbox=dict(fc="#ecfeff", ec="#0e7490"))
ax[1].plot(d.dkat, d.dhyp, "o", ms=8, color="#b45309")
lim = [0, d[["dhyp","dkat"]].max().max()*1.1]
ax[1].plot(lim, lim, "--", color="#334155", lw=1.2, label="garis 1:1")
ax[1].set_xlim(lim); ax[1].set_ylim(lim); ax[1].grid(alpha=.25); ax[1].legend(fontsize=9.5)
ax[1].set_xlabel("Jarak hiposentral dari katalog (km)")
ax[1].set_ylabel(f"Jarak dari (S−P) × {k:.2f} (km)")
res = np.abs(d.dhyp - d.dkat)
ax[1].set_title(f"B · Uji terhadap katalog — simpangan rerata {res.mean():.2f} km",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle(f"Event {EV} · gempa susulan Yogyakarta 2006 · {len(d)} stasiun, gap {ref.gap:.0f}°", fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"w12_wadati.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"1 wadati      Vp/Vs {vpvs:.3f}  sigma {poisson:.3f}  simpangan {res.mean():.2f} km")

# -------------------------------------------------------------- 2. LINGKARAN
fig, ax = plt.subplots(1, 3, figsize=(15.5, 5.6), sharex=True, sharey=True)
for j, (H, jd, ket) in enumerate([
        (0.0,        "A · kedalaman dianggap 0 km",            "Lingkaran terlalu besar dan\nberpotongan di mana-mana —\ntidak ada titik tunggal."),
        (ref.depth,  f"B · kedalaman benar {ref.depth:.1f} km", "Semua lingkaran memusat\npada satu titik."),
        (20.0,       "C · kedalaman dianggap 20 km",           "{n} stasiun kehilangan lingkarannya:\njarak S−P-nya lebih kecil daripada\nkedalaman yang diasumsikan.")]):
    A = ax[j]; hilang = 0
    for s_, r_ in d.iterrows():
        if s_ not in sta.index: continue
        R2 = r_.dhyp**2 - H**2
        if R2 <= 0: hilang += 1; continue
        A.add_patch(Circle((sta.loc[s_,"lon"], sta.loc[s_,"lat"]), np.sqrt(R2)/KM,
                           fill=False, ec="#0e7490", lw=1.0, alpha=.8))
    A.plot(sta.lon, sta.lat, "^", ms=9, color="#334155", mec="white", mew=.8)
    A.plot(ref.longitude, ref.latitude, "*", ms=20, color="#dc2626", mec="white", mew=1, zorder=5)
    A.set_xlim(110.05, 110.85); A.set_ylim(-8.32, -7.58); A.grid(alpha=.25)
    A.set_aspect(1/np.cos(np.radians(7.9)))
    A.set_title(jd, fontsize=11, fontweight="bold", loc="left"); A.set_xlabel("Bujur (°)")
    A.text(.03, .03, ket.format(n=hilang), transform=A.transAxes, fontsize=9, va="bottom",
           bbox=dict(fc="white", ec="#cbd5e1", alpha=.92))
ax[0].set_ylabel("Lintang (°)")
fig.suptitle(f"Metode lingkaran, event {EV} — jari-jari dari (S−P), pusat di tiap stasiun, bintang merah = lokasi katalog\n"
             "Jari-jari di peta = √(jarak hiposentral² − kedalaman²). Menebak kedalaman salah merusak seluruh penentuan episenter.",
             fontweight="bold", fontsize=11.5)
plt.tight_layout(); plt.savefig(OUT+"w12_lingkaran.png", dpi=125, bbox_inches="tight"); plt.close()
print("2 lingkaran")

# --------------------------------------------------------------- 3. GEOMETRI
nll["gapbin"] = pd.cut(nll.gap, [0,90,135,180,225,270,360])
g = nll.groupby("gapbin", observed=True)[["errh_km","errz_km"]].median()
n = nll.groupby("gapbin", observed=True).size()
fig, ax = plt.subplots(1, 2, figsize=(13.2, 4.9))
X = np.arange(len(g)); w = .38
ax[0].bar(X-w/2, g.errh_km, w, label="galat horizontal", color="#0e7490")
ax[0].bar(X+w/2, g.errz_km, w, label="galat vertikal (kedalaman)", color="#b45309")
ax[0].set_xticks(X); ax[0].set_xticklabels([str(i) for i in g.index], fontsize=9)
for i, (a1, a2, cnt) in enumerate(zip(g.errh_km, g.errz_km, n)):
    ax[0].text(i, max(a1,a2)+.04, f"n={cnt:,}".replace(",","."), ha="center", fontsize=8, color="#64748b")
ax[0].set_xlabel("Gap azimut (derajat)"); ax[0].set_ylabel("Galat median (km)")
ax[0].legend(fontsize=9.5); ax[0].grid(alpha=.25, axis="y")
ax[0].set_title("A · Geometri jaringan menentukan ketelitian", fontsize=11, fontweight="bold", loc="left")
r = (nll.errz_km/nll.errh_km).replace([np.inf,-np.inf], np.nan).dropna()
ax[1].hist(r[r<4], bins=60, color="#94a3b8", edgecolor="white")
ax[1].axvline(1, color="#dc2626", lw=1.6, ls="--")
ax[1].text(1.06, ax[1].get_ylim()[1]*.9,
           f"{100*(r>1).mean():.0f}% event punya\ngalat kedalaman LEBIH BESAR\ndaripada galat horizontal",
           fontsize=9.5, color="#dc2626", fontweight="bold", va="top")
ax[1].set_xlabel("Galat vertikal / galat horizontal"); ax[1].set_ylabel("Jumlah event"); ax[1].grid(alpha=.25)
ax[1].set_title(f"B · Kedalaman selalu yang paling sulit (median rasio {r.median():.2f})",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle(f"{len(nll):,} gempa susulan Yogyakarta 2006, lokasi NonLinLoc".replace(",","."), fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"w12_geometri.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"3 geometri    errh {g.errh_km.iloc[0]:.2f} -> {g.errh_km.iloc[-1]:.2f} km | errz>errh {100*(r>1).mean():.0f}%")

# ----------------------------------------------------------- 4. ELIPS GALAT
tt_ = arr.copy()
def permukaan(evid, span=.20, step=.003):
    dd = arr[arr.evid==evid].pivot_table(index="sta", columns="phase", values="tt").dropna(subset=["P"])
    dd = dd.join(sta)
    rf = nll.iloc[evid]
    la = np.arange(rf.latitude-span, rf.latitude+span, step)
    lo = np.arange(rf.longitude-span, rf.longitude+span, step)
    R = np.zeros((len(la), len(lo)))
    for i, a_ in enumerate(la):
        dx = (dd.lon.values[None,:]-lo[:,None])*KM*np.cos(np.radians(a_))
        dy = (dd.lat.values[None,:]-a_)*KM
        R[i,:] = np.sqrt(np.mean((dd.P.values[None,:]-np.sqrt(dx**2+dy**2+rf.depth**2)/VP)**2, axis=1))
    return la, lo, R, rf, dd
BAIK, BURUK = 9101, 8013
fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.8))
for j, evid in enumerate([BAIK, BURUK]):
    la, lo, R, rf, dd = permukaan(evid)
    X = (lo-rf.longitude)*KM*np.cos(np.radians(rf.latitude)); Y = (la-rf.latitude)*KM
    m = R.min()
    cf = ax[j].contourf(X, Y, R, levels=np.linspace(m, m*2.2, 22), cmap="YlGnBu_r")
    ax[j].contour(X, Y, R, levels=[m*1.1], colors="#dc2626", linewidths=2)
    for _, r_ in dd.iterrows():
        ax[j].plot([0, (r_.lon-rf.longitude)*KM*np.cos(np.radians(rf.latitude))*3],
                   [0, (r_.lat-rf.latitude)*KM*3], "-", color="#94a3b8", lw=.7, alpha=.8, zorder=1)
    ax[j].plot(0, 0, "*", ms=20, color="#dc2626", mec="white", mew=1, zorder=6)
    ax[j].set_xlim(-20, 20); ax[j].set_ylim(-20, 20); ax[j].set_aspect("equal"); ax[j].grid(alpha=.2)
    ax[j].set_xlabel("Timur dari katalog (km)")
    ii, jj = np.where(R < 1.1*m)
    ww, _ = np.linalg.eigh(np.cov(np.vstack([X[jj], Y[ii]])))
    ax[j].set_title(f"Event {evid} — gap {rf.gap:.0f}°, {len(dd)} stasiun\n"
                    f"kelonjongan lembah RMS = {np.sqrt(max(ww)/min(ww)):.2f}", fontsize=11.5, fontweight="bold")
    plt.colorbar(cf, ax=ax[j], shrink=.82, label="RMS residu (s)")
ax[0].set_ylabel("Utara dari katalog (km)")
fig.suptitle("Bentuk lembah RMS: garis abu-abu = arah ke stasiun, kontur merah = batas RMS 1,1× minimum\n"
             "Gap azimut buruk tidak membuat galat lebih besar — ia membuatnya BERARAH. Itulah elips galat.",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w12_elips_galat.png", dpi=125, bbox_inches="tight"); plt.close()
print("4 elips galat")

# -------------------------------------------------------------- 5. 4 METODE
vel = pd.read_csv(D+"catalog_velest.csv"); hdd = pd.read_csv(D+"catalog_hypodd.csv")
gc  = pd.read_csv(D+"catalog_growclust.csv")
sets = [("NonLinLoc\n(absolut)", nll.longitude, nll.latitude, nll.depth, "#334155"),
        ("VELEST\n(absolut + model kecepatan)", vel.longitude, vel.latitude, vel.depth, "#0e7490"),
        ("HypoDD\n(beda-ganda / relatif)", hdd.lon, hdd.lat, hdd.depth, "#b45309"),
        ("GrowClust\n(relatif berkluster)", gc.lon, gc.lat, gc.dep, "#7c3aed")]
fig, ax = plt.subplots(2, 4, figsize=(16.5, 7.6), gridspec_kw={"height_ratios":[1.25,1]})
LO, LA = (110.28, 110.58), (-8.10, -7.80)
for j, (nm, lo_, la_, dp, c) in enumerate(sets):
    m = lo_.between(*LO) & la_.between(*LA) & dp.between(-2, 30)
    lo_, la_, dp = lo_[m], la_[m], dp[m]
    ax[0,j].plot(lo_, la_, ".", ms=.8, color=c, alpha=.35)
    ax[0,j].set_xlim(*LO); ax[0,j].set_ylim(*LA); ax[0,j].set_aspect(1/np.cos(np.radians(7.95)))
    ax[0,j].grid(alpha=.2); ax[0,j].set_xlabel("Bujur (°)")
    ax[0,j].set_title(f"{nm}\nn = {len(lo_):,}".replace(",","."), fontsize=10.5, fontweight="bold")
    ax[1,j].plot(la_, dp, ".", ms=.8, color=c, alpha=.35)
    ax[1,j].set_xlim(*LA); ax[1,j].set_ylim(25, 0); ax[1,j].grid(alpha=.2); ax[1,j].set_xlabel("Lintang (°)")
    ax[1,j].text(.03, .05, f"σ kedalaman {dp.std():.2f} km", transform=ax[1,j].transAxes, fontsize=9,
                 bbox=dict(fc="white", ec="#cbd5e1", alpha=.9))
ax[0,0].set_ylabel("Lintang (°)"); ax[1,0].set_ylabel("Kedalaman (km)")
fig.suptitle("Gempa susulan Yogyakarta 2006 — awan gempa yang sama, empat metode penentuan lokasi\n"
             "Baris atas: peta. Baris bawah: penampang kedalaman. Metode relatif mempertajam struktur, tetapi ketelitiannya adalah ketelitian RELATIF.",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w12_empat_metode.png", dpi=125, bbox_inches="tight"); plt.close()
print("5 empat metode")
