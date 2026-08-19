"""
Figur Minggu 2-10 — dari fondasi elastisitas sampai jaringan seismik.
Seismologi PAGF262413, Program Studi Sarjana Geofisika FMIPA UGM.

Sumber data lokal (tidak disertakan di repo):
  arrivals.csv, amplitudes.csv    gempa susulan Yogyakarta 2006
  pilot/mseed/                    rekaman kontinu 3 komponen
  ~/Work/SPAC/work/stationxml/    metadata respons instrumen nyata
  model iasp91 bawaan obspy       untuk fase global

Jalankan dari akar repo:  python3 skrip/figur_minggu02_10.py
"""
import os, glob
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from obspy import read, read_inventory, UTCDateTime
from scipy.signal import butter, sosfiltfilt

OUT = "Gambar/"
YG  = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/")
FS  = 100.

# ============================ MINGGU 3 — GERAK PARTIKEL P DAN S ============
m = pd.read_csv(YG+"seisbench/metadata.csv", low_memory=False)
r = m[(m.station_code=="TF14") & (m.trace_start_time.str.startswith("2006-06-04T19:53:28"))].iloc[0]
P = UTCDateTime(str(r.trace_start_time)) + r.trace_p_arrival_sample/100.
S = UTCDateTime(str(r.trace_start_time)) + r.trace_s_arrival_sample/100.
st = read(YG+"pilot/mseed/TF14/TF14.YK.2006.155.mseed", starttime=P-5, endtime=P+12)
st.detrend("demean"); st.filter("bandpass", freqmin=2, freqmax=20, corners=4, zerophase=True)
d = {tr.stats.channel[-1]: tr.data.astype(float) for tr in st}
t = np.arange(len(d["Z"]))/FS - 5
iP, iS = int(5*FS), int((5+(S-P))*FS)
W = int(0.6*FS)
fig, ax = plt.subplots(1, 3, figsize=(14.5, 4.9))
ax[0].plot(t, d["Z"]/np.abs(d["Z"]).max()+2, lw=.7, color="#1e293b")
ax[0].plot(t, d["N"]/np.abs(d["N"]).max(),   lw=.7, color="#0e7490")
ax[0].plot(t, d["E"]/np.abs(d["E"]).max()-2, lw=.7, color="#b45309")
for lab, off in [("Z",2), ("N",0), ("E",-2)]:
    ax[0].text(-4.7, off+.45, lab, fontweight="bold", fontsize=11)
ax[0].axvspan(0, W/FS, color="#dc2626", alpha=.18); ax[0].axvspan(S-P, S-P+W/FS, color="#2563eb", alpha=.18)
ax[0].set_xlim(-5, 10); ax[0].set_yticks([]); ax[0].set_xlabel("Waktu relatif P (detik)"); ax[0].grid(alpha=.2, axis="x")
ax[0].set_title("A · Tiga komponen, dua jendela", fontsize=11, fontweight="bold", loc="left")
for k, (i0, nm, c) in enumerate([(iP, "jendela P", "#dc2626"), (iS, "jendela S", "#2563eb")], start=1):
    hn, he, hz = d["N"][i0:i0+W], d["E"][i0:i0+W], d["Z"][i0:i0+W]
    sc = max(np.abs(np.r_[hn, hz]).max(), 1e-9)
    ax[k].plot(hn/sc, hz/sc, "-", lw=1.2, color=c)
    ax[k].plot(hn[0]/sc, hz[0]/sc, "o", ms=7, color="k")
    ax[k].set_xlim(-1.2, 1.2); ax[k].set_ylim(-1.2, 1.2); ax[k].set_aspect("equal"); ax[k].grid(alpha=.25)
    ax[k].set_xlabel("Utara (ternormalkan)"); ax[k].set_ylabel("Vertikal (ternormalkan)")
    ax[k].set_title(f"{'BC'[k-1]} · Gerak partikel — {nm}", fontsize=11, fontweight="bold", loc="left")
