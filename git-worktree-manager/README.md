# git-worktree-manager

Manages git worktrees tied to agent feature branches. Handles the full lifecycle: create → register → prune when the remote branch is deleted. Keeps a permanent log of completed tasks across all projects.

## Compatibility

| OS | Status |
|----|--------|
| macOS | ✅ Fully supported |
| Linux | ✅ Fully supported |
| Windows | ⚠️ Script works but install one-liner requires bash; OpenClaw itself is macOS/Linux only |

## Prerequisites

- git ≥ 2.5
- python3

## Install

```bash
# One-liner from GitHub
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/buster-chachi/openclaw-skills.git /tmp/openclaw-skills-tmp && \
  cd /tmp/openclaw-skills-tmp && \
  git sparse-checkout set git-worktree-manager && \
  cp -r git-worktree-manager ~/.openclaw/workspace/skills/ && \
  cd - && rm -rf /tmp/openclaw-skills-tmp
```

## Configuration

All configuration is via standard environment variables — no config file needed. Set these in your shell profile (`~/.bashrc`, `~/.zshrc`) or export them before running.

| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENCLAW_STATE_DIR` | OpenClaw state directory (native OpenClaw var) | `~/.openclaw` |
| `OPENCLAW_HOME` | Fallback if `OPENCLAW_STATE_DIR` not set (native OpenClaw var) | `~/.openclaw` |
| `WORKTREE_ROOT` | Default root for auto-derived worktree paths | `~/Projects` |

`WORKTREE_ROOT` is only used when no explicit path is passed to `register`. Worktrees can live **anywhere on the filesystem** — the path is recorded in the JSON as-is.

## Usage

```bash
SCRIPT=~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py

# Explicit path — works anywhere
git -C ~/Projects/my-repo worktree add /any/path/on/disk -b my-branch
python3 $SCRIPT register /any/path/on/disk my-branch --repo ~/Projects/my-repo \
  --description "what this task does" [--pr https://github.com/...]

# Omit path — auto-derived as <WORKTREE_ROOT>/<repo>-<branch>
git -C ~/Projects/my-repo worktree add ~/Projects/my-repo-my-branch -b my-branch
python3 $SCRIPT register my-branch --repo ~/Projects/my-repo \
  --description "what this task does"

# List active worktrees
python3 $SCRIPT list

# Prune worktrees whose remote branch is gone (runs automatically via heartbeat)
python3 $SCRIPT prune [--dry-run]

# View history of completed tasks
python3 $SCRIPT log [--limit 20]
```

## Data Files

## JSON Format

**`~/.openclaw/worktrees.json`** — active worktrees (keyed by path):
```json
{
  "/Users/buster/Projects/mm_contact_data-add-html-parser": {
    "branch": "add-html-parser",
    "repo": "/Users/buster/Projects/mm_contact_data",
    "prs": [
      "https://github.com/org/repo/pull/42",
      "https://github.com/org/repo/pull/47"
    ],
    "description": "Add HTML response parser to scrape engine"
  }
}
```

**`~/.openclaw/worktree-log.json`** — append-only history after pruning:
```json
[
  {
    "pruned_at": "2026-03-18T21:00:00+00:00",
    "repo": "/Users/buster/Projects/mm_contact_data",
    "branch": "add-html-parser",
    "worktree": "/Users/buster/Projects/mm_contact_data-add-html-parser",
    "prs": ["https://github.com/org/repo/pull/42"],
    "description": "Add HTML response parser to scrape engine"
  }
]
```

`prs` is always a list — calling `register --pr <url>` appends to it, so multiple review cycles are captured without overwriting history.

## Data Files

| File | Purpose |
|------|---------|
| `~/.openclaw/worktrees.json` | Active registry |
| `~/.openclaw/worktree-log.json` | Permanent log of completed tasks |
