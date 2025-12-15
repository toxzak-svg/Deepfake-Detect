import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  async function submit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("/api/flags", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 24, fontFamily: "Arial, sans-serif" }}>
      <h1>Deepfake-Detect — Demo UI</h1>
      <form onSubmit={submit} style={{ marginBottom: 16 }}>
        <input
          placeholder="https://..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ width: "60%", padding: 8, marginRight: 8 }}
        />
        <button type="submit" disabled={loading || !url}>
          {loading ? "Checking..." : "Check URL"}
        </button>
      </form>

      {result && (
        <section>
          <h2>Result</h2>
          <pre style={{ background: "#f7f7f7", padding: 12 }}>{JSON.stringify(result, null, 2)}</pre>
        </section>
      )}
    </main>
  );
}
