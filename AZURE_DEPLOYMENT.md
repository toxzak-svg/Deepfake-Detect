# Azure Deployment Guide for Deepfake-Detect

This guide will walk you through deploying the Deepfake-Detect application to Azure using Azure Developer CLI (azd).

## Prerequisites

### Required Tools

1. **Azure CLI** - [Install](https://aka.ms/install-azure-cli)
   ```bash
   az --version
   ```

2. **Azure Developer CLI (azd)** - [Install](https://aka.ms/install-azd)
   ```bash
   azd version
   ```

3. **Docker** - [Install](https://docs.docker.com/get-docker/)
   ```bash
   docker --version
   ```

### Azure Requirements

- Active Azure subscription
- Permissions to create resources
- Sufficient quota for Container Apps in your region

## Quick Start

### 1. Login to Azure

```bash
# Login to Azure
azd auth login

# Verify your subscription
az account show
```

### 2. Initialize Environment

```bash
# From project root directory
cd c:\dev\projects\Deepfake-Detect-1

# Initialize azd environment (if not already done)
azd init
```

When prompted:
- **Environment name**: Choose a unique name (e.g., `deepfake-detect-dev`)
- **Location**: Select an Azure region (e.g., `eastus`, `westus2`)

### 3. Configure Secrets

Before deploying, you need to add your API keys to Azure Key Vault. First, create a `.azure/<env-name>/.env` file:

```bash
# Create environment variables file
New-Item -ItemType File -Path ".azure\<your-env-name>\.env" -Force
```

Add the following content:

```env
# Perplexity AI API Key (required)
PERPLEXITY_API_KEY=pplx-your-actual-api-key-here

# Application API Keys (comma-separated, or leave as demo-key for testing)
DEEPFAKE_API_KEYS=demo-key
```

### 4. Preview Deployment

Before actually deploying, preview what will be created:

```bash
# Preview infrastructure changes
azd provision --preview
```

Review the output to see:
- Resource Group
- Container Apps Environment
- Container Registry
- Application Insights
- Log Analytics Workspace
- Key Vault
- Managed Identity
- 2 Container Apps (frontend, backend)

### 5. Deploy to Azure

```bash
# Deploy infrastructure and application
azd up
```

This command will:
1. Provision all Azure resources (5-10 minutes)
2. Build Docker images for frontend and backend
3. Push images to Azure Container Registry
4. Deploy containers to Azure Container Apps
5. Configure environment variables and secrets

### 6. Add Secrets to Key Vault

After deployment, manually add the secrets:

```bash
# Get the Key Vault name from azd output
$kvName = azd env get-value AZURE_KEY_VAULT_NAME

# Add Perplexity API key
az keyvault secret set `
  --vault-name $kvName `
  --name "perplexity-api-key" `
  --value "pplx-your-actual-key"

# Add application API keys
az keyvault secret set `
  --vault-name $kvName `
  --name "deepfake-api-keys" `
  --value "your-secure-api-key"
```

### 7. Restart Backend Container App

After adding secrets, restart the backend to pick them up:

```bash
# Redeploy backend service
azd deploy backend
```

### 8. Access Your Application

Get the application URLs:

```bash
# Frontend URL
azd env get-value FRONTEND_URI

# Backend API URL
azd env get-value BACKEND_URI
```

Visit the frontend URL in your browser!

## Testing the Deployment

### Test Backend API

```bash
$backendUrl = azd env get-value BACKEND_URI

# Health check
Invoke-RestMethod -Uri "$backendUrl/health"

# Test detection endpoint
Invoke-RestMethod -Uri "$backendUrl/docs" -Method Get
```

### Test Perplexity Integration

```powershell
$backendUrl = azd env get-value BACKEND_URI

# Test text analysis
$body = @{
    text = "URGENT! Elon Musk is giving away Bitcoin! Send 0.1 BTC to get 1 BTC back!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$backendUrl/perplexity/analyze-text" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Architecture Overview

Your deployed application consists of:

### Azure Resources Created

1. **Resource Group** (`rg-<env-name>`)
   - Contains all resources for this deployment

2. **Container Apps Environment** (`cae-<token>`)
   - Shared environment for both containers
   - Connected to Log Analytics

3. **Azure Container Registry** (`acr<token>`)
   - Stores Docker images
   - SKU: Basic

4. **Backend Container App** (`ca-backend-<token>`)
   - FastAPI with ML models
   - 1 vCPU, 2 GB RAM
   - Auto-scales 1-10 instances
   - Port 8000

5. **Frontend Container App** (`ca-frontend-<token>`)
   - Next.js web UI
   - 0.5 vCPU, 1 GB RAM
   - Auto-scales 0-10 instances
   - Port 3000

6. **Application Insights** (`appi<token>`)
   - Application monitoring
   - Performance metrics
   - Error tracking

7. **Log Analytics Workspace** (`logs<token>`)
   - Centralized logging
   - 30-day retention

8. **Azure Key Vault** (`kv<token>`)
   - Secure secrets storage
   - Stores API keys
   - RBAC enabled

9. **Managed Identity** (`id<token>`)
   - Service identity
   - ACR pull access
   - Key Vault access

## Environment Variables

### Backend Container App

| Variable | Source | Description |
|----------|--------|-------------|
| `PERPLEXITY_API_KEY` | Key Vault Secret | Perplexity AI API key |
| `PERPLEXITY_MODEL` | Config | Model name |
| `PERPLEXITY_TIMEOUT` | Config | API timeout (seconds) |
| `DEEPFAKE_API_KEYS` | Key Vault Secret | Application auth keys |
| `DEEPFAKE_RATE_LIMIT_PER_MIN` | Config | Rate limit |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Telemetry connection |

### Frontend Container App

| Variable | Source | Description |
|----------|--------|-------------|
| `BACKEND_API_URL` | Backend FQDN | Backend service URL |
| `NODE_ENV` | Config | Production environment |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Telemetry connection |

## Monitoring and Logs

### View Application Logs

```bash
# Backend logs
azd monitor --service backend --logs

# Frontend logs
azd monitor --service frontend --logs
```

### Application Insights

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Resource Group
3. Open Application Insights resource
4. Explore:
   - Application Map
   - Performance metrics
   - Failures and exceptions
   - Live metrics stream

### Log Analytics Queries

Example Kusto queries:

```kusto
// All container app logs
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc

// Backend errors
ContainerAppConsoleLogs_CL
| where ContainerAppName_s contains "backend"
| where Log_s contains "ERROR"
| order by TimeGenerated desc

// HTTP requests
AppRequests
| where TimeGenerated > ago(1h)
| summarize count() by ResultCode
```

## Cost Management

### Estimated Monthly Costs

- **Container Apps**: ~$30-50/month
  - Consumption-based pricing
  - Scales to zero when idle
- **Container Registry**: ~$5/month (Basic tier)
- **Application Insights**: ~$10-30/month
  - Based on data ingestion
- **Log Analytics**: ~$5-15/month
- **Key Vault**: ~$1/month

**Total: ~$50-100/month** for development/testing

### Cost Optimization Tips

1. Use consumption plan (scales to zero)
2. Set retention policies on logs
3. Monitor Application Insights data ingestion
4. Delete resources when not in use: `azd down`

## Scaling Configuration

### Manual Scaling

Update scaling rules in [infra/main.bicep](infra/main.bicep):

```bicep
scale: {
  minReplicas: 1
  maxReplicas: 20  // Increase max replicas
  rules: [
    {
      name: 'http-scaling'
      http: {
        metadata: {
          concurrentRequests: '50'
        }
      }
    }
  ]
}
```

Redeploy:
```bash
azd provision
```

### Auto-Scaling Metrics

Container Apps automatically scale based on:
- HTTP request concurrency
- CPU usage
- Memory usage
- Custom metrics (can be configured)

## CI/CD Pipeline

### GitHub Actions Setup

1. Create GitHub secrets:
   ```bash
   # Get values
   azd env get-values
   ```

2. Add to GitHub repository secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_ENV_NAME`

3. Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install azd
        uses: Azure/setup-azd@v0.1.0
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      
      - name: Deploy Application
        run: azd up --no-prompt
        env:
          AZURE_ENV_NAME: ${{ secrets.AZURE_ENV_NAME }}
          AZURE_LOCATION: eastus
```

## Troubleshooting

### Common Issues

#### 1. "Error: Cannot find image"

If containers fail to start with image pull errors:

```bash
# Check managed identity has AcrPull role
az role assignment list --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.ContainerRegistry/registries/<registry-name>
```

#### 2. "Secrets not found"

Ensure secrets are added to Key Vault:

```bash
az keyvault secret list --vault-name <vault-name>
```

#### 3. "Application crashes on startup"

Check container logs:

```bash
# Azure Portal > Container App > Log Stream
# or
az containerapp logs show -n <app-name> -g <resource-group>
```

#### 4. "Can't connect to backend"

Verify backend URL in frontend environment:

```bash
# Check frontend configuration
az containerapp show -n ca-frontend-<token> -g <rg-name> --query "properties.template.containers[0].env"
```

### Getting Help

- Check logs: `azd monitor --logs`
- View deployment: `az deployment group list -g <rg-name>`
- Portal diagnostics: [Azure Portal](https://portal.azure.com)

## Cleanup

### Delete All Resources

```bash
# Remove all Azure resources
azd down

# Optional: Remove local environment
azd env remove <env-name>
```

This deletes:
- Resource Group and all resources
- Container images in registry
- Logs and metrics data

**Note**: Key Vault has soft-delete enabled. Purge manually if needed:

```bash
az keyvault purge --name <vault-name>
```

## Next Steps

1. **Custom Domain**: Configure custom domain for Container Apps
2. **SSL Certificate**: Add managed certificate
3. **Authentication**: Enable Azure AD authentication
4. **API Management**: Add Azure API Management for rate limiting
5. **CDN**: Add Azure CDN for frontend assets
6. **Database**: Add Azure Cosmos DB for persistent storage
7. **Redis Cache**: Add Azure Cache for Redis for caching

## Support

- Azure Documentation: [docs.microsoft.com/azure](https://docs.microsoft.com/azure)
- Azure Developer CLI: [aka.ms/azd](https://aka.ms/azd)
- Container Apps: [aka.ms/containerapps](https://aka.ms/containerapps)
- Project Issues: GitHub Issues

---

**Deployment completed successfully!** 🎉

Your Deepfake-Detect application is now running on Azure!
