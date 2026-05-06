import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const config = new pulumi.Config("accb");
const stackName = pulumi.getStack();
const environment = config.get("environment") ?? stackName;
const namePrefix = `accb-${environment}-gcp-stripe`;
const labels = { managed_by: "accb", environment, family: "canonical-gcp-functions" };

const serviceAccount = new gcp.serviceaccount.Account("function", {
  accountId: `${namePrefix}-fn`,
  displayName: `accb ${environment} Stripe webhook function`,
});

const signingSecret = new gcp.secretmanager.Secret("stripe-signing", {
  secretId: `${namePrefix}-signing`,
  labels,
  replication: { auto: {} },
});

const queue = new gcp.cloudtasks.Queue("fulfillment", {
  name: `${namePrefix}-fulfillment`,
  location: "us-central1",
});

export const serviceAccountEmail = serviceAccount.email;
export const signingSecretName = signingSecret.name;
export const queueName = queue.name;
