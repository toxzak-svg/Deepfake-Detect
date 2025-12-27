# 🛡️ DeepfakeGuard API

## AI-Powered Deepfake Detection API for Telegram, Discord, and NFT Marketplaces

DeepfakeGuard is a simple, paid API service that helps moderators and platforms detect deepfake images and videos before they spread. Built for community protection with instant webhook notifications and optional human review.

## 🚀 Quick Start for API Users

```bash
# 1. Get your free API key (10 scans included)
curl -X POST https://deepfakeguard.com/api/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'

# 2. Scan media for deepfakes
curl -X POST https://api.deepfakeguard.com/v1/scan \
  -H "X-API-Key: dfg_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/suspicious-image.jpg"}'

# 3. Configure webhooks for real-time alerts
curl -X POST https://api.deepfakeguard.com/v1/account/webhook \
  -H "X-API-Key: dfg_your_api_key_here" \
  -d '{"webhook_url": "https://your-server.com/webhook"}'
```

**[View Full API Documentation](https://deepfakeguard.com/docs)** | **[Get Started Free](https://deepfakeguard.com/landing)**

## 💰 Pricing

| Tier | Scans/Month | Manual Review | Price |
| ------ | ---------- | --------------- | ------- |
| **Free** | 10 | ❌ | $0 |
| **Pro** | 500 | ✅ | $49/mo |
| **Enterprise** | Unlimited | ✅ Dedicated Team | Custom |

## 🎯 Product Overview

This is a **commercial API service** that packages deepfake detection as a paid product for:

- **Discord moderators** protecting gaming and crypto communities
- **Telegram group admins** fighting scams and misinformation
- **NFT marketplaces** verifying profile pictures and digital art
- **Social platforms** needing automated content moderation

### Key Features

- ⚡ **Fast Detection** - Results in < 3 seconds via REST API
- 🔔 **Webhook Notifications** - Real-time alerts to your endpoint
- 👁️ **Manual Review** - Human experts verify flagged content (Pro/Enterprise)
- 🎯 **High Accuracy** - 95%+ detection rate on deepfake media
- 🔒 **Privacy First** - Media analyzed and deleted, never stored

### What Makes This Different

Unlike traditional deepfake detection, DeepfakeGuard combines:

1. **AI detection** for instant results
2. **Manual review workflow** for high-stakes decisions
3. **Webhook integration** for seamless automation
4. **Simple pricing** with generous free tier to prove value

## 📚 Repository Contents

This repository contains the full DeepfakeGuard platform:

- **Landing Page** - Marketing site with signup ([`frontend/pages/landing.js`](frontend/pages/landing.js))
- **API Backend** - Detection service with usage tracking ([`backend/app/main.py`](backend/app/main.py))
- **Admin Dashboard** - Manual review interface ([`frontend/pages/admin/review.js`](frontend/pages/admin/review.js))
- **API Documentation** - Integration guides and examples ([`frontend/pages/docs.js`](frontend/pages/docs.js))
- **Go-to-Market Plan** - Launch strategy and growth roadmap ([`GO_TO_MARKET.md`](GO_TO_MARKET.md))

## 🏗️ Technical Architecture

### Core Components

1. **Scan API** (`/v1/scan`) - Main detection endpoint
   - Accepts image/video URLs
   - Returns deepfake probability score (0-1)
   - Tracks usage against tier limits
   - Triggers webhooks on completion

2. 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (optional)

### Local Development

1. **Clone and setup backend**:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Setup frontend** (separate terminal):

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access the app**:

   - Landing page: <http://localhost:3000/landing>
   - API docs: <http://localhost:3000/docs>
   - Admin review: <http://localhost:3000/admin/review>
   - API endpoint: <http://localhost:8000>

### Environment Variables

Create `.env` in the project root:

```bash
# Optional: Perplexity AI for enhanced threat intelligence
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx

# Optional: Email delivery (SendGrid or Azure Communication Services)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx

# Optional: Stripe for Pro/Enterprise subscriptions
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxx
```

1. **Create and activate a virtual environment**:

   ```bash
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:

   ```bash
   # Copy the example file
   cp ../.env.example ../.env
   
   # Edit .env and add your Perplexity API key
   # Get your API key from: https://www.perplexity.ai/settings/api
   ```

4. **Run the backend**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Perplexity AI Integration

This project uses Perplexity.ai for enhanced threat intelligence and real-time scam research.

#### Getting Your API Key

1. Visit [https://www.perplexity.ai](https://www.perplexity.ai)
2. Sign up or log in to your account
3. Navigate to Settings → API
4. Generate a new API key
5. Add it to your `.env` file:

   ```bash
   PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
   ```

#### Available Perplexity Endpoints

- **`POST /perplexity/analyze-scam`**: Analyze URLs for scam indicators using real-time web search
- **`POST /perplexity/research-wallet`**: Research cryptocurrency wallet addresses for scam history
- **`POST /perplexity/verify-endorsement`**: Verify celebrity crypto endorsement claims
- **`POST /perplexity/analyze-text`**: Analyze text for scam patterns and manipulation tactics

#### Model Selection

Configure which Perplexity model to use in your `.env` file:

```bash
# Fastest and most cost-effective
PERPLEXITY_MODEL=llama-3.1-sonar-small-128k-online

# Higher accuracy
PERPLEXITY_MODEL=llama-3.1-sonar-large-128k-online

# Maximum accuracy (more expensive)
PERPLEXITY_MODEL=llama-3.1-sonar-huge-128k-online
```

### Frontend Setup

1. **Navigate to the frontend**:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📖 Integration Examples

### Discord Bot (Python)

```python
import discord
import httpx

DEEPFAKE_API_KEY = "dfg_your_key"
client = discord.Client()

@client.event
async def on_message(message):
    for attachment in message.attachments:
        if attachment.content_type.startswith('image'):
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
                        f"⚠️ Deepfake detected! Score: {result['score']:.0%}"
                    )
