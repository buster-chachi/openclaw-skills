# git-worktree-manager

Manages git worktrees tied to agent feature branches. Handles the full lifecycle: create → register → prune when the remote branch is deleted. Keeps a permanent log of completed tasks across all projects.

## Prerequisites

- git ≥ 2.5
- python3
- `python-dotenv` (optional, for `.env` support): `pip3 install python-dotenv`

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

Create `~/.openclaw/.env` to override defaults:

```env
# Where agent worktrees are created (default: ~/Projects)
WORKTREE_ROOT=/Users/you/Projects

# OpenClaw data dir for registry/log files (default: ~/.openclaw)
OPENCLAW_DIR=/Users/you/.openclaw
```

## Usage

```bash
SCRIPT=~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py

# Create worktree and register (path auto-derived from WORKTREE_ROOT if omitted)
git -C ~/Projects/my-repo worktree add ../my-repo-my-branch -b my-branch
python3 $SCRIPT register --repo ~/Projects/my-repo my-branch \
  --description "what this task does" [--pr https://github.com/...]

# List active worktrees
python3 $SCRIPT list

# Prune worktrees whose remote branch is gone (runs automatically via heartbeat)
python3 $SCRIPT prune [--dry-run]

# View history of completed tasks
python3 $SCRIPT log [--limit 20]
```

## Data Files

| File | Purpose |
|------|---------|
| `~/.openclaw/worktrees.json` | Active registry |
| `~/.openclaw/worktree-log.json` | Permanent log of completed tasks |
