# Pre-Deployment Checklist

Use this checklist before deploying to Azure to ensure everything is ready.

## ✅ Prerequisites

### Tools Installed
- [ ] Azure CLI (`az --version` shows version ≥ 2.50.0)
- [ ] Azure Developer CLI (`azd version` shows version ≥ 1.5.0)
- [ ] Docker (`docker --version` shows version ≥ 20.10.0)
- [ ] Git (for version control)

### Azure Account
- [ ] Active Azure subscription
- [ ] Subscription has sufficient quota for Container Apps
- [ ] Permissions to create resources in subscription
- [ ] Subscription is selected: `az account show`

### API Keys Ready
- [ ] Perplexity API key obtained from [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
- [ ] Application API keys generated (or use `demo-key` for testing)

## ✅ Local Setup

### Project Files
- [ ] All files committed to Git
- [ ] `.env.example` file exists
- [ ] No `.env` file committed (should be in `.gitignore`)

### Docker Test (Optional but Recommended)
- [ ] Backend builds: `docker build -t backend-test ./backend`
- [ ] Frontend builds: `docker build -t frontend-test ./frontend`
- [ ] Backend runs: `docker run -p 8000:8000 backend-test`
- [ ] Frontend runs: `docker run -p 3000:3000 frontend-test`

## ✅ Azure Configuration

### Login
- [ ] Logged in to Azure: `azd auth login`
- [ ] Correct subscription selected
- [ ] Tenant verified (if using multiple tenants)

### Environment Setup
- [ ] Environment name chosen (lowercase, no spaces)
- [ ] Azure region selected (e.g., `eastus`, `westus2`)
- [ ] Region supports Container Apps

### Secrets Prepared
- [ ] `.azure/<env-name>/.env` file created
- [ ] `PERPLEXITY_API_KEY` value added
- [ ] `DEEPFAKE_API_KEYS` value added
- [ ] No secrets committed to Git

## ✅ Infrastructure Review

### Bicep Files
- [ ] `infra/main.bicep` exists
- [ ] `infra/main.parameters.json` exists
- [ ] Core modules exist in `infra/core/`
- [ ] No Bicep errors: `az bicep build -f infra/main.bicep`

### Configuration
- [ ] `azure.yaml` exists
- [ ] Services defined: `backend`, `frontend`
- [ ] Docker paths correct

## ✅ Deployment Preview

### Before Deploying
- [ ] Preview deployment: `azd provision --preview`
- [ ] Review resources to be created
- [ ] Confirm resource names acceptable
- [ ] Estimated costs reviewed (~$50-100/month)

### Expected Resources
- [ ] Resource Group
- [ ] Managed Identity
- [ ] Container Registry
- [ ] Container Apps Environment
- [ ] 2 Container Apps (backend, frontend)
- [ ] Application Insights
- [ ] Log Analytics Workspace
- [ ] Key Vault

## ✅ Deployment

### Initial Deployment
- [ ] Run `azd up`
- [ ] Wait for completion (5-10 minutes)
- [ ] No errors in deployment output
- [ ] Resource URLs captured

### Post-Deployment
- [ ] Secrets added to Key Vault
- [ ] Backend redeployed: `azd deploy backend`
- [ ] Application URLs obtained
- [ ] Frontend accessible via browser
- [ ] Backend health check returns OK

## ✅ Testing

### Smoke Tests
- [ ] Frontend URL loads
- [ ] Backend `/health` endpoint returns `{"status": "ok"}`
- [ ] Backend `/docs` shows API documentation
- [ ] Perplexity endpoints return responses (not errors)

### Functional Tests
```bash
# Test backend health
$backendUrl = azd env get-value BACKEND_URI
Invoke-RestMethod -Uri "$backendUrl/health"

# Test Perplexity integration
$body = @{text = "Test"} | ConvertTo-Json
Invoke-RestMethod -Uri "$backendUrl/perplexity/analyze-text" -Method Post -ContentType "application/json" -Body $body
```

- [ ] Health check passes
- [ ] Perplexity integration works
- [ ] No 500 errors
- [ ] Response times acceptable

## ✅ Monitoring

### Application Insights
- [ ] Application Insights resource exists
- [ ] Telemetry flowing to App Insights
- [ ] No startup errors in logs
- [ ] Request tracking working

### Logs
- [ ] Can view logs: `azd monitor --logs`
- [ ] Backend logs show startup messages
- [ ] Frontend logs show Next.js server running
- [ ] No error-level logs

## ✅ Security

### Secrets
- [ ] No secrets in source code
- [ ] All secrets in Key Vault
- [ ] Managed Identity has Key Vault access
- [ ] No hardcoded API keys in environment variables

### Access Control
- [ ] Managed Identity has AcrPull role
- [ ] Purge protection enabled on Key Vault
- [ ] Anonymous pull disabled on Container Registry
- [ ] HTTPS-only ingress

## ✅ Documentation

### For Team
- [ ] Deployment guide shared: `AZURE_DEPLOYMENT.md`
- [ ] Quick reference available: `AZURE_QUICKSTART.md`
- [ ] Environment documented
- [ ] Resource naming conventions documented

## ✅ Optional Enhancements

### Future Improvements
- [ ] Custom domain configured
- [ ] SSL certificate added
- [ ] CI/CD pipeline set up
- [ ] Scaling rules tuned
- [ ] Cost alerts configured
- [ ] Backup strategy implemented

## Troubleshooting

If any checks fail:

| Issue | Solution |
|-------|----------|
| Tool not installed | See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) prerequisites section |
| Bicep errors | Run `az bicep build -f infra/main.bicep` to see details |
| Deployment failed | Check logs with `azd monitor --logs` |
| Can't access app | Verify ingress settings in Azure Portal |
| Secrets not working | Ensure Key Vault access and restart app |

## Ready to Deploy?

Once all checks pass:

```bash
# Deploy to Azure
azd up

# Monitor deployment
# Watch for completion message and URLs
```

---

**Good luck with your deployment!** 🚀

For detailed instructions, see [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
