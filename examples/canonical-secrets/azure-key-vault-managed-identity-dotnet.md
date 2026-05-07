# Azure Key Vault Managed Identity: .NET

Use a managed identity bound to the Function App. Store app settings as Key
Vault references for platform injection, or retrieve with the SDK at runtime.

```csharp
var credential = new ManagedIdentityCredential();
var client = new SecretClient(new Uri(vaultUri), credential);
KeyVaultSecret secret = await client.GetSecretAsync("accb-dev-app-config");
```
