#!/usr/bin/env python3
"""
Penyiap dataset Milestone M5 — Seismologi PAGF262413.

Membuat paket soal UNIK per mahasiswa dari arsip gempa susulan Yogyakarta 2006,
lalu menulis kunci jawaban terpisah yang TIDAK boleh dibagikan.

Tiap mahasiswa menerima:

  W11 (pemrosesan sinyal & picking)
      3 potongan rekaman 60 detik dari data kontinu mentah, satu per tingkat
      kesulitan (SNR mudah / sedang / sulit). Offset P diacak 12-45 detik
      sehingga posisinya tidak bisa dihafal atau disalin antar-mahasiswa.

  W12 (penentuan lokasi)
      3 event, satu per tingkat kesulitan geometri jaringan (gap azimut
      tersier bawah / tengah / atas), lengkap dengan waktu tempuh P dan S
      di seluruh stasiun yang merekamnya.

Pembagian soal berjenjang (stratified) supaya adil: setiap mahasiswa
mendapat satu soal mudah, satu sedang, dan satu sulit pada tiap tugas.
Tanpa ini, ambang nilai tetap akan menghukum mahasiswa yang kebetulan
mendapat soal berat.

Undian di-seed dari NIM sehingga hasilnya sama persis bila dijalankan ulang.

CATATAN JUJUR: pick rujukan pada kunci berasal dari EqTransformer, bukan
analis manusia. Ia rujukan yang konsisten, bukan kebenaran mutlak.

Pemakaian
---------
    python3 skrip/m5_siapkan_dataset.py --peserta peserta.csv --keluaran dataset_m5

peserta.csv wajib punya kolom: nim, nama
"""
import argparse, os, sys, hashlib
import numpy as np, pandas as pd

ARSIP   = os.path.expanduser("~/Work/Yogya_Earthquake2006/eqt/")
META    = ARSIP + "seisbench/metadata.csv"
ARRIV   = ARSIP + "full/arrivals.csv"
NLL     = ARSIP + "full/catalog_nll.csv"
STADAT  = ARSIP + "hypodd/station.dat"
MSEED   = ARSIP + "pilot/mseed/{sta}/{sta}.YK.{yr}.{doy:03d}.mseed"
TINGKAT = ["mudah", "sedang", "sulit"]
SNR_MIN = 4.0     # lantai kelayakan: di bawah ini P tidak dapat di-pick andal


def seed_stabil(*bagian):
    """Hash stabil antar-proses. hash() bawaan Python diacak tiap run
    (PYTHONHASHSEED), sehingga tidak boleh dipakai untuk undian yang harus
    dapat direproduksi."""
    h = hashlib.sha256("|".join(map(str, bagian)).encode()).hexdigest()
    return int(h[:8], 16)


def kolam_w11(n_perlu, rng):
    """Ambil kandidat rekaman, hitung SNR, bagi jadi tiga tingkat."""
    from obspy import read, UTCDateTime
    from scipy.signal import butter, sosfiltfilt
    import glob, re
    berkas = glob.glob(ARSIP + "pilot/mseed/*/*.mseed")
    sta5 = sorted({f.split("/")[-2] for f in berkas})
    doys = sorted({int(re.search(r"\.(\d{4})\.(\d{3})\.mseed", f).group(2)) for f in berkas})

    m = pd.read_csv(META, low_memory=False)
    m["ts"] = pd.to_datetime(m.trace_start_time, errors="coerce", utc=True)
    m["doy"] = m.ts.dt.dayofyear
    pool = m[m.station_code.isin(sta5) & m.doy.isin(doys)].dropna(subset=["trace_s_arrival_sample"])
    pool = pool.sample(min(len(pool), max(900, n_perlu * 5)), random_state=int(rng.integers(1e9)))

    cache, baris = {}, []
    for _, r in pool.iterrows():
        sta, doy = r.station_code, int(r.doy)
        kunci = (sta, doy)
        if kunci not in cache:
            path = MSEED.format(sta=sta, yr=2006, doy=doy)
            if not os.path.exists(path):
                cache[kunci] = None
            else:
                try:
                    tr = read(path).select(component="Z")[0]
                    cache[kunci] = (tr, tr.data.astype(float), tr.stats.sampling_rate, tr.stats.starttime)
                except Exception:
                    cache[kunci] = None
        if cache[kunci] is None:
            continue
        _, data, fs, t0 = cache[kunci]
        P = UTCDateTime(str(r.trace_start_time)) + r.trace_p_arrival_sample / 100.0
        i = int((P - t0) * fs)
        if i < int(70 * fs) or i > len(data) - int(40 * fs):
            continue
        seg = data[i - int(20 * fs): i + int(10 * fs)]
        seg = seg - np.polyval(np.polyfit(np.arange(len(seg)), seg, 1), np.arange(len(seg)))
        sos = butter(4, [5 / (fs / 2), 25 / (fs / 2)], btype="band", output="sos")
        f = sosfiltfilt(sos, seg)
        derau = np.std(f[int(2 * fs): int(15 * fs)])
        if derau <= 0:
            continue
        snr = np.std(f[int(20 * fs): int(22 * fs)]) / derau
        baris.append(dict(sta=sta, doy=doy, P_abs=str(P),
                          SP=(r.trace_s_arrival_sample - r.trace_p_arrival_sample) / 100.0,
                          M=float(r.source_magnitude), dist=float(r.path_ep_distance_km), snr=float(snr)))
        if len(baris) >= max(600, n_perlu * 3):
            break
    df = pd.DataFrame(baris)
    # Lantai SNR. Rekaman ber-SNR sangat rendah tidak bisa di-pick oleh siapa pun,
    # sehingga memasukkannya ke soal berarti menghukum mahasiswa atas hal yang
    # bukan kesalahannya. "Sulit" harus berarti menuntut, bukan mustahil.
    sebelum = len(df)
    df = df[df.snr >= SNR_MIN].reset_index(drop=True)
    print(f"  lantai SNR >= {SNR_MIN}: {sebelum} -> {len(df)} rekaman")
    if len(df) < n_perlu:
        sys.exit(f"kolam W11 terlalu kecil setelah lantai SNR: {len(df)} < {n_perlu}")
    df["tingkat"] = pd.qcut(df.snr, 3, labels=TINGKAT[::-1])   # SNR tinggi = mudah
    return df


