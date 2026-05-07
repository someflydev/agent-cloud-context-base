# OTel Collector: EKS DaemonSet

ADOT-compatible DaemonSet for `.accb/` EKS workloads. It receives OTLP, exports
traces to X-Ray, and writes structured logs to CloudWatch Logs.

Patch `${ENVIRONMENT}` during deployment so dev and test log groups remain
disjoint.
