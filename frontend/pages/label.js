import { useEffect, useState } from "react";

export default function LabelPage() {
  const [urls, setUrls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/seed').then(r=>r.json()).then(data=>{ setUrls(data.urls||[]); setLoading(false)}).catch(()=>setLoading(false));
  },[]);

  async function submitLabel(url, label) {
    await fetch('/api/label', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, label, reporter: 'web-ui' })
    });
    alert('submitted');
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>Labeling UI</h1>
      {loading && <div>Loading...</div>}
      {!loading && urls.length === 0 && <div>No seed URLs found.</div>}
      {!loading && urls.map(u => (
        <div key={u} style={{ marginBottom: 12, padding: 8, borderBottom: '1px solid #eee' }}>
          <div style={{ marginBottom: 6 }}>{u}</div>
          <button onClick={()=>submitLabel(u,'scam')} style={{ marginRight: 8 }}>Scam</button>
          <button onClick={()=>submitLabel(u,'legit')}>Legit</button>
        </div>
      ))}
    </main>
  )
}
