# IaC Isolation Anchor

- Dev and test never share state backend keys.
- Dev and test never share Pulumi stack state.
- Dev and test never share secret paths.
- Dev and test never share KMS keys when keys are declared.
- Dev and test resource names differ by deterministic suffix.
- Test teardown is the default unless the manifest opts in to persistent test resources.
- `validate_iac_isolation.py` is the gate for these rules once it exists.
