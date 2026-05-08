#!/usr/bin/env bash
set -euo pipefail
example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test -f "${example_dir}/k8s/kustomize/base/kustomization.yaml"
test -f "${example_dir}/k8s/helm/Chart.yaml"
test -f "${example_dir}/iac/terraform/dev/backend.tf"
test -f "${example_dir}/iac/terraform/test/backend.tf"
test -f "${example_dir}/iac/pulumi/go/Pulumi.dev.yaml"
test -f "${example_dir}/iac/pulumi/go/Pulumi.test.yaml"
test -f "${example_dir}/keda-autoscaled-workers/README.md"
python3 "${example_dir}/tests/smoke/test_layout.py"
