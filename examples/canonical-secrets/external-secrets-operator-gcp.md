# External Secrets Operator: GCP

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: accb-app-config
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: accb-gcp-secrets
    kind: ClusterSecretStore
  target:
    name: accb-app-config
  data:
    - secretKey: config
      remoteRef:
        key: accb-dev-app-config
```
