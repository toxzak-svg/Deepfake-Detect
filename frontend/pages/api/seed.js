export default async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).json({ error: "Method not allowed" });
  try {
    const backendRes = await fetch("http://localhost:8000/seed", { headers: { "x-api-key": process.env.BACKEND_API_KEY || "demo-key" } });
    const data = await backendRes.json();
    return res.status(200).json(data);
  } catch (err) {
    return res.status(500).json({ error: String(err) });
  }
}
