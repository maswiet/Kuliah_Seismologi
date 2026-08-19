"""
Figur Minggu 11 — anatomi seismogram dan pemrosesan sinyal digital.
Seismologi PAGF262413, Program Studi Sarjana Geofisika FMIPA UGM.

Sumber data (arsip lokal, tidak disertakan di repo karena ukurannya):
  MS   : miniSEED kontinu 24 jam, gempa susulan Yogyakarta 2006,
         stasiun TF14 jaringan YK, 100 Hz, tiga komponen
  META : metadata SeisBench berisi pick rujukan P dan S (keluaran EqTransformer)

Menghasilkan lima PNG di Gambar/. Diagram w11_konvolusi.svg ditulis tangan,
bukan keluaran skrip ini.

Jalankan dari akar repo:  python3 skrip/figur_minggu11.py
"""
import os
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime
from scipy.signal import butter, sosfiltfilt, sosfilt

MS   = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/pilot/mseed/TF14/TF14.YK.2006.155.mseed")
META = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/seisbench/metadata.csv")
OUT  = "Gambar/"
FS   = 100.

meta = pd.read_csv(META, low_memory=False)

def event(prefix):
    r = meta[(meta.station_code == "TF14") & (meta.trace_start_time.str.startswith(prefix))].iloc[0]
    t0 = UTCDateTime(str(r.trace_start_time))
    return r, t0 + r.trace_p_arrival_sample/100., t0 + r.trace_s_arrival_sample/100.

def trace(P, pre, post, comp=None):
    st = read(MS, starttime=P-pre, endtime=P+post)
    if comp: st = st.select(component=comp)
    out = []
    for tr in st:
        y = tr.data.astype(float)
        out.append(y - np.polyval(np.polyfit(np.arange(len(y)), y, 1), np.arange(len(y))))
    return st, np.array(out)

def bp(x, lo, hi, nc=4, zero=True):
    sos = butter(nc, [lo/(FS/2), hi/(FS/2)], btype="band", output="sos")
    return sosfiltfilt(sos, x) if zero else sosfilt(sos, x)

def spektrum(x):
    x = (x - x.mean()) * np.hanning(len(x))
    return np.fft.rfftfreq(len(x), 1/FS), np.abs(np.fft.rfft(x))

# ---------------------------------------------------------------- 1. PENAPIS
r, P, S = event("2006-06-04T22:50:34")
_, X = trace(P, 20, 12, "Z"); x = X[0]; t = np.arange(len(x))/FS - 20
snr = lambda y: np.std(y[int(20*FS):int(22*FS)]) / np.std(y[int(2*FS):int(15*FS)])
f1, f2 = bp(x, 2, 15), bp(x, 15, 45)
zp, ca = bp(x, 5, 10, 6, True), bp(x, 5, 10, 6, False)

def onset(y):
    n = np.std(y[int(2*FS):int(15*FS)])
    for k in range(int(19.5*FS), int(21.5*FS)):
        if abs(y[k]) > 5*n: return k/FS - 20
    return np.nan
oz, oc = onset(zp), onset(ca)

fig, ax = plt.subplots(4, 1, figsize=(13.5, 10.4))
for i, (y, jd, c) in enumerate([
    (x,  f"A · Rekaman mentah — di mana P mulai?   SNR = {snr(x):.2f}", "#334155"),
    (f1, f'B · Bandpass 2–15 Hz, pita "baku" yang biasa disalin dari buku teks — SNR = {snr(f1):.1f}  (memburuk!)', "#b45309"),
    (f2, f"C · Bandpass 15–45 Hz, dicocokkan dengan frekuensi sudut gempa mikro ini — SNR = {snr(f2):.1f}", "#0e7490")]):
    ax[i].plot(t, y, lw=.55, color=c); ax[i].set_xlim(-20, 12); ax[i].grid(alpha=.25)
    ax[i].axvline(0, color="#dc2626", lw=1.1, ls="--"); ax[i].axvline(S-P, color="#2563eb", lw=1.1, ls="--")
    ax[i].set_title(jd, fontsize=10.5, fontweight="bold", loc="left"); ax[i].set_ylabel("count", fontsize=8)
    if i == 2:
        yl = ax[i].get_ylim()[1]
        ax[i].text(0.3, yl*.6, "P", color="#dc2626", fontweight="bold")
        ax[i].text(S-P+0.3, yl*.6, "S", color="#2563eb", fontweight="bold")
