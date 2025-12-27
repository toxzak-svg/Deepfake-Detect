# Perplexity AI Setup Quick Start

This guide will help you get the Perplexity AI integration up and running in 5 minutes.

## Step 1: Get Your API Key

1. Go to [https://www.perplexity.ai](https://www.perplexity.ai)
2. Sign up or log in
3. Navigate to Settings → API
4. Click "Generate API Key"
5. Copy your API key (starts with `pplx-`)

## Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
PERPLEXITY_API_KEY=pplx-your-actual-key-here
```

## Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 4: Start the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Step 5: Test the Integration

Open a new terminal and test an endpoint:

```bash
curl -X POST "http://localhost:8000/perplexity/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "URGENT! Elon Musk is giving away Bitcoin! Send 0.1 BTC to get 1 BTC back!"
  }'
```

You should see a detailed analysis of the scam patterns in the text.

## Available Endpoints

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

### Key Endpoints:

- **`POST /perplexity/analyze-scam`** - Analyze URLs for scam indicators
- **`POST /perplexity/research-wallet`** - Research wallet addresses
- **`POST /perplexity/verify-endorsement`** - Verify celebrity endorsements
- **`POST /perplexity/analyze-text`** - Analyze text for scam patterns

## Example Usage

### Analyze a Suspicious URL

```bash
curl -X POST "http://localhost:8000/perplexity/analyze-scam" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://suspicious-crypto-site.com",
    "description": "Claims to be an official Bitcoin giveaway"
  }'
```

### Research a Wallet Address

```bash
curl -X POST "http://localhost:8000/perplexity/research-wallet" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
  }'
```

### Verify Celebrity Endorsement

```bash
curl -X POST "http://localhost:8000/perplexity/verify-endorsement" \
  -H "Content-Type: application/json" \
  -d '{
    "celebrity_name": "Elon Musk",
    "crypto_project": "Bitcoin Doubler",
    "claim": "Send Bitcoin to this address and get double back"
  }'
```

## Troubleshooting

### Error: "Perplexity service not configured"

Make sure:
1. `.env` file exists in the project root
2. `PERPLEXITY_API_KEY` is set in `.env`
3. You restarted the backend after adding the key

### Error: "Invalid API key"

1. Check that your API key starts with `pplx-`
2. Verify the key is active at [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
3. Make sure there are no extra spaces in the `.env` file

### Slow Response Times

1. Try using the smaller model:
   ```
   PERPLEXITY_MODEL=llama-3.1-sonar-small-128k-online
   ```
2. Increase timeout in `.env`:
   ```
   PERPLEXITY_TIMEOUT=60
   ```

## Cost Management

Perplexity charges per API request. To optimize costs:

1. Use the smallest model for routine checks
2. Cache responses for frequently-checked URLs
3. Use Perplexity only for high-risk items (after heuristic filtering)
4. Monitor usage at [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)

## Next Steps

- Read the full integration guide: `docs/PERPLEXITY_INTEGRATION.md`
- Check API documentation: `http://localhost:8000/docs`
- Run tests: `pytest backend/tests/test_perplexity.py -v`
- Integrate with frontend UI

## Support

- Perplexity Docs: [https://docs.perplexity.ai](https://docs.perplexity.ai)
- Project Issues: [https://github.com/toxzak-svg/Deepfake-Detect/issues](https://github.com/toxzak-svg/Deepfake-Detect/issues)

Happy scam hunting! 🔍🛡️
