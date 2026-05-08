import * as pulumi from "@pulumi/pulumi";
import { FunctionComponent } from "./components/function-component";
import { StorageComponent } from "./components/storage-component";
import { EventingComponent } from "./components/eventing-component";
import { SecretComponent } from "./components/secret-component";
import { IdentityComponent } from "./components/identity-component";

const stack = pulumi.getStack();
const config = new pulumi.Config("accb");
const environment = config.get("environment") || stack;
const namePrefix = config.get("namePrefix") || `accb-${stack}`;

const storage = new StorageComponent(`${namePrefix}-${environment}-storage`, { environment, namePrefix });
const eventing = new EventingComponent(`${namePrefix}-${environment}-eventing`, { environment, namePrefix });
const secret = new SecretComponent(`${namePrefix}-${environment}-secret`, { environment, namePrefix });
const identity = new IdentityComponent(`${namePrefix}-${environment}-identity`, {
  environment,
  namePrefix,
  storageName: storage.bucketName,
  eventingName: eventing.topicName,
  secretRef: secret.secretId,
});
new FunctionComponent(`${namePrefix}-${environment}-function`, { environment, namePrefix, identityRef: identity.serviceAccountEmail });

export const stackName = stack;
