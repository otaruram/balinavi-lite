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

    # Menstandarkan schema minimum agar engine tetap jalan pada dataset utama maupun fallback.
    def _ensure_core_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        hasil = df.copy()

        if "Place" not in hasil.columns and "nama" in hasil.columns:
            hasil["Place"] = hasil["nama"].astype(str)
        if "Location" not in hasil.columns and "kabupaten_kota" in hasil.columns:
            hasil["Location"] = hasil["kabupaten_kota"].astype(str)
        if "Google Maps Rating" not in hasil.columns and "rating" in hasil.columns:
            hasil["Google Maps Rating"] = pd.to_numeric(hasil["rating"], errors="coerce").fillna(0.0)
        if "Google Reviews (Count)" not in hasil.columns:
            hasil["Google Reviews (Count)"] = 0

        if "Description" not in hasil.columns:
            if "preferensi" in hasil.columns:
                hasil["Description"] = hasil["preferensi"].fillna("").astype(str)
            else:
                hasil["Description"] = ""

        if "deskripsi_suasana" not in hasil.columns:
            place_text = (
                hasil["Place"].fillna("").astype(str)
                if "Place" in hasil.columns
                else pd.Series([""] * len(hasil), index=hasil.index)
            )
            desc_text = (
                hasil["Description"].fillna("").astype(str)
                if "Description" in hasil.columns
                else pd.Series([""] * len(hasil), index=hasil.index)
            )
            hasil["deskripsi_suasana"] = (
                place_text
                + " "
                + desc_text
            )

        if "harga_tiket_clean" not in hasil.columns:
            if "Place" in hasil.columns:
                hasil["harga_tiket_clean"] = hasil["Place"].map(self.kamus_harga_bali).fillna(20000).astype(int)
            else:
                hasil["harga_tiket_clean"] = 20000

        return hasil

    # Melakukan normalisasi min-max agar beberapa sinyal skor bisa digabungkan adil.
    def _normalize_series(self, series: pd.Series) -> pd.Series:
        numeric = pd.to_numeric(series, errors="coerce").fillna(0.0)
        minimum = float(numeric.min())
        maksimum = float(numeric.max())
        if maksimum <= minimum:
            return pd.Series([0.0] * len(numeric), index=numeric.index)
        return (numeric - minimum) / (maksimum - minimum)

    # Menyusun penjelasan singkat agar user paham kenapa sebuah destinasi direkomendasikan.
    def _build_reason(self, row: pd.Series, query_terms: List[str]) -> str:
        teks = str(row.get("deskripsi_suasana", "")).lower()
        terms_match = [term for term in query_terms if term in teks]
        terms_text = ", ".join(terms_match[:3]) if terms_match else "preferensi umum"
        return (
            f"Cocok dengan preferensi: {terms_text}; "
            f"rating {float(row.get('Google Maps Rating', 0.0)):.1f}; "
            f"tiket sekitar Rp{int(row.get('harga_tiket_clean', 0)):,}".replace(",", ".")
        )

    # Membagi rekomendasi ke dalam slot hari perjalanan agar output siap pakai sebagai itinerary.
    def _assign_itinerary_day(self, total_item: int, durasi_hari: int) -> List[int]:
        if total_item <= 0:
            return []
        jumlah_hari = max(int(durasi_hari), 1)
        return [min((idx % jumlah_hari) + 1, jumlah_hari) for idx in range(total_item)]

    # Membaca CSV nyata lalu menambahkan kolom harga bersih dan korpus teks NLP.
    def load_and_enrich_data(self, csv_path: str) -> pd.DataFrame:
        # Membaca file CSV ke DataFrame.
        df = pd.read_csv(csv_path)

        # Menstandarkan kolom inti agar engine scoring tetap konsisten lintas sumber data.
        df = self._ensure_core_columns(df)

        # Memastikan kolom Place tersedia karena dipakai untuk map harga.
        if "Place" not in df.columns:
            # Menghentikan proses dengan pesan jelas jika schema tidak sesuai.
            raise ValueError("Kolom 'Place' tidak ditemukan pada CSV.")

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
        # Menstandarkan schema inti untuk menjaga kompatibilitas dataset fallback/API.
        df_processed = self._ensure_core_columns(df_processed)

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

        # Menyiapkan sinyal skor tambahan agar rekomendasi tidak hanya bergantung pada kemiripan kata.
        kandidat_budget["rating_norm"] = self._normalize_series(kandidat_budget["Google Maps Rating"])
        kandidat_budget["popularitas_norm"] = self._normalize_series(kandidat_budget["Google Reviews (Count)"])
        kandidat_budget["harga_norm"] = self._normalize_series(kandidat_budget["harga_tiket_clean"])
        kandidat_budget["affordability_norm"] = 1.0 - kandidat_budget["harga_norm"]

        # Menggabungkan beberapa sinyal menjadi skor akhir yang lebih stabil dan realistis.
        kandidat_budget["skor_total"] = (
            kandidat_budget["skor_kemiripan"] * 0.45
            + kandidat_budget["rating_norm"] * 0.25
            + kandidat_budget["popularitas_norm"] * 0.15
            + kandidat_budget["affordability_norm"] * 0.15
        )

        # Menyiapkan penjelasan singkat agar output mudah dipahami user non-teknis.
        terms = [kata for kata in str(preferensi_user).lower().split() if kata.strip()]
        kandidat_budget["alasan_rekomendasi"] = kandidat_budget.apply(
            lambda baris: self._build_reason(baris, terms),
            axis=1,
        )

        # Mengurutkan kandidat dari skor total tertinggi ke terendah.
        hasil_terurut = kandidat_budget.sort_values(by="skor_total", ascending=False).copy()

        # Membatasi jumlah hasil agar itinerary tetap fokus dan tidak terlalu panjang.
        max_item = min(len(hasil_terurut), max(int(durasi_hari) * 4, 4))
        hasil_terurut = hasil_terurut.head(max_item).copy()

        # Menambahkan informasi hari itinerary agar langsung bisa dipresentasikan sebagai rencana trip.
        hasil_terurut["itinerary_hari"] = self._assign_itinerary_day(len(hasil_terurut), durasi_hari)

        # Membulatkan skor agar output lebih rapi saat ditampilkan.
        hasil_terurut["skor_kemiripan"] = hasil_terurut["skor_kemiripan"].round(4)
        hasil_terurut["skor_total"] = hasil_terurut["skor_total"].round(4)

        # Memilih kolom output penting untuk konsumsi API frontend.
        kolom_output = [
            "Place",
            "Location",
            "Google Maps Rating",
            "Google Reviews (Count)",
            "harga_tiket_clean",
            "skor_kemiripan",
            "skor_total",
            "itinerary_hari",
            "alasan_rekomendasi",
            "deskripsi_suasana",
        ]

        # Menyaring hanya kolom yang benar-benar ada agar aman jika ada variasi schema minor.
        kolom_output_valid = [kolom for kolom in kolom_output if kolom in hasil_terurut.columns]

        # Mengembalikan hasil sebagai list of dictionary untuk endpoint JSON.
        return hasil_terurut[kolom_output_valid].to_dict(orient="records")
