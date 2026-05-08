package eventingcomponent

import "github.com/pulumi/pulumi/sdk/v3/go/pulumi"

type EventingComponent struct {
	pulumi.ResourceState
	EventingName pulumi.StringOutput
}

func NewEventingComponent(ctx *pulumi.Context, name string, environment string, namePrefix string) (*EventingComponent, error) {
	component := &EventingComponent{}
	if err := ctx.RegisterComponentResource("accb:azure:EventingComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	component.EventingName = pulumi.String(namePrefix + "-" + environment + "-" + stackName + "-events").ToStringOutput()
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"eventingName": component.EventingName})
}
