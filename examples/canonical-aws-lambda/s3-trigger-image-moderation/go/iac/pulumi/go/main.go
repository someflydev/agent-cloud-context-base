package main

import (
	"fmt"

	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/cloudwatch"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/dynamodb"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/iam"
	awslambda "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/lambda"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/secretsmanager"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		stack := ctx.Stack()
		cfg := config.New(ctx, "accb")
		environment := cfg.Get("environment")
		if environment == "" { environment = stack }
		prefix := fmt.Sprintf("accb-%s-s3mod", environment)
		secretPath := cfg.Require("secretPath")
		secret, err := secretsmanager.LookupSecret(ctx, &secretsmanager.LookupSecretArgs{Name: secretPath})
		if err != nil { return err }
		images, err := s3.NewBucket(ctx, fmt.Sprintf("%s-images-%s", prefix, stack), &s3.BucketArgs{Bucket: pulumi.String(fmt.Sprintf("%s-images-%s", prefix, stack))})
		if err != nil { return err }
		table, err := dynamodb.NewTable(ctx, fmt.Sprintf("%s-records-%s", prefix, stack), &dynamodb.TableArgs{Name: pulumi.String(fmt.Sprintf("%s-records-%s", prefix, stack)), BillingMode: pulumi.String("PAY_PER_REQUEST"), HashKey: pulumi.String("pk"), Attributes: dynamodb.TableAttributeArray{&dynamodb.TableAttributeArgs{Name: pulumi.String("pk"), Type: pulumi.String("S")}}})
		if err != nil { return err }
		bus, err := cloudwatch.NewEventBus(ctx, fmt.Sprintf("%s-events-%s", prefix, stack), &cloudwatch.EventBusArgs{Name: pulumi.String(fmt.Sprintf("%s-events-%s", prefix, stack))})
		if err != nil { return err }
		role, err := iam.NewRole(ctx, fmt.Sprintf("%s-lambda-%s", prefix, stack), &iam.RoleArgs{Name: pulumi.String(fmt.Sprintf("%s-lambda-%s", prefix, stack)), AssumeRolePolicy: pulumi.String(`{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}`)})
		if err != nil { return err }
		_, err = iam.NewRolePolicyAttachment(ctx, fmt.Sprintf("%s-lambda-logs-%s", prefix, stack), &iam.RolePolicyAttachmentArgs{Role: role.Name, PolicyArn: pulumi.String("arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")})
		if err != nil { return err }
		_, err = iam.NewRolePolicy(ctx, fmt.Sprintf("%s-lambda-access-%s", prefix, stack), &iam.RolePolicyArgs{Role: role.ID(), Policy: pulumi.Sprintf(`{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["dynamodb:PutItem","dynamodb:UpdateItem"],"Resource":"%s"},{"Effect":"Allow","Action":["rekognition:DetectLabels","rekognition:DetectModerationLabels"],"Resource":"*"},{"Effect":"Allow","Action":["events:PutEvents"],"Resource":"%s"}]}`, table.Arn, bus.Arn)})
		if err != nil { return err }
		fn, err := awslambda.NewFunction(ctx, fmt.Sprintf("%s-handler-%s", prefix, stack), &awslambda.FunctionArgs{Name: pulumi.String(fmt.Sprintf("%s-handler-%s", prefix, stack)), Role: role.Arn, Runtime: pulumi.String("provided.al2023"), Handler: pulumi.String("bootstrap"), Code: pulumi.NewFileArchive("../../../build/function.zip"), Timeout: pulumi.Int(30), Environment: &awslambda.FunctionEnvironmentArgs{Variables: pulumi.StringMap{"TABLE_NAME": table.Name, "EVENT_BUS_NAME": bus.Name, "ENV_VAR_PREFIX": pulumi.String(cfg.Require("envVarPrefix")), "SECRET_PATH": pulumi.String(secretPath)}}})
		if err != nil { return err }
		permission, err := awslambda.NewPermission(ctx, fmt.Sprintf("%s-allow-s3-%s", prefix, stack), &awslambda.PermissionArgs{Action: pulumi.String("lambda:InvokeFunction"), Function: fn.Name, Principal: pulumi.String("s3.amazonaws.com"), SourceArn: images.Arn})
		if err != nil { return err }
		_, err = s3.NewBucketNotification(ctx, fmt.Sprintf("%s-images-notification-%s", prefix, stack), &s3.BucketNotificationArgs{Bucket: images.ID(), LambdaFunctions: s3.BucketNotificationLambdaFunctionArray{&s3.BucketNotificationLambdaFunctionArgs{LambdaFunctionArn: fn.Arn, Events: pulumi.StringArray{pulumi.String("s3:ObjectCreated:*")}}}}, pulumi.DependsOn([]pulumi.Resource{permission}))
		if err != nil { return err }
		ctx.Export("bucketName", images.Bucket)
		ctx.Export("tableName", table.Name)
		ctx.Export("eventBusName", bus.Name)
		ctx.Export("functionName", fn.Name)
		ctx.Export("secretArn", pulumi.String(secret.Arn))
		return nil
	})
}
