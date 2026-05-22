# Setup Dataset CSV dari Kaggle Notebook

1. Buka notebook Kaggle Anda dan jalankan sampai sel terakhir.
2. Jalankan sel ekspor CSV:

```python
output_path = "/kaggle/working/dataset_tempat_wisata_bali_cleaned.csv"
df.to_csv(output_path, index=False)
```

3. Download file `dataset_tempat_wisata_bali_cleaned.csv` dari panel Output Kaggle.
4. Simpan file tersebut ke folder ini (`balinavi-lite/be/data/`).
5. Jalankan backend dari folder `balinavi-lite/be`.

Catatan:
- Backend otomatis membaca `data/dataset_tempat_wisata_bali_cleaned.csv`.
- Harga tiket tetap di-enrich dari hardcoded dictionary pada `recommender.py`.
