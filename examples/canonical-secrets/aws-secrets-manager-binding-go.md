# AWS Secrets Manager Binding: Go

Bind the Lambda or task role to the exact `accb/{environment}/app/config`
secret ARN. Cache in memory for warm invocations.

```go
func LoadSecret(ctx context.Context, client *secretsmanager.Client, name string) (string, error) {
  out, err := client.GetSecretValue(ctx, &secretsmanager.GetSecretValueInput{SecretId: aws.String(name)})
  if err != nil {
    return "", err
  }
  return aws.ToString(out.SecretString), nil
}
```
