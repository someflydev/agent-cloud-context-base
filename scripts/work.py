#!/usr/bin/env python3
"""Runtime continuity tool for accb repositories."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_USER = 1
EXIT_ENV = 2


@dataclass(frozen=True)
class RuntimeFileSpec:
    path: str
    example_path: str
    label: str
    stale_days: int


@dataclass(frozen=True)
class RuntimeFileState:
    spec: RuntimeFileSpec
    exists: bool
    age_seconds: float | None
    word_count: int
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class GitAnchor:
    sha: str
    subject: str
    timestamp: str
    timestamp_epoch: float | None
    changed_files: tuple[str, ...]


@dataclass(frozen=True)
class RepoInspection:
    repo_root: str
    git_anchor: GitAnchor | None
    runtime_files: tuple[RuntimeFileState, ...]
    next_step_hint: str
    plan_review_signal: str
    complexity_budget_posture: str
    quota_readiness: str
    relevant_summary: str | None


RUNTIME_FILES = (
    RuntimeFileSpec("PLAN.md", "PLAN.example.md", "PLAN.md", 30),
    RuntimeFileSpec("context/TASK.md", "context/TASK.example.md", "TASK.md", 7),
    RuntimeFileSpec("context/SESSION.md", "context/SESSION.example.md", "SESSION.md", 3),
    RuntimeFileSpec("context/MEMORY.md", "context/MEMORY.example.md", "MEMORY.md", 30),
)

PROMPT_RE = re.compile(r"PROMPT_(\d{2})")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.json = bool(getattr(args, "json_global", False) or getattr(args, "json_sub", False))
    root = repo_root()
    if root is None:
        print("not a git repo", file=sys.stderr)
        return EXIT_ENV
    try:
        return args.func(root, args)
    except UserError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_USER
    except EnvironmentError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ENV


class UserError(Exception):
    pass


class EnvironmentError(Exception):
    pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage accb runtime continuity, prompt state, and startup inspection."
    )
    parser.add_argument("--json", action="store_true", dest="json_global", help="print machine-readable JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    add(sub, "init-project", "Scaffold runtime files from tracked *.example.md files.", cmd_init_project)
    add(sub, "resume", "Print a Session Context Briefing for the current repository state.", cmd_resume)
    add(sub, "checkpoint", "Record a lightweight checkpoint and print runtime-file review hints.", cmd_checkpoint)
    add(sub, "next", "Print the next recommended prompt file from the local prompt sequence.", cmd_next)
    add(sub, "recent-commits", "Print the last 10 commits with timestamps.", cmd_recent_commits)
    add(sub, "verify", "Run available local structural verification commands.", cmd_verify)

    p = add(sub, "start", "Mark a prompt session as started in work/prompt-sessions.log.", cmd_start)
    p.add_argument("prompt", help="prompt filename such as PROMPT_05.txt")

    p = add(sub, "pause", "Mark a prompt session as paused with a required reason.", cmd_pause)
    p.add_argument("prompt", help="prompt filename such as PROMPT_05.txt")
    p.add_argument("--reason", required=True, help="pause reason")

    p = add(sub, "done", "Mark a prompt session as done with a required completion summary.", cmd_done)
    p.add_argument("prompt", help="prompt filename such as PROMPT_05.txt")
    p.add_argument("--summary", required=True, help="completion summary")

    p = add(sub, "log-quota", "Append a quota usage row to work/quota.log.")
    p.set_defaults(func=cmd_log_quota)
    p.add_argument("--assistant", required=True, help="assistant or model name")
    p.add_argument("--used-pct-5h", required=True, type=float, help="five-hour quota percentage used")

    p = add(sub, "budget-report", "Score a declared startup bundle when the feature gate is enabled.", cmd_budget_report)
    p.add_argument("--bundle", action="append", default=[], help="file included in the startup bundle")

    p = add(sub, "route-check", "Preview heuristic routing for free text when the feature gate is enabled.", cmd_route_check)
    p.add_argument("text", nargs="*", help="free-text request to classify")

    p = add(sub, "startup-trace", "Write a startup trace record when the feature gate is enabled.", cmd_startup_trace)
    p.add_argument("--note", default="", help="optional trace note")

    p = add(sub, "graft", "Install a minimal .accb runtime continuity layer into a target repo.", cmd_graft)
    p.add_argument("target", help="target repository path")

    return parser


def add(sub: argparse._SubParsersAction, name: str, description: str, func=None) -> argparse.ArgumentParser:
    parser = sub.add_parser(name, description=description, help=description)
    parser.add_argument("--json", action="store_true", dest="json_sub", help="print machine-readable JSON")
    if func is not None:
        parser.set_defaults(func=func)
    return parser


def repo_root() -> Path | None:
    result = run(["git", "rev-parse", "--show-toplevel"], check=False)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise EnvironmentError(result.stderr.strip() or f"command failed: {' '.join(cmd)}")
    return result


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_work(root: Path) -> Path:
    work = root / "work"
    work.mkdir(exist_ok=True)
    return work


def cmd_init_project(root: Path, args: argparse.Namespace) -> int:
    created: list[str] = []
    skipped: list[str] = []
    missing: list[str] = []
    for spec in RUNTIME_FILES:
        source = root / spec.example_path
        target = root / spec.path
        if not source.exists():
            missing.append(spec.example_path)
            continue
        if target.exists():
            skipped.append(spec.path)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(), encoding="utf-8")
        created.append(spec.path)
    payload = {"created": created, "skipped": skipped, "missing_examples": missing}
    return output(args, payload, "init-project", [f"created: {', '.join(created) or 'none'}", f"skipped: {', '.join(skipped) or 'none'}"])


def inspect_repo(root: Path) -> RepoInspection:
    anchor = git_anchor(root)
    states = tuple(runtime_state(root, spec) for spec in RUNTIME_FILES)
    next_step = extract_next_step(root)
    return RepoInspection(
        repo_root=str(root),
        git_anchor=anchor,
        runtime_files=states,
        next_step_hint=next_step,
        plan_review_signal=plan_review(root, anchor),
        complexity_budget_posture=complexity_posture(root),
        quota_readiness=quota_readiness(root),
        relevant_summary=relevant_summary(root),
    )


def cmd_resume(root: Path, args: argparse.Namespace) -> int:
    inspection = inspect_repo(root)
    if args.json:
        print(json.dumps(asdict(inspection), indent=2))
        return EXIT_OK

    print("Session Context Briefing")
    print("========================")
    if inspection.git_anchor:
        ga = inspection.git_anchor
        print(f"Git anchor: {ga.sha} {ga.subject} ({ga.timestamp})")
        print(f"Changed files: {', '.join(ga.changed_files) if ga.changed_files else 'none recorded'}")
    else:
        print("Git anchor: unavailable")
    print()
    print("Runtime files:")
    for state in inspection.runtime_files:
        age = "missing" if state.age_seconds is None else human_age(state.age_seconds)
        warnings = f" [{'; '.join(state.warnings)}]" if state.warnings else ""
        print(f"- {state.spec.label}: {age}, {state.word_count} words{warnings}")
    print()
    print(f"Next-step hint: {inspection.next_step_hint}")
    print(f"Plan review: {inspection.plan_review_signal}")
    print(f"Complexity budget: {inspection.complexity_budget_posture}")
    print(f"Quota readiness: {inspection.quota_readiness}")
    if inspection.relevant_summary:
        print(f"Relevant summary: {inspection.relevant_summary}")
    else:
        print("Relevant summary: none found")
    return EXIT_OK


def git_anchor(root: Path) -> GitAnchor | None:
    result = run(["git", "log", "-1", "--format=%H%x00%ct%x00%cI%x00%s"], cwd=root, check=False)
    if result.returncode != 0 or not result.stdout.strip():
        return None
    sha, epoch, stamp, subject = result.stdout.rstrip("\n").split("\x00", 3)
    files = run(["git", "show", "--name-only", "--format=", sha], cwd=root, check=False).stdout.splitlines()
    return GitAnchor(sha[:12], subject, stamp, float(epoch), tuple(line for line in files if line.strip()))


def runtime_state(root: Path, spec: RuntimeFileSpec) -> RuntimeFileState:
    path = root / spec.path
    if not path.exists():
        return RuntimeFileState(spec, False, None, 0, ("missing",))
    text = path.read_text(encoding="utf-8", errors="replace")
    age = datetime.now().timestamp() - path.stat().st_mtime
    warnings: list[str] = []
    if age > spec.stale_days * 86400:
        warnings.append(f"stale over {spec.stale_days}d")
    if "<" in text and ">" in text:
        warnings.append("contains placeholders")
    return RuntimeFileState(spec, True, age, len(re.findall(r"\S+", text)), tuple(warnings))


def extract_next_step(root: Path) -> str:
    task = root / "context/TASK.md"
    if task.exists():
        section = section_text(task.read_text(encoding="utf-8", errors="replace"), "Next Safe Step")
        for line in section.splitlines():
            cleaned = line.strip(" -\t")
            if cleaned:
                return f"{cleaned} (from context/TASK.md)"
    next_prompt = compute_next_prompt(root)
    return f"run {next_prompt}" if next_prompt else "no next prompt detected"


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    match = pattern.search(text)
    if not match:
        return ""
    rest = text[match.end():]
    next_heading = re.search(r"^##\s+", rest, re.M)
    return rest[: next_heading.start()] if next_heading else rest


def plan_review(root: Path, anchor: GitAnchor | None) -> str:
    plan = root / "PLAN.md"
    if not plan.exists():
        return "PLAN.md absent; ok if no roadmap change is active"
    if anchor and anchor.timestamp_epoch and plan.stat().st_mtime < anchor.timestamp_epoch:
        return "PLAN.md predates last commit; review if the roadmap changed"
    return "PLAN.md is not older than the last commit"


def complexity_posture(root: Path) -> str:
    prompt = active_prompt(root)
    if prompt:
        return f"prompt-first active ({prompt}); keep one bounded prompt session"
    return "base startup posture; route before loading stack context"


def active_prompt(root: Path) -> str | None:
    tmp = root / "tmp"
    if tmp.exists():
        prompts = sorted(tmp.glob("PROMPT_*_checklist.md"))
        if prompts:
            match = PROMPT_RE.search(prompts[-1].name)
            if match:
                return f"PROMPT_{match.group(1)}"
    return None


def quota_readiness(root: Path) -> str:
    log = root / "work/quota.log"
    if not log.exists():
        return "no quota log"
    lines = [line for line in log.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    if not lines:
        return "quota log empty"
    try:
        row = json.loads(lines[-1])
        used = float(row.get("used_pct_5h", 0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return "quota log present; latest row unreadable"
    if used >= 90:
        return f"low readiness ({used:.1f}% used)"
    if used >= 70:
        return f"watch quota ({used:.1f}% used)"
    return f"ready ({used:.1f}% used)"


def relevant_summary(root: Path) -> str | None:
    prompt = active_prompt(root)
    summaries = root / "memory/summaries"
    if prompt and summaries.exists():
        matches = sorted(summaries.glob(f"{prompt}_*.md"))
        if matches:
            return str(matches[-1].relative_to(root))
    return None


def cmd_checkpoint(root: Path, args: argparse.Namespace) -> int:
    work = ensure_work(root)
    row = {"time": now_iso(), "active_prompt": active_prompt(root), "next_step": extract_next_step(root)}
    append_json(work / "checkpoint.log", row)
    lines = [
        "checkpoint recorded in work/checkpoint.log",
        "review context/TASK.md, context/SESSION.md, and context/MEMORY.md if the boundary changed",
    ]
    return output(args, row, "checkpoint", lines)


def cmd_next(root: Path, args: argparse.Namespace) -> int:
    prompt = compute_next_prompt(root)
    if not prompt:
        raise EnvironmentError("no prompt files found")
    return output(args, {"next": prompt}, "next", [prompt])


def compute_next_prompt(root: Path) -> str | None:
    prompt_dir = root / ".prompts"
    prompts = sorted(int(m.group(1)) for p in prompt_dir.glob("PROMPT_*.txt") if (m := PROMPT_RE.search(p.name)))
    if not prompts:
        return None
    highest = completed_prompt_number(root)
    for number in prompts:
        if number > highest:
            return f".prompts/PROMPT_{number:02d}.txt"
    return None


def completed_prompt_number(root: Path) -> int:
    highest = 0
    sessions = root / "work/prompt-sessions.log"
    if sessions.exists():
        for line in sessions.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "done" and (m := PROMPT_RE.search(str(row.get("prompt", "")))):
                highest = max(highest, int(m.group(1)))
    concept_map = {
        1: "memory/concepts/cloud-arc-bootstrap-genesis.md",
        2: "memory/concepts/cloud-doctrine-foundations.md",
        3: "memory/concepts/cloud-doctrine-and-anchors-complete.md",
        4: "memory/concepts/spec-validation-and-accb-rules.md",
        5: "memory/concepts/runtime-continuity-and-memory.md",
    }
    for number, rel in concept_map.items():
        if (root / rel).exists():
            highest = max(highest, number)
    return highest


def cmd_prompt_status(root: Path, args: argparse.Namespace, status: str, extra: dict[str, Any]) -> int:
    row = {"time": now_iso(), "status": status, "prompt": args.prompt, **extra}
    append_json(ensure_work(root) / "prompt-sessions.log", row)
    return output(args, row, status, [f"{status}: {args.prompt}"])


def cmd_start(root: Path, args: argparse.Namespace) -> int:
    return cmd_prompt_status(root, args, "started", {})


def cmd_pause(root: Path, args: argparse.Namespace) -> int:
    return cmd_prompt_status(root, args, "paused", {"reason": args.reason})


def cmd_done(root: Path, args: argparse.Namespace) -> int:
    return cmd_prompt_status(root, args, "done", {"summary": args.summary})


def cmd_recent_commits(root: Path, args: argparse.Namespace) -> int:
    fmt = "%h%x00%cI%x00%s"
    result = run(["git", "log", "-10", f"--format={fmt}"], cwd=root)
    rows = []
    lines = []
    for line in result.stdout.splitlines():
        short, stamp, subject = line.split("\x00", 2)
        rows.append({"sha": short, "timestamp": stamp, "subject": subject})
        lines.append(f"{stamp} {short} {subject}")
    return output(args, {"commits": rows}, "recent-commits", lines)


def cmd_log_quota(root: Path, args: argparse.Namespace) -> int:
    row = {"time": now_iso(), "assistant": args.assistant, "used_pct_5h": args.used_pct_5h}
    append_json(ensure_work(root) / "quota.log", row)
    return output(args, row, "log-quota", [f"logged {args.used_pct_5h:.1f}% for {args.assistant}"])


def startup_features(root: Path) -> dict[str, bool]:
    path = root / "context/accb/profile-rules.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("startup_features", {})


def gate(root: Path, key: str) -> bool:
    return bool(startup_features(root).get(key, False))


def cmd_budget_report(root: Path, args: argparse.Namespace) -> int:
    if not gate(root, "budget_report_enabled"):
        return gated(args)
    score = len(args.bundle)
    row = {"bundle": args.bundle, "score": score, "posture": "tiny" if score <= 2 else "small"}
    return output(args, row, "budget-report", [f"bundle score: {score}", f"posture: {row['posture']}"])


def cmd_route_check(root: Path, args: argparse.Namespace) -> int:
    if not gate(root, "route_check_enabled"):
        return gated(args)
    text = " ".join(args.text).lower()
    provider = "aws" if "aws" in text or "lambda" in text else "gcp" if "gcp" in text or "cloud run" in text else "azure" if "azure" in text else "unknown"
    tier = "function" if "lambda" in text or "function" in text else "container" if "container" in text or "cloud run" in text else "k8s" if "k8s" in text or "kubernetes" in text else "unknown"
    row = {"provider": provider, "runtime_tier": tier}
    return output(args, row, "route-check", [f"provider: {provider}", f"runtime tier: {tier}"])


def cmd_startup_trace(root: Path, args: argparse.Namespace) -> int:
    if not gate(root, "startup_trace_enabled"):
        return gated(args)
    trace_dir = ensure_work(root) / "startup-traces"
    trace_dir.mkdir(exist_ok=True)
    row = {"time": now_iso(), "note": args.note, "inspection": asdict(inspect_repo(root))}
    path = trace_dir / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    path.write_text(json.dumps(row, indent=2), encoding="utf-8")
    return output(args, {"path": str(path.relative_to(root))}, "startup-trace", [f"wrote {path.relative_to(root)}"])


def gated(args: argparse.Namespace) -> int:
    if args.json:
        print(json.dumps({"status": "gated", "message": "feature gated off in profile-rules.json"}, indent=2))
    else:
        print("feature gated off in profile-rules.json")
    return EXIT_OK


def cmd_verify(root: Path, args: argparse.Namespace) -> int:
    candidates = [
        ["python3", "scripts/validate_context.py"],
        ["python3", "scripts/validate_manifests.py"],
    ]
    results = []
    for cmd in candidates:
        if not (root / cmd[1]).exists():
            results.append({"command": " ".join(cmd), "status": "missing"})
            continue
        result = run(cmd, cwd=root, check=False)
        results.append({"command": " ".join(cmd), "status": "passed" if result.returncode == 0 else "failed", "returncode": result.returncode})
    failed = any(row.get("status") == "failed" for row in results)
    lines = [f"{row['command']}: {row['status']}" for row in results]
    output(args, {"results": results}, "verify", lines)
    return EXIT_ENV if failed else EXIT_OK


def cmd_graft(root: Path, args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise UserError(f"target is not a directory: {target}")
    if not (target / ".git").exists():
        raise EnvironmentError(f"target is not a git repo root: {target}")
    accb = target / ".accb"
    (accb / "scripts").mkdir(parents=True, exist_ok=True)
    (accb / "context/memory").mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts/work.py", accb / "scripts/work.py")
    for name in ["memory-operating-rules.md", "handoff-snapshots.md", "stop-hook-guidance.md", "MEMORY.contract.md", "MEMORY.template.md"]:
        shutil.copy2(root / "context/memory" / name, accb / "context/memory" / name)
    template = root / "templates/prompt-first/PROMPT_03.template.txt"
    message = "prompt template installed"
    if template.exists():
        dest = accb / "templates/prompt-first/PROMPT_03.analysis.txt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template, dest)
    else:
        message = "prompt template not yet populated — install planned for PROMPT_15"
    row = {"target": str(target), "message": message}
    return output(args, row, "graft", [f"wrote .accb runtime continuity layer to {target}", message])


def append_json(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def human_age(seconds: float) -> str:
    if seconds < 60:
        return f"{int(seconds)}s old"
    if seconds < 3600:
        return f"{int(seconds // 60)}m old"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h old"
    return f"{int(seconds // 86400)}d old"


def output(args: argparse.Namespace, payload: dict[str, Any], title: str, lines: list[str]) -> int:
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for line in lines:
            print(line)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
