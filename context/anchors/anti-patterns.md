# Anti Patterns Anchor

- Do not invent a new architecture when a manifest already fits.
- Do not mix templates with canonical examples.
- Do not introduce a new managed service without a stack pack.
- Do not reuse dev resource names for test.
- Do not bake secrets into images or IaC source.
- Do not host long-running loops or scheduled tasks inside a function.
- Do not call a mocked managed-service client an integration test.
- Use Lane A emulator or Lane B ephemeral real resources for managed-service proof.