def kolam_w12():
    a = pd.read_csv(ARRIV)
    p = a[a.phase == "P"].groupby("evid").agg(nP=("sta", "nunique"), gap=("gap", "first"), rms=("rms", "first"))
    s = a[a.phase == "S"].groupby("evid").agg(nS=("sta", "nunique"))
    j = p.join(s).dropna()
    j = j[(j.nP >= 8) & (j.nS >= 6) & (j.rms < 0.20)]
    j["tingkat"] = pd.qcut(j.gap, 3, labels=TINGKAT)           # gap kecil = mudah
    return j, a


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--peserta", required=True, help="CSV berkolom nim,nama")
    ap.add_argument("--keluaran", default="dataset_m5")
    ap.add_argument("--garam", default="PAGF262413-2026",
                    help="garam undian; ganti tiap semester agar soal tidak berulang")
    ap.add_argument("--panjang", type=float, default=60.0, help="panjang jendela W11 (detik)")
    args = ap.parse_args()

    from obspy import read, UTCDateTime, Stream
    peserta = pd.read_csv(args.peserta, dtype={"nim": str})
    for k in ("nim", "nama"):
        if k not in peserta.columns:
            sys.exit(f"peserta.csv wajib punya kolom '{k}'")
    n = len(peserta)
    print(f"peserta: {n}")

    rng_global = np.random.default_rng(seed_stabil(args.garam))
    w11 = kolam_w11(n * 3, rng_global)
    w12, arrivals = kolam_w12()
    sta = pd.read_csv(STADAT, sep=r"\s+", header=None, names=["sta", "lat", "lon"])
    nll = pd.read_csv(NLL)
    print(f"kolam W11 {len(w11)} rekaman | kolam W12 {len(w12)} event")

    # --- pembagian berjenjang tanpa berbagi soal ---
    pakai11 = {t: list(rng_global.permutation(w11.index[w11.tingkat == t].to_numpy())) for t in TINGKAT}
    pakai12 = {t: list(rng_global.permutation(w12.index[w12.tingkat == t].to_numpy())) for t in TINGKAT}
    for t in TINGKAT:
        if len(pakai11[t]) < n or len(pakai12[t]) < n:
            sys.exit(f"tingkat '{t}' tidak cukup untuk {n} mahasiswa "
                     f"(W11 {len(pakai11[t])}, W12 {len(pakai12[t])})")

    os.makedirs(os.path.join(args.keluaran, "_kunci"), exist_ok=True)
    kunci = []

    for baris_ke, (_, mhs) in enumerate(peserta.iterrows()):
        nim = str(mhs.nim).strip()
        rng = np.random.default_rng(seed_stabil(args.garam, nim))
        folder = os.path.join(args.keluaran, nim)
        os.makedirs(folder, exist_ok=True)

        # ---------- W11 ----------
        st_out, info = Stream(), []
        for k, t in enumerate(TINGKAT, 1):
            r = w11.loc[pakai11[t][baris_ke]]
            P = UTCDateTime(r.P_abs)
            offset = float(rng.uniform(12, args.panjang - 15))
            path = MSEED.format(sta=r.sta, yr=2006, doy=int(r.doy))
            st = read(path, starttime=P - offset, endtime=P - offset + args.panjang)
            for tr in st:
                tr.stats.location = f"{k:02d}"
            st_out += st
            soal = f"W11-{k:02d}"
            info.append(dict(soal=soal, tingkat=t, stasiun=r.sta,
                             mulai=str(st[0].stats.starttime), panjang_s=args.panjang,
                             laju_cuplik_hz=st[0].stats.sampling_rate))
            kunci.append(dict(nim=nim, nama=mhs.nama, tugas="W11", soal=soal, tingkat=t,
                              P_ref_s=round(offset, 3), S_ref_s=round(offset + r.SP, 3),
                              SP_ref_s=round(r.SP, 3), M=r.M, jarak_km=round(r.dist, 1),
                              snr=round(r.snr, 2), stasiun=r.sta))
        st_out.write(os.path.join(folder, f"W11_{nim}.mseed"), format="MSEED")
        pd.DataFrame(info).to_csv(os.path.join(folder, f"W11_{nim}_soal.csv"), index=False)

        # ---------- W12 ----------
        blok = []
        for k, t in enumerate(TINGKAT, 1):
            evid = int(pakai12[t][baris_ke])
            sub = arrivals[arrivals.evid == evid].pivot_table(index="sta", columns="phase", values="tt").reset_index()
            soal = f"W12-{k:02d}"
            sub.insert(0, "soal", soal)
            blok.append(sub[["soal", "sta"] + [c for c in ("P", "S") if c in sub.columns]])
            rf = nll.iloc[evid]
            kunci.append(dict(nim=nim, nama=mhs.nama, tugas="W12", soal=soal, tingkat=t,
                              lat_ref=round(rf.latitude, 5), lon_ref=round(rf.longitude, 5),
                              depth_ref_km=round(rf.depth, 2), gap=round(rf.gap, 1),
                              errh_kat_km=rf.errh_km, errz_kat_km=rf.errz_km,
                              rms_kat_s=round(rf.rms, 4), nphs=int(rf.nphs)))
        pd.concat(blok).to_csv(os.path.join(folder, f"W12_{nim}_waktu_tiba.csv"), index=False)
        sta.to_csv(os.path.join(folder, "W12_stasiun.csv"), index=False)

        with open(os.path.join(folder, "BACA_SAYA.txt"), "w") as f:
            f.write(f"""Paket soal Milestone M5 — Seismologi PAGF262413
Nama : {mhs.nama}
NIM  : {nim}

Berkas kalian
  W11_{nim}.mseed          3 rekaman 60 detik (location 01, 02, 03)
  W11_{nim}_soal.csv       keterangan tiap rekaman
  W12_{nim}_waktu_tiba.csv waktu tempuh P dan S di tiap stasiun
  W12_stasiun.csv          koordinat stasiun

Paket ini UNIK untuk kalian. Menyalin jawaban teman tidak akan cocok
dengan data kalian sendiri.

Setoran memakai format baku (lihat notebook praktik). Kolom ketidakpastian
WAJIB diisi — selang sempit yang meleset bernilai lebih rendah daripada
selang lebar yang tepat.
""")
        if (baris_ke + 1) % 10 == 0 or baris_ke + 1 == n:
            print(f"  {baris_ke+1}/{n} paket ditulis")

    kdf = pd.DataFrame(kunci)
    kpath = os.path.join(args.keluaran, "_kunci", "kunci_m5.csv")
    kdf.to_csv(kpath, index=False)
    with open(os.path.join(args.keluaran, "_kunci", "PRIVAT_JANGAN_DIBAGIKAN.txt"), "w") as f:
        f.write("Folder ini berisi kunci jawaban M5. Jangan diunggah ke repositori publik\n"
                "dan jangan dibagikan ke mahasiswa.\n\n"
                "Pick rujukan berasal dari EqTransformer, bukan analis manusia. Perlakukan\n"
                "sebagai rujukan yang konsisten, bukan kebenaran mutlak.\n")
    with open(os.path.join(args.keluaran, ".gitignore"), "w") as f:
        f.write("_kunci/\n")

    print(f"\nselesai: {n} paket di {args.keluaran}/")
    print(f"kunci   : {kpath}  ({len(kdf)} baris) — JANGAN dibagikan")
    print(f"sebaran W11 SNR per tingkat:\n{w11.groupby('tingkat',observed=True).snr.median().round(1).to_string()}")
    print(f"sebaran W12 gap per tingkat:\n{w12.groupby('tingkat',observed=True).gap.median().round(0).to_string()}")


if __name__ == "__main__":
    main()
