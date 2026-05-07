# AWS SSM Parameter Store Binding: Python

Use SecureString parameters encrypted by an environment-scoped KMS key:
`/accb/dev/app/config` and `/accb/test/app/config`.

```python
import os
import boto3

def load_parameter():
    client = boto3.client("ssm")
    response = client.get_parameter(Name=os.environ["ACCB_PARAMETER_NAME"], WithDecryption=True)
    return response["Parameter"]["Value"]
```
