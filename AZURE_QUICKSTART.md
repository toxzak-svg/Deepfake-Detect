# Azure Deployment Quick Reference

## Prerequisites Checklist

- [ ] Azure CLI installed (`az --version`)
- [ ] Azure Developer CLI installed (`azd version`)
- [ ] Docker installed (`docker --version`)
- [ ] Active Azure subscription
- [ ] Perplexity API key ready

## Deployment Steps

```bash
# 1. Login
azd auth login

# 2. Initialize (first time only)
azd init

# 3. Deploy
azd up
```

## After Deployment

```bash
# Get Key Vault name
$kvName = azd env get-value AZURE_KEY_VAULT_NAME

# Add secrets
az keyvault secret set --vault-name $kvName --name "perplexity-api-key" --value "<your-key>"
az keyvault secret set --vault-name $kvName --name "deepfake-api-keys" --value "<your-keys>"

# Restart backend
azd deploy backend

# Get URLs
azd env get-value FRONTEND_URI
azd env get-value BACKEND_URI
```

## Common Commands

| Command | Description |
|---------|-------------|
| `azd up` | Deploy infrastructure and code |
| `azd provision` | Deploy infrastructure only |
| `azd deploy` | Deploy application code only |
| `azd monitor --logs` | View application logs |
| `azd down` | Delete all Azure resources |
| `azd env list` | List all environments |
| `azd env get-values` | Show all environment values |

## Monitoring

```bash
# View logs
azd monitor --service backend --logs
azd monitor --service frontend --logs

# Get Application Insights name
azd env get-value APPLICATIONINSIGHTS_NAME
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Cannot pull image" | Check managed identity has AcrPull role |
| "Secret not found" | Add secrets to Key Vault, restart app |
| "App won't start" | Check logs: `azd monitor --logs` |
| "Deployment failed" | Run `azd provision --preview` first |

## Resource URLs

After deployment, find resources in Azure Portal:

1. Go to [portal.azure.com](https://portal.azure.com)
2. Search for resource group: `rg-<your-env-name>`
3. View all deployed resources

## Clean Up

```bash
# Remove everything
azd down

# Confirm deletion
# Type 'yes' when prompted
```

## Environment Variables

Set in `.azure/<env-name>/.env`:

```env
PERPLEXITY_API_KEY=pplx-xxxxx
DEEPFAKE_API_KEYS=your-keys
```

## Cost Estimate

- Container Apps: ~$30-50/month
- Supporting services: ~$20-50/month
- **Total: ~$50-100/month**

Scale to zero when idle to save costs!

## Support

- Full guide: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
- Deployment plan: [.azure/plan.copilotmd](.azure/plan.copilotmd)
- Summary: [.azure/summary.copilotmd](.azure/summary.copilotmd)

---

**Need help?** Check the full deployment guide or Azure docs.
