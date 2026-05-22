# Mengimpor tipe List agar anotasi tipe data list menjadi jelas untuk pembaca pemula.
from typing import List

# Mengimpor pandas untuk memudahkan manipulasi data tabular berbentuk DataFrame.
import pandas as pd

# Mengimpor FastAPI sebagai framework backend HTTP API yang ringan dan cepat.
from fastapi import FastAPI

# Mengimpor CORSMiddleware agar frontend Streamlit boleh mengakses endpoint backend lintas origin.
from fastapi.middleware.cors import CORSMiddleware

# Mengimpor BaseModel untuk validasi struktur request JSON dan Field untuk aturan nilai input.
from pydantic import BaseModel, Field

# Mengimpor TfidfVectorizer untuk mengubah teks vibe menjadi representasi angka berbasis TF-IDF.
from sklearn.feature_extraction.text import TfidfVectorizer

# Mengimpor cosine_similarity untuk menghitung tingkat kemiripan preferensi user terhadap deskripsi tempat.
from sklearn.metrics.pairwise import cosine_similarity

# Membuat objek aplikasi FastAPI sebagai pintu utama semua endpoint backend.
app = FastAPI(title="BaliNavi Lite API", version="1.0.0")

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


# Membuat fungsi helper untuk mensimulasikan data tempat wisata Bali yang sederhana namun representatif.
def siapkan_dataset_bali() -> pd.DataFrame:
    # Menyiapkan list data mentah 5 tempat wisata seolah berasal dari dataset Kaggle.
    data_tempat = [
        {
            "nama_tempat": "Pantai Kuta",
            "kategori": "Pantai",
            "vibe_deskripsi": "pantai ramai sunset surfing belanja kuliner malam",
        },
        {
            "nama_tempat": "Ubud Monkey Forest",
            "kategori": "Alam",
            "vibe_deskripsi": "hutan asri tenang budaya alam spiritual jalan kaki",
        },
        {
            "nama_tempat": "Tegallalang Rice Terrace",
            "kategori": "Pemandangan",
            "vibe_deskripsi": "sawah hijau foto instagram santai udara segar",
        },
        {
            "nama_tempat": "Pura Tanah Lot",
            "kategori": "Budaya",
            "vibe_deskripsi": "pura ikonik sunset budaya sejarah sakral",
        },
        {
            "nama_tempat": "Garuda Wisnu Kencana",
            "kategori": "Taman Budaya",
            "vibe_deskripsi": "patung megah pertunjukan seni budaya keluarga",
        },
    ]

    # Membuat kamus harga sintetis hasil riset manual untuk menutup data harga tiket yang bolong.
    kamus_harga_bali = {
        "Pantai Kuta": 15000,
        "Ubud Monkey Forest": 80000,
        "Tegallalang Rice Terrace": 25000,
        "Pura Tanah Lot": 60000,
        "Garuda Wisnu Kencana": 125000,
    }

    # Mengubah list dictionary menjadi DataFrame agar mudah difilter dan diperingkat.
    df = pd.DataFrame(data_tempat)

    # Menambahkan kolom harga_tiket menggunakan .map() dari nama tempat ke kamus harga.
    df["harga_tiket"] = df["nama_tempat"].map(kamus_harga_bali)

    # Mengisi nilai harga yang masih kosong dengan 0 sebagai fallback aman pada contoh edukatif.
    df["harga_tiket"] = df["harga_tiket"].fillna(0)

    # Mengubah tipe harga menjadi integer agar output rapi dan konsisten.
    df["harga_tiket"] = df["harga_tiket"].astype(int)

    # Mengembalikan DataFrame siap pakai untuk proses filtering dan ranking.
    return df


# Membuat endpoint POST untuk menghasilkan rekomendasi berdasarkan budget dan preferensi vibe.
@app.post("/api/rekomendasi")
def rekomendasi_trip(payload: RekomendasiRequest) -> List[dict]:
    # Menyiapkan dataset simulasi Bali yang sudah diperkaya harga tiket dari kamus hardcode.
    df = siapkan_dataset_bali()

    # Menghitung batas budget maksimum per orang per hari agar aturan bisnis lebih adil.
    budget_maks_per_orang_per_hari = payload.total_budget / (payload.jumlah_orang * payload.durasi_hari)

    # Memfilter data hanya untuk tempat yang harga tiketnya tidak melebihi batas budget terhitung.
    kandidat = df[df["harga_tiket"] <= budget_maks_per_orang_per_hari].copy()

    # Jika kandidat kosong maka langsung kembalikan list kosong agar frontend mudah menangani kondisi ini.
    if kandidat.empty:
        return []

    # Membuat vectorizer TF-IDF untuk membaca pola kata penting pada kolom vibe_deskripsi.
    vectorizer = TfidfVectorizer()

    # Melatih vectorizer pada teks kandidat lalu mengubah teks menjadi matriks fitur numerik.
    matriks_tfidf = vectorizer.fit_transform(kandidat["vibe_deskripsi"])

    # Mengubah preferensi user menjadi vektor TF-IDF pada ruang fitur yang sama.
    vektor_user = vectorizer.transform([payload.preferensi_user.lower()])

    # Menghitung skor kemiripan cosine antara vektor user dengan setiap tempat kandidat.
    skor_kemiripan = cosine_similarity(vektor_user, matriks_tfidf).flatten()

    # Menyimpan skor kemiripan ke kolom baru agar bisa diurutkan dari paling relevan.
    kandidat["skor_kemiripan"] = skor_kemiripan

    # Mengurutkan kandidat dari skor tertinggi ke terendah untuk membentuk ranking rekomendasi.
    hasil = kandidat.sort_values(by="skor_kemiripan", ascending=False)

    # Memilih kolom penting saja agar response JSON ringkas dan mudah dibaca di frontend.
    hasil = hasil[["nama_tempat", "kategori", "harga_tiket", "vibe_deskripsi", "skor_kemiripan"]]

    # Membulatkan skor agar tampilan output lebih ramah presentasi dan tidak terlalu panjang.
    hasil["skor_kemiripan"] = hasil["skor_kemiripan"].round(4)

    # Mengonversi DataFrame menjadi list of dict supaya sesuai format response JSON endpoint.
    return hasil.to_dict(orient="records")
