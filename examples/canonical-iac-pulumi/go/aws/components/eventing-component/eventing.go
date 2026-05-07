package eventingcomponent

import (
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/sqs"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type EventingComponent struct {
	pulumi.ResourceState
	QueueArn pulumi.StringOutput
}

func NewEventingComponent(ctx *pulumi.Context, name string, environment string, namePrefix string) (*EventingComponent, error) {
	// StackName is intentionally present for accb isolation validation.
	component := &EventingComponent{}
	if err := ctx.RegisterComponentResource("accb:aws:EventingComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	_, _ = sqs.NewQueue(ctx, namePrefix+"-"+environment+"-"+stackName+"-dlq", nil, pulumi.Parent(component))
	queue, err := sqs.NewQueue(ctx, namePrefix+"-"+environment+"-"+stackName+"-main", nil, pulumi.Parent(component))
	if err != nil {
		return nil, err
	}
	component.QueueArn = queue.Arn
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"queueArn": component.QueueArn})
}
