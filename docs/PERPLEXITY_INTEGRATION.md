# Perplexity AI Integration Guide

## Overview

The Perplexity AI integration enhances the Deepfake-Detect system with real-time web research capabilities for threat intelligence, scam verification, and content analysis.

## Why Perplexity?

- **Real-time web search**: Access up-to-date information about scams and threats
- **Fact-checking**: Verify celebrity endorsement claims with credible sources
- **Threat intelligence**: Research wallet addresses and domain histories
- **Pattern detection**: Identify manipulation tactics in text content

## Quick Start

1. Get your API key from [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Add it to `.env`:
   ```
   PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
   ```
3. Restart the backend server

## Available Endpoints

### 1. Analyze Scam Indicators
**Endpoint**: `POST /perplexity/analyze-scam`

Analyzes a URL for crypto scam indicators using real-time web search.

**Request**:
```json
{
  "url": "https://suspicious-site.com",
  "description": "Claims Elon Musk is giving away Bitcoin",
  "additional_context": "Posted on Twitter with 10k shares"
}
```

**Response**:
```json
{
  "analysis": "Detailed analysis with risk assessment...",
  "url": "https://suspicious-site.com",
  "model": "llama-3.1-sonar-small-128k-online",
  "success": true
}
```

**Use Cases**:
- Verify if a URL has known scam reports
- Check domain registration history
- Find similar phishing attempts
- Identify deepfake or celebrity impersonation

### 2. Research Wallet Address
**Endpoint**: `POST /perplexity/research-wallet`

Researches a cryptocurrency wallet address for scam history.

**Request**:
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
}
```

**Response**:
```json
{
  "research": "Analysis of wallet history and reputation...",
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "model": "llama-3.1-sonar-small-128k-online",
  "success": true
}
```

**Use Cases**:
- Check if a wallet is associated with known scams
- Review transaction patterns
- Find reports on blockchain explorers
- Assess risk level before interaction

### 3. Verify Celebrity Endorsement
**Endpoint**: `POST /perplexity/verify-endorsement`

Verifies claims about celebrity crypto endorsements.

**Request**:
```json
{
  "celebrity_name": "Elon Musk",
  "crypto_project": "Bitcoin Giveaway",
  "claim": "Doubling all Bitcoin sent to this address"
}
```

**Response**:
```json
{
  "verification": "Fact-check results with sources...",
  "celebrity": "Elon Musk",
  "project": "Bitcoin Giveaway",
  "model": "llama-3.1-sonar-small-128k-online",
  "success": true
}
```

**Use Cases**:
- Detect fake celebrity endorsements
- Verify official announcements
- Check verified social media
- Find scam warnings

### 4. Analyze Text for Scam Patterns
**Endpoint**: `POST /perplexity/analyze-text`

Analyzes text content for common scam patterns and manipulation tactics.

**Request**:
```json
{
  "text": "🚨 URGENT! Elon Musk is giving away 5000 BTC! Send 0.1 BTC to receive 1 BTC back! Only 24 hours left! 🚀"
}
```

**Response**:
```json
{
  "analysis": "Identified scam patterns and risk level...",
  "text_length": 113,
  "model": "llama-3.1-sonar-small-128k-online",
  "success": true
}
```

**Use Cases**:
- Identify urgency tactics
- Detect guaranteed return promises
- Find impersonation language
- Spot giveaway/airdrop scams

## Model Options

Configure in `.env`:

### Small (Recommended for Development)
```
PERPLEXITY_MODEL=llama-3.1-sonar-small-128k-online
```
- Fastest response time
- Most cost-effective
- Good for high-volume requests

### Large (Balanced)
```
PERPLEXITY_MODEL=llama-3.1-sonar-large-128k-online
```
- Higher accuracy
- Moderate cost
- Better for complex analysis

### Huge (Maximum Accuracy)
```
PERPLEXITY_MODEL=llama-3.1-sonar-huge-128k-online
```
- Best accuracy
- Higher cost
- Use for critical verifications

## Integration with Existing Detection

### Combined Approach

The Perplexity integration works alongside the existing detection pipeline:

1. **Heuristic Analysis** (Fast, Free)
   - Keyword matching
   - URL pattern checks
   - Basic text analysis

2. **ML Model Detection** (Medium, Local)
   - Image/video deepfake detection
   - Frame-by-frame analysis
   - Baseline classifier

3. **Perplexity AI Research** (Comprehensive, API Cost)
   - Real-time web search
   - Fact verification
   - Threat intelligence

### Suggested Workflow

```python
# 1. Run fast heuristics first
basic_score = detect_basic_patterns(url)

# 2. If suspicious, run ML models
if basic_score > 0.3:
    ml_score = run_deepfake_detector(url)

# 3. If still suspicious, use Perplexity for verification
if ml_score > 0.5:
    perplexity_result = await analyze_with_perplexity(url)
```

## Cost Optimization

### Best Practices

1. **Cache Results**: Store Perplexity responses for frequently-checked URLs
2. **Rate Limiting**: Use Perplexity only for high-risk items
3. **Batch Processing**: Group similar queries when possible
4. **Model Selection**: Use smaller models for routine checks

### Example Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_scam_analysis(url: str):
    return perplexity_service.analyze_scam_indicators(url)
```

## Error Handling

All endpoints return `success: false` on errors:

```json
{
  "analysis": null,
  "url": "https://example.com",
  "error": "API rate limit exceeded",
  "success": false
}
```

The backend will return HTTP 503 if Perplexity is not configured:

```json
{
  "detail": "Perplexity service not configured. Set PERPLEXITY_API_KEY environment variable."
}
```

## Security Considerations

1. **API Key Protection**: Never commit `.env` file to version control
2. **Rate Limiting**: Monitor API usage to prevent abuse
3. **Input Validation**: All inputs are validated before sending to Perplexity
4. **Content Filtering**: Perplexity responses are from web search; validate before displaying

## Testing

Test the integration with curl:

```bash
# Health check
curl http://localhost:8000/health

# Test scam analysis
curl -X POST "http://localhost:8000/perplexity/analyze-scam" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "description": "Test analysis"
  }'
```

## Support

- Perplexity Documentation: [https://docs.perplexity.ai](https://docs.perplexity.ai)
- Project Issues: [GitHub Issues](https://github.com/toxzak-svg/Deepfake-Detect/issues)
- API Pricing: [https://www.perplexity.ai/pricing](https://www.perplexity.ai/pricing)

## Future Enhancements

- [ ] Response caching with Redis
- [ ] Batch analysis endpoint
- [ ] Webhook notifications for high-risk findings
- [ ] Integration with frontend UI
- [ ] Automated periodic rescanning of flagged content
