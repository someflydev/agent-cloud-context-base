package main

import (
	"fmt"

	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/bigquery"
	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/secretmanager"
	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/serviceaccount"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		cfg := config.New(ctx, "accb")
		environment := cfg.Require("environment")
		namePrefix := fmt.Sprintf("accb-%s-gcp-monitoring-router", environment)
		labels := pulumi.StringMap{"managed_by": pulumi.String("accb"), "environment": pulumi.String(environment), "family": pulumi.String("canonical-gcp-functions")}

		sa, err := serviceaccount.NewAccount(ctx, "function", &serviceaccount.AccountArgs{
			AccountId:   pulumi.String(fmt.Sprintf("%s-fn", namePrefix)),
			DisplayName: pulumi.String(fmt.Sprintf("accb %s monitoring router function", environment)),
		})
		if err != nil {
			return err
		}
		dataset, err := bigquery.NewDataset(ctx, "audit", &bigquery.DatasetArgs{
			DatasetId: pulumi.String(fmt.Sprintf("accb_%s_gcp_monitoring_router_audit", environment)),
			Location:  pulumi.String("US"),
			Labels:    labels,
		})
		if err != nil {
			return err
		}
		secret, err := secretmanager.NewSecret(ctx, "slack-webhook", &secretmanager.SecretArgs{
			SecretId: pulumi.String(fmt.Sprintf("%s-slack", namePrefix)),
			Labels:   labels,
			Replication: &secretmanager.SecretReplicationArgs{
				Auto: &secretmanager.SecretReplicationAutoArgs{},
			},
		})
		if err != nil {
			return err
		}
		ctx.Export("serviceAccountEmail", sa.Email)
		ctx.Export("auditDataset", dataset.DatasetId)
		ctx.Export("slackSecret", secret.Name)
		return nil
	})
}
