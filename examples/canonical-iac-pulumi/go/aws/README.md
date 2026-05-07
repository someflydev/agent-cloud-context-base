# Canonical Pulumi IaC: Go AWS

Seed tree for `.accb/` generated repos using AWS and Pulumi Go.

```sh
pulumi stack select dev
pulumi config set --secret accb:appSecretRef accb/dev/app/config
pulumi stack select test
pulumi config set --secret accb:appSecretRef accb/test/app/config
```
