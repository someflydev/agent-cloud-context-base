package functioncomponent

import "github.com/pulumi/pulumi/sdk/v3/go/pulumi"

type FunctionComponent struct{ pulumi.ResourceState }

func NewFunctionComponent(ctx *pulumi.Context, name string, environment string, namePrefix string, identityRef pulumi.StringOutput) (*FunctionComponent, error) {
	component := &FunctionComponent{}
	if err := ctx.RegisterComponentResource("accb:gcp:FunctionComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"functionName": pulumi.String(namePrefix + "-" + environment + "-" + stackName + "-handler")})
}
