# Frontend Vercel - BaliNavi Lite

Frontend ini adalah web statis (HTML/CSS/JS) yang siap deploy ke Vercel.

## 1) Konfigurasi URL Backend
Frontend saat ini menggunakan URL hardcoded Streamlit:
- `https://balinavi.streamlit.app`

Alur integrasi final:
1. User isi form di FE Vercel.
2. FE mengirim parameter lewat query string ke Streamlit (`total_budget`, `durasi_hari`, `jumlah_orang`, `preferensi_user`).
3. Streamlit BE auto-run engine hybrid dan menampilkan hasil.

Jika URL Streamlit berubah, edit langsung pada file `script.js`.

## 2) Run Lokal
Cukup buka `index.html` menggunakan static server.

## 3) Deploy ke Vercel
1. Import folder `fe` ke Vercel Project.
2. Framework preset pilih `Other`.
3. Deploy langsung (karena static site tanpa konfigurasi env wajib).

## 4) Catatan Integrasi
- Backend mode yang dipakai sekarang adalah Streamlit app (`be/streamlit_app.py`).
- Frontend menampilkan tautan Streamlit dari nilai hardcoded di `script.js`.
