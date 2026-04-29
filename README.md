# agent-cloud-context-base (accb)

`agent-cloud-context-base` (`accb`) is a context-first foundation for
generating and running assistant-friendly cloud-native backend repositories.

Status: under construction. The system is being built incrementally through
the `.prompts/PROMPT_NN.txt` sequence (see `.prompts/`).

## Scope

- Serverless functions (AWS Lambda, GCP Cloud Functions, Azure Functions)
- Managed containers (Cloud Run, App Runner, Container Apps)
- Kubernetes platforms (EKS, GKE, AKS)
- Infrastructure as Code (Terraform; Pulumi in TypeScript, Python, Go, .NET)
- First-class dev/test environment isolation for every cloud surface

Derived repos receive a hidden `.accb/` payload that captures the chosen
profile (archetype + primary stack + manifests + support services), the
validation contract, and a session boot document.

## Boot

See `AGENT.md` and `CLAUDE.md`. Once the runtime tools land in PROMPT_05,
start sessions with `python3 scripts/work.py resume`.
