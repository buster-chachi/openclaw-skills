# openclaw-skills

A collection of agent skills for [OpenClaw](https://openclaw.ai). Each skill extends what Buster (or any OpenClaw agent) can do.

## Installing a Skill

```bash
# Install a single skill directly from GitHub (no full clone needed)
SKILL=git-worktree-manager
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/buster-chachi/openclaw-skills.git /tmp/openclaw-skills-tmp && \
  cd /tmp/openclaw-skills-tmp && \
  git sparse-checkout set $SKILL && \
  cp -r $SKILL ~/.openclaw/workspace/skills/ && \
  cd - && rm -rf /tmp/openclaw-skills-tmp

# Via ClawHub (if published)
clawhub install <skill-name>
```

## Skills

| Skill | Description | Prerequisites |
|-------|-------------|---------------|
| [git-worktree-manager](./git-worktree-manager/) | Manage agent git worktrees across projects — create, register, prune, and log | git, python3, python-dotenv (optional) |

## Configuration

Skills that support environment overrides read from `~/.openclaw/.env`. See each skill's README for supported variables.
