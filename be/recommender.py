# Mengimpor anotasi tipe List agar kontrak input-output fungsi lebih jelas untuk tim.
from typing import List

# Mengimpor pandas sebagai alat utama membaca CSV, map dictionary, dan olah DataFrame.
import pandas as pd

# Mengimpor TfidfVectorizer untuk mengubah teks suasana menjadi representasi numerik NLP.
from sklearn.feature_extraction.text import TfidfVectorizer

# Mengimpor cosine_similarity untuk menghitung kemiripan preferensi user terhadap destinasi.
from sklearn.metrics.pairwise import cosine_similarity


# Mendefinisikan class utama rekomendasi hybrid yang akan dipakai service/backend.
class HybridRecommender:
    # Menjalankan inisialisasi class sekali saat objek dibuat.
    def __init__(self) -> None:
        # Menyimpan kamus harga tiket hasil estimasi/riset untuk menutup gap data Kaggle.
        self.kamus_harga_bali = {
            # Contoh destinasi dari request Anda dengan estimasi harga tiket masuk.
            "Taman Mumbul Sangeh": 30000,
            # Contoh destinasi dari request Anda dengan estimasi harga tiket masuk.
            "Sangeh Monkey Forest": 30000,
            # Contoh destinasi dari request Anda dengan estimasi harga tiket masuk.
            "Objek Wisata Sangeh": 30000,
            # Contoh destinasi dari request Anda yang bersifat ruang publik gratis.
            "Satria Gatotkaca Park": 0,
            # Contoh destinasi dari request Anda yang diasumsikan tanpa tiket masuk.
            "Desa Wisata Penarungan": 0,
            # Contoh destinasi dari request Anda dengan estimasi tiket konservatif.
            "Di kaki Gunung Agung": 15000,
            # Contoh destinasi dari request Anda dengan estimasi tiket konservatif.
            "West Garden Pangi": 20000,
            # Contoh destinasi dari request Anda yang dikategorikan gratis.
            "Taman desa Dalung": 0,
            # Contoh destinasi dari request Anda yang dikategorikan gratis.
            "Kedonganan": 0,
            # Contoh destinasi dari request Anda dengan estimasi tiket konservatif.
            "Obyek Wisata Batu Belah Antiga": 30000,
        }

    # Membaca CSV mentah lalu menyuntikkan harga tiket dan membangun fitur teks NLP.
    def load_and_enrich_data(self, csv_path: str) -> pd.DataFrame:
        # Membaca file CSV Kaggle ke DataFrame agar bisa diproses lanjut.
        df = pd.read_csv(csv_path)

        # Memetakan kolom nama ke kamus harga menggunakan .map() sesuai kebutuhan MVP.
        df["harga_tiket"] = df["nama"].map(self.kamus_harga_bali)

        # Mengisi nama yang tidak ditemukan di kamus dengan default 20000 agar tetap usable.
        df["harga_tiket"] = df["harga_tiket"].fillna(20000)

        # Mengubah tipe harga ke integer supaya output konsisten untuk hitung budget.
        df["harga_tiket"] = df["harga_tiket"].astype(int)

        # Menyiapkan kolom teks gabungan dari atribut utama untuk korpus content-based NLP.
        df["deskripsi_suasana"] = (
            # Mengambil nama destinasi lalu memastikan aman jika ada nilai kosong.
            df["nama"].fillna("").astype(str)
            # Menambahkan pemisah spasi agar token kata tidak menempel.
            + " "
            # Menambahkan kategori destinasi sebagai sinyal tema aktivitas.
            + df["kategori"].fillna("").astype(str)
            # Menambahkan pemisah spasi agar token kata tidak menempel.
            + " "
            # Menambahkan kabupaten/kota untuk konteks lokasi dan nuansa daerah.
            + df["kabupaten_kota"].fillna("").astype(str)
            # Menambahkan pemisah spasi agar token kata tidak menempel.
            + " "
            # Menambahkan preferensi asli dari dataset sebagai sinyal suasana pengguna.
            + df["preferensi"].fillna("").astype(str)
        )

        # Mengembalikan DataFrame yang sudah diperkaya harga dan fitur teks.
        return df

    # Menghasilkan rekomendasi hybrid berdasarkan aturan budget dan kemiripan preferensi.
    def get_recommendations(
        self,
        df_processed: pd.DataFrame,
        total_budget: float,
        durasi_hari: int,
        jumlah_orang: int,
        preferensi_user: str,
    ) -> List[dict]:
        # Menghitung budget harian per orang sebagai batas keras Rule-Based Filtering.
        budget_harian_per_orang = total_budget / (durasi_hari * jumlah_orang)

        # Memfilter hanya destinasi dengan harga tiket yang masih masuk batas budget.
        kandidat_budget = df_processed[df_processed["harga_tiket"] <= budget_harian_per_orang].copy()

        # Mengembalikan list kosong jika tidak ada kandidat yang lolos filter budget.
        if kandidat_budget.empty:
            # Mengembalikan struktur JSON kosong agar backend mudah menangani kondisi ini.
            return []

        # Membuat vectorizer TF-IDF untuk menilai kedekatan makna teks preferensi.
        vectorizer = TfidfVectorizer()

        # Melatih vectorizer pada korpus kandidat dan mengubahnya menjadi matriks fitur.
        matriks_tfidf = vectorizer.fit_transform(kandidat_budget["deskripsi_suasana"].fillna("").astype(str))

        # Mengubah input preferensi user menjadi vektor pada ruang fitur yang sama.
        vektor_user = vectorizer.transform([str(preferensi_user).lower()])

        # Menghitung skor cosine similarity antara user dan setiap destinasi kandidat.
        skor_kemiripan = cosine_similarity(vektor_user, matriks_tfidf).flatten()

        # Menyimpan skor kemiripan ke kolom baru agar bisa dipakai untuk ranking.
        kandidat_budget["skor_kemiripan"] = skor_kemiripan

        # Mengurutkan hasil dari skor tertinggi ke terendah agar rekomendasi paling relevan ada di atas.
        hasil_terurut = kandidat_budget.sort_values(by="skor_kemiripan", ascending=False)

        # Membulatkan skor supaya output lebih rapi saat ditampilkan di API/Frontend.
        hasil_terurut["skor_kemiripan"] = hasil_terurut["skor_kemiripan"].round(4)

        # Mengembalikan seluruh kolom penting dalam format list of dictionary siap konsumsi FastAPI.
        return hasil_terurut.to_dict(orient="records")
