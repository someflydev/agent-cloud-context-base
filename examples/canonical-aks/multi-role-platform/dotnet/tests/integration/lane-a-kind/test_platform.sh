#!/usr/bin/env bash
set -euo pipefail
ns="$(kubectl get ns -l accb.dev/runtime-tier=k8s -o jsonpath='{.items[0].metadata.name}')"
kubectl wait --for=condition=available deployment --all -n "${ns}" --timeout=120s
kubectl create job --from=cronjob/multi-role-platform-scheduled-export-kind cron-fire-once -n "${ns}" || true
kubectl wait --for=condition=complete job/cron-fire-once -n "${ns}" --timeout=120s || true
