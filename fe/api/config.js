export default function handler(req, res) {
  const backendUrl = process.env.BACKEND_URL || "";
  const streamlitUrl = process.env.STREAMLIT_APP_URL || "";

  res.setHeader("Cache-Control", "no-store");
  res.status(200).json({
    backendUrl,
    streamlitUrl,
  });
}
