# Backend Streamlit - BaliNavi Lite

## Tujuan
Folder `be` dapat dijalankan sebagai aplikasi Streamlit Cloud menggunakan file `streamlit_app.py`.

## 1) Main File Path untuk Streamlit Cloud
Isi field **Main file path** dengan:

`be/streamlit_app.py`

## 2) Branch
Gunakan branch:

`main`

## 3) Dependencies
Semua dependency sudah ada di `be/requirements.txt`.

## 4) Dataset Path
Secara default aplikasi membaca:

`data/Bali Popular Destination for Tourist 2022 - Sheet1.csv`

Anda dapat override dengan env var `DATASET_PATH` di Streamlit Cloud jika diperlukan.

## 5) Catatan Arsitektur
- `streamlit_app.py` menjalankan engine hybrid secara langsung untuk demo.
- `main.py` tetap tersedia bila Anda ingin mode API FastAPI terpisah.
