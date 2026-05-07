# Azure Key Vault Managed Identity: Python

```python
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

def load_secret(vault_url: str, secret_name: str) -> str:
    client = SecretClient(vault_url=vault_url, credential=ManagedIdentityCredential())
    return client.get_secret(secret_name).value
```
