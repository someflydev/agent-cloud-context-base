import * as pulumi from "@pulumi/pulumi";

const cfg = new pulumi.Config("accb");
const env = cfg.require("environment");
const name = `accb-azure-${env}-multi-role-platform`;
const secretPath = cfg.requireSecret("secretPath");

pulumi.export("clusterName", name);
pulumi.export("workloadIdentity", `${name}-managed-identity`);
pulumi.export("secretPath", secretPath);
