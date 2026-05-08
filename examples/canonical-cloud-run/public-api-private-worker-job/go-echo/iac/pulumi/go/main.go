package main

import (
	"fmt"

	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/cloudrunv2"
	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/pubsub"
	"github.com/pulumi/pulumi-gcp/sdk/v7/go/gcp/serviceaccount"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		cfg := config.New(ctx, "accb")
		environment := cfg.Require("environment")
		stackName := ctx.Stack()
		namePrefix := fmt.Sprintf("accb-%s-cloudrun-public-worker-go", environment)
		labels := pulumi.StringMap{"managed_by": pulumi.String("accb"), "environment": pulumi.String(stackName), "family": pulumi.String("canonical-cloud-run")}
		image := cfg.Get("image")
		if image == "" {
			image = fmt.Sprintf("gcr.io/example/%s:latest", namePrefix)
		}

		sa, err := serviceaccount.NewAccount(ctx, "service", &serviceaccount.AccountArgs{
			AccountId:   pulumi.String(namePrefix + "-svc"),
			DisplayName: pulumi.String("accb " + environment + " Cloud Run public worker Go"),
		})
		if err != nil {
			return err
		}
		topic, err := pubsub.NewTopic(ctx, "review", &pubsub.TopicArgs{Name: pulumi.String(namePrefix + "-review"), Labels: labels})
		if err != nil {
			return err
		}
		service, err := cloudrunv2.NewService(ctx, "public", &cloudrunv2.ServiceArgs{
			Name:     pulumi.String(namePrefix + "-public"),
			Location: pulumi.String(cfg.Get("region")),
			Template: &cloudrunv2.ServiceTemplateArgs{
				ServiceAccount: sa.Email,
				Containers: cloudrunv2.ServiceTemplateContainerArray{
					&cloudrunv2.ServiceTemplateContainerArgs{Image: pulumi.String(image)},
				},
			},
			Labels: labels,
		})
		if err != nil {
			return err
		}
		ctx.Export("service_uri", service.Uri)
		ctx.Export("review_topic", topic.Name)
		return nil
	})
}
