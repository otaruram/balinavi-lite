const form = document.getElementById("rekomendasi-form");
const statusEl = document.getElementById("status");
const submitBtn = document.getElementById("submit-btn");
const resultsBody = document.getElementById("results-body");
const countBadge = document.getElementById("count-badge");

const backendUrl = window.BALINAVI_BACKEND_URL || "http://localhost:8000/api/rekomendasi";

function formatRupiah(value) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(Number(value) || 0);
}

function renderRows(data) {
  if (!Array.isArray(data) || data.length === 0) {
    resultsBody.innerHTML = '<tr><td colspan="4" class="empty">Tidak ada rekomendasi yang sesuai budget.</td></tr>';
    countBadge.textContent = "0 hasil";
    return;
  }

  const rows = data
    .map((item) => {
      const name = item.Place || item.nama || "-";
      const location = item.Location || item.kabupaten_kota || "-";
      const ticket = item.harga_tiket_clean ?? item.harga_tiket ?? 0;
      const score = item.skor_kemiripan ?? 0;
      return `
        <tr>
          <td>${name}</td>
          <td>${location}</td>
          <td>${formatRupiah(ticket)}</td>
          <td>${Number(score).toFixed(4)}</td>
        </tr>
      `;
    })
    .join("");

  resultsBody.innerHTML = rows;
  countBadge.textContent = `${data.length} hasil`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    total_budget: Number(document.getElementById("total_budget").value),
    durasi_hari: Number(document.getElementById("durasi_hari").value),
    jumlah_orang: Number(document.getElementById("jumlah_orang").value),
    preferensi_user: String(document.getElementById("preferensi_user").value || "").trim(),
  };

  submitBtn.disabled = true;
  statusEl.textContent = "Menghubungi backend dan menghitung rekomendasi...";

  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    renderRows(data);
    statusEl.textContent = "Rekomendasi berhasil didapatkan.";
  } catch (error) {
    console.error(error);
    statusEl.textContent = `Gagal menghubungi backend (${error.message}). Cek URL API dan CORS.`;
  } finally {
    submitBtn.disabled = false;
  }
});
