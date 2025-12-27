export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { email } = req.body;

  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

  try {
    // Call backend to create account
    const response = await fetch(`${backendUrl}/v1/account/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        tier: 'free',
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json(error);
    }

    const data = await response.json();

    // In production, the backend would send email via SendGrid
    // For demo, we return the API key in response
    console.log(`✅ New signup: ${email} - API Key: ${data.api_key}`);

    // TODO: Send email with SendGrid/Azure Communication Services
    // await sendWelcomeEmail(email, data.api_key);

    return res.status(200).json({
      message: 'API key sent to your email',
      apiKey: data.api_key, // Remove this in production (send via email only)
      docsUrl: '/docs',
    });
  } catch (error) {
    console.error('Signup error:', error);
    return res.status(500).json({ error: 'Failed to create account' });
  }
}
