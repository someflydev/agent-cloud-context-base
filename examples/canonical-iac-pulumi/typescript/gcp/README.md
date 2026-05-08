# Canonical Pulumi IaC: TypeScript GCP

Seed tree for `.accb/` generated repos using GCP and Pulumi TypeScript.

Stacks:

- `dev`: `Pulumi.dev.yaml`
- `test`: `Pulumi.test.yaml`

Set secrets out of band:

```sh
pulumi stack select dev
pulumi config set --secret accb:appSecretRef accb/dev/app/config
pulumi stack select test
pulumi config set --secret accb:appSecretRef accb/test/app/config
```