n1 = np.abs(zp[int(19*FS):int(22*FS)]).max(); n2 = np.abs(ca[int(19*FS):int(22*FS)]).max()
ax[3].plot(t, zp/n1, lw=1.3, color="#0e7490", label=f"zero-phase, 2 lintasan  →  onset {oz:+.2f} s")
ax[3].plot(t, ca/n2, lw=1.3, color="#b45309", label=f"kausal, 1 lintasan  →  onset {oc:+.2f} s")
ax[3].axvline(0, color="#dc2626", lw=1.2, ls="--"); ax[3].set_xlim(-1.0, 1.5); ax[3].grid(alpha=.25)
ax[3].legend(fontsize=9.5, loc="upper left"); ax[3].set_xlabel("Waktu relatif terhadap pick P rujukan (detik)")
ax[3].set_title(f"D · Bandpass 5–10 Hz yang sama, dua cara menjalankannya — selisih onset {abs(oc-oz)*1000:.0f} ms  ≈ {abs(oc-oz)*6:.1f} km kesalahan lokasi",
                fontsize=10.5, fontweight="bold", loc="left")
fig.suptitle(f"TF14 · gempa susulan Yogyakarta 2006-06-04 22:50 · M{r.source_magnitude:.2f} · jarak {r.path_ep_distance_km:.1f} km", fontweight="bold", y=.997)
plt.tight_layout(); plt.savefig(OUT+"w11_penapis.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"1 penapis   SNR {snr(x):.2f} -> {snr(f1):.1f} -> {snr(f2):.1f} | onset {oz:+.2f}/{oc:+.2f} ({abs(oc-oz)*1000:.0f} ms)")

# --------------------------------------------------------- 2. TIGA KOMPONEN
r2, P2, S2 = event("2006-06-04T19:53:28")
st2, X2 = trace(P2, 8, 12)
idx = {tr.stats.channel[-1]: i for i, tr in enumerate(st2)}
t2 = np.arange(X2.shape[1])/FS - 8
fig, ax = plt.subplots(3, 1, figsize=(13, 6.6), sharex=True)
for i, (ch, lab, c) in enumerate([("Z", "Z — vertikal", "#1e293b"), ("N", "N — utara", "#0e7490"), ("E", "E — timur", "#b45309")]):
    y = bp(X2[idx[ch]], 2, 25)
    ax[i].plot(t2, y, lw=.6, color=c); ax[i].set_ylabel(lab, fontsize=10); ax[i].grid(alpha=.25)
    ax[i].axvline(0, color="#dc2626", lw=1.2); ax[i].axvline(S2-P2, color="#2563eb", lw=1.2)
    yl = ax[i].get_ylim()[1]
    ax[i].text(0.15, yl*.7, "P", color="#dc2626", fontweight="bold")
    ax[i].text(S2-P2+0.15, yl*.7, "S", color="#2563eb", fontweight="bold")
    ax[i].text(.985, .08, f"amplitudo puncak {np.abs(y).max():.0f} count", transform=ax[i].transAxes,
               ha="right", fontsize=9, bbox=dict(fc="white", ec="#cbd5e1", alpha=.85))
ax[0].set_xlim(-3, 10); ax[2].set_xlabel("Waktu relatif terhadap P (detik)")
ax[0].set_title(f"TF14 · M{r2.source_magnitude:.2f}, jarak {r2.path_ep_distance_km:.1f} km, S−P = {S2-P2:.2f} s · bandpass 2–25 Hz\n"
                "P kuat di vertikal; S jauh lebih besar di kedua horizontal — itulah tanda gelombang transversal",
                fontweight="bold", fontsize=11)
plt.tight_layout(); plt.savefig(OUT+"w11_tiga_komponen.png", dpi=125, bbox_inches="tight"); plt.close()
print("2 tiga komponen")

# --------------------------------------------------------------- 3. ALIASING
_, XA = trace(P2, 20, 15, "Z"); xa = XA[0]
fig, ax = plt.subplots(2, 1, figsize=(13, 7.2))
f0, T, fsg = 30., .25, 40.
tc = np.linspace(0, T, 4000); ts = np.arange(0, T, 1/fsg); fa = abs(f0 - round(f0/fsg)*fsg)
ax[0].plot(tc, np.sin(2*np.pi*f0*tc), lw=1.3, color="#94a3b8", label=f"sinyal asli {f0:.0f} Hz")
ax[0].plot(tc, np.sin(2*np.pi*fa*tc + np.pi), lw=2.2, color="#dc2626", label=f'yang "terbaca" {fa:.0f} Hz — palsu')
ax[0].plot(ts, np.sin(2*np.pi*f0*ts), "o", ms=8, color="#1e293b", label=f"cuplikan pada {fsg:.0f} Hz (Nyquist {fsg/2:.0f} Hz)")
ax[0].legend(fontsize=9.5, loc="upper right"); ax[0].grid(alpha=.25); ax[0].set_xlim(0, T)
ax[0].set_xlabel("Waktu (detik)")
ax[0].set_title(f'A · Konsep: {f0:.0f} Hz dicuplik pada {fsg:.0f} Hz menyamar jadi {fa:.0f} Hz. Frekuensi di atas Nyquist tidak hilang — ia melipat ke bawah.',
                fontsize=10.5, fontweight="bold", loc="left")
from scipy.signal import decimate
seg = xa[int(18*FS):int(26*FS)]; t8 = np.arange(len(seg))/FS
salah = seg[::5]; benar = decimate(seg, 5, ftype="iir", zero_phase=True)
ax[1].plot(t8, seg, lw=.6, color="#cbd5e1", label="asli 100 Hz")
ax[1].plot(np.arange(len(salah))/20., salah, lw=1.1, color="#dc2626", label="ambil tiap sampel ke-5 TANPA tapis anti-alias → 20 Hz")
ax[1].plot(np.arange(len(benar))/20., benar, lw=1.1, color="#0e7490", label="desimasi BENAR (tapis dulu, baru cuplik) → 20 Hz")
ax[1].set_xlim(1.6, 3.4); ax[1].grid(alpha=.25); ax[1].legend(fontsize=9.5, loc="upper right")
ax[1].set_xlabel("Waktu (detik)"); ax[1].set_ylabel("count")
ax[1].set_title("B · Pada data nyata TF14: menurunkan laju cuplik tanpa menapis lebih dulu menyuntikkan energi frekuensi tinggi sebagai riak palsu.",
                fontsize=10.5, fontweight="bold", loc="left")
plt.tight_layout(); plt.savefig(OUT+"w11_aliasing.png", dpi=125, bbox_inches="tight"); plt.close()
print("3 aliasing")

# --------------------------------------------------------------- 4. SPEKTRUM
tt = np.arange(len(xa))/FS - 20; W = int(2.5*FS); i0 = int(20*FS)
wins = [("Derau (sebelum P)", xa[i0-int(14*FS):i0-int(14*FS)+W], "#64748b", -14),
        ("Jendela P",         xa[i0:i0+W],                        "#dc2626", 0),
        ("Jendela S",         xa[i0+int((S2-P2)*FS):i0+int((S2-P2)*FS)+W], "#2563eb", S2-P2)]
fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.1))
ax[0].plot(tt, xa, lw=.5, color="#334155")
for lab, seg_, c, off in wins:
    ax[0].axvspan(off, off+2.5, color=c, alpha=.20)
    ax[0].text(off+1.25, ax[0].get_ylim()[1]*.82, lab.split()[0], ha="center", fontsize=9, color=c, fontweight="bold")
