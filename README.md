# openclaw-skills

A collection of agent skills for [OpenClaw](https://openclaw.ai). Each skill extends what Buster (or any OpenClaw agent) can do.

## Installing a Skill

```bash
# Via ClawHub (if published)
clawhub install <skill-name>

# Manually
cp -r <skill-folder> ~/.openclaw/workspace/skills/
```

## Skills

| Skill | Description | Prerequisites |
|-------|-------------|---------------|
| [git-worktree-manager](./git-worktree-manager/) | Manage agent git worktrees across projects — create, register, prune, and log | git, python3, python-dotenv (optional) |

## Configuration

Skills that support environment overrides read from `~/.openclaw/.env`. See each skill's README for supported variables.
