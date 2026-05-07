# GCP Secret Manager Binding: Python

Grant the runtime service account `roles/secretmanager.secretAccessor` on only
the environment-scoped secret.

```python
from google.cloud import secretmanager

def load_secret(project_id: str, secret_id: str, version: str = "latest") -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    return client.access_secret_version(request={"name": name}).payload.data.decode("utf-8")
```
