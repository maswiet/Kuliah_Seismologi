#!/usr/bin/env python3
"""
Pengoreksi otomatis Milestone M5 — Seismologi PAGF262413.

Membaca setoran mahasiswa, membandingkannya dengan kunci, lalu menulis papan
pantau sesuai rancangan pada Asesmen_Era_AI_Seismologi.md.

Yang dihitung
-------------
  dt_P     galat pick P terhadap pick rujukan, detik (median antar-soal)
  err_km   galat episenter terhadap katalog, kilometer (median antar-soal)
  cal      laju cakupan: seberapa sering nilai rujukan jatuh di dalam selang
           keyakinan yang dilaporkan mahasiswa. Target ~0,80.
  R        rasio retensi U/A. Ini DIAGNOSTIK, bukan nilai dan bukan tuduhan.
  nilai    0,25*A + 0,75*U bila skor A dan U tersedia

Pemicu viva
-----------
Viva dijalankan pada mahasiswa yang tertandai DAN pada sampel acak
(bawaan 15%). Sampel acak itu bukan hiasan: tanpanya, dipanggil viva sama
dengan dituduh. Dengan sampel acak, dipanggil viva adalah hal biasa.

Kesehatan instrumen
-------------------
Selain menilai mahasiswa, skrip ini menilai SOALNYA SENDIRI lewat korelasi
A dengan U. Kelas sehat berada di sekitar 0,6-0,8. Bila korelasinya runtuh
ke nol, artefak yang dikumpulkan sudah berhenti mengukur apa pun -- dan yang
perlu diperbaiki adalah rancangan tugasnya, bukan mahasiswanya.

CATATAN JUJUR: pick rujukan berasal dari EqTransformer, bukan analis manusia.
dt_P besar belum tentu berarti mahasiswa salah. Ambang di sini memicu
percakapan, bukan sanksi.

Pemakaian
---------
    python3 skrip/m5_koreksi.py --kunci dataset_m5/_kunci/kunci_m5.csv \\
                                --setoran setoran/ --skor skor_AU.csv \\
                                --keluaran hasil_m5

setoran/  : kumpulan CSV setoran (boleh satu berkas per mahasiswa)
skor_AU.csv (opsional) : kolom nim, A, U
"""
import argparse, os, sys, glob, hashlib
import numpy as np, pandas as pd

KM_PER_DEG = 111.19
ALIAS = {
    "nim": ["nim", "NIM", "npm"],
    "soal": ["soal", "event", "kode"],
    "P_detik": ["P_detik", "P", "P_saya", "p_detik"],
    "S_detik": ["S_detik", "S", "S_saya", "s_detik"],
    "lat": ["lat", "latitude", "lintang"],
    "lon": ["lon", "longitude", "bujur"],
    "kedalaman_km": ["kedalaman_km", "depth", "kedalaman", "h_km"],
    "sel_bawah": ["P_selang_bawah", "kedalaman_selang_bawah", "selang_bawah", "ci_lo"],
    "sel_atas": ["P_selang_atas", "kedalaman_selang_atas", "selang_atas", "ci_hi"],
}


def rapikan(df):
    out = pd.DataFrame(index=df.index)
    for baku, kandidat in ALIAS.items():
        for c in kandidat:
            if c in df.columns:
                out[baku] = df[c]
                break
    return out


def baca_setoran(folder):
    berkas = sorted(glob.glob(os.path.join(folder, "*.csv")))
    if not berkas:
        sys.exit(f"tidak ada CSV di {folder}")
    kumpul, rusak = [], []
    for f in berkas:
        try:
            d = pd.read_csv(f, dtype={"nim": str})
            r = rapikan(d)
            if "nim" not in r or "soal" not in r:
                rusak.append((os.path.basename(f), "kolom nim/soal tidak ditemukan"))
                continue
            r["berkas"] = os.path.basename(f)
            kumpul.append(r)
        except Exception as e:
            rusak.append((os.path.basename(f), str(e)[:60]))
    if rusak:
        print("setoran yang tidak terbaca:")
        for n, a in rusak:
            print(f"  {n}: {a}")
    if not kumpul:
        sys.exit("tidak ada setoran yang terbaca")
    s = pd.concat(kumpul, ignore_index=True)
    s["nim"] = s.nim.astype(str).str.strip()
    return s


def jarak_km(lat1, lon1, lat2, lon2):
    return np.hypot((lon1 - lon2) * KM_PER_DEG * np.cos(np.radians(lat1)),
                    (lat1 - lat2) * KM_PER_DEG)


