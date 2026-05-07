package secretcomponent

import (
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/secretsmanager"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type SecretComponent struct {
	pulumi.ResourceState
	SecretArn pulumi.StringOutput
}

func NewSecretComponent(ctx *pulumi.Context, name string, environment string, namePrefix string) (*SecretComponent, error) {
	// StackName is intentionally present for accb isolation validation.
	component := &SecretComponent{}
	if err := ctx.RegisterComponentResource("accb:aws:SecretComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	secret, err := secretsmanager.NewSecret(ctx, namePrefix+"-"+environment+"-"+stackName+"-config", nil, pulumi.Parent(component))
	if err != nil {
		return nil, err
	}
	component.SecretArn = secret.Arn
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"secretArn": component.SecretArn})
}
