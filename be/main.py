# Mengimpor os untuk membaca konfigurasi path dataset dari environment variable.
import os

# Mengimpor tipe List agar anotasi tipe data list menjadi jelas untuk pembaca pemula.
from typing import List

# Mengimpor pandas untuk membangun fallback dataset lokal saat file Kaggle belum tersedia.
import pandas as pd

# Mengimpor FastAPI sebagai framework backend HTTP API yang ringan dan cepat.
from fastapi import FastAPI

# Mengimpor CORSMiddleware agar frontend Streamlit boleh mengakses endpoint backend lintas origin.
from fastapi.middleware.cors import CORSMiddleware

# Mengimpor BaseModel untuk validasi struktur request JSON dan Field untuk aturan nilai input.
from pydantic import BaseModel, Field

# Mengimpor class HybridRecommender agar logic hybrid terpusat dalam satu file.
from recommender import HybridRecommender

# Membuat objek aplikasi FastAPI sebagai pintu utama semua endpoint backend.
app = FastAPI(title="BaliNavi Lite API", version="1.0.0")

# Membuat satu instance recommender agar kamus harga dan logic hybrid dipakai konsisten.
recommender = HybridRecommender()

# Menentukan path dataset dari environment atau fallback ke file CSV nyata yang ada saat ini.
DATASET_PATH = os.getenv("DATASET_PATH", "data/Bali Popular Destination for Tourist 2022 - Sheet1.csv")

# Menambahkan middleware CORS agar request dari frontend tidak diblokir browser saat beda host/port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mendefinisikan skema request agar payload dari frontend tervalidasi otomatis.
class RekomendasiRequest(BaseModel):
    # total_budget berisi total dana perjalanan pengguna dan harus lebih besar dari nol.
    total_budget: int = Field(..., gt=0, description="Total budget perjalanan")
    # durasi_hari berisi lama liburan dalam hari dan harus minimal satu hari.
    durasi_hari: int = Field(..., gt=0, description="Durasi perjalanan dalam hari")
    # jumlah_orang berisi jumlah peserta trip dan harus minimal satu orang.
    jumlah_orang: int = Field(..., gt=0, description="Jumlah orang dalam rombongan")
    # preferensi_user berisi kata kunci suasana yang dicari user untuk proses NLP sederhana.
    preferensi_user: str = Field(..., min_length=1, description="Preferensi vibe/suasana")


# Membuat helper untuk menyediakan dataset fallback jika file CSV Kaggle belum terpasang.
def bangun_dataset_fallback() -> pd.DataFrame:
    # Menyiapkan data mini berformat kolom Kaggle agar pipeline recommender tetap kompatibel.
    data_fallback = [
        {
            "nama": "Taman Mumbul Sangeh",
            "kategori": "alam",
            "kabupaten_kota": "Badung",
            "rating": 4.3,
            "preferensi": "tenang alam hijau",
            "latitude": -8.5001,
            "longitude": 115.2065,
        },
        {
            "nama": "Sangeh Monkey Forest",
            "kategori": "alam",
            "kabupaten_kota": "Badung",
            "rating": 4.4,
            "preferensi": "hutan satwa keluarga",
            "latitude": -8.4829,
            "longitude": 115.2070,
        },
        {
            "nama": "Satria Gatotkaca Park",
            "kategori": "taman kota",
            "kabupaten_kota": "Badung",
            "rating": 4.2,
            "preferensi": "foto landmark transit",
            "latitude": -8.7469,
            "longitude": 115.1672,
        },
        {
            "nama": "West Garden Pangi",
            "kategori": "alam",
            "kabupaten_kota": "Tabanan",
            "rating": 4.1,
            "preferensi": "santai kebun keluarga",
            "latitude": -8.5032,
            "longitude": 115.0210,
        },
        {
            "nama": "Obyek Wisata Batu Belah Antiga",
            "kategori": "budaya",
            "kabupaten_kota": "Karangasem",
            "rating": 4.0,
            "preferensi": "sejarah budaya lokal",
            "latitude": -8.5128,
            "longitude": 115.5891,
        },
    ]

    # Mengubah list dictionary fallback menjadi DataFrame siap diproses recommender.
    return pd.DataFrame(data_fallback)


# Membuat helper pemuat data utama agar endpoint tidak berisi detail handling file.
def muat_dataset_terproses() -> pd.DataFrame:
    # Mencoba memuat dataset Kaggle dari path konfigurasi dan langsung diperkaya harga.
    if os.path.exists(DATASET_PATH):
        return recommender.load_and_enrich_data(DATASET_PATH)

    # Membangun fallback dataset saat file belum tersedia agar demo tetap bisa jalan.
    df_fallback = bangun_dataset_fallback()

    # Menyuntikkan harga menggunakan kamus internal recommender agar logika tetap konsisten.
    df_fallback["harga_tiket_clean"] = df_fallback["nama"].map(recommender.kamus_harga_bali).fillna(20000).astype(int)

    # Membuat kolom deskripsi suasana supaya fallback tetap kompatibel dengan TF-IDF pipeline.
    df_fallback["deskripsi_suasana"] = (
        df_fallback["nama"].fillna("").astype(str)
        + " "
        + df_fallback["kategori"].fillna("").astype(str)
        + " "
        + df_fallback["kabupaten_kota"].fillna("").astype(str)
        + " "
        + df_fallback["preferensi"].fillna("").astype(str)
    )

    # Mengembalikan dataset fallback yang sudah memiliki kolom wajib pipeline hybrid.
    return df_fallback


# Membuat endpoint POST untuk menghasilkan rekomendasi berdasarkan budget dan preferensi vibe.
@app.post("/api/rekomendasi")
def rekomendasi_trip(payload: RekomendasiRequest) -> List[dict]:
    # Memuat dataset utama Kaggle atau fallback lokal yang sudah punya kolom wajib hybrid.
    df_processed = muat_dataset_terproses()

    # Menjalankan engine hybrid terpusat agar logic data dan rekomendasi tidak dobel di file lain.
    hasil = recommender.get_recommendations(
        df_processed=df_processed,
        total_budget=payload.total_budget,
        durasi_hari=payload.durasi_hari,
        jumlah_orang=payload.jumlah_orang,
        preferensi_user=payload.preferensi_user,
    )

    # Mengembalikan list rekomendasi final untuk dikonsumsi frontend Streamlit.
    return hasil
