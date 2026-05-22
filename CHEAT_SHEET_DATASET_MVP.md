# CHEAT SHEET DATASET MVP - BALI NAVI LITE

## Tujuan Sesi Mentoring
- Membantu tim keluar dari kebuntuan data harga destinasi tanpa mengorbankan progres MVP.
- Menetapkan strategi dataset yang realistis, dapat dijelaskan ke juri, dan bisa langsung dipakai model.

## Masalah Inti Tim
- Dataset Kaggle destinasi Bali belum punya kolom harga tiket yang konsisten.
- Tanpa harga, fitur budget filtering tidak bisa berjalan secara nyata.

## Solusi Taktis (Yang Bisa Dipertanggungjawabkan)
1. Gunakan strategi data bertingkat:
- Level A: sumber resmi (website destinasi, kanal pemerintah, sumber primer).
- Level B: sumber sekunder kredibel (OTA, media travel terpercaya).
- Level C: estimasi terstandar tim (rule-based by kategori/lokasi).
2. Semua harga wajib punya metadata kualitas data.
3. Transparan saat presentasi: jelaskan mana data faktual, mana estimasi.

## Skema Tabel Harga Wajib
Gunakan tabel bernama misalnya `harga_destinasi_master.csv` dengan kolom:
1. nama_destinasi
2. harga_tiket
3. sumber_harga
4. tanggal_update
5. tingkat_kepercayaan
6. catatan_asumsi

Contoh isi:

| nama_destinasi | harga_tiket | sumber_harga | tanggal_update | tingkat_kepercayaan | catatan_asumsi |
|---|---:|---|---|---|---|
| Tanah Lot | 60000 | situs resmi | 2026-05-20 | A | tiket domestik dewasa |
| Pantai Kuta | 15000 | media travel | 2026-05-20 | B | biaya area/parkir |
| Desa Wisata X | 20000 | estimasi internal | 2026-05-20 | C | median kategori desa wisata |

## Aturan Estimasi Supaya Tidak Ngawang
1. Kelompokkan destinasi per kategori: pantai, pura, alam, taman budaya, desa wisata.
2. Tetapkan rentang harga per kategori.
3. Jika harga tidak ditemukan:
- pilih median kategori di kabupaten yang sama,
- lalu tandai `tingkat_kepercayaan = C`.
4. Jangan mencampur data A/B/C tanpa label.

## Implementasi Cepat di Kode (Pipeline Inti)
1. Baca dataset utama.
2. Suntik harga via dictionary/map.
3. Isi fallback default untuk nama yang belum ketemu.
4. Simpan kolom confidence agar evaluasi model fair.

Contoh ringkas:

```python
import pandas as pd

wisata_df = pd.read_csv("dataset_wisata_bali.csv")
kamus_harga = {
    "Taman Mumbul Sangeh": 30000,
    "Sangeh Monkey Forest": 30000,
    "Satria Gatotkaca Park": 0,
}

wisata_df["harga_tiket"] = wisata_df["nama"].map(kamus_harga).fillna(20000).astype(int)
```

## Cara Menjawab Pertanyaan Juri Soal Validitas Data
Kalimat aman:
- "Untuk MVP, kami menerapkan data sourcing bertingkat (A/B/C) dan seluruh nilai harga memiliki jejak sumber serta timestamp update."
- "Kami memisahkan data faktual dan data estimasi secara eksplisit agar auditability terjaga."
- "Roadmap setelah MVP adalah meningkatkan coverage sumber Level A secara bertahap."

## Evaluasi Minimal Yang Harus Tim Lakukan
1. Coverage harga: berapa persen destinasi punya nilai harga.
2. Proporsi confidence: A, B, C.
3. Outlier check: destinasi gratis bernilai tinggi atau sebaliknya.
4. Dampak ke rekomendasi: apakah filter budget menghasilkan output yang masuk akal.

## Rencana 7 Hari Menjelang Demo
1. Hari 1: lock daftar destinasi prioritas.
2. Hari 2-3: isi sumber A/B untuk destinasi paling populer.
3. Hari 4: isi fallback estimasi C untuk sisanya.
4. Hari 5: validasi acak 10-15 data.
5. Hari 6: freeze dataset versi demo.
6. Hari 7: rehearsal narasi teknis + risk statement.

## Risk Statement (Yang Profesional)
- "Data harga di fase MVP sebagian masih estimasi, namun sudah terstruktur, terlacak sumbernya, dan cukup untuk validasi engine rekomendasi budget."

## Checklist Sebelum Mentoring
1. Tim paham beda data A/B/C.
2. Tim bisa jelaskan alasan memilih fallback 20000.
3. Tim bisa tunjukkan 1 contoh destinasi: sumber, harga, confidence.
4. Tim bisa jelaskan roadmap penguatan kualitas data.