ax[0].set_xlim(-16, 8); ax[0].grid(alpha=.25); ax[0].set_xlabel("Waktu relatif P (detik)"); ax[0].set_ylabel("count")
ax[0].set_title("A · Tiga jendela pada trace yang sama", fontsize=10.5, fontweight="bold", loc="left")
fN, AN = spektrum(wins[0][1])
for lab, seg_, c, _ in wins:
    f, A = spektrum(seg_); ax[1].loglog(f[1:], A[1:], lw=1.2, color=c, label=lab)
ax[1].axvspan(15, 45, color="#0e7490", alpha=.10)
ax[1].text(25, 3e5, "pita 15–45 Hz\nyang dipakai\ndi figur penapis", fontsize=8.5, ha="center", color="#0e7490", fontweight="bold")
ax[1].set_xlim(.5, 50); ax[1].grid(alpha=.25, which="both"); ax[1].legend(fontsize=9.5, loc="lower left")
ax[1].set_xlabel("Frekuensi (Hz)"); ax[1].set_ylabel("Amplitudo spektral")
ax[1].set_title("B · Derau runtuh cepat di atas ~10 Hz, sinyal tidak — itulah sebabnya pita tinggi menang",
                fontsize=10.5, fontweight="bold", loc="left")
fig.suptitle(f"TF14 · M{r2.source_magnitude:.2f}, jarak {r2.path_ep_distance_km:.1f} km — memilih pita lewat itu keputusan berdasar spektrum, bukan kebiasaan", fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"w11_spektrum.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"4 spektrum  derau 1 Hz = {AN[np.argmin(abs(fN-1))]:.0f}, 30 Hz = {AN[np.argmin(abs(fN-30))]:.0f}")

# --------------------------------------------------------------- 5. STACKING
sig = xa[i0:i0+int(1.5*FS)].copy()
_, XQ = trace(P2, 600, -500, "Z"); quiet = XQ[0]
rng = np.random.default_rng(11); Ns = [1, 2, 4, 8, 16, 32, 64, 128]; TRIAL = 40
L, pos, AMP = int(4*FS), int(1.2*FS), .05
med, keep = [], {}
for N in Ns:
    v = []
    for k in range(TRIAL):
        acc = np.zeros(L)
        for _ in range(N):
            j = rng.integers(0, len(quiet)-L); n = quiet[j:j+L].copy()
            n[pos:pos+len(sig)] += sig*AMP; acc += n
        acc /= N; v.append(np.std(acc[pos:pos+len(sig)])/np.std(acc[:pos-20]))
        if k == 0: keep[N] = acc
    med.append(float(np.median(v)))
fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.9)); tS = np.arange(L)/FS
for N, off, c in [(1, 0, "#94a3b8"), (8, 3.2, "#b45309"), (64, 6.4, "#0e7490")]:
    ax[0].plot(tS, keep[N]/np.abs(keep[64]).max() + off, lw=.7, color=c)
    ax[0].text(.06, off+1.35, f"N = {N}   SNR = {med[Ns.index(N)]:.1f}", fontsize=9.5, color=c, fontweight="bold")
