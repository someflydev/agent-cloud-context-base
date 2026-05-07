package main

import (
	"fmt"

	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/pubsub"
	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/serviceaccount"
	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/storage"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		cfg := config.New(ctx, "accb")
		environment := cfg.Require("environment")
		namePrefix := fmt.Sprintf("accb-%s-gcp-gcs-trigger-ocr-to-firestore", environment)
		labels := pulumi.StringMap{"managed_by": pulumi.String("accb"), "environment": pulumi.String(environment), "family": pulumi.String("canonical-gcp-functions")}

		sa, err := serviceaccount.NewAccount(ctx, "function", &serviceaccount.AccountArgs{
			AccountId:   pulumi.String(fmt.Sprintf("%s-fn", namePrefix)),
			DisplayName: pulumi.String(fmt.Sprintf("accb %s GCS OCR function", environment)),
		})
		if err != nil {
			return err
		}
		bucket, err := storage.NewBucket(ctx, "input", &storage.BucketArgs{
			Name:                     pulumi.String(fmt.Sprintf("%s-input", namePrefix)),
			Location:                 pulumi.String("US"),
			UniformBucketLevelAccess: pulumi.Bool(true),
			Labels:                   labels,
		})
		if err != nil {
			return err
		}
		topic, err := pubsub.NewTopic(ctx, "downstream", &pubsub.TopicArgs{
			Name:   pulumi.String(fmt.Sprintf("%s-downstream", namePrefix)),
			Labels: labels,
		})
		if err != nil {
			return err
		}
		ctx.Export("serviceAccountEmail", sa.Email)
		ctx.Export("inputBucketName", bucket.Name)
		ctx.Export("downstreamTopicName", topic.Name)
		return nil
	})
}
