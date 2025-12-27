# DeepfakeGuard - Quick Setup Guide

## 🚀 Get Your API Live in 30 Minutes

This guide walks you through deploying DeepfakeGuard and getting your first customer.

## Step 1: Local Testing (5 minutes)

### Start the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Start the Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

### Test it Works
1. Open http://localhost:3000/landing
2. Enter your email to get an API key
3. Check the terminal - you'll see the API key printed
4. Open http://localhost:3000/docs to see the API documentation

## Step 2: Deploy to Azure (15 minutes)

### Install Prerequisites
```bash
# Install Azure CLI
# Windows (PowerShell): 
winget install Microsoft.AzureCLI

# macOS:
brew install azure-cli

# Install Azure Developer CLI
# Windows:
winget install Microsoft.Azd

# macOS:
brew install azd
```

### Deploy
```bash
# Login to Azure
az login
azd auth login

# Initialize and deploy
azd init
azd up

# Follow the prompts:
# - Choose a name (e.g., "deepfakeguard")
# - Select subscription
# - Select region (eastus, westus2, etc.)
```

This will deploy:
- ✅ FastAPI backend to Azure Container Apps
- ✅ Next.js frontend to Azure Container Apps
- ✅ Container Registry for images
- ✅ Application Insights for monitoring

**Cost**: ~$50-100/month for development workload

### Get Your URLs
After deployment, note these URLs:
```bash
Backend: https://deepfakeguard-api.YOUR_REGION.azurecontainerapps.io
Frontend: https://deepfakeguard.YOUR_REGION.azurecontainerapps.io
```

## Step 3: Production Setup (10 minutes)

### A. Set Up Email Delivery (SendGrid - Free Tier)

1. **Create SendGrid Account**:
   - Go to https://sendgrid.com/free/
   - Sign up (Free: 100 emails/day)

2. **Get API Key**:
   - Dashboard → Settings → API Keys
   - Create API Key with "Mail Send" permissions

3. **Add to Azure**:
   ```bash
   az webapp config appsettings set \
     --name deepfakeguard-api \
     --settings SENDGRID_API_KEY=SG.xxxxxx
   ```

### B. Set Up Domain (Optional but Recommended)

1. **Buy domain** (Namecheap, GoDaddy, etc.): ~$10/year
2. **Add CNAME records**:
   ```
   api.deepfakeguard.com → your-backend.azurecontainerapps.io
   www.deepfakeguard.com → your-frontend.azurecontainerapps.io
   ```

### C. Set Up Stripe for Payments

1. **Create Stripe Account**: https://dashboard.stripe.com/register
2. **Get API Keys**: Dashboard → Developers → API Keys
3. **Add to Azure**:
   ```bash
   az webapp config appsettings set \
     --name deepfakeguard-api \
     --settings STRIPE_SECRET_KEY=sk_live_xxxxx
   ```

### D. Configure Production Database (Azure Cosmos DB)

```bash
# Create Cosmos DB account
az cosmosdb create \
  --name deepfakeguard-db \
  --resource-group rg-deepfakeguard \
  --default-consistency-level Session

# Create database
az cosmosdb sql database create \
  --account-name deepfakeguard-db \
  --resource-group rg-deepfakeguard \
  --name deepfakeguard

# Create containers
az cosmosdb sql container create \
  --account-name deepfakeguard-db \
  --database-name deepfakeguard \
  --name users \
  --partition-key-path "/email"

az cosmosdb sql container create \
  --account-name deepfakeguard-db \
  --database-name deepfakeguard \
  --name scans \
  --partition-key-path "/api_key"
```

**Cost**: ~$25/month (400 RU/s)

## Step 4: Get Your First Customer (varies)

### A. Test the Signup Flow

1. Go to your landing page
2. Enter your email
3. Check inbox for API key (if SendGrid configured)
4. Test the API:
   ```bash
   curl -X POST https://api.deepfakeguard.com/v1/scan \
     -H "X-API-Key: dfg_your_test_key" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/test.jpg"}'
   ```

### B. Reach Out to Potential Customers

**Discord Server Owners:**
```
Subject: Free tool to stop deepfake scams in your Discord

Hi [Name],

I noticed your server has [X] members. With AI deepfakes on the rise, 
I built a free API to help moderators detect manipulated images/videos.

Free tier: 10 scans
Pro tier: $49/month for 500 scans + manual review

Would you be interested in trying it? Happy to set up a custom bot for you.

[Your Name]
DeepfakeGuard.com
```

**Telegram Group Admins:**
```
Hi! I built DeepfakeGuard - an API to detect deepfake scams in Telegram groups.

Perfect for crypto/NFT communities. Free tier: 10 scans.
Takes 5 minutes to integrate: https://deepfakeguard.com/docs

Let me know if you'd like help setting it up!
```

### C. Post on Communities

- **Product Hunt**: Launch and get feedback
- **Reddit**: r/Discord, r/Telegram, r/NFT
- **Twitter**: Tag crypto/NFT influencers
- **Discord/Telegram**: Join moderation communities

## Step 5: Monitor & Iterate

### Check Logs
```bash
# Backend logs
az containerapp logs show \
  --name deepfakeguard-api \
  --resource-group rg-deepfakeguard \
  --follow

# Frontend logs
az containerapp logs show \
  --name deepfakeguard-frontend \
  --resource-group rg-deepfakeguard \
  --follow
```

### Monitor Usage
- Application Insights: Azure Portal → Your Resource Group → Application Insights
- Track:
  - Signups per day
  - API calls per customer
  - Conversion rate (Free → Pro)
  - Webhook delivery success rate

### Key Metrics to Watch

**Week 1:**
- ✅ 10+ signups
- ✅ 1+ Pro conversion
- ✅ < 3s scan latency

**Month 1:**
- ✅ 100+ signups
- ✅ 10+ Pro customers ($490 MRR)
- ✅ 1+ Enterprise deal

## Troubleshooting

### API Key Not Showing
- Check backend logs for signup errors
- Verify SendGrid API key is set
- Test email delivery manually

### Scans Failing
- Check model is loaded: Logs should show "BaselineDetector initialized"
- Verify image URLs are publicly accessible
- Check Application Insights for errors

### Webhooks Not Firing
- Verify customer provided valid HTTPS endpoint
- Check webhook service logs
- Test with https://webhook.site

## Next Steps

1. ✅ Deploy to Azure
2. ✅ Configure SendGrid
3. ✅ Set up Stripe
4. ⏳ Get first 10 signups
5. ⏳ Convert 1st Pro customer
6. ⏳ Build manual review workflow
7. ⏳ Hire first reviewer
8. ⏳ Scale to $5K MRR

## Need Help?

- **Documentation**: [GO_TO_MARKET.md](GO_TO_MARKET.md)
- **API Docs**: https://deepfakeguard.com/docs
- **Azure Support**: https://azure.microsoft.com/support/

**Let's ship it! 🚀**
