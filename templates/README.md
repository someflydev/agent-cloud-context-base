# Templates

Templates are starter scaffolds for derived cloud repos. Use them when
`scripts/new_cloud_repo.py` (PROMPT_16) or a focused manual change needs a
short, adaptable starting point.

- templates are not canonical examples (those live in `examples/`)
- templates stay short and adaptable
- doctrine and canonical examples still control the recommended pattern
- front-facing templates such as `readme/README.template.md` follow the
  documentation-timing-discipline doctrine -- substantive prose only after
  the derived repo has earned it

## Groups

- `agent-md/`, `claude-md/` -- assistant entrypoints
- `readme/` -- minimal-front-door bootstrap doc
- `gitignore/` -- stack-aware ignore rules
- `iac/terraform/<aws|gcp|azure>/` -- provider-specific Terraform with
  dev+test pair
- `iac/pulumi/<typescript|python|go>/<aws|gcp|azure>/` plus
  `iac/pulumi/dotnet/azure/` -- Pulumi starters aligned with the
  language policy for this arc
- `function/aws-lambda/<python|typescript|go>/`,
  `function/gcp-cloudfn/<python|typescript|go>/`,
  `function/azure-fn/<python|typescript|dotnet-isolated>/` --
  handler skeletons + minimal IaC reference
- `container/<cloudrun|apprunner>/<python-fastapi|typescript-hono|go-echo>/`
  plus `container/aca/<python-fastapi|typescript-hono|go-echo|dotnet-aspnet>/` --
  Dockerfile + minimal service skeleton
- `k8s/<eks|gke|aks>/{base,overlays/dev,overlays/test}/` -- Kustomize
  starter
- `k8s/helm-chart/` -- Helm chart scaffold with values.dev / values.test
- `smoke-tests/`, `integration-tests/` -- starter test scripts per stack
  family
- `observability/` -- OTel collector config + structured-log fixtures
- `manifest/` -- `profile-summary.template.yaml` for derived repos
- `prompt-first/` -- `PROMPT_01.template.txt`, `PROMPT_02.template.txt`,
  plus `PROMPT_03.template.txt`
  The third template is the graft template used by `work.py graft`.
