# Frontend Vercel - BaliNavi Lite

Frontend ini adalah web statis (HTML/CSS/JS) yang siap deploy ke Vercel.

## 1) Konfigurasi URL Backend
Frontend saat ini menggunakan URL hardcoded:
- Streamlit app: `https://balinavi.streamlit.app`
- Endpoint API: `https://balinavi.streamlit.app/api/rekomendasi`

Jika URL berubah, edit langsung pada file `script.js`.

## 2) Run Lokal
Cukup buka `index.html` menggunakan static server.

## 3) Deploy ke Vercel
1. Import folder `fe` ke Vercel Project.
2. Framework preset pilih `Other`.
3. Deploy langsung (karena static site tanpa konfigurasi env wajib).

## 4) Catatan Integrasi
- Backend FastAPI tetap terpisah di folder `be`.
- CORS backend sudah terbuka (`allow_origins=["*"]`) untuk mempermudah integrasi MVP.
- Frontend menampilkan tautan Streamlit dari nilai hardcoded di `script.js`.
