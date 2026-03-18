---
name: git-worktree-manager
description: Manage git worktrees tied to agent feature branches across any repo. Use when spawning an agent to work on a feature branch (to create a worktree and register it), when checking worktree status, or when pruning stale worktrees after PRs are merged. Handles the full lifecycle: create worktree → register → prune when remote branch is deleted. Works with any git repository.
---

# git-worktree-manager

Manages agent worktrees so branches and directories stay in sync and clean up automatically after PRs merge. Works with any git repo.

## Registry

Worktree metadata is stored at `~/.openclaw/worktrees.json` (path → branch + repo).

## Script

All operations go through `scripts/worktree_manager.py`.

```bash
# Register a worktree after creating it
python3 ~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py \
  register <worktree-path> <branch> --repo <repo-root> \
  [--pr <pr-url>] [--description "short task description"]

# List active registered worktrees
python3 ~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py list

# Prune worktrees whose remote branch no longer exists (logs completed tasks)
python3 ~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py prune [--dry-run]

# Show history of completed/pruned worktrees
python3 ~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py log [--limit 20]
```

## Storage

- Active registry: `~/.openclaw/worktrees.json`
- Completed task log: `~/.openclaw/worktree-log.json` — permanent record of every pruned worktree with date, repo, branch, PR URL, and description

## Agent Task Lifecycle

### 1. Create worktree and register
```bash
REPO=~/Projects/<repo-name>
BRANCH=<branch-name>
WORKTREE=~/Projects/<repo-name>-<feature>

cd $REPO
git fetch origin
git worktree add $WORKTREE -b $BRANCH
python3 ~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py \
  register $WORKTREE $BRANCH --repo $REPO \
  --description "brief description of task"
```

### 2. Agent works in the worktree directory
Agent's cwd should be the worktree path, not the main repo root.

### 3. After PR is merged and remote branch deleted, prune
```bash
python3 ~/.openclaw/workspace/skills/git-worktree-manager/scripts/worktree_manager.py prune
```

Removes the worktree directory and local branch for any entry whose remote branch is gone.

## Periodic Cleanup

Run `prune` after PRs merge, or let the heartbeat handle it daily. Use `--dry-run` to preview.
