// Main Bicep file for Deepfake-Detect Azure deployment
// This file orchestrates all Azure resources needed for the application

targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the environment for resource naming')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string = resourceGroup().location

@description('Id of the user or app to assign application roles')
param principalId string = ''

// Generate unique token for resource naming (max 32 chars total)
var resourceToken = uniqueString(subscription().id, resourceGroup().id, location, environmentName)

// Tags
var tags = {
  'azd-env-name': environmentName
}

// ============================================================================
// MANAGED IDENTITY (Required by AZD rules - must exist before other resources)
// ============================================================================

resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id${resourceToken}'
  location: location
  tags: tags
}

// ============================================================================
// MONITORING - Log Analytics and Application Insights
// ============================================================================

module monitoring './core/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    tags: tags
    resourceToken: resourceToken
  }
}

// ============================================================================
// CONTAINER REGISTRY
// ============================================================================

module containerRegistry './core/registry.bicep' = {
  name: 'registry'
  params: {
    location: location
    tags: tags
    resourceToken: resourceToken
  }
}

// MANDATORY: AcrPull role assignment for managed identity
// This must be defined BEFORE any container apps
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: resourceGroup()
  name: guid(resourceGroup().id, userAssignedIdentity.id, 'AcrPull')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // AcrPull role
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ============================================================================
// KEY VAULT - Secure secrets storage
// ============================================================================

module keyVault './core/security.bicep' = {
  name: 'security'
  params: {
    location: location
    tags: tags
    resourceToken: resourceToken
    principalId: principalId
    userAssignedIdentityPrincipalId: userAssignedIdentity.properties.principalId
  }
}

// ============================================================================
// CONTAINER APPS ENVIRONMENT
// ============================================================================

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'cae${resourceToken}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: monitoring.outputs.logAnalyticsWorkspaceId
        sharedKey: monitoring.outputs.logAnalyticsWorkspacePrimarySharedKey
      }
    }
  }
}

// ============================================================================
// BACKEND CONTAINER APP (FastAPI with ML models)
// ============================================================================

resource backendContainerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'ca-backend-${resourceToken}'
  location: location
  tags: union(tags, {
    'azd-service-name': 'backend'
  })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    environmentId: containerAppsEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto'
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: false
        }
      }
      registries: [
        {
          server: containerRegistry.outputs.registryLoginServer
          identity: userAssignedIdentity.id
        }
      ]
      secrets: [
        {
          name: 'perplexity-api-key'
          keyVaultUrl: '${keyVault.outputs.keyVaultEndpoint}secrets/perplexity-api-key'
          identity: userAssignedIdentity.id
        }
        {
          name: 'deepfake-api-keys'
          keyVaultUrl: '${keyVault.outputs.keyVaultEndpoint}secrets/deepfake-api-keys'
          identity: userAssignedIdentity.id
        }
        {
          name: 'appinsights-connection-string'
          value: monitoring.outputs.applicationInsightsConnectionString
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            {
              name: 'PERPLEXITY_API_KEY'
              secretRef: 'perplexity-api-key'
            }
            {
              name: 'PERPLEXITY_MODEL'
              value: 'llama-3.1-sonar-small-128k-online'
            }
            {
              name: 'PERPLEXITY_TIMEOUT'
              value: '30'
            }
            {
              name: 'DEEPFAKE_API_KEYS'
              secretRef: 'deepfake-api-keys'
            }
            {
              name: 'DEEPFAKE_RATE_LIMIT_PER_MIN'
              value: '60'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'appinsights-connection-string'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
  dependsOn: [
    acrPullRoleAssignment
  ]
}

// ============================================================================
// FRONTEND CONTAINER APP (Next.js)
// ============================================================================

resource frontendContainerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'ca-frontend-${resourceToken}'
  location: location
  tags: union(tags, {
    'azd-service-name': 'frontend'
  })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    environmentId: containerAppsEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 3000
        transport: 'auto'
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST']
          allowedHeaders: ['*']
          allowCredentials: false
        }
      }
      registries: [
        {
          server: containerRegistry.outputs.registryLoginServer
          identity: userAssignedIdentity.id
        }
      ]
      secrets: [
        {
          name: 'appinsights-connection-string'
          value: monitoring.outputs.applicationInsightsConnectionString
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'BACKEND_API_URL'
              value: 'https://${backendContainerApp.properties.configuration.ingress.fqdn}'
            }
            {
              name: 'NODE_ENV'
              value: 'production'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'appinsights-connection-string'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
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
    }
  }
  dependsOn: [
    acrPullRoleAssignment
  ]
}

// ============================================================================
// OUTPUTS (Required by AZD)
// ============================================================================

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output RESOURCE_GROUP_ID string = resourceGroup().id

// Container Registry
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.registryEndpoint
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.registryName

// Container Apps
output BACKEND_URI string = 'https://${backendContainerApp.properties.configuration.ingress.fqdn}'
output FRONTEND_URI string = 'https://${frontendContainerApp.properties.configuration.ingress.fqdn}'

// Monitoring
output APPLICATIONINSIGHTS_CONNECTION_STRING string = monitoring.outputs.applicationInsightsConnectionString
output APPLICATIONINSIGHTS_NAME string = monitoring.outputs.applicationInsightsName

// Security
output AZURE_KEY_VAULT_NAME string = keyVault.outputs.keyVaultName
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.keyVaultEndpoint

// Managed Identity
output MANAGED_IDENTITY_CLIENT_ID string = userAssignedIdentity.properties.clientId
output MANAGED_IDENTITY_NAME string = userAssignedIdentity.name
