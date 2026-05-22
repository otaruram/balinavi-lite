// Dataset 34 destinasi Bali — embedded langsung, tidak butuh backend
const DATASET = [
  { place: "Tanah Lot",                          location: "Tabanan",          harga: 20000,  rating: 4.7, keywords: "sunset pura laut spiritual budaya romantis foto" },
  { place: "Mount Batur",                        location: "Kintamani, Bangli", harga: 100000, rating: 4.5, keywords: "gunung vulkanik sunrise trekking petualangan alam aktif" },
  { place: "Uluwatu Temple",                     location: "Badung",           harga: 30000,  rating: 4.7, keywords: "pura tebing laut sunset kecak budaya spiritual foto" },
  { place: "Ubud Monkey Forest",                 location: "Gianyar",          harga: 50000,  rating: 4.4, keywords: "monyet hutan alam budaya santai hijau ubud" },
  { place: "Goa Gajah",                          location: "Gianyar",          harga: 50000,  rating: 4.2, keywords: "goa sejarah arkeologi budaya spiritual tenang candi" },
  { place: "Jatiluwih Rice Terraces",            location: "Tabanan",          harga: 40000,  rating: 4.7, keywords: "sawah hijau foto alam subak tenang panorama unesco" },
  { place: "Tegallalang Rice Terrace",           location: "Gianyar",          harga: 15000,  rating: 4.4, keywords: "sawah hijau foto alam ubud panorama swing" },
  { place: "Pura Ulun Danu Bratan",              location: "Buleleng",         harga: 50000,  rating: 4.7, keywords: "danau pura alam dingin pegunungan foto spiritual" },
  { place: "Seminyak Beach",                     location: "Badung",           harga: 0,      rating: 4.3, keywords: "pantai sunset bar kuliner romantis santai mewah" },
  { place: "Nusa Dua Beach",                     location: "Badung",           harga: 0,      rating: 4.5, keywords: "pantai bersih resort mewah snorkeling tenang keluarga" },
  { place: "Besakih Temple",                     location: "Karangasem",       harga: 60000,  rating: 4.5, keywords: "pura terbesar spiritual budaya sejarah sakral agama" },
  { place: "Kuta Beach",                         location: "Badung",           harga: 0,      rating: 4.2, keywords: "pantai surfing sunset ramai belanja kuliner muda" },
  { place: "Pura Lempuyang",                     location: "Karangasem",       harga: 55000,  rating: 4.6, keywords: "pura agung gerbang surga foto spiritual budaya" },
  { place: "Sidemen Valley",                     location: "Karangasem",       harga: 0,      rating: 4.6, keywords: "lembah sawah tenang alam foto panorama sejuk" },
  { place: "Tirta Empul Temple",                 location: "Gianyar",          harga: 50000,  rating: 4.6, keywords: "pura air suci mandi spiritual pemurnian budaya" },
  { place: "West Bali National Park",            location: "Jembrana",         harga: 200000, rating: 4.4, keywords: "taman nasional alam liar diving snorkeling petualangan konservasi" },
  { place: "Garuda Wisnu Kencana",               location: "Badung",           harga: 100000, rating: 4.5, keywords: "patung budaya pertunjukan seni foto taman mewah" },
  { place: "Bali Zoo",                           location: "Gianyar",          harga: 90000,  rating: 4.3, keywords: "kebun binatang anak keluarga satwa edukasi seru" },
  { place: "Bali Bird Park",                     location: "Gianyar",          harga: 385000, rating: 4.4, keywords: "burung eksotis keluarga edukasi anak satwa foto" },
  { place: "Tirta Gangga",                       location: "Karangasem",       harga: 50000,  rating: 4.6, keywords: "taman air kolam foto tenang sejarah kerajaan" },
  { place: "Tegenungan Waterfall",               location: "Gianyar",          harga: 15000,  rating: 4.4, keywords: "air terjun alam segar foto kolam renang hijau" },
  { place: "Bali Swing",                         location: "Gianyar",          harga: 150000, rating: 4.2, keywords: "swing foto ekstrem sawah ubud instagram keren" },
  { place: "Waterboom Bali",                     location: "Badung",           harga: 495000, rating: 4.4, keywords: "waterpark seru anak keluarga kolam seluncur hiburan" },
  { place: "Campuhan Ridge Walk",                location: "Gianyar",          harga: 0,      rating: 4.5, keywords: "trekking jalan kaki alam hijau pagi santai ubud" },
  { place: "Bali Safari and Marine Park",        location: "Gianyar",          harga: 720000, rating: 4.4, keywords: "safari gajah keluarga anak mewah safari malam" },
  { place: "Bajra Sandhi Monument",              location: "Denpasar",         harga: 30000,  rating: 4.4, keywords: "monumen sejarah budaya museum perjuangan foto" },
  { place: "Sukawati Art Market",                location: "Gianyar",          harga: 0,      rating: 4.1, keywords: "pasar seni belanja oleh-oleh murah budaya kerajinan" },
  { place: "Taman Ujung",                        location: "Karangasem",       harga: 50000,  rating: 4.5, keywords: "taman air kerajaan foto sejarah romantis panorama" },
  { place: "Secret Garden Village",              location: "Bedugul, Tabanan", harga: 45000,  rating: 4.4, keywords: "taman bunga kopi coklat edukasi agro foto hijau" },
  { place: "Penglipuran Village",                location: "Bangli",           harga: 50000,  rating: 4.7, keywords: "desa adat budaya tradisional bersih tenang bambu" },
  { place: "Banjar Hot Spring",                  location: "Buleleng",         harga: 20000,  rating: 4.3, keywords: "pemandian air panas relaksasi alam sejuk pegunungan" },
  { place: "Bali Pulina",                        location: "Gianyar",          harga: 100000, rating: 4.3, keywords: "kopi luwak agrowisata kebun teh santai foto pemandangan" },
  { place: "Goa Lawah Temple",                   location: "Klungkung",        harga: 20000,  rating: 4.2, keywords: "pura kelelawar goa spiritual budaya sejarah sakral" },
  { place: "Pantai Batu Bolong",                 location: "Badung",           harga: 5000,   rating: 4.4, keywords: "pantai sunset pura foto santai surfing canggu" },
];

