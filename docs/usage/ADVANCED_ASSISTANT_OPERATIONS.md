# Advanced Assistant Operations

Long sessions should stay profile-first. Keep the active provider, runtime tier, language, IaC tool, manifest, support services, and isolation declaration visible in `context/SESSION.md` or the generated repo's `.accb/profile/selection.json`.

## Long Sessions

Use `python3 scripts/work.py checkpoint` after each meaningful boundary: generation, manifest change, docs pass, validation pass, or failed proof. Use `pause` with a reason when credentials, Docker, cloud quota, or operator input blocks the next proof.

## Multi-Agent Work

Split only along disjoint ownership boundaries: docs vs scripts, one provider family vs another, or one generated repo smoke vs another. Each worker should report changed files and proof commands. The integrating assistant owns final validation and must not claim `done` from a delegated summary alone.

## Higher-Autonomy Modes

Enable `budget_report` when context bundles are getting broad or repeated sessions load too much by habit. Enable `startup_trace` when you need an audit record of what the assistant declared it loaded. Enable `route_check` when operator prompts are scenario-heavy and you want a heuristic provider/runtime/archetype preview before manifest selection.

These gates are advisory unless a generated repo profile makes them mandatory. Validation scripts and explicit proof commands remain the completion authority.
