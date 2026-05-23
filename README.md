# BaliNavi Lite

BaliNavi Lite adalah versi ringkas dari project BaliNavi yang difokuskan ke satu aplikasi Streamlit (BE-only) untuk menghasilkan rekomendasi destinasi berdasarkan budget dan preferensi pengguna.

## Fokus Repo

- Arsitektur monolith ringan untuk demo dan deployment cepat.
- Engine rekomendasi hybrid ada di layer backend Streamlit.
- Tanpa frontend terpisah.
- Data destinasi berada di folder backend.

## Struktur Folder

```text
balinavi-lite/
|-- be/
|   |-- data/
|   |   |-- Bali Popular Destination for Tourist 2022 - Sheet1.csv
|   |   `-- README.md
|   |-- logs/                         # dibuat otomatis saat app berjalan
|   |-- main.py                       # opsi API (tidak dipakai untuk deploy utama)
|   |-- recommender.py                # engine hybrid recommendation
|   |-- requirements.txt              # dependency runtime utama
|   |-- runtime.txt                   # pin runtime python level be
|   `-- streamlit_app.py              # entrypoint deploy Streamlit Cloud
|-- runtime.txt                       # pin runtime python level repo
`-- README.md
```

## Alur Kerja Aplikasi

1. User memasukkan total budget, durasi hari, jumlah orang, dan preferensi suasana di UI Streamlit.
2. App memuat dataset CSV dari path default atau env var DATASET_PATH.
3. Engine membersihkan dan memperkaya data:
	- mapping harga tiket ke integer rupiah,
	- fallback harga default jika place belum terpetakan,
	- pembentukan kolom teks deskripsi_suasana.
4. Rule-based filter budget dijalankan terlebih dahulu.
5. Kandidat lolos budget di-ranking dengan hybrid scoring:
	- TF-IDF + cosine similarity,
	- rating,
	- popularitas,
	- affordability.
6. Hasil dikembalikan sebagai ranking, alasan rekomendasi, dan itinerary harian.

## Catatan Data Harga

- Harga tiket pada sistem adalah estimasi terstruktur dari teks fee dataset (rule-based extraction).
- Bukan feed harga real-time dari penyedia tiket.
- Cocok untuk simulasi budgeting dan perencanaan awal.

## Dependency Utama

File: be/requirements.txt

- pandas
- scikit-learn
- streamlit
- pillow

## Menjalankan di Lokal

### 1) Siapkan environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependency:

```bash
pip install -r be/requirements.txt
```

### 2) Jalankan app

```bash
streamlit run be/streamlit_app.py
```

### 3) URL lokal

```text
http://localhost:8501
```

## Deployment ke Streamlit Cloud

1. Pilih repo: balinavi-lite.
2. Pilih branch: main.
3. Main file path: be/streamlit_app.py.
4. Pastikan runtime pin tersedia:
	- runtime.txt
	- be/runtime.txt
5. Deploy atau Reboot app.

## Runtime & Stabilitas

- Runtime dipin ke Python 3.12.10.
- Tujuannya menekan risiko build dependency native di environment cloud.
- Jika ada error runtime, cek:
  - log deploy pada Streamlit Cloud,
  - file log lokal app di be/logs/streamlit_app.log.

## Cara Mengganti Dataset

Opsi 1:
- timpa file default di be/data/Bali Popular Destination for Tourist 2022 - Sheet1.csv.

Opsi 2:
- set env var DATASET_PATH ke file CSV lain.

Contoh PowerShell:

```powershell
$env:DATASET_PATH = "C:\path\ke\dataset.csv"
streamlit run be/streamlit_app.py
```

## Status Scope Lite

- Yang dipakai untuk deliver utama: Streamlit app + recommender engine.
- main.py tetap ada untuk fleksibilitas, tetapi bukan entrypoint deployment utama.

## Ringkasan Cepat

- Entry deploy: be/streamlit_app.py
- Engine hybrid: be/recommender.py
- Data utama: be/data/Bali Popular Destination for Tourist 2022 - Sheet1.csv
- Dependency: be/requirements.txt
- Runtime pin: runtime.txt