fig.suptitle("Gelombang P bergerak SEJAJAR arah rambat, S TEGAK LURUS terhadapnya — terbaca dari data nyata TF14",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w03_gerak_partikel.png", dpi=125, bbox_inches="tight"); plt.close()
print("W3 gerak partikel")

# ====================== MINGGU 4 — KURVA WAKTU TEMPUH NYATA ================
arr = pd.read_csv(YG+"full/arrivals.csv")
fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
hasil = {}
for ph, c in [("P", "#dc2626"), ("S", "#2563eb")]:
    s = arr[(arr.phase == ph) & (arr.epi < 60)]
    k = np.polyfit(s.epi, s.tt, 1); hasil[ph] = k
    ax[0].plot(s.epi, s.tt, ".", ms=.7, color=c, alpha=.25)
    xx = np.linspace(0, 60, 10)
    ax[0].plot(xx, np.polyval(k, xx), "-", color=c, lw=2,
               label=f"{ph}: {1/k[0]:.2f} km/s  (n={len(s):,})".replace(",", "."))
ax[0].set_xlabel("Jarak episentral (km)"); ax[0].set_ylabel("Waktu tempuh (detik)")
ax[0].legend(fontsize=10); ax[0].grid(alpha=.25); ax[0].set_xlim(0, 60)
ax[0].set_title("A · Kurva waktu tempuh dari 195.348 pengamatan nyata", fontsize=11, fontweight="bold", loc="left")
vp, vs = 1/hasil["P"][0], 1/hasil["S"][0]
sp = arr.pivot_table(index=["evid", "sta"], columns="phase", values="tt").dropna()
sp["SP"] = sp.S - sp.P
ax[1].plot(sp.P, sp.SP, ".", ms=.7, color="#0e7490", alpha=.2)
kk = np.polyfit(sp.P, sp.SP, 1)
xx = np.linspace(0, sp.P.max(), 10)
ax[1].plot(xx, np.polyval(kk, xx), "-", color="#dc2626", lw=2,
           label=f"kemiringan {kk[0]:.3f} → $V_P/V_S$ = {1+kk[0]:.3f}")
ax[1].set_xlabel("Waktu tempuh P (detik)"); ax[1].set_ylabel("S − P (detik)")
ax[1].legend(fontsize=10); ax[1].grid(alpha=.25)
ax[1].set_title(f"B · Wadati seluruh katalog — $V_P/V_S$ = {1+kk[0]:.2f}", fontsize=11, fontweight="bold", loc="left")
fig.suptitle(f"Kecepatan kerak Yogyakarta dari data sendiri: $V_P$ = {vp:.2f} km/s, $V_S$ = {vs:.2f} km/s, "
             f"nisbah {vp/vs:.2f}", fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w04_waktu_tempuh.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"W4 waktu tempuh  Vp {vp:.2f}  Vs {vs:.2f}  Vp/Vs {vp/vs:.2f} (Wadati {1+kk[0]:.2f})")

# ========================== MINGGU 6 — FASE SEISMIK GLOBAL ================
from obspy.taup import TauPyModel
mdl = TauPyModel(model="iasp91")
fase = ["P", "PP", "PcP", "PKIKP", "S", "SS", "ScS"]
war = dict(zip(fase, ["#dc2626", "#f97316", "#7c3aed", "#0e7490", "#2563eb", "#059669", "#b45309"]))
fig, ax = plt.subplots(1, 2, figsize=(13.6, 5.4))
degs = np.arange(5, 175, 2.5)
for ph in fase:
    x, y = [], []
    for dg in degs:
        try:
            a = mdl.get_travel_times(source_depth_in_km=15, distance_in_degree=float(dg), phase_list=[ph])
            if a: x.append(dg); y.append(a[0].time/60)
        except Exception: pass
    if x: ax[0].plot(x, y, ".", ms=2.5, color=war[ph], label=ph)
ax[0].set_xlabel("Jarak episentral (derajat)"); ax[0].set_ylabel("Waktu tempuh (menit)")
ax[0].legend(fontsize=9.5, ncol=2, markerscale=4); ax[0].grid(alpha=.25)
ax[0].set_title("A · Kurva waktu tempuh global, model iasp91", fontsize=11, fontweight="bold", loc="left")
arv = mdl.get_ray_paths(source_depth_in_km=15, distance_in_degree=75,
                        phase_list=["P", "PcP", "PKIKP", "S"])
axp = fig.add_subplot(122, projection="polar"); ax[1].remove()
R = 6371.
for a in arv:
    axp.plot(a.path["dist"], R - a.path["depth"], lw=1.6, color=war.get(a.name, "#334155"), label=a.name)
for rr, c, lw in [(R, "#334155", 1.5), (R-2891, "#dc2626", 1.2), (1221.5, "#0e7490", 1.2)]:
    th = np.linspace(0, 2*np.pi, 200); axp.plot(th, np.full_like(th, rr), "-", color=c, lw=lw)
axp.set_theta_zero_location("N"); axp.set_ylim(0, R); axp.set_yticks([]); axp.set_xticks([])
axp.legend(fontsize=9, loc="lower left", bbox_to_anchor=(-.05, -.02))
axp.set_title("B · Lintasan sinar pada jarak 75°\nmerah = batas inti (2891 km), biru = inti dalam",
              fontsize=11, fontweight="bold")
fig.suptitle("Fase seismik global — satu gempa menghasilkan puluhan kedatangan berbeda",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w06_fase_global.png", dpi=125, bbox_inches="tight"); plt.close()
print("W6 fase global")

# ============================ MINGGU 7 — ATENUASI DAN Q ===================
amp = pd.read_csv(YG+"full/amplitudes.csv")
mg  = pd.read_csv(YG+"full/catalog_magnitude.csv")[["evid", "ML"]]
j = amp.merge(mg, on="evid")
j = j[j.ML.between(0.5, 1.5) & j.hypo_km.between(3, 60)]
lr = np.log10(j.hypo_km); la = np.log10(j.amp_mm)
n_geo = np.polyfit(lr, la, 1)[0]
bins = pd.cut(j.hypo_km, np.arange(0, 62, 4))
med = j.groupby(bins, observed=True).apply(lambda g: np.median(np.log10(g.amp_mm)), include_groups=False)
xs = np.array([iv.mid for iv in med.index])
fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
ax[0].plot(j.hypo_km, j.amp_mm, ".", ms=1, color="#cbd5e1", alpha=.4)
ax[0].plot(xs, 10**med.values, "o-", color="#dc2626", lw=2, ms=7, label="median per 4 km")
ax[0].plot(xs, 10**(med.values[0]) * (xs/xs[0])**(-1.0), "--", color="#0e7490", lw=1.8,
           label="penyebaran geometris murni (1/R)")
ax[0].set_xscale("log"); ax[0].set_yscale("log")
ax[0].set_xlabel("Jarak hiposentral (km)"); ax[0].set_ylabel("Amplitudo (mm)")
ax[0].legend(fontsize=9.5); ax[0].grid(alpha=.25, which="both")
ax[0].set_title(f"A · Peluruhan terukur $R^{{{n_geo:.2f}}}$ — lebih curam daripada 1/R",
                fontsize=11, fontweight="bold", loc="left")
sisa = la - (n_geo*lr + np.polyfit(lr, la, 1)[1])
ax[1].plot(j.hypo_km, sisa, ".", ms=1, color="#94a3b8", alpha=.3)
ax[1].axhline(0, color="#334155", lw=1)
ax[1].set_xlabel("Jarak hiposentral (km)"); ax[1].set_ylabel("sisa $\\log_{10}$ amplitudo")
ax[1].set_ylim(-1.5, 1.5); ax[1].grid(alpha=.25)
ax[1].set_title("B · Sisanya datar — model satu suku sudah menangkap polanya",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle("Atenuasi: amplitudo tidak hanya berkurang karena muka gelombang melebar,\n"
             "tetapi juga karena bumi menyerap energi sepanjang lintasan",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w07_atenuasi.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"W7 atenuasi      eksponen peluruhan {n_geo:.2f}")

# ====================== MINGGU 9 — RESPONS INSTRUMEN NYATA ================
xs_ = sorted(glob.glob(os.path.expanduser("~/Work/SPAC/work/stationxml/*.xml")))
inv = read_inventory(xs_[0]); ch = inv[0][0][0]
f = np.logspace(-3, np.log10(ch.sample_rate/2), 400)
resp, fr = ch.response.get_evalresp_response(t_samp=1/ch.sample_rate, nfft=8192, output="VEL")
fr = fr[1:]; resp = resp[1:]
fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
ax[0].loglog(fr, np.abs(resp), lw=2, color="#0e7490")
ax[0].axvline(1.0, color="#dc2626", ls="--", lw=1.4)
ax[0].text(1.1, np.abs(resp).max()*.3, "perioda alami\n≈ 1 Hz", color="#dc2626", fontsize=9.5, fontweight="bold")
ax[0].set_xlabel("Frekuensi (Hz)"); ax[0].set_ylabel("Amplitudo respons (count per m/s)")
ax[0].grid(alpha=.25, which="both")
ax[0].set_title("A · Kurva respons amplitudo", fontsize=11, fontweight="bold", loc="left")
ax[1].semilogx(fr, np.degrees(np.angle(resp)), lw=2, color="#b45309")
ax[1].axvline(1.0, color="#dc2626", ls="--", lw=1.4); ax[1].axhline(0, color="#334155", lw=.8)
ax[1].set_xlabel("Frekuensi (Hz)"); ax[1].set_ylabel("Fasa respons (derajat)")
ax[1].grid(alpha=.25, which="both")
ax[1].set_title("B · Kurva respons fasa — instrumen juga MENGGESER waktu",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle(f"Respons nyata {inv[0].code}.{inv[0][0].code}.{ch.code} — "
             f"sensitivitas {ch.response.instrument_sensitivity.value:.2e} count/(m/s)\n"
             "Di bawah perioda alaminya seismometer nyaris buta: itulah sebabnya dekonvolusi respons wajib",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w09_respons_instrumen.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"W9 respons       {inv[0].code}.{inv[0][0].code}.{ch.code}, {len(ch.response.response_stages)} tahap")
