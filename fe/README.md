# Frontend Vercel - BaliNavi Lite

Frontend ini adalah web statis (HTML/CSS/JS) yang siap deploy ke Vercel.

## 1) Konfigurasi URL Backend
Frontend membaca URL backend dari endpoint runtime `/api/config`.

Di Vercel, set Environment Variable:
- `BACKEND_URL` = `https://your-backend-domain/api/rekomendasi`

Contoh:
- `BACKEND_URL=https://balinavi-be.onrender.com/api/rekomendasi`

## 2) Run Lokal
Cukup buka `index.html` menggunakan static server.

Jika lokal tanpa Vercel, Anda bisa jalankan dengan Vercel CLI agar fungsi `/api/config` tetap aktif:
- `vercel dev`

## 3) Deploy ke Vercel
1. Import folder `fe` ke Vercel Project.
2. Framework preset pilih `Other`.
3. Tambahkan env `BACKEND_URL` di Project Settings.
4. Deploy langsung (karena static site + serverless function ringan).

## 4) Catatan Integrasi
- Backend FastAPI tetap terpisah di folder `be`.
- CORS backend sudah terbuka (`allow_origins=["*"]`) untuk mempermudah integrasi MVP.
