package main

import (
	"encoding/json"
	"fmt"

	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/dynamodb"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/iam"
	awslambda "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/lambda"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/secretsmanager"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/sqs"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		stack := ctx.Stack()
		cfg := config.New(ctx, "accb")
		environment := cfg.Get("environment")
		if environment == "" {
			environment = stack
		}
		prefix := fmt.Sprintf("accb-%s-translate", environment)
		secretPath := cfg.Require("secretPath")
		translateSecret, err := secretsmanager.LookupSecret(ctx, &secretsmanager.LookupSecretArgs{Name: secretPath})
		if err != nil {
			return err
		}
		source, err := s3.NewBucket(ctx, fmt.Sprintf("%s-source-%s", prefix, stack), &s3.BucketArgs{Bucket: pulumi.String(fmt.Sprintf("%s-source-%s", prefix, stack))})
		if err != nil {
			return err
		}
		dest, err := s3.NewBucket(ctx, fmt.Sprintf("%s-dest-%s", prefix, stack), &s3.BucketArgs{Bucket: pulumi.String(fmt.Sprintf("%s-dest-%s", prefix, stack))})
		if err != nil {
			return err
		}
		dlq, err := sqs.NewQueue(ctx, fmt.Sprintf("%s-dlq-%s", prefix, stack), &sqs.QueueArgs{Name: pulumi.String(fmt.Sprintf("%s-dlq-%s", prefix, stack))})
		if err != nil {
			return err
		}
		policy, _ := json.Marshal(map[string]any{"deadLetterTargetArn": dlq.Arn, "maxReceiveCount": 3})
		jobs, err := sqs.NewQueue(ctx, fmt.Sprintf("%s-jobs-%s", prefix, stack), &sqs.QueueArgs{Name: pulumi.String(fmt.Sprintf("%s-jobs-%s", prefix, stack)), VisibilityTimeoutSeconds: pulumi.Int(120), RedrivePolicy: pulumi.String(string(policy))})
		if err != nil {
			return err
		}
		table, err := dynamodb.NewTable(ctx, fmt.Sprintf("%s-jobs-%s", prefix, stack), &dynamodb.TableArgs{
			Name:        pulumi.String(fmt.Sprintf("%s-jobs-%s", prefix, stack)),
			BillingMode: pulumi.String("PAY_PER_REQUEST"),
			HashKey:     pulumi.String("pk"),
			Attributes:  dynamodb.TableAttributeArray{&dynamodb.TableAttributeArgs{Name: pulumi.String("pk"), Type: pulumi.String("S")}},
		})
		if err != nil {
			return err
		}
		role, err := iam.NewRole(ctx, fmt.Sprintf("%s-lambda-%s", prefix, stack), &iam.RoleArgs{
			Name:             pulumi.String(fmt.Sprintf("%s-lambda-%s", prefix, stack)),
			AssumeRolePolicy: pulumi.String(`{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}`),
		})
		if err != nil {
			return err
		}
		_, err = iam.NewRolePolicyAttachment(ctx, fmt.Sprintf("%s-lambda-logs-%s", prefix, stack), &iam.RolePolicyAttachmentArgs{
			Role:      role.Name,
			PolicyArn: pulumi.String("arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"),
		})
		if err != nil {
			return err
		}
		_, err = iam.NewRolePolicy(ctx, fmt.Sprintf("%s-lambda-access-%s", prefix, stack), &iam.RolePolicyArgs{
			Role: role.ID(),
			Policy: pulumi.Sprintf(`{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:GetObject"],"Resource":"%s/*"},{"Effect":"Allow","Action":["s3:PutObject"],"Resource":"%s/*"},{"Effect":"Allow","Action":["dynamodb:PutItem","dynamodb:UpdateItem"],"Resource":"%s"},{"Effect":"Allow","Action":["translate:TranslateText"],"Resource":"*"},{"Effect":"Allow","Action":["sqs:ReceiveMessage","sqs:DeleteMessage","sqs:GetQueueAttributes"],"Resource":"%s"}]}`,
				source.Arn, dest.Arn, table.Arn, jobs.Arn),
		})
		if err != nil {
			return err
		}
		function, err := awslambda.NewFunction(ctx, fmt.Sprintf("%s-handler-%s", prefix, stack), &awslambda.FunctionArgs{
			Name:    pulumi.String(fmt.Sprintf("%s-handler-%s", prefix, stack)),
			Role:    role.Arn,
			Runtime: pulumi.String("provided.al2023"),
			Handler: pulumi.String("bootstrap"),
			Code:    pulumi.NewFileArchive("../../../build/function.zip"),
			Timeout: pulumi.Int(60),
			Environment: &awslambda.FunctionEnvironmentArgs{
				Variables: pulumi.StringMap{
					"TABLE_NAME":     table.Name,
					"SOURCE_BUCKET":  source.Bucket,
					"DEST_BUCKET":    dest.Bucket,
					"ENV_VAR_PREFIX": pulumi.String(cfg.Require("envVarPrefix")),
					"SECRET_PATH":    pulumi.String(secretPath),
				},
			},
		})
		if err != nil {
			return err
		}
		_, err = awslambda.NewEventSourceMapping(ctx, fmt.Sprintf("%s-jobs-%s", prefix, stack), &awslambda.EventSourceMappingArgs{
			EventSourceArn: jobs.Arn,
			FunctionName:  function.Arn,
			BatchSize:     pulumi.Int(1),
		})
		if err != nil {
			return err
		}
		ctx.Export("sourceBucket", source.Bucket)
		ctx.Export("destBucket", dest.Bucket)
		ctx.Export("queueUrl", jobs.Url)
		ctx.Export("tableName", table.Name)
		ctx.Export("functionName", function.Name)
		ctx.Export("secretArn", pulumi.String(translateSecret.Arn))
		return nil
	})
}
