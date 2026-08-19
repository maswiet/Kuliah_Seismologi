"""
Figur Minggu 13 — magnitudo, momen, energi, dan intensitas.
Seismologi PAGF262413, Program Studi Sarjana Geofisika FMIPA UGM.

Sumber data (arsip lokal, tidak disertakan di repo karena ukurannya):
  catalog_magnitude.csv, amplitudes.csv   gempa susulan Yogyakarta 2006
  BMKG_Earthquake_Catalog.csv             katalog BMKG 1998-2024

Menghasilkan empat PNG di Gambar/. Jalankan dari akar repo:
    python3 skrip/figur_minggu13.py
"""
import os
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

D    = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/full/")
BMKG = os.path.expanduser("~/Work/DATA/AFM/BMKG_Earthquake_Catalog.csv")
OUT  = "Gambar/"
DM   = 0.1

mag = pd.read_csv(D+"catalog_magnitude.csv")
amp = pd.read_csv(D+"amplitudes.csv")

# ------------------------------------------- 1. MAGNITUDO ADALAH RATA-RATA
j = amp.merge(mag[["evid","ML","n_sta"]], on="evid")
j["ml_sta"] = np.log10(j.amp_mm) + 2.76*np.log10(j.hypo_km) - 2.48   # kalibrasi Hutton-Boore
j["sisa"]   = j.ml_sta - j.ML
g = j.groupby("evid").ml_sta.agg(["std","count","mean"])
g = g[g["count"] >= 5]
contoh = mag.loc[mag.n_sta.idxmax(), "evid"]
sub = j[j.evid == contoh].sort_values("hypo_km")

fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
ax[0].plot(sub.hypo_km, sub.ml_sta, "o", ms=10, color="#0e7490")
for _, r in sub.iterrows():
    ax[0].annotate(r.sta, (r.hypo_km, r.ml_sta), textcoords="offset points", xytext=(7,-3), fontsize=8)
mrata = sub.ml_sta.mean()
ax[0].axhline(mrata, color="#dc2626", lw=1.6, ls="--", label=f"rata-rata = {mrata:.2f}")
ax[0].fill_between([sub.hypo_km.min()-2, sub.hypo_km.max()+2],
                   mrata-sub.ml_sta.std(), mrata+sub.ml_sta.std(), color="#dc2626", alpha=.10,
                   label=f"± 1 simpangan baku ({sub.ml_sta.std():.2f})")
ax[0].set_xlabel("Jarak hiposentral (km)"); ax[0].set_ylabel("Magnitudo dihitung di stasiun itu")
ax[0].legend(fontsize=9.5); ax[0].grid(alpha=.25)
ax[0].set_title(f"A · Satu gempa, {len(sub)} stasiun, {len(sub)} jawaban berbeda",
                fontsize=11, fontweight="bold", loc="left")
ax[1].hist(g["std"], bins=50, color="#94a3b8", edgecolor="white")
ax[1].axvline(g["std"].median(), color="#dc2626", lw=1.8, ls="--")
ax[1].text(g["std"].median()*1.08, ax[1].get_ylim()[1]*.85,
           f"median {g['std'].median():.2f}\nsatuan magnitudo",
           color="#dc2626", fontweight="bold", fontsize=10)
