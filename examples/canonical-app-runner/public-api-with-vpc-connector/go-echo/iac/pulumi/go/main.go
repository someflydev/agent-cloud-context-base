package main

import (
	"fmt"

	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/ecr"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/iam"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		cfg := config.New(ctx, "accb")
		environment := cfg.Require("environment")
		stackName := ctx.Stack()
		namePrefix := fmt.Sprintf("accb-%s-apprunner-vpc-api-go", environment)
		tags := pulumi.StringMap{"ManagedBy": pulumi.String("accb"), "Environment": pulumi.String(stackName), "Family": pulumi.String("canonical-app-runner")}

		repo, err := ecr.NewRepository(ctx, "service", &ecr.RepositoryArgs{
			Name: pulumi.String(namePrefix + "-repo"),
			Tags: tags,
		})
		if err != nil {
			return err
		}
		role, err := iam.NewRole(ctx, "service-role", &iam.RoleArgs{
			Name: pulumi.String(namePrefix + "-service-role"),
			AssumeRolePolicy: pulumi.String(`{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"tasks.apprunner.amazonaws.com"},"Action":"sts:AssumeRole"}]}`),
			Tags: tags,
		})
		if err != nil {
			return err
		}
		ctx.Export("repository_url", repo.RepositoryUrl)
		ctx.Export("service_role_arn", role.Arn)
		return nil
	})
}
