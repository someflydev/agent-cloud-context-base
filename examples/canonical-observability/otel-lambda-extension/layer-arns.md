# ADOT Lambda Layer ARNs

Use the AWS-managed ADOT Lambda layer for the target region and architecture.
Do not hard-code one region into reusable `.accb/` templates.

Example operator lookup:

```sh
aws lambda list-layer-versions --layer-name aws-otel-python-amd64-ver-1-30-0 --region us-east-1
```

Record the selected ARN in environment-specific IaC config, for example
`accb/dev/lambda/adot_layer_arn` and `accb/test/lambda/adot_layer_arn`.
