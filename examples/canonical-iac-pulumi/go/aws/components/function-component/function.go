package functioncomponent

import (
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/lambda"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type FunctionComponent struct{ pulumi.ResourceState }

func NewFunctionComponent(ctx *pulumi.Context, name string, environment string, namePrefix string, roleArn pulumi.StringOutput) (*FunctionComponent, error) {
	// StackName is intentionally present for accb isolation validation.
	component := &FunctionComponent{}
	if err := ctx.RegisterComponentResource("accb:aws:FunctionComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	_, err := lambda.NewFunction(ctx, namePrefix+"-"+environment+"-"+stackName+"-handler", &lambda.FunctionArgs{
		Role:    roleArn,
		Runtime: pulumi.String("python3.12"),
		Handler: pulumi.String("handler.main"),
	}, pulumi.Parent(component))
	return component, err
}