ax[1].set_xlabel("Simpangan baku antar-stasiun (satuan magnitudo)"); ax[1].set_ylabel("Jumlah event")
ax[1].grid(alpha=.25)
ax[1].set_title(f"B · Sebaran pada {len(g):,} event dengan ≥5 stasiun".replace(",","."),
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle("Magnitudo bukan hasil pengukuran tunggal — ia rata-rata dari banyak stasiun yang tidak pernah sepakat",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w13_magnitudo_rerata.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"1 rata-rata   sebar antar-stasiun median {g['std'].median():.2f} satuan magnitudo")

# ---------------------------------------------------- 2. AMPLITUDO & JARAK
fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
kel = [(-1.0, -0.5), (-0.2, 0.2), (0.8, 1.4), (2.0, 3.6)]
warna = ["#cbd5e1", "#94a3b8", "#0e7490", "#b45309"]
for (lo, hi), c in zip(kel, warna):
    s = j[j.ML.between(lo, hi)]
    ax[0].loglog(s.hypo_km, s.amp_mm, ".", ms=1.6, color=c, alpha=.35,
                 label=f"ML {lo:+.1f} .. {hi:+.1f}  (n={len(s):,})".replace(",","."))
R = np.logspace(np.log10(2), np.log10(80), 50)
ax[0].loglog(R, 10**(-2.76*np.log10(R)+1.9), "--", color="#dc2626", lw=1.8,
             label="peluruhan −2,76 log R")
ax[0].set_xlabel("Jarak hiposentral (km)"); ax[0].set_ylabel("Amplitudo (mm)")
lg = ax[0].legend(fontsize=8.5, markerscale=6); ax[0].grid(alpha=.25, which="both")
ax[0].set_title("A · Amplitudo mentah jatuh dua orde hanya karena jarak",
                fontsize=11, fontweight="bold", loc="left")
ax[1].plot(j.hypo_km, j.sisa, ".", ms=1.2, color="#94a3b8", alpha=.25)
bin_ = pd.cut(j.hypo_km, np.arange(0, 80, 5))
med = j.groupby(bin_, observed=True).sisa.median()
xs = [iv.mid for iv in med.index]
ax[1].plot(xs, med.values, "o-", color="#dc2626", lw=2, ms=6, label="median per 5 km")
ax[1].axhline(0, color="#334155", lw=1)
ax[1].set_ylim(-3, 1); ax[1].set_xlabel("Jarak hiposentral (km)")
ax[1].set_ylabel("Magnitudo stasiun − magnitudo katalog")
ax[1].legend(fontsize=9.5); ax[1].grid(alpha=.25)
ax[1].set_title("B · Sisanya bergantung jarak — bukan sekadar pergeseran tetap,\n"
                "suku koreksi jaraknya sendiri yang tidak cocok untuk Jawa",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle("Mengapa magnitudo mustahil tanpa koreksi jarak — dan mengapa kalibrasi impor tidak bisa dipakai begitu saja",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w13_amplitudo_jarak.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"2 amplitudo   bias kalibrasi HB87 di Jawa {j.sisa.median():+.2f} satuan magnitudo")

# -------------------------------------------------------------- 3. SATURASI
b = pd.read_csv(BMKG, low_memory=False)
b["Magnitude"] = pd.to_numeric(b.Magnitude, errors="coerce")
b = b.dropna(subset=["Magnitude"])
pilih = ["MLv", "mb", "Mw(mB)"]
lbl = {"MLv": "$M_L$ (lokal)", "mb": "$m_b$ (badan)", "Mw(mB)": "$M_W$ (momen)"}
war = {"MLv": "#0e7490", "mb": "#b45309", "Mw(mB)": "#7c3aed"}
fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
for t in pilih:
    s = b[b["Mag Type"] == t].Magnitude
    ax[0].hist(s, bins=np.arange(1, 8.5, 0.15), histtype="step", lw=2, color=war[t],
               label=f"{lbl[t]}  n={len(s):,}  maks {s.max():.1f}".replace(",","."))
    ax[0].axvline(s.max(), color=war[t], lw=1.2, ls=":")
ax[0].set_xlabel("Magnitudo"); ax[0].set_ylabel("Jumlah gempa"); ax[0].set_yscale("log")
ax[0].legend(fontsize=9.5); ax[0].grid(alpha=.25)
ax[0].set_title("A · Tiap skala berhenti di tempat yang berbeda", fontsize=11, fontweight="bold", loc="left")
q = pd.DataFrame({t: b[b["Mag Type"] == t].Magnitude.quantile([.5, .9, .99, 1.0]).values for t in pilih},
                 index=["median", "persentil 90", "persentil 99", "maksimum"])
X = np.arange(len(q)); w = .26
for i, t in enumerate(pilih):
    ax[1].bar(X + (i-1)*w, q[t], w, color=war[t], label=lbl[t])
    for x, v in zip(X + (i-1)*w, q[t]):
        ax[1].text(x, v+.06, f"{v:.1f}", ha="center", fontsize=8.5, color=war[t], fontweight="bold")
ax[1].set_xticks(X); ax[1].set_xticklabels(q.index); ax[1].set_ylabel("Magnitudo")
ax[1].legend(fontsize=9.5); ax[1].grid(alpha=.25, axis="y"); ax[1].set_ylim(0, 9)
ax[1].set_title("B · Langit-langit tiap skala, bukan kebetulan", fontsize=11, fontweight="bold", loc="left")
fig.suptitle(f"Saturasi skala magnitudo — bukti dari {len(b):,} gempa katalog BMKG 1998–2024\n".replace(",",".") +
             "$M_L$ mentok di 6,6 dan $m_b$ di 7,0; hanya $M_W$ yang terus naik. Itulah sebabnya \"skala Richter\" keliru untuk gempa besar.",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w13_saturasi.png", dpi=125, bbox_inches="tight"); plt.close()
print("3 saturasi    " + ", ".join(f"{t} maks {b[b['Mag Type']==t].Magnitude.max():.1f}" for t in pilih))

# --------------------------------------------------- 4. GUTENBERG-RICHTER
M = mag.ML.dropna().values
def b_mle(mc):
    s = M[M >= mc - DM/2]
    return ((1/np.log(10))/(s.mean()-(mc-DM/2)), len(s)) if len(s) >= 100 else (np.nan, 0)
mcs = np.arange(-0.4, 1.7, 0.1)
bs  = np.array([b_mle(m)[0] for m in mcs])
ns  = np.array([b_mle(m)[1] for m in mcs])
bins = np.arange(M.min(), M.max()+DM, DM)
hist, _ = np.histogram(M, bins=bins)
mc_naif = bins[np.argmax(hist)]
b_naif, _ = b_mle(mc_naif)
plateau = slice(np.argmin(abs(mcs-0.7)), np.argmin(abs(mcs-1.0))+1)
b_baik = np.nanmean(bs[plateau]); mc_baik = 0.8

fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.0))
kum = np.array([(M >= x).sum() for x in bins])
ax[0].semilogy(bins, kum, "o", ms=3.5, color="#334155", label="kumulatif")
ax[0].semilogy(bins[:-1]+DM/2, hist, ".", ms=3, color="#cbd5e1", label="tak kumulatif")
xx = np.linspace(mc_baik, M.max(), 20)
a = np.log10((M >= mc_baik).sum()) + b_baik*mc_baik
ax[0].semilogy(xx, 10**(a - b_baik*xx), "-", color="#dc2626", lw=2,
               label=f"b = {b_baik:.2f} (Mc = {mc_baik:.1f})")
a2 = np.log10((M >= mc_naif).sum()) + b_naif*mc_naif
ax[0].semilogy(xx, 10**(a2 - b_naif*xx), "--", color="#b45309", lw=2,
               label=f"b = {b_naif:.2f} (Mc naif = {mc_naif:.1f})")
ax[0].axvline(mc_baik, color="#dc2626", lw=1, ls=":")
ax[0].axvline(mc_naif, color="#b45309", lw=1, ls=":")
ax[0].set_xlabel("Magnitudo $M_L$"); ax[0].set_ylabel("Jumlah gempa ≥ M")
ax[0].legend(fontsize=9.5); ax[0].grid(alpha=.25, which="both")
ax[0].set_title(f"A · Frekuensi–magnitudo, {len(M):,} gempa susulan".replace(",","."),
                fontsize=11, fontweight="bold", loc="left")
ax[1].plot(mcs, bs, "o-", color="#0e7490", lw=1.6, ms=5)
ax[1].axvspan(0.7, 1.0, color="#dcfce7", alpha=.8)
ax[1].text(0.85, np.nanmin(bs)+0.05, "dataran\nstabil", ha="center", fontsize=9.5,
           color="#15803d", fontweight="bold")
ax[1].axvline(mc_naif, color="#b45309", lw=1.6, ls="--")
ax[1].text(mc_naif+0.04, np.nanmax(bs)-0.03, f"Mc naif dari\nmaximum curvature\nb = {b_naif:.2f}",
           fontsize=9, color="#b45309", fontweight="bold", va="top")
ax[1].axhline(b_baik, color="#dc2626", lw=1.2, ls=":")
ax[1].set_xlabel("Ambang kelengkapan Mc yang dipakai"); ax[1].set_ylabel("b-value yang dihasilkan")
ax[1].grid(alpha=.25)
ax[1].set_title(f"B · b bergantung pada Mc: {b_naif:.2f} vs {b_baik:.2f} — beda {100*(b_baik-b_naif)/b_naif:.0f}%",
                fontsize=11, fontweight="bold", loc="left")
fig.suptitle("Nilai-b tidak keluar begitu saja dari data — ia keluar dari pilihan Mc yang kalian buat",
             fontweight="bold", fontsize=12)
plt.tight_layout(); plt.savefig(OUT+"w13_gutenberg_richter.png", dpi=125, bbox_inches="tight"); plt.close()
print(f"4 G-R         Mc naif {mc_naif:.2f} -> b {b_naif:.2f} | dataran Mc 0,8 -> b {b_baik:.2f}")
