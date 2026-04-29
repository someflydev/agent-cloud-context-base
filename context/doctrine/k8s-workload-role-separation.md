# K8s Workload Role Separation

Kubernetes topology should reflect workload roles. A shared codebase can produce multiple process classes, but each process class gets its own controller and scaling policy.

## Separate Process Classes

- Run the API as a Deployment with an HPA when request scaling is needed.
- Run workers as a Deployment with KEDA or HPA driven by queue depth.
- Run one-off work as Jobs with explicit parallelism.
- Run schedules as CronJobs.
- Run control-plane components as Deployments with leader election where needed.

## Use One Role Per Pod

- Do not co-locate API, worker, and scheduler roles in one Deployment.
- Give each role its own command, probes, resources, and identity.
- Keep sidecars limited to cross-cutting infrastructure such as proxies or telemetry.
- Avoid multi-process shells as the primary container command.
- Keep logs attributable to the workload role.

## Scale Independently

- Set role-specific resource requests and limits.
- Set role-specific autoscaling metrics.
- Set CronJob concurrencyPolicy.
- Set successfulJobsHistoryLimit and failedJobsHistoryLimit for scheduled work.
- Keep worker concurrency aligned with downstream service quotas.

## Verify Role Boundaries

- Test API readiness separately from worker startup.
- Test queue-drain behavior separately from request handling.
- Test job completion and failure paths.
- Test CronJob schedule and concurrency behavior where practical.
- Stop when one Kubernetes object is asked to own multiple process classes.
