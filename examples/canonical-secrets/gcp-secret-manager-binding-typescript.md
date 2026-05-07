# GCP Secret Manager Binding: TypeScript

```ts
import {SecretManagerServiceClient} from "@google-cloud/secret-manager";

export async function loadSecret(projectId: string, secretId: string) {
  const client = new SecretManagerServiceClient();
  const name = `projects/${projectId}/secrets/${secretId}/versions/latest`;
  const [version] = await client.accessSecretVersion({name});
  return version.payload?.data?.toString("utf8") ?? "";
}
```
