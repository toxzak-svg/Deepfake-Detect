// Azure Container Registry for storing Docker images

@description('Primary location for all resources')
param location string = resourceGroup().location

@description('Tags for all resources')
param tags object = {}

@description('Unique resource token for naming')
param resourceToken string

// ============================================================================
// CONTAINER REGISTRY
// ============================================================================

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: 'acr${resourceToken}'
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false // Security best practice
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
    zoneRedundancy: 'Disabled'
  }
}

// ============================================================================
// OUTPUTS
// ============================================================================

output registryLoginServer string = containerRegistry.properties.loginServer
output registryName string = containerRegistry.name
output registryId string = containerRegistry.id
output registryEndpoint string = 'https://${containerRegistry.properties.loginServer}'
