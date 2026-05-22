# Mengimpor tipe Dict agar struktur dictionary harga lebih eksplisit dan mudah dibaca.
from typing import Dict, List

# Mengimpor pandas untuk membaca CSV dan melakukan transformasi tabular berbasis DataFrame.
import pandas as pd

# Mengimpor TfidfVectorizer untuk mengubah teks deskripsi menjadi fitur numerik NLP.
from sklearn.feature_extraction.text import TfidfVectorizer

# Mengimpor cosine_similarity untuk menghitung kemiripan preferensi user dengan destinasi.
from sklearn.metrics.pairwise import cosine_similarity


# Mendefinisikan class HybridRecommender sebagai engine utama rekomendasi budget + preferensi.
class HybridRecommender:
    # Menjalankan inisialisasi object untuk menyiapkan kamus harga bersih.
    def __init__(self) -> None:
        # Menyimpan kamus harga dalam Rupiah yang sudah dibersihkan untuk wisatawan lokal dewasa.
        self.kamus_harga_bali: Dict[str, int] = {
            # Menetapkan harga lokal dewasa Tanah Lot dari deskripsi fee yang eksplisit.
            "Tanah Lot": 20000,
            # Menetapkan harga Mount Batur dari informasi biaya trekking per orang.
            "Mount Batur": 100000,
            # Menetapkan harga Uluwatu Temple berdasarkan fee dewasa 30.000.
            "Uluwatu Temple": 30000,
            # Menetapkan harga Ubud Monkey Forest berdasarkan fee dewasa 50.000.
            "Ubud Monkey Forest": 50000,
            # Menetapkan harga Goa Gajah berdasarkan fee dewasa 50.000.
            "Goa Gajah": 50000,
            # Menetapkan harga Jatiluwih berdasarkan tiket masuk 40.000.
            "Jatiluwih Rice Terraces in Bali": 40000,
            # Menetapkan harga Tegallalang berdasarkan tiket 15.000.
            "Tenggalang Rice Terrace": 15000,
            # Menetapkan harga Ulun Danu Bratan berdasarkan fee dewasa 50.000.
            "Pura Ulun Danu Bratan": 50000,
            # Menetapkan harga Seminyak Beach nol karena biaya bersifat opsional/variatif.
            "Seminyak Beach": 0,
            # Menetapkan harga Nusa Dua Beach nol karena biaya bersifat opsional/variatif.
            "Nusa Dua Beach": 0,
            # Menetapkan harga Besakih Temple berdasarkan tiket dewasa 60.000.
            "Besakih Temple (Pura Besakih)": 60000,
            # Menetapkan harga Kuta Beach nol karena akses masuk pantai gratis.
            "Kuta Beach": 0,
            # Menetapkan harga Lempuyang 55.000 dari angka tiket yang tersedia pada deskripsi.
            "Pura Penataran Agung Lempuyang": 55000,
            # Menetapkan harga Sidemen Valley nol karena tidak ada tiket baku pada deskripsi.
            "Sidemen Valley": 0,
            # Menetapkan harga Tirta Empul berdasarkan fee dewasa 50.000.
            "Tirta Empul Temple": 50000,
            # Menetapkan harga West Bali National Park dari batas bawah rentang fee 200.000-300.000.
            "West Bali National Park": 200000,
            # Menetapkan harga GWK dari batas bawah rentang fee 100.000-125.000.
            "Garuda Wisnu Kencana Cultural Park": 100000,
            # Menetapkan harga Bali Zoo dari harga mulai 90.000.
            "Bali Zoo": 90000,
            # Menetapkan harga Bali Bird Park dari tiket dewasa 385.000.
            "Bali Bird Park": 385000,
            # Menetapkan harga Tirta Gangga dari tiket masuk 50.000.
            "Tirta Gangga": 50000,
            # Menetapkan harga Tegenungan Waterfall dari tiket dewasa 15.000.
            "Tegenungan Waterfall": 15000,
            # Menetapkan harga Bali Swing dari batas bawah rentang 10 USD sekitar 150.000 Rupiah.
            "Bali Swing": 150000,
            # Menetapkan harga Waterboom Bali dari tiket dewasa 495.000.
            "Waterboom Bali": 495000,
            # Menetapkan harga Campuhan Ridge Walk nol karena lintasan bersifat gratis.
            "Campuhan Ridge Walk": 0,
            # Menetapkan harga Bali Safari berdasarkan tiket dewasa 720.000.
            "Bali Safari and Marine Park": 720000,
            # Menetapkan harga Bajra Sandhi berdasarkan tiket dewasa 30.000.
            "Bajra Sandhi Monument": 30000,
            # Menetapkan harga Sukawati Art Market nol karena biaya masuk tidak baku.
            "Sukawati Art Market": 0,
            # Menetapkan harga Taman Ujung dari batas bawah rentang 50.000-75.000.
            "Taman Ujung": 50000,
            # Menetapkan harga Secret Garden Village dari harga mulai 45.000.
            "Secret Garden Village": 45000,
            # Menetapkan harga Penglipuran Village dari harga mulai 50.000.
            "Penglipuran Village": 50000,
            # Menetapkan harga Banjar Hot Spring dari harga mulai 20.000.
            "Banjar Hot Spring": 20000,
            # Menetapkan harga Bali Pulina dari harga mulai 100.000.
            "Bali Pulina": 100000,
            # Menetapkan harga Goa Lawah Temple dari harga mulai 20.000.
            "Goa Lawah Temple": 20000,
            # Menetapkan harga Pantai Batu Bolong berdasarkan biaya parkir akses umum 5.000.
            "Pantai Batu Bolong": 5000,
        }

    # Membaca CSV nyata lalu menambahkan kolom harga bersih dan korpus teks NLP.
    def load_and_enrich_data(self, csv_path: str) -> pd.DataFrame:
        # Membaca file CSV ke DataFrame.
        df = pd.read_csv(csv_path)

        # Memastikan kolom Place tersedia karena dipakai untuk map harga.
        if "Place" not in df.columns:
            # Menghentikan proses dengan pesan jelas jika schema tidak sesuai.
            raise ValueError("Kolom 'Place' tidak ditemukan pada CSV.")

        # Memastikan kolom Description tersedia karena dipakai untuk fitur NLP.
        if "Description" not in df.columns:
            # Menghentikan proses dengan pesan jelas jika schema tidak sesuai.
            raise ValueError("Kolom 'Description' tidak ditemukan pada CSV.")

        # Membuat kolom harga_tiket_clean dari hasil map Place ke kamus_harga_bali.
        df["harga_tiket_clean"] = df["Place"].map(self.kamus_harga_bali)

        # Mengisi nilai yang tidak ditemukan dengan default 20.000 agar pipeline tetap stabil.
        df["harga_tiket_clean"] = df["harga_tiket_clean"].fillna(20000)

        # Mengubah tipe harga menjadi integer agar aman dipakai operasi budget.
        df["harga_tiket_clean"] = df["harga_tiket_clean"].astype(int)

        # Membuat kolom deskripsi_suasana dari Place dan Description sebagai korpus NLP.
        df["deskripsi_suasana"] = (
            # Mengambil Place dan mengamankan nilai kosong.
            df["Place"].fillna("").astype(str)
            # Menambahkan spasi agar token kata tidak menempel.
            + " "
            # Menggabungkan Description agar konteks preferensi lebih kaya.
            + df["Description"].fillna("").astype(str)
        )

        # Mengembalikan DataFrame yang sudah diperkaya untuk tahap rekomendasi.
        return df

    # Menjalankan rekomendasi hybrid: filter budget dulu, lalu ranking NLP.
    def get_recommendations(
        self,
        df_processed: pd.DataFrame,
        total_budget: float,
        durasi_hari: int,
        jumlah_orang: int,
        preferensi_user: str,
    ) -> List[dict]:
        # Menghitung plafon budget harian per orang berdasarkan input user.
        plafon_harian_per_orang = total_budget / (durasi_hari * jumlah_orang)

        # Memfilter destinasi yang harga_tiket_clean tidak melewati plafon harian.
        kandidat_budget = df_processed[df_processed["harga_tiket_clean"] <= plafon_harian_per_orang].copy()

        # Mengembalikan list kosong jika semua destinasi gugur di tahap budget.
        if kandidat_budget.empty:
            # Mengembalikan struktur kosong agar frontend mudah menangani no result.
            return []

        # Membuat vectorizer TF-IDF untuk mengubah teks destinasi menjadi fitur numerik.
        vectorizer = TfidfVectorizer()

        # Melatih TF-IDF pada deskripsi_suasana kandidat hasil filter budget.
        matriks_tfidf = vectorizer.fit_transform(kandidat_budget["deskripsi_suasana"].fillna("").astype(str))

        # Mengubah preferensi user menjadi vektor pada ruang fitur yang sama.
        vektor_user = vectorizer.transform([str(preferensi_user).lower()])

        # Menghitung cosine similarity sebagai skor relevansi antara user dan tiap destinasi.
        skor_kemiripan = cosine_similarity(vektor_user, matriks_tfidf).flatten()

        # Menyimpan skor kemiripan ke kolom baru agar bisa diurutkan.
        kandidat_budget["skor_kemiripan"] = skor_kemiripan

        # Mengurutkan kandidat dari skor tertinggi ke terendah.
        hasil_terurut = kandidat_budget.sort_values(by="skor_kemiripan", ascending=False)

        # Membulatkan skor agar output lebih rapi saat ditampilkan.
        hasil_terurut["skor_kemiripan"] = hasil_terurut["skor_kemiripan"].round(4)

        # Memilih kolom output penting untuk konsumsi API frontend.
        kolom_output = [
            "Place",
            "Location",
            "Google Maps Rating",
            "Google Reviews (Count)",
            "harga_tiket_clean",
            "skor_kemiripan",
            "deskripsi_suasana",
        ]

        # Menyaring hanya kolom yang benar-benar ada agar aman jika ada variasi schema minor.
        kolom_output_valid = [kolom for kolom in kolom_output if kolom in hasil_terurut.columns]

        # Mengembalikan hasil sebagai list of dictionary untuk endpoint JSON.
        return hasil_terurut[kolom_output_valid].to_dict(orient="records")
