# OTel Collector: Cloud Run Sidecar

Use this collector as a Cloud Run sidecar for `.accb/` services that emit OTLP
traces and logs. The config exports to Google Cloud Trace and Cloud Logging.

Set the app container to send OTLP to `http://localhost:4318` or
`localhost:4317`. Keep dev/test Cloud Run services, service accounts, and log
filters environment-scoped.
