# Cold Start And Runtime Selection

Runtime selection must fit latency, package shape, and operational cost. Cold starts are acceptable when they fit the user contract and become architectural when they threaten p99 behavior.

## Budget Cold Starts

- Expect AWS Lambda under 1s p99 for typical Python, Node, or Go functions without VPC.
- Add roughly 500ms to 2s for AWS Lambda VPC attachment.
- Add roughly 1s to 3s for JVM or .NET on AWS Lambda unless SnapStart or provisioned concurrency is used.
- Expect GCP Cloud Functions Gen2 under 1s for most runtimes, with min instances available for tighter budgets.
- Expect Azure Functions Consumption around 500ms to 2s, with Premium or Flex for more predictable startup.

## Choose Smaller Runtimes

- Prefer Go, Node, or Python when a function has a tight p99 budget.
- Avoid large dependency trees in request-path functions.
- Keep initialization work outside the hot path where the runtime permits it.
- Use smaller packages before buying provisioned capacity.
- Record language and runtime assumptions in the manifest.

## Use Warm Capacity Deliberately

- Use AWS provisioned concurrency when function latency justifies its cost.
- Use GCP min instances for Cloud Run or Cloud Functions when cold starts violate the contract.
- Use Azure Premium or Flex when Consumption variability is unacceptable.
- Treat warm capacity as an always-on cost.
- Pair warm capacity with budget alarms.

## Escalate When Needed

- Escalate to a managed container when startup, binary needs, or request duration no longer fit a function.
- Increase AWS Lambda memory when CPU-bound work is the bottleneck.
- Document the chosen memory size and reason.
- Test p99-sensitive paths in the deployed runtime.
- Mark completion incomplete when latency assumptions are not measured.
