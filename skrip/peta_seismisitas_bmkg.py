"""
Peta seismisitas Indonesia dari katalog BMKG — bahan Minggu 1 Seismologi PAGF262413.

Sumber data : katalog BMKG lokal (CSV), kolom Date, Latitude, Longitude,
              Magnitude, Depth (km).
Keluaran    : PNG peta, titik diwarnai kedalaman hiposenter, ukuran menurut
              magnitudo, diurutkan dangkal-ke-dalam agar event dalam tampak.
Kebutuhan   : pygmt >= 0.18, gmt >= 6.5, pandas.

Ubah CATALOG ke berkas katalog terbaru untuk memperbarui rentang tahunnya;
judul peta mengambil tahun langsung dari data, jadi ikut menyesuaikan sendiri.
"""
import pandas as pd, numpy as np, pygmt
CATALOG="/Users/maswiet/Work/DATA/AFM/BMKG_Earthquake_Catalog.csv"
OUT="Gambar/w01_seismisitas_indonesia.png"
df=pd.read_csv(CATALOG,low_memory=False)
df['d']=pd.to_datetime(df['Date'],format='%d-%b-%Y',errors='coerce')
for c in ['Latitude','Longitude','Magnitude','Depth (km)']:
    df[c]=pd.to_numeric(df[c],errors='coerce')
df=df.dropna(subset=['Latitude','Longitude','Magnitude','Depth (km)','d'])
df=df[df['Depth (km)'].between(0,750) & df['Magnitude'].between(0,10)]
df=df.sort_values('Depth (km)')           # dangkal dulu, dalam di atas
y0,y1=df.d.dt.year.min(), df.d.dt.year.max()
print(f"plot {len(df):,} event, {y0}–{y1}")

REG=[94,142,-15,7.5]
fig=pygmt.Figure()
pygmt.config(FONT_TITLE="15p,Helvetica-Bold", FONT_LABEL="10p", FONT_ANNOT_PRIMARY="9p", MAP_FRAME_TYPE="plain")
fig.coast(region=REG,projection="M22c",land="gray91",water="#f0f6fa",
          shorelines="0.35p,gray20",borders="1/0.25p,gray55",resolution="i")
pygmt.makecpt(cmap="seis",series=[0,700,25],reverse=False)
fig.plot(x=df.Longitude,y=df.Latitude,fill=df['Depth (km)'],cmap=True,
         style="cc",size=0.006*(1.35**df.Magnitude),pen=None,transparency=15)
fig.colorbar(frame=["x+lKedalaman hiposenter (km)"],position="JBC+w12c/0.4c+h+o0c/1.1c")
n_fmt=f"{len(df):,}".replace(",",".")
judul=f"Seismisitas Indonesia - Katalog BMKG {y0}-{y1} ({n_fmt} gempa)"
fig.basemap(region=REG,projection="M22c",
            frame=[f"WSne+t{judul}","xa10f5+lBujur Timur","ya5f2.5+lLintang"])
fig.savefig(OUT,dpi=200,crop=True)
print("selesai")
