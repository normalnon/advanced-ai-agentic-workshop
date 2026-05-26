---
name: qzcli
description: "A kubectl/docker-style CLI for managing GPU compute jobs on the Qizhi (启智) platform."
---

# qzcli

> **Path within category:** `skills/skills-codex/qzcli/SKILL.md`


# qzcli — 启智平台任务管理

A kubectl/docker-style CLI for managing GPU compute jobs on the Qizhi (启智) platform.

**GitHub:** [tianyilt/qzcli_tool](https://github.com/tianyilt/qzcli_tool)

## Installation

```bash
pip install rich requests prompt_toolkit mcp
git clone https://github.com/tianyilt/qzcli_tool
cd qzcli_tool && pip install -e .
```

### MCP Integration (optional)

To use qzcli as an MCP tool directly from Claude Code or Codex:

```bash
# Claude Code
claude mcp add qzcli -- qzcli-mcp

# Codex
codex mcp add qzcli -- qzcli-mcp
```


## Quick Start

```bash
# 1. Login
qzcli login

# 2. Discover and cache workspaces/compute groups (run once, re-run after joining new workspaces)
qzcli res -u

# 3. Check available nodes
qzcli avail

# 4. List running jobs
qzcli ls -c -r
```


## Resource Discovery

```bash
# List cached workspaces
qzcli res --list

# Refresh all workspace resource cache (run this first!)
qzcli res -u

# Refresh a specific workspace
qzcli res -w MY_WORKSPACE -u

# Set a human-readable alias for a workspace
qzcli res -w ws-xxxxxxxx --name "My Workspace"
```


## Job Submission

### Interactive (recommended for first-time use)

```bash
# Full interactive selection: workspace → project → compute group → spec
qzcli create -i

# Interactive for a specific workspace only
qzcli create -i -w "My Workspace"
```

The TUI shows GPU type, availability, and spec status at each level. Press `Enter/→` to go deeper, `←` to go back.

### Non-interactive

```bash
# Using names (resolved from qzcli res cache)
qzcli create \
  --name "my-training-job" \
  --command "bash /path/to/train.sh" \
  --workspace "My Workspace" \
  --compute-group "My Compute Group" \
  --image YOUR_REGISTRY/team/image:tag \
  --instances 4 \
  --priority 10

# Using IDs directly
qzcli create \
  --name "my-job" \
  --command "bash /path/to/train.sh" \
  --workspace ws-YOUR_WORKSPACE_ID \
  --compute-group lcg-YOUR_LCG_ID \
  --spec YOUR_SPEC_ID \
  --image YOUR_REGISTRY/team/image:tag \
  --instances 4
```

**Key parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--name` / `-n` | required | Job name |
| `--command` / `-c` | required | Command to run |
| `--workspace` / `-w` | | Workspace name or ID (`ws-...`) |
| `--compute-group` / `-g` | auto | Compute group name or ID (`lcg-...`) |
| `--spec` / `-s` | auto | Resource spec ID |
| `--image` / `-m` | | Docker image |
| `--instances` | 1 | Number of instances |
| `--shm` | 1200 | Shared memory (GiB) |
| `--priority` | 10 | Priority (1–10) |
| `--dry-run` | | Preview only, don't submit |
| `--json` | | JSON output for scripting |

```bash
# Preview before submitting
qzcli create --name test --command "echo hi" --workspace "My Workspace" \
  --image YOUR_IMAGE --dry-run
```

### Env-var passthrough (for existing submission scripts)

```bash
# Pass vars directly — do NOT use "export VAR; bash script.sh"
WORKSPACE_ID="ws-YOUR_WORKSPACE_ID" \
LCG_ID="lcg-YOUR_LCG_ID" \
SPEC_ID="YOUR_SPEC_ID" \
CHECKPOINT_DIR="/path/to/checkpoint" \
bash YOUR_SUBMIT_SCRIPT.sh
```

### HPC / CPU jobs (Slurm)

```bash
qzcli hpc \
  --name "my-cpu-job" \
  --workspace ws-YOUR_WORKSPACE_ID \
  --compute-group lcg-YOUR_LCG_ID \
  --predef-quota-id YOUR_QUOTA_ID \
  --cpu 55 --mem-gi 300 --instances 30 \
  --image YOUR_REGISTRY/team/cpu-image:tag \
  --entrypoint "cd /path/to/dir && bash run.sh"
```


## Job Management

```bash
# List jobs
qzcli ls -c -w MY_WORKSPACE          # specific workspace
qzcli ls -c --all-ws                 # all workspaces
qzcli ls -c -w MY_WORKSPACE -r       # running only
qzcli ls -c -w MY_WORKSPACE -n 50    # show 50

# Stop a job
qzcli stop JOB_ID

# Job status / details
qzcli status JOB_ID

# Watch all running jobs (refresh every 10s)
qzcli watch -i 10

# Workspace view with GPU utilization
qzcli ws
qzcli ws -a           # all projects
qzcli ws -p "My Project"
```
