# Deepfake-Detect
Next.js app that detects and flags deepfake crypto giveaways.

## Design & Research

This repository contains a prototype Next.js app for detecting and flagging deepfake crypto airdrops and giveaway scams. A concise research summary and recommended architecture are included in the companion design document: `DEEPFAKE_DETECT_DESIGN.md`.

See `DEEPFAKE_DETECT_DESIGN.md` for the full specification, detection signals, MVP roadmap, risks, and suggested tech stack.

## Features

- **Video & Image Analysis**: Detect deepfake artifacts in media using baseline ML models
- **URL Scanning**: Analyze URLs for crypto scam patterns and heuristics
- **Text Analysis**: Identify giveaway keywords and urgency tactics
- **AI-Powered Threat Intelligence**: Real-time scam research using Perplexity.ai
- **Wallet Research**: Investigate cryptocurrency addresses for scam history
- **Celebrity Endorsement Verification**: Fact-check crypto endorsement claims
- **Browser Extension**: Flag suspicious content directly in your browser

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (optional)

### Backend Setup

1. **Clone the repository and navigate to the backend**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy the example file
   cp ../.env.example ../.env
   
   # Edit .env and add your Perplexity API key
   # Get your API key from: https://www.perplexity.ai/settings/api
   ```

5. **Run the backend**:
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
   ```
   PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
   ```

#### Available Perplexity Endpoints

- **`POST /perplexity/analyze-scam`**: Analyze URLs for scam indicators using real-time web search
- **`POST /perplexity/research-wallet`**: Research cryptocurrency wallet addresses for scam history
- **`POST /perplexity/verify-endorsement`**: Verify celebrity crypto endorsement claims
- **`POST /perplexity/analyze-text`**: Analyze text for scam patterns and manipulation tactics

#### Model Selection

Configure which Perplexity model to use in your `.env` file:

```
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
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### Docker Setup (Optional)

Run both frontend and backend with Docker Compose:

```bash
docker-compose up --build
```

## API Documentation

Once the backend is running, visit:
- API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

### Example API Calls

#### Detect Deepfake
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: demo-key" \
  -d '{"url": "https://example.com/image.jpg"}'
```

#### Analyze Scam with Perplexity
```bash
curl -X POST "http://localhost:8000/perplexity/analyze-scam" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://suspicious-site.com",
    "description": "Claim about Elon Musk crypto giveaway"
  }'
```

#### Research Wallet Address
```bash
curl -X POST "http://localhost:8000/perplexity/research-wallet" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"}'
```

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # API endpoints
│   │   └── services/    # Service modules
│   │       └── perplexity.py  # Perplexity AI integration
│   ├── models/          # ML models
│   ├── scripts/         # Utility scripts
│   └── config.py        # Configuration
├── frontend/            # Next.js frontend
├── extension/           # Browser extension
└── docs/                # Documentation
```

## Contributing

See the design document for development roadmap and guidelines.

## License

See LICENSE file for details.

