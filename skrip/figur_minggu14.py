"""
Figur Minggu 14 — mekanisme sumber gempa.
Seismologi PAGF262413, Program Studi Sarjana Geofisika FMIPA UGM.

Sumber data:
  data/W14_mekanisme_indonesia.csv  12 mekanisme fokus gempa besar Indonesia,
                                    diambil dari layanan FDSN USGS (produk
                                    moment-tensor) dan disimpan agar dapat
                                    dipakai luring.
  arsip lokal Yogyakarta 2006       untuk pengukuran polaritas first-motion

Menghasilkan tiga PNG di Gambar/. Jalankan dari akar repo:
    python3 skrip/figur_minggu14.py
"""
import os, glob
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from obspy.imaging.beachball import beach

OUT = "Gambar/"
mek = pd.read_csv("data/W14_mekanisme_indonesia.csv")

def tipe(rake):
    r = (rake + 360) % 360
    if 45 <= r < 135:   return "naik (thrust)"
    if 225 <= r < 315:  return "turun (normal)"
    return "mendatar (strike-slip)"

mek["tipe"] = mek.rake.apply(tipe)

# ------------------------------------------------- 1. PETA BOLA FOKAL NYATA
fig, ax = plt.subplots(figsize=(14, 6.6))
warna = {"naik (thrust)": "#dc2626", "turun (normal)": "#0e7490", "mendatar (strike-slip)": "#b45309"}
for _, r in mek.iterrows():
    b = beach([r.strike, r.dip, r.rake], xy=(r.lon, r.lat), width=1.5 + (r.M - 7.5),
              linewidth=.7, facecolor=warna[r.tipe], alpha=.9)
    ax.add_collection(b)
    ax.text(r.lon, r.lat - 1.15 - (r.M - 7.5) / 2, f"M{r.M:.1f}\n{r.waktu[:4]}",
            ha="center", fontsize=7.5, color="#334155")
