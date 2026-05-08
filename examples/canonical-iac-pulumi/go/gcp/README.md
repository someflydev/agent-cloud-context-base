# Canonical Pulumi IaC: Go GCP

Seed tree for `.accb/` generated repos using GCP and Pulumi Go.

```sh
pulumi stack select dev
pulumi config set --secret accb:appSecretRef accb/dev/app/config
pulumi stack select test
pulumi config set --secret accb:appSecretRef accb/test/app/config
```
