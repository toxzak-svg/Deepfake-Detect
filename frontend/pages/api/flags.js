export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const { url } = req.body || {};
  if (!url) return res.status(400).json({ error: "url required" });

  try {
    const backendRes = await fetch("http://localhost:8000/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-api-key": process.env.BACKEND_API_KEY || "demo-key" },
      body: JSON.stringify({ url, source: "nextjs" }),
    });

    const data = await backendRes.json();
    return res.status(200).json(data);
  } catch (err) {
    return res.status(500).json({ error: String(err) });
  }
}
