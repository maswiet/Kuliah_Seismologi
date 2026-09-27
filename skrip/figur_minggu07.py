"""
Figur Minggu 7 — pengaruh t* pada bentuk gelombang dan spektrum, serta
bagaimana Q sungguh-sungguh diukur dengan metode nisbah spektral.

Jalankan dari akar repo:
    python3 skrip/figur_minggu07.py

Keluaran:
    Gambar/w07_tstar_spektrum.png

Sumber dimodelkan dengan spektrum Brune omega-kuadrat, lalu dikenai operator
serapan exp(-pi f t*). Operator itu di sini dipakai **berfasa nol** demi
kesederhanaan gambar; serapan sungguhan bersifat kausal, sehingga ia juga
menggeser fasa dan membuat kecepatan bergantung frekuensi (Kramers-Kronig).
Pelebaran pulsa dan hilangnya frekuensi tinggi — dua hal yang ingin
ditunjukkan panel (a) dan (b) — tidak terpengaruh penyederhanaan itu.
"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "Gambar"

FC = 8.0            # frekuensi sudut sumber (Hz) -- gempa mikro
V_S = 3.5           # km/s
DT = 0.002
NT = 2048
RNG = np.random.default_rng(7)

# stasiun: (nama, jarak km, Q)
STASIUN = [("dekat", 10.0, 200.0), ("jauh", 45.0, 200.0)]


def spektrum_sumber(f):
    """Brune omega-kuadrat."""
    return 1.0 / (1.0 + (f / FC) ** 2)


def jejak(tstar, f, fase):
    """Bentuk gelombang dari spektrum sumber yang diserap, fasa acak tetap."""
    A = spektrum_sumber(f) * np.exp(-np.pi * f * tstar)
    spek = A * np.exp(1j * fase)
    return np.fft.irfft(spek, n=NT)


def main():
    os.makedirs(OUT, exist_ok=True)
    f = np.fft.rfftfreq(NT, DT)
    f[0] = 1e-6
    fase = np.zeros(f.size)      # fasa nol: pulsa simetris, agar pelebarannya terbaca
    t = np.arange(NT) * DT

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15, 4.9))

    # ---- (a) bentuk gelombang untuk beberapa t* -----------------------------
    warna = ["#0f172a", "#0e7490", "#d97706", "#dc2626"]
    lebar = []
    for c, ts in zip(warna, [0.0, 0.02, 0.05, 0.10]):
        w = np.roll(jejak(ts, f, fase), NT // 2)
        tt = t - t[NT // 2]
        a1.plot(tt, w / np.abs(jejak(0.0, f, fase)).max(), color=c, lw=1.8,
                label=f"$t^*$ = {ts:.2f} s" + ("  (tanpa serapan)" if ts == 0 else ""))
        atas = np.where(w >= 0.5 * w.max())[0]          # lebar setengah puncak
        lebar.append((ts, (atas[-1] - atas[0]) * DT * 1000, w.max() / np.abs(jejak(0.0, f, fase)).max()))
    a1.set(xlim=(-0.12, 0.12), xlabel="waktu (s)",
           ylabel="amplitudo (dinormalkan ke pulsa utuh)",
           title="(a) Serapan menumpulkan puncak\ndan melebarkan pulsa")
    a1.text(.03, .30, "\n".join(f"$t^*$={a:.2f}: lebar {b:.0f} ms, puncak {100*c:.0f}%"
                                 for a, b, c in lebar),
            transform=a1.transAxes, fontsize=8, va="top",
            bbox=dict(fc="w", ec="0.75"))
    a1.legend(fontsize=8.5); a1.grid(alpha=.25)

    # ---- (b) spektrum -------------------------------------------------------
    for c, ts in zip(warna, [0.0, 0.02, 0.05, 0.10]):
        a2.loglog(f, spektrum_sumber(f) * np.exp(-np.pi * f * ts), color=c, lw=1.8,
                  label=f"$t^*$ = {ts:.2f} s")
    a2.axvline(FC, color="0.5", ls=":", lw=1.2)
    a2.text(FC * 1.08, 2e-4, f"$f_c$ = {FC:.0f} Hz", fontsize=8.5, color="0.4")
    a2.set(xlim=(0.5, 120), ylim=(1e-5, 2),
           xlabel="frekuensi (Hz)", ylabel="amplitudo spektral",
           title="(b) Yang hilang adalah frekuensi tinggi\n— karena $f$ ada di eksponennya")
    a2.legend(fontsize=8.5); a2.grid(alpha=.25, which="both")

    # ---- (c) metode nisbah spektral: mengukur Q -----------------------------
    (n1, r1, q1), (n2, r2, q2) = STASIUN
    ts1, ts2 = r1 / (q1 * V_S), r2 / (q2 * V_S)
    derau = 0.06
    A1 = spektrum_sumber(f) * np.exp(-np.pi * f * ts1) * np.exp(RNG.normal(0, derau, f.size))
    A2 = spektrum_sumber(f) * np.exp(-np.pi * f * ts2) * np.exp(RNG.normal(0, derau, f.size))
    nis = np.log(A2 / A1)

    pita = (f >= 2) & (f <= 40)                 # pita pengukuran
    kem, pot = np.polyfit(f[pita], nis[pita], 1)
    dts = -kem / np.pi                           # selisih t*
    q_ukur = (r2 - r1) / (V_S * dts)

    a3.plot(f[pita], nis[pita], ".", ms=3, color="#94a3b8", label="data (berderau)")
    a3.plot(f[pita], kem * f[pita] + pot, "-", color="#dc2626", lw=2.2,
            label=f"cocokan: kemiringan = $-\\pi\\,\\Delta t^*$")
    a3.plot(f[pita], -np.pi * (ts2 - ts1) * f[pita] + pot, "--", color="#0e7490", lw=1.6,
            label="garis sejati")
    a3.set(xlabel="frekuensi (Hz)", ylabel=r"$\ln\,(A_\mathrm{jauh}/A_\mathrm{dekat})$",
           title="(c) Beginilah $Q$ diukur:\nkemiringan garis, bukan amplitudo mutlak")
    a3.grid(alpha=.25); a3.legend(fontsize=8.5, loc="lower left")
    a3.text(.97, .95,
            f"$Q$ sejati = {q1:.0f}\n$Q$ terukur = {q_ukur:.0f}\n"
            f"galat = {100*(q_ukur-q1)/q1:+.1f} %",
            transform=a3.transAxes, ha="right", va="top", fontsize=9.5,
            bbox=dict(fc="w", ec="0.6"))

    fig.suptitle("Faktor kualitas $Q$: apa yang dilakukannya pada gelombang, "
                 "dan bagaimana ia diukur", fontweight="bold", fontsize=12)
    fig.tight_layout()
    fig.savefig(f"{OUT}/w07_tstar_spektrum.png", dpi=150)
    plt.close(fig)

    print(f"  t* dekat = {ts1*1000:.1f} ms, t* jauh = {ts2*1000:.1f} ms")
    print(f"  Q sejati {q1:.0f} -> Q terukur {q_ukur:.1f} "
          f"(galat {100*(q_ukur-q1)/q1:+.1f} %)")


if __name__ == "__main__":
    main()
