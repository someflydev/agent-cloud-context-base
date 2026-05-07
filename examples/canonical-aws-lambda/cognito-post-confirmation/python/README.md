# Cognito Post Confirmation - Python

Cognito post-confirmation invokes Lambda, the handler claims the user-pool/user-name pair, creates an application profile record, and publishes a signup event for downstream onboarding workflows.

## Dev/Test Isolation

- Terraform state: `accb/canonical-aws-lambda/cognito-post-confirmation/python/dev.tfstate` and `.../test.tfstate`
- Environment variables: `ACCB_DEV_*` and `ACCB_TEST_*`
- Secret paths: `/accb/dev/cognito-post-confirmation/*` and `/accb/test/cognito-post-confirmation/*`
- Resource names: `accb-${environment}-cognito-post-confirmation-*`

## Verification

```bash
bash examples/canonical-aws-lambda/cognito-post-confirmation/python/tests/verify.sh
```

Lane A uses ministack and is gated by `ACCB_RUN_LOCAL_PROVIDER=1`. Lane B uses ephemeral real AWS resources, requires explicit AWS credentials, incurs real cost, and must be destroyed immediately after verification.
