package secretcomponent

import "github.com/pulumi/pulumi/sdk/v3/go/pulumi"

type SecretComponent struct {
	pulumi.ResourceState
	SecretRef pulumi.StringOutput
}

func NewSecretComponent(ctx *pulumi.Context, name string, environment string, namePrefix string) (*SecretComponent, error) {
	component := &SecretComponent{}
	if err := ctx.RegisterComponentResource("accb:azure:SecretComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	component.SecretRef = pulumi.String(namePrefix + "-" + environment + "-" + stackName + "-config").ToStringOutput()
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"secretRef": component.SecretRef})
}
