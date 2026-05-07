# External Secrets Operator: Azure

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: accb-app-config
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: accb-azure-keyvault
    kind: ClusterSecretStore
  target:
    name: accb-app-config
  data:
    - secretKey: config
      remoteRef:
        key: accb-dev-app-config
```