const form = document.getElementById("rekomendasi-form");
const statusEl = document.getElementById("status");
const submitBtn = document.getElementById("submit-btn");
const resultsBody = document.getElementById("results-body");
const countBadge = document.getElementById("count-badge");

function formatRupiah(value) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(Number(value) || 0);
}

function scoreKeyword(keywords, preferensi) {
  if (!preferensi) return 0;
  const words = preferensi.toLowerCase().split(/\s+/).filter(Boolean);
  const kw = keywords.toLowerCase();
  return words.filter((w) => kw.includes(w)).length;
}

function recommend(totalBudget, durasiHari, jumlahOrang, preferensi) {
  const plafonPerOrang = totalBudget / (durasiHari * jumlahOrang);
  return DATASET
    .filter((d) => d.harga <= plafonPerOrang)
    .map((d) => ({ ...d, skor: scoreKeyword(d.keywords, preferensi) }))
    .sort((a, b) => b.skor - a.skor || b.rating - a.rating);
}

function renderRows(data) {
  if (!data.length) {
    resultsBody.innerHTML = '<tr><td colspan="4" class="empty">Tidak ada destinasi yang sesuai budget.</td></tr>';
    countBadge.textContent = "0 hasil";
    return;
  }
  resultsBody.innerHTML = data
    .map(
      (d) => `<tr>
        <td>${d.place}</td>
        <td>${d.location}</td>
        <td>${formatRupiah(d.harga)}</td>
        <td>${d.rating.toFixed(1)}</td>
      </tr>`
    )
    .join("");
  countBadge.textContent = `${data.length} hasil`;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  submitBtn.disabled = true;
  statusEl.textContent = "Memproses...";

  const totalBudget  = Number(document.getElementById("total_budget").value);
  const durasiHari   = Number(document.getElementById("durasi_hari").value);
  const jumlahOrang  = Number(document.getElementById("jumlah_orang").value);
  const preferensi   = String(document.getElementById("preferensi_user").value || "").trim();

  const hasil = recommend(totalBudget, durasiHari, jumlahOrang, preferensi);
  renderRows(hasil);
  statusEl.textContent = hasil.length
    ? `${hasil.length} destinasi sesuai budget & preferensi kamu.`
    : "Coba naikkan budget atau kurangi jumlah hari/orang.";
  submitBtn.disabled = false;
});
