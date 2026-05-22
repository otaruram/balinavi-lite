# Frontend Vercel - BaliNavi Lite

Frontend ini adalah web statis (HTML/CSS/JS) yang siap deploy ke Vercel.

## 1) Konfigurasi URL Backend
Secara default frontend memanggil:
- `http://localhost:8000/api/rekomendasi`

Untuk production, set URL backend lewat global script sebelum `script.js`, contoh:

```html
<script>
  window.BALINAVI_BACKEND_URL = "https://your-backend-domain/api/rekomendasi";
</script>
<script src="./script.js"></script>
```

## 2) Run Lokal
Cukup buka `index.html` menggunakan static server.

## 3) Deploy ke Vercel
1. Import folder `fe` ke Vercel Project.
2. Framework preset pilih `Other`.
3. Deploy langsung (karena static site tanpa build command).

## 4) Catatan Integrasi
- Backend FastAPI tetap terpisah di folder `be`.
- CORS backend sudah terbuka (`allow_origins=["*"]`) untuk mempermudah integrasi MVP.
