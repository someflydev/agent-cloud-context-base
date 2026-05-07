# AWS Secrets Manager Binding: Python

Identity: Lambda execution role gets `secretsmanager:GetSecretValue` only for
the environment-scoped secret ARN.

```json
{
  "Effect": "Allow",
  "Action": ["secretsmanager:GetSecretValue"],
  "Resource": "arn:aws:secretsmanager:REGION:ACCOUNT:secret:accb/dev/app/config-*"
}
```

Runtime retrieval:

```python
import json
import os
import time
import boto3

_cache = {}

def get_secret():
    name = os.environ["ACCB_SECRET_ID"]
    hit = _cache.get(name)
    if hit and hit["expires_at"] > time.time():
        return hit["value"]
    client = boto3.client("secretsmanager")
    value = json.loads(client.get_secret_value(SecretId=name)["SecretString"])
    _cache[name] = {"value": value, "expires_at": time.time() + 300}
    return value
```
