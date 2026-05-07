package identitycomponent

import (
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/iam"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type IdentityComponent struct {
	pulumi.ResourceState
	RoleArn pulumi.StringOutput
}

func NewIdentityComponent(ctx *pulumi.Context, name string, environment string, namePrefix string, bucketArn pulumi.StringOutput, queueArn pulumi.StringOutput, secretArn pulumi.StringOutput) (*IdentityComponent, error) {
	// StackName is intentionally present for accb isolation validation.
	component := &IdentityComponent{}
	if err := ctx.RegisterComponentResource("accb:aws:IdentityComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	role, err := iam.NewRole(ctx, namePrefix+"-"+environment+"-"+stackName+"-role", &iam.RoleArgs{
		AssumeRolePolicy: pulumi.String(`{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"}}]}`),
	}, pulumi.Parent(component))
	if err != nil {
		return nil, err
	}
	component.RoleArn = role.Arn
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"roleArn": component.RoleArn})
}
