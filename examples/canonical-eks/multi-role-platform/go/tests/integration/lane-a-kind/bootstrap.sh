#!/usr/bin/env bash
set -euo pipefail
cluster="${ACCB_KIND_CLUSTER:-accb-canonical-eks}"
kind create cluster --name "${cluster}" --config "$(dirname "$0")/kind-config.yaml"
kubectl config use-context "kind-${cluster}"
kubectl apply -k "$(dirname "$0")/../../../k8s/kustomize/overlays/kind"
echo "ministack replaces managed services for Lane A"