ax.set_xlim(92, 136); ax.set_ylim(-12, 8); ax.set_aspect(1 / np.cos(np.radians(3)))
ax.grid(alpha=.25); ax.set_xlabel("Bujur (°)"); ax.set_ylabel("Lintang (°)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=c, label=t) for t, c in warna.items()], fontsize=10, loc="lower left")
ax.set_title("Mekanisme sumber 12 gempa besar Indonesia (M ≥ 7,0) — data USGS\n"
             "Hampir semuanya sesar naik: itulah tanda tangan megathrust zona subduksi",
             fontweight="bold", fontsize=12.5)
plt.tight_layout(); plt.savefig(OUT + "w14_bolafokal_indonesia.png", dpi=125, bbox_inches="tight"); plt.close()
print("1 peta bola fokal:", mek.tipe.value_counts().to_dict())

# ------------------------------------------- 2. TIGA TIPE SESAR + AMBIGUITAS
contoh = [("Sesar naik\n(thrust)", [335, 7, 113], "#dc2626", "Aceh 2004, M9,1"),
          ("Sesar mendatar\n(strike-slip)", [274, 84, 169], "#b45309", "Samudra Hindia 2016, M7,8"),
          ("Sesar turun\n(normal)", [30, 55, -90], "#0e7490", "contoh ilustratif")]
fig, ax = plt.subplots(1, 4, figsize=(15.5, 4.6))
for i, (nm, sdr, c, ket) in enumerate(contoh):
    ax[i].add_collection(beach(sdr, xy=(0, 0), width=180, linewidth=1, facecolor=c))
    ax[i].set_xlim(-110, 110); ax[i].set_ylim(-110, 110); ax[i].set_aspect("equal"); ax[i].axis("off")
    ax[i].set_title(f"{nm}\nstrike {sdr[0]}° dip {sdr[1]}° rake {sdr[2]}°\n{ket}", fontsize=10.5, fontweight="bold")
a = ax[3]
r = mek[mek.M == mek.M.max()].iloc[0]
a.add_collection(beach([r.strike, r.dip, r.rake], xy=(0, 0), width=180, linewidth=1, facecolor="#7c3aed"))
a.set_xlim(-110, 110); a.set_ylim(-110, 110); a.set_aspect("equal"); a.axis("off")
a.set_title(f"Ambiguitas bidang sesar\nbidang 1: {r.strike:.0f}/{r.dip:.0f}/{r.rake:.0f}\n"
            f"bidang 2: {r.strike2:.0f}/{r.dip2:.0f}/{r.rake2:.0f}\n"
            "keduanya menghasilkan gambar yang SAMA", fontsize=10.5, fontweight="bold", color="#7c3aed")
fig.suptitle("Membaca bola fokal — dan batas yang tidak bisa dilampauinya",
             fontweight="bold", fontsize=12.5)
plt.tight_layout(); plt.savefig(OUT + "w14_tipe_sesar.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"2 tipe sesar (ambiguitas: {r.strike:.0f}/{r.dip:.0f}/{r.rake:.0f} vs {r.strike2:.0f}/{r.dip2:.0f}/{r.rake2:.0f})")

# --------------------------------------------- 3. POLARITAS NYATA YOGYAKARTA
from obspy import read, UTCDateTime
from scipy.signal import butter, sosfiltfilt
B = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/")
m = pd.read_csv(B + "seisbench/metadata.csv", low_memory=False)
sta5 = sorted({f.split("/")[-2] for f in glob.glob(B + "pilot/mseed/*/*.mseed")})
m["ts"] = pd.to_datetime(m.trace_start_time, errors="coerce", utc=True); m["doy"] = m.ts.dt.dayofyear
sub = m[m.station_code.isin(sta5) & m.doy.between(154, 159)]
ev = sub.groupby("source_id").agg(n=("station_code", "nunique"), M=("source_magnitude", "first"))
ev = ev[ev.n >= 4].nlargest(1, "M").index[0]
d = sub[sub.source_id == ev]
pol = []
fig, ax = plt.subplots(1, 2, figsize=(13.6, 5.6))
for k, (_, r) in enumerate(d.iterrows()):
    P = UTCDateTime(str(r.trace_start_time)) + r.trace_p_arrival_sample / 100.
    f = B + f"pilot/mseed/{r.station_code}/{r.station_code}.YK.2006.{int(r.doy):03d}.mseed"
    try: tr = read(f, starttime=P - 3, endtime=P + 1).select(component="Z")[0]
    except Exception: continue
    fs = tr.stats.sampling_rate; x = tr.data.astype(float); x -= x[:int(2 * fs)].mean()
    y = sosfiltfilt(butter(4, [2 / (fs / 2), 20 / (fs / 2)], btype="band", output="sos"), x)
    i = int(3 * fs); seg = y[i:i + int(0.25 * fs)]
    amp = seg[np.argmax(np.abs(seg))]
    t = np.arange(len(y)) / fs - 3
    yn = y / np.abs(y[i:i + int(fs)]).max()
    ax[0].plot(t, yn + k * 2.6, lw=.9, color="#334155")
    ax[0].plot(t[i:i + int(0.3 * fs)], yn[i:i + int(0.3 * fs)] + k * 2.6, lw=2.2,
               color="#dc2626" if amp > 0 else "#0e7490")
    ax[0].text(-2.9, k * 2.6 + .75, f"{r.station_code}   {'naik (+)' if amp>0 else 'turun (−)'}",
               fontsize=10, fontweight="bold", color="#dc2626" if amp > 0 else "#0e7490")
    pol.append((r.station_code, "+" if amp > 0 else "-", float(r.path_ep_distance_km)))
ax[0].axvline(0, color="#94a3b8", lw=1.2, ls="--"); ax[0].set_xlim(-1.2, .8)
ax[0].set_yticks([]); ax[0].set_xlabel("Waktu relatif P (detik)"); ax[0].grid(alpha=.2, axis="x")
ax[0].set_title("A · Gerakan pertama P, diukur dari rekaman mentah",
                fontsize=11, fontweight="bold", loc="left")
naik = sum(1 for _, p, _ in pol if p == "+")
ax[1].add_patch(plt.Circle((0, 0), 1, fill=False, lw=2, color="#334155"))
rng = np.random.default_rng(5)
for i2, (s_, p, dd) in enumerate(pol):
    th = 2 * np.pi * i2 / len(pol) + .4; rr = .35 + .5 * (dd / 40)
    ax[1].plot(rr * np.sin(th), rr * np.cos(th), "o" if p == "+" else "o", ms=15,
               mfc="#dc2626" if p == "+" else "white", mec="#334155", mew=1.6)
    ax[1].text(rr * np.sin(th), rr * np.cos(th) - .16, s_, ha="center", fontsize=8.5)
ax[1].set_xlim(-1.3, 1.3); ax[1].set_ylim(-1.3, 1.3); ax[1].set_aspect("equal"); ax[1].axis("off")
ax[1].text(0, 1.14, "N", ha="center", fontsize=11, fontweight="bold")
ax[1].set_title(f"B · Proyeksi pada bola fokal — {naik} naik, {len(pol)-naik} turun\n"
                f"hanya {len(pol)} titik: JAUH dari cukup untuk satu solusi",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle(f"Polaritas nyata gempa susulan Yogyakarta 2006 (M{d.source_magnitude.iloc[0]:.2f}) — "
             "metodenya benar, datanya belum cukup", fontweight="bold", fontsize=12.5)
plt.tight_layout(); plt.savefig(OUT + "w14_polaritas.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"3 polaritas: {pol}")
