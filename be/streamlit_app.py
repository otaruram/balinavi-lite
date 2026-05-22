# Mengimpor os untuk membaca path dataset dari environment variable Streamlit Cloud.
import os

# Mengimpor pandas untuk menampilkan hasil rekomendasi dalam bentuk tabel rapi.
import pandas as pd

# Mengimpor streamlit sebagai framework utama aplikasi BE di Streamlit Cloud.
import streamlit as st

# Mengimpor engine hybrid agar logic rekomendasi tetap satu sumber dan konsisten.
from recommender import HybridRecommender

# Mengatur konfigurasi halaman supaya tampilan nyaman saat demo mentoring.
st.set_page_config(page_title="BaliNavi BE - Streamlit", page_icon="B", layout="wide")

# Menentukan path dataset default yang dipakai ketika env DATASET_PATH belum diisi.
DATASET_PATH = os.getenv("DATASET_PATH", "data/Bali Popular Destination for Tourist 2022 - Sheet1.csv")

# Membuat instance recommender sekali agar pemanggilan fungsi lebih efisien.
recommender = HybridRecommender()


# Membuat helper parsing integer dari query param agar aman jika user kirim nilai tidak valid.
def parse_int_query(value: str, default: int, min_value: int) -> int:
    # Mencoba konversi nilai query param menjadi integer.
    try:
        parsed = int(value)
    # Jika gagal konversi maka gunakan nilai default agar aplikasi tetap stabil.
    except (TypeError, ValueError):
        return default
    # Mengembalikan nilai terbesar antara parsed dan min_value agar tidak melanggar batas input.
    return max(parsed, min_value)


# Mengambil query param dari URL agar frontend Vercel bisa mengirim parameter ke Streamlit.
query = st.query_params

# Menyiapkan default total budget dari query jika ada, atau gunakan nilai bawaan aplikasi.
default_total_budget = parse_int_query(query.get("total_budget", 500000), default=500000, min_value=10000)

# Menyiapkan default durasi hari dari query jika ada, atau gunakan nilai bawaan aplikasi.
default_durasi_hari = parse_int_query(query.get("durasi_hari", 2), default=2, min_value=1)

# Menyiapkan default jumlah orang dari query jika ada, atau gunakan nilai bawaan aplikasi.
default_jumlah_orang = parse_int_query(query.get("jumlah_orang", 2), default=2, min_value=1)

# Menyiapkan default preferensi dari query jika ada, atau gunakan preferensi bawaan aplikasi.
default_preferensi_user = str(query.get("preferensi_user", "sunset budaya"))

# Menentukan apakah aplikasi perlu auto-run dari query param auto_run=1.
auto_run = str(query.get("auto_run", "0")) == "1"

# Menampilkan judul aplikasi backend agar jelas bahwa ini mode BE berbasis Streamlit.
st.title("BaliNavi Backend Engine (Streamlit)")

# Menampilkan ringkasan peran aplikasi supaya user paham ini engine rekomendasi.
st.caption("Aplikasi ini menjalankan logika hybrid budget + NLP langsung di Streamlit Cloud.")

# Menampilkan path dataset aktif agar transparan saat debugging data source.
st.write(f"Dataset path aktif: {DATASET_PATH}")

# Mencoba memuat dan memperkaya dataset menggunakan engine recommender.
try:
    # Memanggil loader utama untuk map harga_tiket_clean dan membangun deskripsi_suasana.
    df_processed = recommender.load_and_enrich_data(DATASET_PATH)
# Menangkap error loading agar aplikasi tidak crash total saat dataset bermasalah.
except Exception as exc:
    # Menampilkan pesan error yang jelas agar perbaikan cepat dilakukan.
    st.error(f"Gagal memuat dataset: {exc}")
    # Menghentikan eksekusi lebih lanjut agar blok input tidak jalan pada data invalid.
    st.stop()

# Membuat layout dua kolom agar form input lebih ringkas dan rapi.
col1, col2 = st.columns(2)

# Menempatkan input total budget pada kolom pertama.
with col1:
    # Input total budget dalam Rupiah.
    total_budget = st.number_input("Total budget (Rupiah)", min_value=10000, value=default_total_budget, step=10000)
    # Input durasi perjalanan dalam hari.
    durasi_hari = st.number_input("Durasi perjalanan (hari)", min_value=1, value=default_durasi_hari, step=1)

# Menempatkan input jumlah orang dan preferensi pada kolom kedua.
with col2:
    # Input jumlah orang dalam rombongan.
    jumlah_orang = st.number_input("Jumlah orang", min_value=1, value=default_jumlah_orang, step=1)
    # Input preferensi suasana untuk proses NLP ranking.
    preferensi_user = st.text_input("Preferensi suasana", value=default_preferensi_user)

# Menjalankan proses rekomendasi saat tombol ditekan.
run_clicked = st.button("Jalankan Rekomendasi")

# Menjalankan proses saat tombol ditekan atau saat mode auto_run aktif dari query param.
if run_clicked or auto_run:
    # Menjalankan engine hybrid dengan parameter input user.
    hasil = recommender.get_recommendations(
        df_processed=df_processed,
        total_budget=float(total_budget),
        durasi_hari=int(durasi_hari),
        jumlah_orang=int(jumlah_orang),
        preferensi_user=preferensi_user,
    )

    # Menangani kondisi jika tidak ada hasil yang lolos filter budget.
    if not hasil:
        # Menampilkan warning agar user mencoba parameter budget lain.
        st.warning("Tidak ada rekomendasi yang lolos budget harian per orang.")
    else:
        # Menampilkan notifikasi sukses dan jumlah destinasi yang didapat.
        st.success(f"Berhasil mendapatkan {len(hasil)} rekomendasi.")
        # Mengubah list dictionary menjadi DataFrame agar tabel rapi di Streamlit.
        df_hasil = pd.DataFrame(hasil)
        # Menampilkan tabel hasil rekomendasi untuk bahan analisis dan demo.
        st.dataframe(df_hasil, use_container_width=True)

# Menambahkan expander agar data sampel bisa dilihat saat live mentoring.
with st.expander("Lihat Sampel Dataset Terproses"):
    # Menampilkan 10 baris awal supaya reviewer paham struktur fitur yang dipakai model.
    st.dataframe(df_processed.head(10), use_container_width=True)