def dalam_selang(nilai, lo, hi):
    if pd.isna(nilai) or pd.isna(lo) or pd.isna(hi):
        return np.nan
    lo, hi = min(lo, hi), max(lo, hi)
    return float(lo <= nilai <= hi)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kunci", required=True)
    ap.add_argument("--setoran", required=True)
    ap.add_argument("--skor", help="CSV berkolom nim,A,U (opsional)")
    ap.add_argument("--keluaran", default="hasil_m5")
    ap.add_argument("--amb-dt", type=float, default=0.5, help="ambang |dt_P| detik")
    ap.add_argument("--amb-km", type=float, default=15.0, help="ambang galat episenter km")
    ap.add_argument("--amb-R", type=float, default=0.60, help="ambang rasio retensi")
    ap.add_argument("--sampel-acak", type=float, default=0.15, help="proporsi sampel viva acak")
    ap.add_argument("--garam", default="PAGF262413-2026")
    args = ap.parse_args()

    kunci = pd.read_csv(args.kunci, dtype={"nim": str})
    kunci["nim"] = kunci.nim.astype(str).str.strip()
    setor = baca_setoran(args.setoran)
    os.makedirs(args.keluaran, exist_ok=True)

    g = setor.merge(kunci, on=["nim", "soal"], how="left", indicator=True)
    yatim = g[g._merge == "left_only"][["nim", "soal", "berkas"]]
    if len(yatim):
        print(f"\n{len(yatim)} baris setoran tidak cocok dengan kunci (nim/soal keliru):")
        print(yatim.head(10).to_string(index=False))
    g = g[g._merge == "both"].drop(columns="_merge")

    w11 = g[g.tugas == "W11"].copy()
    w11["dt_P"] = (w11.P_detik - w11.P_ref_s).abs()
    w11["cakup"] = [dalam_selang(r.P_ref_s, r.sel_bawah, r.sel_atas) for _, r in w11.iterrows()]

    w12 = g[g.tugas == "W12"].copy()
    w12["err_km"] = jarak_km(w12.lat, w12.lon, w12.lat_ref, w12.lon_ref)
    w12["cakup"] = [dalam_selang(r.depth_ref_km, r.sel_bawah, r.sel_atas) for _, r in w12.iterrows()]

    papan = kunci[["nim", "nama"]].drop_duplicates().set_index("nim")
    papan["n_W11"] = w11.groupby("nim").size()
    papan["dt_P"] = w11.groupby("nim").dt_P.median().round(3)
    papan["dt_P_maks"] = w11.groupby("nim").dt_P.max().round(3)
    papan["n_W12"] = w12.groupby("nim").size()
    papan["err_km"] = w12.groupby("nim").err_km.median().round(2)
    papan["err_km_maks"] = w12.groupby("nim").err_km.max().round(2)
    cak = pd.concat([w11[["nim", "cakup"]], w12[["nim", "cakup"]]])
    papan["cal"] = cak.groupby("nim").cakup.mean().round(2)

    if args.skor:
        sk = pd.read_csv(args.skor, dtype={"nim": str})
        sk["nim"] = sk.nim.astype(str).str.strip()
        papan = papan.join(sk.set_index("nim")[["A", "U"]])
        papan["R"] = (papan.U / papan.A.replace(0, np.nan)).round(3)
        papan["nilai"] = (0.25 * papan.A + 0.75 * papan.U).round(1)
    else:
        papan["A"] = papan["U"] = papan["R"] = papan["nilai"] = np.nan

    papan["lulus_dt"] = papan.dt_P <= args.amb_dt
    papan["lulus_km"] = papan.err_km <= args.amb_km

    alasan = []
    for nim, r in papan.iterrows():
        a = []
        if pd.notna(r.R) and r.R < args.amb_R: a.append(f"R={r.R:.2f}")
        if pd.notna(r.dt_P) and r.dt_P > args.amb_dt: a.append(f"dt_P={r.dt_P:.2f}s")
        if pd.notna(r.err_km) and r.err_km > args.amb_km: a.append(f"err={r.err_km:.1f}km")
        if pd.isna(r.n_W11) or pd.isna(r.n_W12): a.append("setoran tidak lengkap")
        alasan.append("; ".join(a))
    papan["tertandai"] = [bool(a) for a in alasan]
    papan["alasan"] = alasan

    # sampel acak — reproducible, tapi tidak dapat ditebak mahasiswa
    def undi(nim):
        h = hashlib.sha256(f"{args.garam}|viva|{nim}".encode()).hexdigest()
        return int(h[:8], 16) / 0xFFFFFFFF
    papan["sampel_acak"] = [(not t) and (undi(n) < args.sampel_acak)
                            for n, t in zip(papan.index, papan.tertandai)]
    papan["viva"] = papan.tertandai | papan.sampel_acak

    papan.to_csv(os.path.join(args.keluaran, "papan_pantau.csv"))
    vv = papan[papan.viva][["nama", "alasan", "tertandai", "sampel_acak"]].copy()
    vv["alasan"] = np.where(vv.tertandai, vv.alasan, "sampel acak")
    vv.to_csv(os.path.join(args.keluaran, "daftar_viva.csv"))

    # ---------- ringkasan mutu ----------
    L = []
    P = L.append
    P("RINGKASAN MUTU M5 — Seismologi PAGF262413")
    P("=" * 62)
    P(f"mahasiswa pada kunci        : {len(papan)}")
    P(f"menyetorkan W11             : {int(papan.n_W11.notna().sum())}")
    P(f"menyetorkan W12             : {int(papan.n_W12.notna().sum())}")
    P("")
    P("KETEPATAN")
    P(f"  median |dt_P| kelas       : {papan.dt_P.median():.3f} s   (ambang {args.amb_dt} s)")
    P(f"  lulus ambang dt_P         : {int(papan.lulus_dt.sum())}/{int(papan.dt_P.notna().sum())}")
    P(f"  median galat episenter    : {papan.err_km.median():.2f} km  (ambang {args.amb_km} km)")
    P(f"  lulus ambang episenter    : {int(papan.lulus_km.sum())}/{int(papan.err_km.notna().sum())}")
    P("")
    P("KALIBRASI KETIDAKPASTIAN")
    P(f"  laju cakupan kelas        : {papan.cal.mean():.2f}   (target ~0,80)")
    if papan.cal.mean() < 0.6:
        P("  -> terlalu percaya diri: selang yang dilaporkan terlalu sempit")
    elif papan.cal.mean() > 0.95:
        P("  -> terlalu hati-hati: selang terlalu lebar sehingga tidak informatif")
    P("")
    if papan.R.notna().any():
        P("RETENSI")
        P(f"  median R                  : {papan.R.median():.2f}   (ambang {args.amb_R})")
        P(f"  R < ambang                : {int((papan.R < args.amb_R).sum())} mahasiswa")
        ok = papan[["A", "U"]].dropna()
        N_MIN_KORELASI = 15   # di bawah ini korelasi terlalu berisik untuk ditafsirkan
        if len(ok) < N_MIN_KORELASI:
            P(f"  korelasi A vs U           : tidak dilaporkan (n={len(ok)} < {N_MIN_KORELASI})")
            P("  -> sampel terlalu kecil; korelasi pada n sekecil ini didominasi derau.")
        else:
            r = float(np.corrcoef(ok.A, ok.U)[0, 1])
            P(f"  korelasi A vs U           : {r:.2f}  (n={len(ok)})")
            if r < 0.3:
                P("  -> ALARM: artefak berbantuan sudah berhenti mengukur pemahaman.")
                P("     Yang perlu diperbaiki rancangan tugasnya, bukan mahasiswanya.")
            elif r > 0.85:
                P("  -> verifikasi mungkin terlalu mirip tugasnya; pertimbangkan variasi soal.")
            else:
                P("  -> sehat (rentang wajar 0,6-0,8).")
        pede = papan[(papan.cal.notna()) & (papan.cal <= 0.25)]
    if len(pede):
        P(f"  perlu umpan balik kalibrasi ({len(pede)} mahasiswa):")
        for nim, r in pede.iterrows():
            P(f"    {nim} {r.nama}: cakupan {r.cal:.2f} — selang terlalu sempit, "
              f"bukan tanda teliti melainkan tanda belum paham batas ketidakpastiannya")
        P("  Ini BUKAN pemicu viva. Ia sinyal pengajaran: bahas ulang cara melaporkan selang.")
    P("")
    P("VIVA")
    P(f"  tertandai                 : {int(papan.tertandai.sum())}")
    P(f"  sampel acak               : {int(papan.sampel_acak.sum())}")
    P(f"  total dipanggil           : {int(papan.viva.sum())}  "
      f"(~{int(papan.viva.sum())*5} menit pada 5 menit/orang)")
    P("")
    P("PENGINGAT")
    P("  Pick rujukan berasal dari EqTransformer, bukan analis manusia.")
    P("  dt_P besar memicu percakapan, bukan sanksi. Viva yang memutuskan.")
    teks = "\n".join(L)
    print("\n" + teks)
    open(os.path.join(args.keluaran, "ringkasan_mutu.txt"), "w").write(teks + "\n")
    print(f"\nditulis: {args.keluaran}/papan_pantau.csv, daftar_viva.csv, ringkasan_mutu.txt")


if __name__ == "__main__":
    main()
