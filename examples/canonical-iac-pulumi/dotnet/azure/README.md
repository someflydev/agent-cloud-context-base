# Canonical Pulumi IaC: .NET Azure

Seed tree for `.accb/` generated repos using Azure and Pulumi .NET.

```sh
pulumi stack select dev
pulumi config set --secret accb:appSecretRef accb/dev/app/config
pulumi stack select test
pulumi config set --secret accb:appSecretRef accb/test/app/config
```
