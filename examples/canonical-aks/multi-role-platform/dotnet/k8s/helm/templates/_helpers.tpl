{{- define "accb.name" -}}multi-role-platform{{- end -}}
{{- define "accb.labels" -}}
app.kubernetes.io/name: {{ include "accb.name" . }}
app.kubernetes.io/managed-by: Helm
accb.dev/runtime-tier: k8s
{{- end -}}
