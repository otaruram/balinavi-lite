const form = document.getElementById("rekomendasi-form");
const statusEl = document.getElementById("status");
const submitBtn = document.getElementById("submit-btn");
const resultsBody = document.getElementById("results-body");
const countBadge = document.getElementById("count-badge");
const streamlitLinkWrap = document.getElementById("streamlit-link-wrap");
const streamlitLink = document.getElementById("streamlit-link");

const streamlitUrl = "https://balinavi.streamlit.app";

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

streamlitLink.href = streamlitUrl;
streamlitLinkWrap.classList.remove("hidden");
statusEl.textContent = "Form akan mengirim parameter langsung ke aplikasi Streamlit backend.";

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    total_budget: Number(document.getElementById("total_budget").value),
    durasi_hari: Number(document.getElementById("durasi_hari").value),
    jumlah_orang: Number(document.getElementById("jumlah_orang").value),
    preferensi_user: String(document.getElementById("preferensi_user").value || "").trim(),
  };

  submitBtn.disabled = true;
  statusEl.textContent = "Mengarahkan ke Streamlit backend...";

  const params = new URLSearchParams({
    total_budget: String(payload.total_budget),
    durasi_hari: String(payload.durasi_hari),
    jumlah_orang: String(payload.jumlah_orang),
    preferensi_user: payload.preferensi_user,
    auto_run: "1",
  });

  window.location.href = `${streamlitUrl}?${params.toString()}`;
});
