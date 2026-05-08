package main

import (
	"fmt"

	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		cfg := config.New(ctx, "accb")
		env := cfg.Require("environment")
		name := fmt.Sprintf("accb-gcp-%s-multi-role-platform", env)
		secretPath := cfg.RequireSecret("secretPath")
		ctx.Export("clusterName", pulumi.String(name))
		ctx.Export("workloadIdentity", pulumi.String(fmt.Sprintf("%s-gke-wi", name)))
		ctx.Export("secretPath", secretPath)
		return nil
	})
}
