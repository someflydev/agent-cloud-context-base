# Secret Not In Source

Literal credentials do not belong in source files, IaC variables, committed
Pulumi config, examples, or test fixtures.

The failure mode is credential disclosure through git history, logs, generated
payloads, or copied examples. A fake-looking value can also teach the wrong
pattern and later become a real credential by accident.

Use provider secret stores, Pulumi secret config, Terraform variables supplied
outside git, or emulator-only placeholder values that are clearly non-secret.

When this policy fails, rotate any real credential, remove the value from source,
and replace it with a documented secret binding.
