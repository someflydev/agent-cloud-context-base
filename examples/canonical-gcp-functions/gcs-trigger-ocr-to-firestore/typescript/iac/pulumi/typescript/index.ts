import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const config = new pulumi.Config("accb");
const stackName = pulumi.getStack();
const environment = config.get("environment") ?? stackName;
const namePrefix = `accb-${environment}-gcp-gcs-trigger-ocr-to-firestore`;
const labels = { managed_by: "accb", environment, family: "canonical-gcp-functions" };

const serviceAccount = new gcp.serviceaccount.Account("function", {
  accountId: `${namePrefix}-fn`,
  displayName: `accb ${environment} GCS OCR function`,
});

const inputBucket = new gcp.storage.Bucket("input", {
  name: `${namePrefix}-input`,
  location: "US",
  uniformBucketLevelAccess: true,
  labels,
});

const downstream = new gcp.pubsub.Topic("downstream", { name: `${namePrefix}-downstream`, labels });

export const serviceAccountEmail = serviceAccount.email;
export const inputBucketName = inputBucket.name;
export const downstreamTopicName = downstream.name;
