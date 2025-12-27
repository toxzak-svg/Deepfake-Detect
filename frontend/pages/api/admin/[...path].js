// Proxy endpoint for backend admin routes
export default async function handler(req, res) {
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
  
  const { path } = req.query;
  const endpoint = Array.isArray(path) ? path.join('/') : path;
  
  try {
    const response = await fetch(`${backendUrl}/admin/${endpoint}`, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Key': req.headers['x-admin-key'] || '',
      },
      body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to proxy request' });
  }
}
