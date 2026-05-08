import * as app from "@pulumi/azure-native/app";
import * as containerregistry from "@pulumi/azure-native/containerregistry";
import * as documentdb from "@pulumi/azure-native/documentdb";
import * as keyvault from "@pulumi/azure-native/keyvault";
import * as managedidentity from "@pulumi/azure-native/managedidentity";
import * as operationalinsights from "@pulumi/azure-native/operationalinsights";
import * as pulumi from "@pulumi/pulumi";
import * as resources from "@pulumi/azure-native/resources";
import * as servicebus from "@pulumi/azure-native/servicebus";
import * as storage from "@pulumi/azure-native/storage";

const config = new pulumi.Config("accb");
const environment = config.require("environment");
const stackName = pulumi.getStack();
const location = config.get("location") ?? "eastus";
const image = config.get("image") ?? `accb${environment}acr.azurecr.io/aca-public-worker-typescript:latest`;
const namePrefix = `accb-${environment}-aca-public-worker-typescript`;
const tags = {
  ManagedBy: "accb",
  Environment: environment,
  StackName: stackName,
  Family: "canonical-container-apps"
};

const group = new resources.ResourceGroup("main", {
  resourceGroupName: `${namePrefix}-rg`,
  location,
  tags
});

const identity = new managedidentity.UserAssignedIdentity("aca", {
  resourceGroupName: group.name,
  resourceName: `${namePrefix}-mi`,
  location: group.location,
  tags
});

const logs = new operationalinsights.Workspace("logs", {
  resourceGroupName: group.name,
  workspaceName: `${namePrefix}-logs`,
  location: group.location,
  sku: { name: "PerGB2018" },
  retentionInDays: 30,
  tags
});

const env = new app.ManagedEnvironment("env", {
  resourceGroupName: group.name,
  environmentName: `${namePrefix}-env`,
  location: group.location,
  appLogsConfiguration: {
    destination: "log-analytics",
    logAnalyticsConfiguration: {
      customerId: logs.customerId,
      sharedKey: logs.sharedKeys.apply((keys) => keys.primarySharedKey)
    }
  },
  tags
});

const acr = new containerregistry.Registry("acr", {
  registryName: `accb${environment}acapublictsacr`,
  resourceGroupName: group.name,
  location: group.location,
  sku: { name: "Basic" },
  adminUserEnabled: false,
  tags
});

const bus = new servicebus.Namespace("events", {
  namespaceName: `${namePrefix}-sb`,
  resourceGroupName: group.name,
  location: group.location,
  sku: { name: "Standard", tier: "Standard" },
  tags
});

const queue = new servicebus.Queue("work", {
  queueName: `${namePrefix}-work`,
  namespaceName: bus.name,
  resourceGroupName: group.name
});

const cosmos = new documentdb.DatabaseAccount("state", {
  accountName: `${namePrefix}-cosmos`,
  resourceGroupName: group.name,
  location: group.location,
  databaseAccountOfferType: "Standard",
  kind: "GlobalDocumentDB",
  locations: [{ locationName: group.location, failoverPriority: 0 }],
  consistencyPolicy: { defaultConsistencyLevel: "Session" },
  tags
});

const attachments = new storage.StorageAccount("attachments", {
  accountName: `accb${environment}acapublictsblob`,
  resourceGroupName: group.name,
  location: group.location,
  sku: { name: "Standard_LRS" },
  kind: "StorageV2",
  tags
});

const vault = new keyvault.Vault("secrets", {
  vaultName: `${namePrefix}-kv`,
  resourceGroupName: group.name,
  location: group.location,
  properties: {
    tenantId: identity.tenantId,
    sku: { family: "A", name: "standard" }
  },
  tags
});

const assignedIdentity = identity.id.apply((id) => ({ [id]: {} }));

const publicApi = new app.ContainerApp("public-api", {
  containerAppName: `${namePrefix}-api`,
  resourceGroupName: group.name,
  managedEnvironmentId: env.id,
  location: group.location,
  configuration: {
    ingress: { external: true, targetPort: 8080 },
    secrets: [
      {
        name: "api-key",
        keyVaultUrl: vault.properties.apply((properties) => `${properties.vaultUri}secrets/api-key`),
        identity: identity.id
      }
    ]
  },
  identity: { type: "UserAssigned", userAssignedIdentities: assignedIdentity },
  template: {
    containers: [
      {
        name: "api",
        image,
        env: [
          { name: "SERVICEBUS_QUEUE", value: queue.name },
          { name: "API_SECRET_NAME", secretRef: "api-key" }
        ],
        resources: { cpu: 0.5, memory: "1Gi" }
      }
    ],
    scale: { minReplicas: 1, maxReplicas: 5 }
  },
  tags
});

const privateWorker = new app.ContainerApp("private-worker", {
  containerAppName: `${namePrefix}-worker`,
  resourceGroupName: group.name,
  managedEnvironmentId: env.id,
  location: group.location,
  configuration: {
    ingress: { external: false, targetPort: 8080 }
  },
  identity: { type: "UserAssigned", userAssignedIdentities: assignedIdentity },
  template: {
    containers: [
      {
        name: "worker",
        image,
        resources: { cpu: 0.5, memory: "1Gi" }
      }
    ],
    scale: {
      minReplicas: 0,
      maxReplicas: 10,
      rules: [
        {
          name: "servicebus-depth",
          custom: {
            type: "azure-servicebus",
            metadata: {
              queueName: queue.name,
              namespace: bus.name,
              messageCount: "5"
            }
          }
        }
      ]
    }
  },
  tags
});

const retryJob = new app.Job("retry-job", {
  jobName: `${namePrefix}-retry`,
  resourceGroupName: group.name,
  managedEnvironmentId: env.id,
  location: group.location,
  configuration: {
    triggerType: "Event",
    replicaTimeout: 300,
    replicaRetryLimit: 1,
    eventTriggerConfig: {
      parallelism: 1,
      replicaCompletionCount: 1,
      scale: {
        minExecutions: 0,
        maxExecutions: 5,
        rules: [
          {
            name: "servicebus-retry",
            type: "azure-servicebus",
            metadata: {
              queueName: queue.name,
              namespace: bus.name,
              messageCount: "5"
            }
          }
        ]
      }
    }
  },
  template: {
    containers: [
      {
        name: "retry",
        image,
        args: ["/retry"],
        resources: { cpu: 0.5, memory: "1Gi" }
      }
    ]
  },
  tags
});

export const publicApiUrl = publicApi.configuration.apply((cfg) => cfg.ingress?.fqdn);
export const privateWorkerName = privateWorker.name;
export const retryJobName = retryJob.name;
export const servicebusQueue = queue.name;
export const cosmosAccount = cosmos.name;
export const attachmentAccount = attachments.name;
export const keyVaultUri = vault.properties.apply((properties) => properties.vaultUri);
export const managedIdentityId = identity.id;
export const acrLoginServer = acr.loginServer;
export const logWorkspace = logs.name;
