#!/usr/bin/env python3
"""
git-worktree-manager: Manage agent worktrees tied to branches.
- Register a worktree path → branch mapping
- Check if remote branch still exists
- Prune worktrees and local branches when remote is gone
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path.home() / ".openclaw" / "worktrees.json"
LOG_PATH = Path.home() / ".openclaw" / "worktree-log.json"


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text())
    return {}


def save_registry(reg: dict):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2))


def run(cmd: list[str], cwd=None, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=check)


def register(worktree_path: str, branch: str, repo: str, pr: str = "", description: str = ""):
    reg = load_registry()
    reg[worktree_path] = {"branch": branch, "repo": repo, "pr": pr, "description": description}
    save_registry(reg)
    print(f"Registered: {worktree_path} → branch '{branch}' in {repo}")


def list_worktrees():
    reg = load_registry()
    if not reg:
        print("No worktrees registered.")
        return
    for path, info in reg.items():
        print(f"  {path}  branch={info['branch']}  repo={info['repo']}")


def load_log() -> list:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text())
    return []


def append_log(entry: dict):
    log = load_log()
    log.append(entry)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(log, indent=2))


def show_log(limit: int = 20):
    log = load_log()
    if not log:
        print("No completed worktrees logged.")
        return
    for entry in reversed(log[-limit:]):
        pr = entry.get("pr", "—")
        print(f"  [{entry['pruned_at'][:10]}] {entry['repo']}  branch={entry['branch']}  pr={pr}  desc={entry.get('description', '')}")


def remote_branch_exists(repo: str, branch: str) -> bool:
    result = run(["git", "ls-remote", "--heads", "origin", branch], cwd=repo, check=False)
    return branch in result.stdout


def prune(dry_run: bool = False):
    reg = load_registry()
    to_remove = []

    for wt_path, info in reg.items():
        branch = info["branch"]
        repo = info["repo"]

        if remote_branch_exists(repo, branch):
            print(f"[alive]  {branch} still exists on remote — skipping")
            continue

        print(f"[gone]   {branch} no longer on remote — cleaning up {wt_path}")
        if not dry_run:
            # Remove worktree
            run(["git", "worktree", "remove", "--force", wt_path], cwd=repo, check=False)
            # Prune worktree metadata
            run(["git", "worktree", "prune"], cwd=repo, check=False)
            # Delete local branch
            run(["git", "branch", "-D", branch], cwd=repo, check=False)
            to_remove.append(wt_path)
            append_log({
                "pruned_at": datetime.now(timezone.utc).isoformat(),
                "repo": repo,
                "branch": branch,
                "worktree": wt_path,
                "pr": info.get("pr", ""),
                "description": info.get("description", ""),
            })
            print(f"         Removed worktree and local branch '{branch}'")
        else:
            print(f"         [dry-run] would remove worktree and branch '{branch}'")

    for p in to_remove:
        del reg[p]
    if to_remove:
        save_registry(reg)
        print(f"\nCleaned up {len(to_remove)} worktree(s).")
    elif not dry_run:
        print("Nothing to clean up.")


def main():
    parser = argparse.ArgumentParser(description="Git worktree lifecycle manager")
    sub = parser.add_subparsers(dest="cmd")

    reg_p = sub.add_parser("register", help="Register a worktree")
    reg_p.add_argument("path", help="Worktree directory path")
    reg_p.add_argument("branch", help="Branch name")
    reg_p.add_argument("--repo", default=".", help="Repo root (default: cwd)")
    reg_p.add_argument("--pr", default="", help="PR URL (optional)")
    reg_p.add_argument("--description", default="", help="Short description of the task")

    sub.add_parser("list", help="List registered worktrees")

    log_p = sub.add_parser("log", help="Show completed worktree history")
    log_p.add_argument("--limit", type=int, default=20)

    prune_p = sub.add_parser("prune", help="Remove worktrees whose remote branch is gone")
    prune_p.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.cmd == "register":
        register(args.path, args.branch, args.repo, pr=args.pr, description=args.description)
    elif args.cmd == "list":
        list_worktrees()
    elif args.cmd == "prune":
        prune(dry_run=args.dry_run)
    elif args.cmd == "log":
        show_log(limit=args.limit)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
