---
accb_origin: canonical
accb_source_path: context/validation/archetypes/managed-container-service.md
accb_role: validation
accb_version: 1
---

# Managed Container Service Validation

Build the container image, run the service locally or in the provider test
lane, and exercise health, readiness, and one representative route. Validate
IaC isolation before deploy.

Proof commands should include the image build, service startup, readiness
probe, route smoke test, and IaC isolation gate. If the service consumes
secrets or managed storage, include one provider-bound round trip.

Common failure modes are root container users, missing readiness routes,
provider startup timeouts, secrets copied into env files, and shared dev/test
resource names. Reference container image, secret, observability, and IaC
isolation doctrine.
