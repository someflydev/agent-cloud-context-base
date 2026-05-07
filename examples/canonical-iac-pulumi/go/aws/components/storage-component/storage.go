package storagecomponent

import (
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type StorageComponent struct {
	pulumi.ResourceState
	BucketArn pulumi.StringOutput
}

func NewStorageComponent(ctx *pulumi.Context, name string, environment string, namePrefix string) (*StorageComponent, error) {
	// StackName is intentionally present for accb isolation validation.
	component := &StorageComponent{}
	if err := ctx.RegisterComponentResource("accb:aws:StorageComponent", name, component); err != nil {
		return nil, err
	}
	stackName := ctx.Stack()
	bucket, err := s3.NewBucket(ctx, namePrefix+"-"+environment+"-"+stackName+"-artifacts", nil, pulumi.Parent(component))
	if err != nil {
		return nil, err
	}
	component.BucketArn = bucket.Arn
	return component, ctx.RegisterResourceOutputs(component, pulumi.Map{"bucketArn": component.BucketArn})
}
