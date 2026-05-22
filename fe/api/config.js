export default function handler(req, res) {
  const backendUrl = process.env.BACKEND_URL || "";

  res.setHeader("Cache-Control", "no-store");
  res.status(200).json({
    backendUrl,
  });
}