```

### Telegram Bot

```python
import httpx
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

DEEPFAKE_API_KEY = "dfg_your_key"

async def handle_photo(update: Update, context):
    file = await update.message.photo[-1].get_file()
    fileUrl = await file.download_as_bytearray()
    
    async with httpx.AsyncClient() as http:
        response = await http.post(
            'https://api.deepfakeguard.com/v1/scan',
            headers={'X-API-Key': DEEPFAKE_API_KEY},
            json={'url': file.file_path}
        )
        data = response.json()
    
    if data['score'] > 0.6:
        await update.message.delete()
        await update.message.reply_text('⚠️ Deepfake detected and removed!')

bot('message:photo', handle_photo)
```

### Webhook Handler

```javascript
// Express.js webhook endpoint
app.post('/webhook', (req, res) => {
  const { event, data } = req.body;
  
  switch (event) {
    case 'scan.flagged':
      console.log(`🚨 Deepfake detected: ${data.url}`);
      console.log(`Score: ${data.score}, Severity: ${data.severity}`);
      // Auto-moderate or alert admins
      break;
      
    case 'review.completed':
      console.log(`✅ Manual review: ${data.reviewed_verdict}`);
      // Update your database with final verdict
      break;
  }
  
  res.status(200).send('OK');
});
```

## 📁 Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py                    # API endpoints (scan, account, admin)
│   │   └── services/
│   │       ├── api_key_manager.py    # Key generation & usage tracking
│   │       ├── webhook_service.py     # Webhook notifications
│   │       └── perplexity.py          # AI threat intelligence
│   ├── models/
│   │   └── baseline.py               # Deepfake detection model
│   └── config.py                      # Configuration
│
├── frontend/
│   └── pages/
│       ├── landing.js                # Marketing landing page
│       ├── docs.js                   # API documentation
│       ├── admin/
│       │   └── review.js             # Manual review dashboard
│       └── api/
│           └── signup.js             # Account creation endpoint
│
├── GO_TO_MARKET.md                   # Launch strategy & growth plan
└── README.md                          # This file
```

## 🚀 Deployment & Launch

### Quick Deploy to Azure

```bash
azd auth login
azd up
```

See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for complete deployment instructions.

### Go-to-Market Strategy

See [GO_TO_MARKET.md](GO_TO_MARKET.md) for:

- Launch checklist (4-week plan)
- Customer acquisition strategy
- Pricing rationale
- Manual review workflow
- Growth metrics and targets

### Revenue Projections

- **Month 1**: $1,000 MRR (10 Pro customers)
- **Month 3**: $5,000 MRR (50 Pro + 3-5 Enterprise)
- **Month 12**: Scale to $20K+ MRR

## 🎯 Target Customers

1. **Discord Servers** - Gaming, crypto, NFT communities (50K+ members)
2. **Telegram Groups** - Crypto trading, investment groups
3. **NFT Marketplaces** - Profile verification, art authenticity
4. **Social Platforms** - Content moderation at scale

## 💡 Why This Works

1. **Free tier proves value** - 10 scans show the quality immediately
2. **Manual review differentiates** - Not just AI, human verification
3. **Webhooks enable automation** - Seamless bot integration
4. **Simple pricing** - No complex tiers, transparent costs
5. **Solves real pain** - Deepfakes are a growing threat in communities

## 📄 License

See LICENSE file for details.


