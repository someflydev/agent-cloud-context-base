package storagecomponent

import "github.com/pulumi/pulumi/sdk/v3/go/pulumi"

type StorageComponent struct {
	pulumi.ResourceState
	StorageName pulumi.StringOutput
}

func NewStorageComponent(ctx *pulumi.Context, name string, environment string, namePrefix string) (*StorageComponent, error) {
	component := &StorageComponent{}
	if err := ctx.RegisterComponentResource("accb:gcp:StorageComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	component.StorageName = pulumi.String(namePrefix + "-" + environment + "-" + stackName + "-artifacts").ToStringOutput()
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"storageName": component.StorageName})
}
