package identitycomponent

import "github.com/pulumi/pulumi/sdk/v3/go/pulumi"

type IdentityComponent struct {
	pulumi.ResourceState
	IdentityRef pulumi.StringOutput
}

func NewIdentityComponent(ctx *pulumi.Context, name string, environment string, namePrefix string, storageName pulumi.StringOutput, eventingName pulumi.StringOutput, secretRef pulumi.StringOutput) (*IdentityComponent, error) {
	component := &IdentityComponent{}
	if err := ctx.RegisterComponentResource("accb:azure:IdentityComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	component.IdentityRef = pulumi.String(namePrefix + "-" + environment + "-" + stackName + "-runtime").ToStringOutput()
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"identityRef": component.IdentityRef})
}
