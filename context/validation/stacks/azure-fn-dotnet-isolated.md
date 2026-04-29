---
accb_origin: canonical
accb_source_path: context/validation/stacks/azure-fn-dotnet-isolated.md
accb_role: validation
accb_version: 1
---

# Azure Functions Dotnet Isolated Validation

Validate isolated-process startup and invoke the function with the real binding
payload for the selected trigger. The worker process must start with declared
configuration and no plaintext secrets.

Invariants: `dotnet test` covers handler behavior, host startup succeeds,
managed identity bindings are least privilege, Key Vault access is explicit,
and replay with the same event identity is safe.

PROMPT_09 adds deeper stack-specific gates.
