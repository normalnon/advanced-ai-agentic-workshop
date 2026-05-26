---
name: linear
description: "Standalone CLI for the Linear issue tracker. Zero dependencies beyond Python 3."
---

# linear

> **Path within category:** `linear/SKILL.md`


# Linear CLI

Standalone CLI for the Linear issue tracker. Zero dependencies beyond Python 3.

## Setup

On first use, authenticate via browser OAuth (no API keys needed):

```bash
linear auth
```

Opens the browser for Linear authorization. Uses MCP Dynamic Client Registration + PKCE — credentials are stored at `~/.config/linear/` with `0600` permissions.

The CLI script is bundled at `scripts/linear` within this skill directory. Execute it directly or reference its absolute path.

## Commands

### Create an issue

```bash
linear create "Issue title" \
  --team GLE \
  --state Todo \
  --assignee me \
  --due today \
  --priority high \
  --description "Markdown description" \
  --label "Bug"
```

Priority: `urgent`, `high`, `medium`, `low`, `none` (or 0-4).

Due date: `YYYY-MM-DD`, `today`, `tomorrow`.

### List issues

```bash
linear list --mine --status "In Progress"
linear list --team GLE --status Todo --limit 10
linear list --priority high --json
```

### Show issue details

```bash
linear show GLE-123
linear show GLE-123 --json
```

### Update an issue

```bash
linear update GLE-123 --state "In Progress"
linear update GLE-123 --priority urgent --due 2026-05-01
linear update GLE-123 --assignee me --title "New title"
```

### Add a comment

```bash
linear comment GLE-123 "This is done, merging now"
```

### Workspace info

```bash
linear teams
linear me
linear statuses --team GLE
linear labels --team GLE
```

## Conventions

- Use team key (e.g. `GLE`), not full team name, in `--team` flags.
- Default assignee: `me` unless specified otherwise.
- Default state for new issues: `Todo`.
- Use `--due today` for same-day tasks.
- The CLI outputs human-readable text by default; pass `--json` for machine-readable output.
- When creating issues from conversation context, write a concise title and structured markdown description.
