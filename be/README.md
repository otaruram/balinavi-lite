# Backend Streamlit - BaliNavi Lite

## Tujuan
Folder `be` dapat dijalankan sebagai aplikasi Streamlit Cloud menggunakan file `streamlit_app.py`.
Project ini sekarang difokuskan ke backend Streamlit (frontend statis terpisah tidak dipakai untuk deployment utama).

## 1) Main File Path untuk Streamlit Cloud
Isi field **Main file path** dengan:

`be/streamlit_app.py`

## 2) Branch
Gunakan branch:

`main`

## 3) Dependencies
Semua dependency runtime BE ada di `be/requirements.txt` (fokus untuk app Streamlit).

## 3.1) Python Runtime (Direkomendasikan)
Secara default deployment dipin ke Python 3.12 melalui file:

`runtime.txt`

Isi file:

`python-3.12.10`

Catatan: `be/requirements.txt` sudah diperbarui agar kompatibilitas Python 3.14 juga lebih baik
(termasuk pembaruan Streamlit/Pillow) jika platform belum membaca runtime pin.

## 4) Dataset Path
Secara default aplikasi membaca:

`data/Bali Popular Destination for Tourist 2022 - Sheet1.csv`

Anda dapat override dengan env var `DATASET_PATH` di Streamlit Cloud jika diperlukan.

## 5) Catatan Arsitektur
- `streamlit_app.py` menjalankan engine hybrid secara langsung untuk demo.
- `main.py` tetap tersedia bila Anda ingin mode API FastAPI terpisah.
