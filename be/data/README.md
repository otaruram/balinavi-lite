# Dataset BaliNavi Lite

Folder ini menyimpan dataset utama untuk engine rekomendasi BaliNavi Lite.

## File aktif saat ini

- `Bali Popular Destination for Tourist 2022 - Sheet1.csv`

## Cara pakai

1. Simpan file CSV Anda di folder ini.
2. Secara default app membaca file:
	- `be/data/Bali Popular Destination for Tourist 2022 - Sheet1.csv`
3. Jika ingin pakai file lain, set env var `DATASET_PATH` sebelum menjalankan Streamlit.

Contoh PowerShell:

```powershell
$env:DATASET_PATH = "C:\path\ke\dataset_lain.csv"
streamlit run be/streamlit_app.py
```

## Catatan

- Engine tetap membuat kolom `harga_tiket_clean` dari mapping harga pada `be/recommender.py`.
- Jika nama place tidak ada di kamus harga, sistem memakai fallback default `20000` agar pipeline tetap stabil.
