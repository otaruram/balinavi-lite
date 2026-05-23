# Mengimpor os untuk membaca path dataset dari environment variable Streamlit Cloud.
import os
import logging

# Mengimpor pandas untuk menampilkan hasil rekomendasi dalam bentuk tabel rapi.
import pandas as pd

# Mengimpor streamlit sebagai framework utama aplikasi BE di Streamlit Cloud.
import streamlit as st

# Mengimpor engine hybrid agar logic rekomendasi tetap satu sumber dan konsisten.
from recommender import HybridRecommender

# Mengatur konfigurasi halaman supaya tampilan nyaman saat demo mentoring.
st.set_page_config(page_title="BaliNavi BE - Streamlit", page_icon="B", layout="wide")

# Menentukan path dataset default relatif terhadap lokasi file ini agar benar di Streamlit Cloud.
_HERE = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.getenv("DATASET_PATH", os.path.join(_HERE, "data", "Bali Popular Destination for Tourist 2022 - Sheet1.csv"))

# Menyusun lokasi log aplikasi agar error runtime bisa ditelusuri saat deploy.
LOG_DIR = os.path.join(_HERE, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, "streamlit_app.log")

# Menyiapkan logger tunggal untuk aplikasi Streamlit ini.
logger = logging.getLogger("balinavi_lite_streamlit")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)
    logger.propagate = False

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


# Membuat helper format Rupiah agar ringkasan biaya lebih enak dibaca.
def format_rupiah(value: float) -> str:
    return f"Rp{int(value):,}".replace(",", ".")


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
st.caption(f"Log file: {LOG_FILE_PATH}")

# Mencoba memuat dan memperkaya dataset menggunakan engine recommender.
try:
    # Memanggil loader utama untuk map harga_tiket_clean dan membangun deskripsi_suasana.
    df_processed = recommender.load_and_enrich_data(DATASET_PATH)
# Menangkap error loading agar aplikasi tidak crash total saat dataset bermasalah.
except Exception as exc:
    logger.exception("Gagal memuat dataset pada path: %s", DATASET_PATH)
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
    try:
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
            plafon_harian = float(total_budget) / (int(durasi_hari) * int(jumlah_orang))
            st.info(
                "Coba naikkan total budget atau sederhanakan rencana. "
                f"Plafon saat ini: {format_rupiah(plafon_harian)} per orang per hari."
            )
        else:
            # Mengubah list dictionary menjadi DataFrame agar bisa ditampilkan sebagai planner ringkas.
            df_hasil = pd.DataFrame(hasil)

            # Menyiapkan ringkasan KPI agar user cepat membaca kualitas rencana trip.
            total_tiket = float(df_hasil["harga_tiket_clean"].sum()) if "harga_tiket_clean" in df_hasil.columns else 0.0
            budget_terpakai = (total_tiket / float(total_budget) * 100.0) if float(total_budget) > 0 else 0.0
            skor_rata = float(df_hasil["skor_total"].mean()) if "skor_total" in df_hasil.columns else 0.0

            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric("Total Rekomendasi", f"{len(df_hasil)} destinasi")
            with kpi2:
                st.metric("Estimasi Total Tiket", format_rupiah(total_tiket))
            with kpi3:
                st.metric("Skor Rata-rata", f"{skor_rata:.2f}")

            st.progress(min(max(budget_terpakai / 100.0, 0.0), 1.0))
            st.caption(f"Perkiraan penggunaan budget tiket: {budget_terpakai:.1f}% dari total budget.")

            # Menampilkan notifikasi sukses dan top insight hasil ranking.
            top_place = str(df_hasil.iloc[0].get("Place", "Top destinasi"))
            st.success(f"Rencana berhasil dibuat. Top pick saat ini: {top_place}.")

            # Menampilkan tabel hasil rekomendasi yang sudah diperkaya skor dan alasan.
            kolom_tampil = [
                "Place",
                "Location",
                "harga_tiket_clean",
                "Google Maps Rating",
                "skor_total",
                "itinerary_hari",
                "alasan_rekomendasi",
            ]
            kolom_tampil = [kol for kol in kolom_tampil if kol in df_hasil.columns]
            st.dataframe(df_hasil[kolom_tampil], use_container_width=True)

            # Menampilkan itinerary per hari agar output langsung siap dipakai user.
            if "itinerary_hari" in df_hasil.columns:
                st.subheader("Itinerary Harian")
                max_hari = int(df_hasil["itinerary_hari"].max())
                tab_hari = st.tabs([f"Hari {idx}" for idx in range(1, max_hari + 1)])
                for idx, tab in enumerate(tab_hari, start=1):
                    with tab:
                        agenda_hari = df_hasil[df_hasil["itinerary_hari"] == idx]
                        if agenda_hari.empty:
                            st.caption("Belum ada destinasi untuk hari ini.")
                            continue
                        for _, item in agenda_hari.iterrows():
                            nama = item.get("Place", "Destinasi")
                            lokasi = item.get("Location", "Lokasi tidak tersedia")
                            rating = float(item.get("Google Maps Rating", 0.0))
                            harga = float(item.get("harga_tiket_clean", 0.0))
                            alasan = item.get("alasan_rekomendasi", "Cocok dengan profil perjalanan kamu.")
                            with st.container(border=True):
                                st.markdown(f"### {nama}")
                                st.write(f"Lokasi: {lokasi}")
                                st.write(f"Rating: {rating:.1f} | Estimasi tiket: {format_rupiah(harga)}")
                                st.caption(alasan)
    except Exception as exc:
        logger.exception(
            "Gagal menjalankan rekomendasi. budget=%s, durasi=%s, orang=%s, preferensi=%s",
            total_budget,
            durasi_hari,
            jumlah_orang,
            preferensi_user,
        )
        st.error(f"Terjadi error saat menjalankan rekomendasi: {exc}")
        st.info(f"Cek log detail di: {LOG_FILE_PATH}")

# Menambahkan expander agar data sampel bisa dilihat saat live mentoring.
with st.expander("Lihat Sampel Dataset Terproses"):
    # Menampilkan 10 baris awal supaya reviewer paham struktur fitur yang dipakai model.
    st.dataframe(df_processed.head(10), use_container_width=True)
