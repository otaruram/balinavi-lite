# Mengimpor os untuk membaca environment variable URL backend saat deployment.
import os

# Mengimpor pandas agar data JSON dari backend mudah ditampilkan rapi menjadi DataFrame.
import pandas as pd

# Mengimpor requests untuk melakukan HTTP POST dari Streamlit ke FastAPI.
import requests

# Mengimpor Streamlit sebagai framework UI sederhana untuk frontend MVP.
import streamlit as st

# Mengatur konfigurasi halaman agar tampilan lebih nyaman di desktop maupun mobile.
st.set_page_config(page_title="BaliNavi Lite", page_icon="B", layout="centered")

# Menentukan URL endpoint backend dari environment variable atau fallback lokal.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/rekomendasi")

# Menambahkan CSS sederhana bertema monokrom agar antarmuka terlihat clean dan fokus.
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8f8f8 0%, #eeeeee 100%);
        color: #111111;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #111111;
        letter-spacing: 0.3px;
    }
    .stButton > button {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #111111;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #2a2a2a;
        border-color: #2a2a2a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Membuat fungsi helper untuk mengirim payload ke backend dan menangani error secara ramah.
def ambil_rekomendasi(payload: dict):
    # Mencoba melakukan request POST ke backend dengan timeout agar UI tidak menggantung lama.
    try:
        # Mengirim payload JSON ke endpoint backend sesuai kontrak API.
        response = requests.post(BACKEND_URL, json=payload, timeout=20)
        # Memicu exception jika status code bukan 2xx agar mudah ditangani di except.
        response.raise_for_status()
        # Mengembalikan data JSON list dict dari backend dan pesan error None.
        return response.json(), None
    # Menangkap semua error jaringan atau HTTP agar user mendapat feedback jelas.
    except requests.RequestException as exc:
        # Mengembalikan list kosong dan string error agar frontend tetap stabil.
        return [], str(exc)


# Menampilkan judul utama aplikasi agar konteks penggunaan langsung terlihat.
st.title("BaliNavi Lite - Rekomendasi Budget + Vibe")

# Menampilkan deskripsi singkat supaya user paham alur input dan output aplikasi.
st.write("Masukkan preferensi perjalanan Anda, lalu klik tombol untuk mendapatkan rekomendasi.")

# Membuat input angka total budget dengan batas minimal agar tidak menerima nilai nol/negatif.
total_budget = st.number_input("Total budget (Rupiah)", min_value=10000, value=500000, step=10000)

# Membuat input angka durasi hari dengan minimal 1 hari.
durasi_hari = st.number_input("Durasi perjalanan (hari)", min_value=1, value=2, step=1)

# Membuat input angka jumlah orang dengan minimal 1 orang.
jumlah_orang = st.number_input("Jumlah orang", min_value=1, value=2, step=1)

# Membuat input teks preferensi vibe agar proses NLP punya query user.
preferensi_user = st.text_input("Preferensi suasana (contoh: sunset budaya santai)", value="sunset budaya")

# Menyediakan tombol aksi utama yang memicu request ke backend.
if st.button("Cari Rekomendasi"):
    # Menyusun payload sesuai schema Pydantic di backend.
    payload = {
        "total_budget": int(total_budget),
        "durasi_hari": int(durasi_hari),
        "jumlah_orang": int(jumlah_orang),
        "preferensi_user": preferensi_user.strip(),
    }

    # Memanggil fungsi request agar logika networking tidak menumpuk di blok UI.
    hasil, error = ambil_rekomendasi(payload)

    # Jika ada error maka tampilkan pesan error agar user bisa troubleshooting cepat.
    if error:
        st.error(f"Gagal menghubungi backend: {error}")
    # Jika hasil kosong maka tampilkan warning bahwa tidak ada tempat sesuai budget.
    elif not hasil:
        st.warning("Tidak ada rekomendasi yang cocok dengan budget per orang per hari Anda.")
    # Jika ada hasil maka tampilkan dalam tabel agar mudah dibandingkan.
    else:
        st.success("Rekomendasi berhasil didapatkan.")
        df_hasil = pd.DataFrame(hasil)
        st.dataframe(df_hasil, use_container_width=True)
