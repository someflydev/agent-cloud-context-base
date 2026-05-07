package main

import (
	eventingcomponent "accb-canonical-iac-pulumi-go-aws/components/eventing-component"
	functioncomponent "accb-canonical-iac-pulumi-go-aws/components/function-component"
	identitycomponent "accb-canonical-iac-pulumi-go-aws/components/identity-component"
	secretcomponent "accb-canonical-iac-pulumi-go-aws/components/secret-component"
	storagecomponent "accb-canonical-iac-pulumi-go-aws/components/storage-component"

	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		stackName := ctx.Stack()
		env := stackName
		namePrefix := "accb-" + stackName
		storage, _ := storagecomponent.NewStorageComponent(ctx, namePrefix+"-"+env+"-storage", env, namePrefix)
		eventing, _ := eventingcomponent.NewEventingComponent(ctx, namePrefix+"-"+env+"-eventing", env, namePrefix)
		secret, _ := secretcomponent.NewSecretComponent(ctx, namePrefix+"-"+env+"-secret", env, namePrefix)
		identity, _ := identitycomponent.NewIdentityComponent(ctx, namePrefix+"-"+env+"-identity", env, namePrefix, storage.BucketArn, eventing.QueueArn, secret.SecretArn)
		_, _ = functioncomponent.NewFunctionComponent(ctx, namePrefix+"-"+env+"-function", env, namePrefix, identity.RoleArn)
		ctx.Export("stackName", pulumi.String(stackName))
		return nil
	})
}
