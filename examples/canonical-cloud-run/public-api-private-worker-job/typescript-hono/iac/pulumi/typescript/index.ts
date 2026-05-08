import * as gcp from "@pulumi/gcp";
import * as pulumi from "@pulumi/pulumi";

const cfg = new pulumi.Config("accb");
const environment = cfg.require("environment");
const stackName = pulumi.getStack();
const namePrefix = `accb-${environment}-cloudrun-public-worker-typescript`;
const labels = { managed_by: "accb", environment: stackName, family: "canonical-cloud-run" };
const image = cfg.get("image") ?? `gcr.io/example/${namePrefix}:latest`;
const region = cfg.get("region") ?? "us-central1";

const serviceAccount = new gcp.serviceaccount.Account("service", {
  accountId: `${namePrefix}-svc`,
  displayName: `accb ${environment} Cloud Run public worker TypeScript`
});

const reviewTopic = new gcp.pubsub.Topic("review", {
  name: `${namePrefix}-review`,
  labels
});

const publicService = new gcp.cloudrunv2.Service("public", {
  name: `${namePrefix}-public`,
  location: region,
  template: {
    serviceAccount: serviceAccount.email,
    containers: [{ image }]
  },
  labels
});

export const serviceUri = publicService.uri;
export const reviewTopicName = reviewTopic.name;