ax[0].axvline(pos/FS, color="#dc2626", lw=1.1, ls="--"); ax[0].set_yticks([]); ax[0].grid(alpha=.25, axis="x")
ax[0].set_xlabel("Waktu (detik)"); ax[0].set_ylim(-1.6, 8.4)
ax[0].set_title("A · Sinyal sama ditumpuk N kali di atas derau TF14 asli", fontsize=10.5, fontweight="bold", loc="left")
ax[1].loglog(Ns, med, "o-", color="#0e7490", lw=1.7, ms=7, label=f"pengukuran (median {TRIAL} percobaan)")
ax[1].loglog(Ns, med[0]*np.sqrt(Ns), "--", color="#dc2626", lw=1.5, label=r"teori   SNR $\propto\ \sqrt{N}$")
ax[1].set_xlabel("Jumlah jejak yang ditumpuk, N"); ax[1].set_ylabel("SNR"); ax[1].grid(alpha=.25, which="both"); ax[1].legend(fontsize=9.5)
ax[1].set_title("B · Menumpuk 100 jejak memberi 10× perbaikan — bukan 100×", fontsize=10.5, fontweight="bold", loc="left")
fig.suptitle("Stacking: derau acak saling meniadakan, sinyal koheren bertahan", fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"w11_stacking.png", dpi=125, bbox_inches="tight"); plt.close()
print("5 stacking  SNR:", [round(s, 1) for s in med])
