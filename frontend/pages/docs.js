import Head from 'next/head';

export default function APIDocs() {
  return (
    <>
      <Head>
        <title>API Documentation - DeepfakeGuard</title>
      </Head>

      <div className="min-h-screen bg-gray-900 text-white">
        {/* Navigation */}
        <nav className="bg-black/50 backdrop-blur-md border-b border-purple-500/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <a href="/landing" className="flex items-center space-x-2">
                <span className="text-3xl">🛡️</span>
                <span className="text-2xl font-bold">DeepfakeGuard</span>
              </a>
              <div className="flex space-x-6">
                <a href="/landing" className="text-gray-300 hover:text-white">Home</a>
                <a href="/api/docs" className="text-purple-400">API Docs</a>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header */}
          <div className="mb-12">
            <h1 className="text-5xl font-bold mb-4">API Documentation</h1>
            <p className="text-xl text-gray-400">
              Simple REST API for deepfake detection with webhook notifications
            </p>
          </div>

          {/* Quick Start */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Quick Start</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-lg font-semibold mb-3">1. Get Your API Key</h3>
              <p className="text-gray-400 mb-4">
                Sign up at our <a href="/landing" className="text-purple-400 hover:text-purple-300">landing page</a> to receive your API key instantly. Free tier includes 10 scans.
              </p>

              <h3 className="text-lg font-semibold mb-3">2. Make Your First Request</h3>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-green-400">{`curl -X POST https://api.deepfakeguard.com/v1/scan \\
  -H "X-API-Key: dfg_your_api_key_here" \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://example.com/suspicious-video.mp4"
  }'`}</code>
              </pre>
            </div>
          </section>

          {/* Authentication */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Authentication</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <p className="text-gray-300 mb-4">
                Include your API key in the <code className="bg-gray-700 px-2 py-1 rounded">X-API-Key</code> header with every request:
              </p>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-blue-400">X-API-Key: dfg_your_api_key_here</code>
              </pre>
            </div>
          </section>

          {/* Endpoints */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-6">API Endpoints</h2>

            {/* Scan Media */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-6">
              <div className="flex items-center space-x-3 mb-4">
                <span className="bg-green-600 px-3 py-1 rounded text-sm font-bold">POST</span>
                <span className="text-xl font-mono">/v1/scan</span>
              </div>
              <p className="text-gray-400 mb-4">Scan an image or video for deepfake detection.</p>

              <h4 className="font-semibold mb-2">Request Body</h4>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto mb-4">
                <code className="text-yellow-400">{`{
  "url": "https://example.com/media.jpg",
  "source": "telegram"  // optional
}`}</code>
              </pre>

              <h4 className="font-semibold mb-2">Response</h4>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto mb-4">
                <code className="text-green-400">{`{
  "score": 0.85,              // 0-1, higher = more likely deepfake
  "flags": [
    "model_suspect_frame",
    "contains_giveaway_keyword"
  ],
  "details": {
    "scan_id": "abc123...",
    "manual_review_pending": true,
    "scans_remaining": 7
  }
}`}</code>
              </pre>

              <h4 className="font-semibold mb-2">Example (JavaScript)</h4>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-purple-400">{`const response = await fetch('https://api.deepfakeguard.com/v1/scan', {
  method: 'POST',
  headers: {
    'X-API-Key': 'dfg_your_api_key_here',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://example.com/suspicious-image.jpg'
  })
});

const result = await response.json();
console.log('Deepfake score:', result.score);`}</code>
              </pre>
            </div>

            {/* Get Stats */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-6">
              <div className="flex items-center space-x-3 mb-4">
                <span className="bg-blue-600 px-3 py-1 rounded text-sm font-bold">GET</span>
                <span className="text-xl font-mono">/v1/account/stats</span>
              </div>
              <p className="text-gray-400 mb-4">Get your account usage statistics.</p>

              <h4 className="font-semibold mb-2">Response</h4>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-green-400">{`{
  "email": "user@example.com",
  "tier": "free",
  "scans_used": 3,
  "scans_limit": 10,
  "scans_remaining": 7,
  "total_scans": 3
}`}</code>
              </pre>
            </div>

            {/* Update Webhook */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-6">
              <div className="flex items-center space-x-3 mb-4">
                <span className="bg-green-600 px-3 py-1 rounded text-sm font-bold">POST</span>
                <span className="text-xl font-mono">/v1/account/webhook</span>
              </div>
              <p className="text-gray-400 mb-4">Configure webhook URL for real-time notifications.</p>

              <h4 className="font-semibold mb-2">Request Body</h4>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-yellow-400">{`{
  "webhook_url": "https://your-server.com/webhook"
}`}</code>
              </pre>
            </div>
          </section>

          {/* Webhooks */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Webhooks</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <p className="text-gray-300 mb-6">
                Receive instant notifications when scans complete or deepfakes are detected.
                Configure your webhook URL via the API or dashboard.
              </p>

              <h3 className="text-xl font-semibold mb-3">Event Types</h3>

              <div className="space-y-4 mb-6">
                <div className="bg-gray-900 rounded p-4">
                  <h4 className="font-semibold mb-2">scan.completed</h4>
                  <p className="text-gray-400 text-sm mb-2">Triggered when any scan finishes</p>
                  <pre className="bg-black rounded p-3 overflow-x-auto text-sm">
                    <code className="text-green-400">{`{
  "event": "scan.completed",
  "timestamp": "2025-12-27T10:30:00Z",
  "data": {
    "scan_id": "abc123",
    "url": "https://...",
    "score": 0.35,
    "is_flagged": false
  }
}`}</code>
                  </pre>
                </div>

                <div className="bg-gray-900 rounded p-4">
                  <h4 className="font-semibold mb-2">scan.flagged</h4>
                  <p className="text-gray-400 text-sm mb-2">Triggered when deepfake is detected (score {'>'} 0.6)</p>
                  <pre className="bg-black rounded p-3 overflow-x-auto text-sm">
                    <code className="text-red-400">{`{
  "event": "scan.flagged",
  "timestamp": "2025-12-27T10:30:00Z",
  "data": {
    "scan_id": "abc123",
    "url": "https://...",
    "score": 0.85,
    "severity": "high",
    "manual_review_pending": true
  }
}`}</code>
                  </pre>
                </div>

                <div className="bg-gray-900 rounded p-4">
                  <h4 className="font-semibold mb-2">review.completed</h4>
                  <p className="text-gray-400 text-sm mb-2">Triggered after manual review (Pro/Enterprise only)</p>
                  <pre className="bg-black rounded p-3 overflow-x-auto text-sm">
                    <code className="text-blue-400">{`{
  "event": "review.completed",
  "timestamp": "2025-12-27T12:00:00Z",
  "data": {
    "scan_id": "abc123",
    "original_score": 0.85,
    "reviewed_verdict": "confirmed",
    "reviewer_notes": "Clear facial manipulation"
  }
}`}</code>
                  </pre>
                </div>
              </div>

              <h3 className="text-xl font-semibold mb-3">Webhook Security</h3>
              <ul className="list-disc list-inside text-gray-400 space-y-2">
                <li>Always use HTTPS endpoints</li>
                <li>Verify the webhook source by checking the timestamp</li>
                <li>Return 200 OK within 10 seconds to acknowledge receipt</li>
                <li>Implement idempotency using the scan_id to handle retries</li>
              </ul>
            </div>
          </section>

          {/* Rate Limits */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Rate Limits</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3">Tier</th>
                    <th className="text-left py-3">Scans/Month</th>
                    <th className="text-left py-3">Manual Review</th>
                  </tr>
                </thead>
                <tbody className="text-gray-300">
                  <tr className="border-b border-gray-700">
                    <td className="py-3">Free</td>
                    <td className="py-3">10</td>
                    <td className="py-3">❌ No</td>
                  </tr>
                  <tr className="border-b border-gray-700">
                    <td className="py-3">Pro ($49/mo)</td>
                    <td className="py-3">500</td>
                    <td className="py-3">✅ Yes</td>
                  </tr>
                  <tr>
                    <td className="py-3">Enterprise</td>
                    <td className="py-3">Unlimited</td>
                    <td className="py-3">✅ Dedicated Team</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Error Codes */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Error Codes</h2>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="space-y-3 text-gray-300">
                <div className="flex">
                  <code className="bg-red-900/50 text-red-300 px-3 py-1 rounded mr-4">400</code>
                  <span>Bad Request - Invalid parameters</span>
                </div>
                <div className="flex">
                  <code className="bg-red-900/50 text-red-300 px-3 py-1 rounded mr-4">401</code>
                  <span>Unauthorized - Invalid or missing API key</span>
                </div>
                <div className="flex">
                  <code className="bg-yellow-900/50 text-yellow-300 px-3 py-1 rounded mr-4">429</code>
                  <span>Rate Limited - Monthly scan limit reached</span>
                </div>
                <div className="flex">
                  <code className="bg-red-900/50 text-red-300 px-3 py-1 rounded mr-4">500</code>
                  <span>Server Error - Something went wrong on our end</span>
                </div>
              </div>
            </div>
          </section>

          {/* SDKs & Examples */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Integration Examples</h2>

            {/* Discord Bot */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-4">
              <h3 className="text-xl font-semibold mb-3">Discord Bot (Python)</h3>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-purple-400">{`import discord
import httpx

DEEPFAKE_API_KEY = "dfg_your_key"
client = discord.Client()

@client.event
async def on_message(message):
    for attachment in message.attachments:
        if attachment.content_type.startswith('image'):
            # Scan the image
            async with httpx.AsyncClient() as http:
                response = await http.post(
                    'https://api.deepfakeguard.com/v1/scan',
                    headers={'X-API-Key': DEEPFAKE_API_KEY},
                    json={'url': attachment.url, 'source': 'discord'}
                )
                result = response.json()
                
                if result['score'] > 0.6:
                    await message.delete()
                    await message.channel.send(
                        f"⚠️ Potential deepfake detected! Score: {result['score']:.0%}"
                    )`}</code>
              </pre>
            </div>

            {/* Telegram Bot */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-semibold mb-3">Telegram Bot (Node.js)</h3>
              <pre className="bg-black rounded-lg p-4 overflow-x-auto">
                <code className="text-green-400">{`const { Telegraf } = require('telegraf');
const axios = require('axios');

const bot = new Telegraf(process.env.BOT_TOKEN);
const DEEPFAKE_API_KEY = 'dfg_your_key';

bot.on('photo', async (ctx) => {
  const photo = ctx.message.photo[ctx.message.photo.length - 1];
  const fileUrl = await ctx.telegram.getFileLink(photo.file_id);
  
  const { data } = await axios.post(
    'https://api.deepfakeguard.com/v1/scan',
    { url: fileUrl.href, source: 'telegram' },
    { headers: { 'X-API-Key': DEEPFAKE_API_KEY } }
  );
  
  if (data.score > 0.6) {
    await ctx.deleteMessage();
    await ctx.reply('⚠️ Deepfake detected and removed!');
  }
});`}</code>
              </pre>
            </div>
          </section>

          {/* Support */}
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Need Help?</h2>
            <div className="bg-purple-900/30 border border-purple-500/50 rounded-lg p-6">
              <p className="text-gray-300 mb-4">
                Questions or issues? We're here to help!
              </p>
              <div className="space-y-2 text-gray-300">
                <p>📧 Email: <a href="mailto:support@deepfakeguard.com" className="text-purple-400 hover:text-purple-300">support@deepfakeguard.com</a></p>
                <p>💬 Discord: <a href="#" className="text-purple-400 hover:text-purple-300">Join our community</a></p>
                <p>📚 Status: <a href="#" className="text-purple-400 hover:text-purple-300">status.deepfakeguard.com</a></p>
              </div>
            </div>
          </section>
        </div>
      </div>

      <style jsx>{`
        code {
          font-family: 'Monaco', 'Courier New', monospace;
          font-size: 0.9em;
        }
      `}</style>
    </>
  );
}
