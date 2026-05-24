---
name: claude-skills
description: Consolidated expert tools and guidelines for claude skills.
---

# 🛠️ Consolidated Skills: CLAUDE-SKILLS
This playbook contains a combined registry of expert capabilities for **claude-skills**.

## 1. Expert Skill: present
> **Path within category:** `present/SKILL.md`


# Present — Narrated Interactive Presentations

Generate a self-contained HTML presentation with dual article/slides mode, ElevenLabs narration, optional GPT Image 2 illustrations, and scroll-reveal animations.

## What This Skill Produces

A single `index.html` file (plus audio and optional image assets) that can be:
- Opened locally in a browser
- Deployed to Vercel, Netlify, or any static host
- Shared as a folder

The output has two modes the viewer can toggle between:
1. **Article mode** — long-form scrollable report with Tufte-inspired typography
2. **Slides mode** — navigable presentation with keyboard/click navigation and narrated audio playback

## Quick Start

```
/present "AI adoption research for Arseny" --slides 12 --voice daniel --images risograph
```

Or with a file:
```
/present path/to/research.md --detail detailed --voice alice
```

## Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `--slides` | 5-20 | 12 | Number of slides |
| `--detail` | `executive`, `standard`, `detailed` | `standard` | Content depth |
| `--voice` | ElevenLabs voice name | `daniel` | Narrator voice |
| `--images` | style name or `none` | `none` | Image generation style |
| `--image-prompt` | custom string | auto | Override image prompt prefix |
| `--output` | path | `./presentation/` | Output directory |
| `--deploy` | vercel project or `none` | `none` | Auto-deploy target |
| `--title` | string | auto | Presentation title |
| `--no-audio` | flag | false | Skip audio generation |

### Detail Levels

- **`executive`** (5-7 slides): Key findings only. One stat slide, one recommendation slide, sources. Best for busy stakeholders who need the bottom line.
- **`standard`** (10-14 slides): Full narrative arc. Problem, evidence, analysis, recommendations, sources. The default for most presentations.
- **`detailed`** (15-20 slides): Deep dive. Includes methodology, multiple evidence sections, case studies, detailed recommendations with implementation steps.

### Voice Options

Uses ElevenLabs API. The key must be available in `~/claude-skills/elevenlabs-tts/.env` as `ELEVENLABS_API_KEY`.

Recommended voices for presentations:
- **daniel** — Steady Broadcaster, British, formal (default)
- **alice** — Clear Educator, British, professional
- **matilda** — Knowledgeable, American, upbeat
- **brian** — Deep Resonant, American, comforting
- **george** — Warm Storyteller, British, mature

### Image Styles

When `--images` is set, the skill generates illustrations for key slides using GPT Image 2 (`~/.claude/skills/gpt-image-2/scripts/gpt_image_2.py`). Available styles:

- `risograph` — Gerd Arntz isotype style, muted colors, sand texture
- `editorial` — Magazine photography style, dramatic lighting
- `blueprint` — Technical drawing aesthetic, white on blue
- `ink` — Black ink illustration, hand-drawn feel
- `constellation` — Data visualization aesthetic, dots and lines
- Custom: pass `--image-prompt "your style description"` to override

Images are generated in `--draft` mode first (~$0.006/image). The skill decides which slides benefit from illustration (typically 3-5 out of 12).

## Workflow

### Step 1: Content Analysis

Read the input content (a topic description, a markdown file, vault notes, meeting transcript, or research). Identify:
- The core argument or narrative
- Key data points and statistics
- Natural section breaks
- Quotable findings with sources

### Step 2: Slide Planning

Based on `--detail` and `--slides`, create a slide plan. Each slide needs:

```
Slide N: [Type] — [Title]
Content: [what appears on screen]
Narration: [what the voice says — always more than what's on screen]
Read time: [seconds for an average reader to absorb the visual content]
Image: [yes/no, with prompt if yes]
```

Slide types: `title`, `summary`, `stat`, `evidence`, `comparison`, `quote`, `framework`, `recommendation`, `case-study`, `sources`

The narration script should be conversational and add context beyond what's displayed. It should NOT just read the slide text aloud — it should explain, connect, and elaborate. Target 15-30 seconds of narration per slide.

### Step 3: Generate Audio

For each slide, generate narration using ElevenLabs:

```bash
python3 ~/.claude/skills/elevenlabs-tts/scripts/elevenlabs_tts.py \
  --voice <voice_name> \
  --text "<narration>" \
  --output <output_dir>/audio/slide-<N>.mp3
```

Or use the direct API via the script at `scripts/generate_audio.py` in this skill.

Also generate a transition sound (Rhodes chord) for slide-to-slide transitions.

After generation, get durations with ffprobe to calculate slide timing.

### Step 4: Generate Images (if enabled)

For slides that benefit from illustration, generate images using GPT Image 2:

```bash
python3 ~/.claude/skills/gpt-image-2/scripts/gpt_image_2.py --draft --size 1536x1024 \
  "<style prefix> <slide-specific prompt>" \
  <output_dir>/images/<name>.png
```

Typically generate 3-5 images for a 12-slide deck. Choose slides where a visual metaphor strengthens the point — stat slides, concept slides, and the title slide are good candidates. Don't illustrate every slide.

### Step 5: Build HTML

Use the template at `assets/template.html` as the base. The template includes:

- **Typography**: EB Garamond (body) + DM Sans (labels/numbers)
- **Color palette**: Configurable via CSS variables in `:root`
- **Article mode**: Tufte-inspired layout with executive summary box, stat cards, two-column sections, data tables
- **Slides mode**: Full-viewport slides with fade transitions, keyboard navigation (arrows, space), dot indicators
- **Audio engine**: Single reusable `<audio>` element, slide-synced playback with progress bar, transition sounds between slides
- **Auto-hide controls**: Top bar (mode switcher + audio) appears when cursor enters top 20% of viewport. Bottom nav appears in bottom 20%. Shift+. toggles always-show/always-hide/zone mode.
- **Scroll-reveal animations**: Intersection Observer-based fade-up for sections, staggered stat cards, animated counters, h2 rule-draw effect
- **`prefers-reduced-motion`**: All animations disabled when user prefers reduced motion

Populate the template by replacing placeholder sections with the actual slide and article content.

### Step 6: Test

Open in browser using `/real-browser` or `open <path>`. Verify:
- [ ] Article mode renders correctly, images load
- [ ] Slides mode: all slides navigable, text fits within viewport
- [ ] Audio plays when play button is clicked
- [ ] Audio syncs to slide advancement (each slide waits for narration + read time)
- [ ] Transition sounds play between slides
- [ ] Auto-hide works for top and bottom bars
- [ ] Keyboard navigation (arrows, space) works in slide mode

### Step 7: Deploy (if requested)

If `--deploy` is set, copy output to the target project's `public/` folder and deploy:

```bash
cp -r <output_dir>/* <project_path>/public/<slug>/
cd <project_path> && vercel deploy --prod --yes
```

## HTML Architecture

### Audio Sync Model

Each slide has three timing properties:
- `data-audio="slide-name"` — maps to audio file
- `data-read-time="N"` — seconds for reading the visual content

The audio engine calculates: `slide_duration = max(audio_duration, read_time) + 2s`. After narration ends, it waits for any remaining read time plus a 2-second buffer, plays a transition sound (1.8s), then advances to the next slide.

### Avoiding AI-Looking Formatting

The following patterns read as AI-generated and should be avoided:
- Colored left-bar + bold heading + description blocks (finding cards)
- Large italic pull quotes with colored left border
- Uniform card grids with icon + heading + description
- Gradient text on metrics

Instead use:
- Natural prose paragraphs with inline emphasis
- Definition lists (`<dl>`) for structured points
- Tables for comparisons
- Direct statements woven into flowing text

### Image Paths

Use absolute paths from the deployment root: `/slug/images/name.png`, not relative paths. Relative paths break when URLs load without trailing slashes.

## Files

- `SKILL.md` — This file
- `scripts/generate_audio.py` — ElevenLabs TTS batch generator
- `assets/template.html` — Base HTML template with all CSS/JS
- `references/slide-types.md` — Detailed slide type specifications and examples


================================================================================

## 2. Expert Skill: granola
> **Path within category:** `granola/SKILL.md`


# Granola Meeting Importer

Query Granola via Personal API to list notes, view transcripts, and export to Obsidian vault in the same format as the Fathom skill.

## Prerequisites

- Granola Business or Enterprise plan (Personal API required)
- API key in sops-encrypted `~/Brains/brain/.env.granola` as `GRANOLA_API_KEY=grn_...`
- No additional dependencies (uses stdlib only)

## Usage

```bash
python3 ~/.claude/skills/granola/scripts/granola.py <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `list` | List notes from Personal API |
| `show <note_id>` | Show note details (summary, attendees, optionally transcript) |
| `export <note_id>` | Export note to Obsidian markdown (Fathom-compatible format) |

### Options

| Option | Applies to | Description |
|--------|-----------|-------------|
| `--format text\|json` | list, show | Output format (default: text) |
| `--after <ISO date>` | list | Filter notes created after date |
| `--all` | list | Paginate through all results |
| `--transcript` | show | Include transcript in output |
| `--vault <path>` | export | Obsidian vault path (default: ~/Brains/brain) |
| `--output <path>` | export | Custom output file path |

## Examples

### List recent meetings
```bash
python3 ~/.claude/skills/granola/scripts/granola.py list
python3 ~/.claude/skills/granola/scripts/granola.py list --format json
python3 ~/.claude/skills/granola/scripts/granola.py list --after 2026-05-01
```

### Show note with transcript
```bash
python3 ~/.claude/skills/granola/scripts/granola.py show not_5FkswTp4Omkpm5
python3 ~/.claude/skills/granola/scripts/granola.py show not_5FkswTp4Omkpm5 --transcript --format json
```

### Export to Obsidian
```bash
python3 ~/.claude/skills/granola/scripts/granola.py export not_5FkswTp4Omkpm5
python3 ~/.claude/skills/granola/scripts/granola.py export not_5FkswTp4Omkpm5 --vault ~/Brains/brain
```

## Output Format

Exported notes match Fathom skill format for consistency:

```markdown

# Meeting Title

## Summary
{AI-generated summary}

## Transcript
**Speaker Name**: What they said...
```

Files saved as: `YYYYMMDD-meeting-title-slug.md`

## API Details

- **Base URL**: `https://public-api.granola.ai/v1`
- **Auth**: Bearer token (Personal API key, never expires)
- **Rate limits**: 25 req burst / 5 req/sec sustained
- **Important**: API only returns notes with generated summaries — in-progress meetings won't appear

## Known Limitations

- **No live/in-progress access** — notes appear only after Granola generates the AI summary
- **No per-utterance speaker names** — Granola provides `source` (microphone vs speaker) and optional `diarization_label`. Export assigns meeting owner to microphone utterances
- **Note IDs required** — use `list` first to get `not_xxxx` IDs, then `show`/`export`

## Integration

- **transcript-analyzer**: After export, run transcript-analyzer on the output file for deeper analysis
- **Fathom skill**: Granola exports use the same frontmatter and transcript format as Fathom exports, so downstream tools work with both


================================================================================

## 3. Expert Skill: ecosystem
> **Path within category:** `ecosystem/SKILL.md`


# Ecosystem Audit

On-demand audit of the Claude Code ecosystem. Runs 4 checks, prints a full report with an attention summary, and appends a summary to today's daily note.

## Workflow

Run all 4 checks sequentially using the bash blocks below. Each block runs in a fresh shell, so after all checks complete, compose the daily note summary and attention rollup from the terminal output you've collected.

**CRITICAL**: Run `date +"%Y%m%d"` before writing to the daily note.

### Step 1: Skill Health

Scan `~/.claude/skills/` for skill freshness and broken symlinks.

```bash
NOW=$(date +%s)
D30=$((NOW - 30*86400))
D90=$((NOW - 90*86400))
ACTIVE="" BROKEN=""
ACTIVE_N=0 RECENT_N=0 STALE_N=0 BROKEN_N=0 TOTAL=0

for entry in ~/.claude/skills/*/; do
  [ -d "$entry" ] || continue
  name=$(basename "$entry")
  TOTAL=$((TOTAL + 1))

  if [ -L "${entry%/}" ] && [ ! -e "${entry%/}" ]; then
    target=$(readlink "${entry%/}")
    BROKEN="${BROKEN}  - ${name} -> ${target}\n"
    BROKEN_N=$((BROKEN_N + 1))
    continue
  fi

  real_path="$entry"
  if [ -L "${entry%/}" ]; then
    real_path="$(readlink "${entry%/}")/"
  fi

  newest=$(find "$real_path" -type f -exec stat -f %m {} + 2>/dev/null | sort -rn | head -1)
  [ -z "$newest" ] && newest=0

  if [ "$newest" -ge "$D30" ]; then
    ACTIVE="${ACTIVE}, ${name}"
    ACTIVE_N=$((ACTIVE_N + 1))
  elif [ "$newest" -ge "$D90" ]; then
    RECENT_N=$((RECENT_N + 1))
  else
    STALE_N=$((STALE_N + 1))
  fi
done

echo "### Skills (${TOTAL} total)"
echo "- Active (30d): ${ACTIVE_N}${ACTIVE:+ — ${ACTIVE:2}}"
echo "- Recent (30-90d): ${RECENT_N}"
echo "- Stale (>90d): ${STALE_N}"
echo "- Broken symlinks: ${BROKEN_N}"
[ -n "$BROKEN" ] && printf "$BROKEN"
```

### Step 2: Project Pulse

Scan `~/ai_projects/` for git repo activity and CLAUDE.md presence. Cap dormant and abandoned lists at 10 names to keep output readable.

```bash
NOW=$(date +%s)
D30=$((NOW - 30*86400))
D180=$((NOW - 180*86400))
ACTIVE="" DORMANT="" ABANDONED="" DORMANT_N=0 ABANDONED_N=0 NO_CLAUDE=0
ACTIVE_N=0 GIT_TOTAL=0 DIR_TOTAL=0 NODATA=0

for dir in ~/ai_projects/*/; do
  [ -d "$dir" ] || continue
  DIR_TOTAL=$((DIR_TOTAL + 1))
  [ -d "${dir}.git" ] || continue
  GIT_TOTAL=$((GIT_TOTAL + 1))

  last_commit=$(git -C "$dir" log -1 --format=%ct 2>/dev/null)
  if [ -z "$last_commit" ]; then
    NODATA=$((NODATA + 1))
    continue
  fi

  name=$(basename "$dir")

  if [ "$last_commit" -ge "$D30" ]; then
    ACTIVE="${ACTIVE}, ${name}"
    ACTIVE_N=$((ACTIVE_N + 1))
  elif [ "$last_commit" -ge "$D180" ]; then
    DORMANT_N=$((DORMANT_N + 1))
    [ "$DORMANT_N" -le 10 ] && DORMANT="${DORMANT}, ${name}"
  else
    ABANDONED_N=$((ABANDONED_N + 1))
    [ "$ABANDONED_N" -le 10 ] && ABANDONED="${ABANDONED}, ${name}"
  fi

  [ ! -f "${dir}CLAUDE.md" ] && NO_CLAUDE=$((NO_CLAUDE + 1))
done

DORMANT_SUFFIX=""
[ "$DORMANT_N" -gt 10 ] && DORMANT_SUFFIX=" and $((DORMANT_N - 10)) more"
ABANDONED_SUFFIX=""
[ "$ABANDONED_N" -gt 10 ] && ABANDONED_SUFFIX=" and $((ABANDONED_N - 10)) more"

echo ""
echo "### Projects (${DIR_TOTAL} dirs, ${GIT_TOTAL} git repos)"
echo "- Active (30d): ${ACTIVE_N}${ACTIVE:+ — ${ACTIVE:2}}"
echo "- Dormant (30-180d): ${DORMANT_N}${DORMANT:+ — ${DORMANT:2}${DORMANT_SUFFIX}}"
echo "- Abandoned (>6mo): ${ABANDONED_N}${ABANDONED:+ — ${ABANDONED:2}${ABANDONED_SUFFIX}}"
[ "$NODATA" -gt 0 ] && echo "- No data (empty/corrupt): ${NODATA}"
echo "- Missing CLAUDE.md: ${NO_CLAUDE}"
```

### Step 3: CLAUDE.md Drift

Check if CLAUDE.md files are stale relative to their project's latest commit. Uses git commit dates (not filesystem mtime) for accuracy.

```bash
NOW=$(date +%s)
STALE_LIST="" STALE_N=0
UNTRACKED_LIST="" UNTRACKED_N=0

while IFS= read -r claude_file; do
  project_dir=$(dirname "$claude_file")
  while [ ! -d "${project_dir}/.git" ] && [ "$project_dir" != "$HOME/ai_projects" ]; do
    project_dir=$(dirname "$project_dir")
  done
  [ -d "${project_dir}/.git" ] || continue

  claude_commit=$(git -C "$project_dir" log -1 --format=%ct -- "$claude_file" 2>/dev/null)
  project_commit=$(git -C "$project_dir" log -1 --format=%ct 2>/dev/null)
  [ -z "$project_commit" ] && continue

  if [ -z "$claude_commit" ]; then
    rel_path="${claude_file#$HOME/}"
    UNTRACKED_LIST="${UNTRACKED_LIST}  - ~/${rel_path}\n"
    UNTRACKED_N=$((UNTRACKED_N + 1))
    continue
  fi

  diff=$((project_commit - claude_commit))
  if [ "$diff" -gt $((90*86400)) ]; then
    rel_path="${claude_file#$HOME/}"
    claude_date=$(date -r "$claude_commit" +%Y-%m-%d)
    project_date=$(date -r "$project_commit" +%Y-%m-%d)
    STALE_LIST="${STALE_LIST}  - ~/${rel_path} (last: ${claude_date}, project: ${project_date})\n"
    STALE_N=$((STALE_N + 1))
  fi
done < <(find ~/ai_projects -maxdepth 2 -name CLAUDE.md 2>/dev/null)

echo ""
echo "### CLAUDE.md Drift"
echo "- Stale instructions (>90d behind project): ${STALE_N}"
[ -n "$STALE_LIST" ] && printf "$STALE_LIST"
echo "- Untracked: ${UNTRACKED_N}"
[ -n "$UNTRACKED_LIST" ] && printf "$UNTRACKED_LIST"
```

### Step 4: Mac Mini Health

SSH to agents-mac-mini and check services. Uses `-T` to avoid pseudo-tty and `ECOSYS:` prefix to filter iTerm escape codes from the output.

Custom services on the Mac Mini use various prefixes (`com.server.*`, `com.telegram-agent.*`, `com.photopulse.*`, `com.health.*`, `com.temporal.*`, `ai.hermes.*`, etc.), so count all non-Apple LaunchAgents.

```bash
echo ""
echo "### Mac Mini"

MINI_OUTPUT=$(ssh -T -o ConnectTimeout=5 -o BatchMode=yes mac-mini 'export TERM=dumb; thumb=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null); viz=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://localhost:8081/ 2>/dev/null); agents=$(launchctl list 2>/dev/null | tail -n +2 | awk "{print \$3}" | grep -cv "^com\.apple" || echo 0); hdb_size=$(stat -f %z ~/ai_projects/health-import/health.db 2>/dev/null || echo 0); echo "ECOSYS:${thumb}|${viz}|${agents}|${hdb_size}"' 2>/dev/null)

DATA=$(echo "$MINI_OUTPUT" | grep "^ECOSYS:" | sed 's/^ECOSYS://')

if [ -z "$DATA" ]; then
  echo "- Status: UNREACHABLE (SSH failed)"
else
  IFS='|' read -r THUMB VIZ AGENTS HDB_SIZE <<< "$DATA"
  [ "$THUMB" = "200" ] && echo "- Thumb server (:8080): UP" || echo "- Thumb server (:8080): DOWN (${THUMB})"
  [ "$VIZ" = "200" ] && echo "- Viz server (:8081): UP" || echo "- Viz server (:8081): DOWN (${VIZ})"
  echo "- Custom LaunchAgents: ${AGENTS}"
  if [ "$HDB_SIZE" -gt 0 ] 2>/dev/null; then
    HDB_GB=$(echo "scale=1; ${HDB_SIZE}/1073741824" | bc)
    echo "- Health DB: ${HDB_GB} GB"
  else
    echo "- Health DB: NOT FOUND"
  fi
fi
```

### Step 5: Attention Summary + Daily Note

After printing the full terminal report, add an attention summary highlighting anything that needs action:

```
### Attention
- [list any: broken symlinks, services DOWN, stale CLAUDE.md, Mac Mini unreachable]
- If nothing needs attention: "All clear."
```

Then compose a summary and write it to today's daily note.

Get today's date first:

```bash
TODAY=$(date +"%Y%m%d")
```

Build the summary block from the results you collected in Steps 1-4 (re-read the terminal output above — variables don't carry across bash blocks). Format:

```markdown
## Ecosystem

Skills: N active / N recent / N stale / N broken
Projects: N active / N dormant / N abandoned
CLAUDE.md drift: N stale, N untracked
Mac Mini: [status summary]

_Ecosystem audit · YYYY-MM-DD_
```

Write to `~/Brains/brain/Daily/${TODAY}.md`:
- If `## Ecosystem` section already exists, replace everything from `## Ecosystem` to the next `##` heading (or `- - -` separator)
- If it doesn't exist, insert above the first `- - -` separator
- If any red flags (broken symlinks > 0, services down, stale CLAUDE.md > 3), prepend `> [!warning] Ecosystem issues detected`


================================================================================

## 4. Expert Skill: tufte-report
> **Path within category:** `tufte-report/SKILL.md`


# Tufte Report — Data-Driven Infographic Skill

Create standalone HTML reports that combine editorial narrative with interactive data visualization in Edward Tufte's style: high information density, minimal chart junk, typography-first design.

## Design Philosophy

Tufte's core principles drive every decision:
- **Data-ink ratio**: every pixel of ink should represent data, not decoration
- **Small multiples**: repeat a design to show comparison, not animation
- **Sparklines**: word-sized graphics that live inside prose
- **Layering**: overview first, then detail on demand
- **Integration**: text and graphics share the same visual space (sidenotes, not footnotes)

The report should feel like a well-edited magazine feature — you read it top to bottom, narrative carries you through the data, and every chart earns its space by answering a specific question.

## Onboarding — Ask Before Building

Before writing ANY code, ask these questions. Do not proceed until all are answered:

1. **What data sources do you have?** (CSV, JSON, SQLite, API endpoint, or raw numbers)
2. **What is the primary question this report should answer?** (one sentence — this becomes the title and drives all design decisions)
3. **How many sections do you need?** (cap at 8 — push back if more are requested; each section should answer one sub-question)
4. **What's the output format?** (standalone HTML file, or embedded component)
5. **Time budget?** Provide an estimate:
   - 1-2 sections with tables only: ~200 LOC, ~5 min bypass / ~10 min manual
   - 3-4 sections with 2-3 charts: ~500 LOC, ~15 min bypass / ~25 min manual
   - 5-8 sections with charts + health data + sparklines: ~1200 LOC, ~30 min bypass / ~50 min manual

## Scope Protection

This skill enforces hard limits to prevent scope creep:

- **Max 8 sections** — if the user asks for more, suggest combining related topics
- **Max 2 chart types per section** — a section gets one primary chart and optionally one supporting chart or table. More than that means the section should split
- **Max 3 colors per chart** — beyond that, use small multiples instead of rainbow legends
- **No 3D charts, no pie charts, no donut charts** — these violate Tufte principles
- **No gratuitous animation** — scroll-reveal on enter is fine; spinning, bouncing, or pulsing is not
- **Every chart must have a caption** — if you can't write a one-sentence caption explaining what the chart shows, the chart shouldn't exist

When the user asks for something outside these limits, respond with: "That would take the report from [current LOC estimate] to [new estimate]. The extra complexity adds [X] but risks [Y]. Shall I proceed, or can we [simpler alternative]?"

## Architecture

```
report.html (standalone, no build step)
├── Google Fonts CDN (EB Garamond)
├── jsDelivr CDN (Monaspace Argon woff2)
├── jsDelivr CDN (Chart.js 4.x UMD)
├── Inline <style> (design system CSS)
├── Inline HTML (semantic structure)
└── Inline <script> (data + Chart.js configs + sparklines + scroll-reveal)
```

No build tools, no frameworks, no npm. One file, opens in any browser.

## Design System

Read `references/design-tokens.md` for the complete CSS variables, typography scale, and color palette.

Read `references/components.md` for the HTML+CSS snippet of every reusable component.

Read `references/charts.md` for Chart.js configuration patterns and inline SVG sparkline code.

## Report Structure Template

Every report follows this skeleton:

```
1. Title + subtitle + data source tags (monospace, subtle)
2. [Optional] Status dashboard (4-column KPI strip)
3. Overview narrative with inline sparklines + TOC sidebar
4. Summary cards (2-4 KPI tiles with sparklines)
5. Sections (each: state-line → chart+narrative aside → table+narrative aside)
6. [Optional] Decision register (threshold table with status colors)
7. Footer (generation date, sources)
```

### Section Pattern

Each section follows this rhythm:
```
<h2> with ↑ back-to-top link
<p class="state-line"> — one italic sentence, the takeaway
<div class="aside-container"> — chart on left, narrative on right
<div class="aside-container"> — table on left, interpretation on right
```

The alternation of chart→narrative→table→narrative creates visual breathing room and prevents "wall of data" fatigue.

### Rules for Narrative Text

- **State-lines** (the italic intro under each heading): one sentence, max 20 words, states the conclusion not the topic. "HRV down 13%, steps down 42%" not "This section covers health metrics"
- **Aside narratives**: 3-4 short paragraphs, each starting with a bold keyword. Written like a newspaper sidebar — facts first, interpretation second
- **Flyouts**: reserved for actionable insights or methodology notes. The ✦ symbol marks them as "pay attention"
- **No "tells its own story"** or similar filler. Every sentence should contain a number or a decision

## Dual-Font Strategy

| Context | Font | Why |
|---------|------|-----|
| All body text, headers, captions | EB Garamond | Classical editorial feel, excellent readability |
| All numbers in tables | Monaspace Argon | Tabular figures align in columns, monospace scannability |
| Big numbers in cards/dashboards | Monaspace Argon | Visual weight, distinct from prose |
| Status indicators, trend percentages | Monaspace Argon | Precision signaling |
| Data source tags, code references | Monaspace Argon | Technical register |
| Ornament separators (:::) | Monaspace Argon with ligatures | Programming aesthetic, replaces floral Unicode |

## Color Principles

Use `--ink` (near-black) for text, `--bg` (warm white) for background. Chart colors must be semantically meaningful — don't assign colors randomly:

- **Orange** (`--spark-claude`, #c45a28): primary data stream, effort/work metrics
- **Green** (`--spark-wispr`, #2a7a5a): growth, positive health signals, English language
- **Purple** (`--spark-social`, #5a5aaa): social/communication metrics
- **Blue** (rgba(42,80,140)): secondary overlay lines on charts
- **Red** (#a02a2a): alerts, negative trends, declining metrics
- **Amber** (#c89000): warnings, watch-level signals
- **Green** (#2a7a3a): healthy baselines, positive trends

Never use more than 3 colors in a single chart. If you need more, use opacity/saturation variations of the same hue.

## Session Lessons (What Goes Wrong)

Based on building the reference report, these are the recurring problems:

1. **Chart.js CDN version**: Use `@4` not a specific patch version — specific versions may not exist
2. **Chart.js defaults**: Set individual properties, never replace entire objects (`Chart.defaults.scale.grid.color = '#eee'` not `Chart.defaults.scale.grid = {color: '#eee'}`)
3. **Legend circles**: Use `usePointStyle: false` with `boxWidth: 8, boxHeight: 8, borderRadius: 4` for true circles. `usePointStyle: true` creates ovals
4. **file:// protocol**: Charts won't load CDN scripts via file://. Always test via localhost
5. **Back-to-back charts**: Always separate consecutive charts with narrative, a table, or an ornament. Two charts in a row = "wall of data"
6. **Table overflow on mobile**: Wrap in `.table-wrapper` and add `.hide-mobile` to secondary columns
7. **Dual-axis charts**: Use sparingly — they invite false visual equivalence. Always label both axes clearly
8. **Narrative overreach**: Don't claim correlations without computing them. "r = 0.10" is more trustworthy than "strong relationship"

## Universal Data Adapter

When the user provides data from any source (CSV, JSON, SQLite, API, raw numbers), normalize it into the standard **ReportData** intermediate format before generating HTML. This decouples data ingestion from report rendering.

Read `references/data-adapter.md` for the ReportData JSON schema, field reference, and adapter instructions for each source type.

**Workflow:**
1. User provides data → identify source type
2. Transform into ReportData JSON (ask user for `meta.question` and desired sections)
3. Confirm the normalized structure with the user
4. Generate HTML from the ReportData using the block library

## Composable Block Library

Reports are assembled from typed blocks, each with a defined data contract. This replaces ad-hoc HTML generation with a systematic approach.

Read `references/blocks.md` for the complete block catalog: sparkline-row, kpi-card, trend-chart, data-table, correlation-matrix, narrative, heatmap, strip-chart.

Each block defines:
- **Data contract** (what JSON shape it expects)
- **HTML template** (copy-paste ready)
- **Composition rules** (how blocks pair and sequence)

## Preview Server

For iterative development, use the built-in live-reload server:

```bash
python3 ~/.claude/skills/tufte-report/scripts/serve.py report.html
```

Serves on `localhost:8042`, auto-reloads on file change with scroll position preserved. Zero dependencies — Python stdlib only.

Read `references/preview-server.md` for details. After generating a report, offer to start the preview server for the user.


================================================================================

## 5. Expert Skill: llm-cli
> **Path within category:** `llm-cli/SKILL.md`


# LLM CLI Skill

## Purpose

This skill enables seamless interaction with multiple LLM providers (OpenAI, Anthropic, Google Gemini, Ollama) through the `llm` CLI tool. It processes textual and multimedia information with support for both one-off executions and interactive conversation modes.

## When to Use This Skill

Trigger this skill when:
- User wants to process text/files with an LLM
- User needs to choose between multiple available LLMs
- User wants interactive conversation with an LLM
- User needs to pipe content through an LLM for processing
- User wants to use specific model aliases (e.g., "claude-opus", "gpt-4o")

Example user requests:
- "Process this file with Claude"
- "Analyze this text with the fastest available model"
- "Start an interactive chat with OpenAI"
- "Use Gemini to summarize this document"
- "Chat mode with my local Ollama instance"

## Supported Providers & Models

### OpenAI
- **Latest Models (2025)**:
  - `gpt-5` - Most advanced model
  - `gpt-4-1` / `gpt-4.1` - Latest high-performance
  - `gpt-4-1-mini` / `gpt-4.1-mini` - Smaller, faster version
  - `gpt-4o` - Multimodal omni model
  - `gpt-4o-mini` - Lightweight multimodal
  - `o3` - Advanced reasoning
  - `o3-mini` / `o3-mini-high` - Reasoning variants

**Aliases**: `openai`, `gpt`

### Anthropic
- **Latest Models (2025)**:
  - `claude-sonnet-4.5` - Latest flagship model
  - `claude-opus-4.1` - Complex task specialist
  - `claude-opus-4` - Coding specialist
  - `claude-sonnet-4` - Balanced performance
  - `claude-3.5-sonnet` - Previous generation
  - `claude-3.5-haiku` - Fast & efficient

**Aliases**: `anthropic`, `claude`

### Google Gemini
- **Latest Models (2025)**:
  - `gemini-2.5-pro` - Most advanced
  - `gemini-2.5-flash` - Default fast model
  - `gemini-2.5-flash-lite` - Speed optimized
  - `gemini-2.0-flash` - Previous generation
  - `gemini-2.5-computer-use` - UI interaction

**Aliases**: `google`, `gemini`

### Ollama (Local)
- **Popular Models**:
  - `llama3.1` - Meta's latest (8b, 70b, 405b)
  - `llama3.2` - Compact versions (1b, 3b)
  - `mistral-large-2` - Mistral flagship
  - `deepseek-coder` - Code specialist
  - `starcode2` - Code models

**Aliases**: `ollama`, `local`

## Workflow Overview

```
User Input (with optional model)
    ↓
Check Available Providers (env vars)
    ↓
Determine Model to Use:
  - If specified: Use provided model
  - If ambiguous: Show selection menu
  - Otherwise: Use last remembered choice
    ↓
Load/Create Config (~/.claude/llm-skill-config.json)
    ↓
Detect Input Type:
  - stdin/piped
  - file path
  - inline text
    ↓
Execute llm CLI:
  - Non-interactive: Process & return
  - Interactive: Keep conversation loop
    ↓
Save Model Choice to Config
```

## Features

### 1. Provider Detection
- Checks environment variables for API keys
- Suggests available LLM providers on first run
- Detects: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `OLLAMA_BASE_URL`

### 2. Model Selection
- Accept model aliases (`gpt-4o`, `claude-opus`, `gemini-2.5-pro`)
- Accept provider aliases (`openai`, `anthropic`, `google`, `ollama`)
- Interactive menu when selection is ambiguous
- Remembers last used model in `~/.claude/llm-skill-config.json`

### 3. Input Processing
- Accepts stdin/piped input
- Processes file paths (detects: .txt, .md, .json, .pdf, images)
- Handles inline text prompts
- Supports multimedia files with appropriate encoding

### 4. Execution Modes

#### Non-Interactive (Default)
```bash
llm "Your prompt here"
llm --model gpt-4o "Process this text"
llm < file.txt
cat document.md | llm "Summarize"
```

#### Interactive Mode
```bash
llm --interactive
llm -i
llm --model claude-opus --interactive
```

### 5. Configuration
Persistent config location: `~/.claude/llm-skill-config.json`
```json
{
  "last_model": "claude-sonnet-4.5",
  "default_provider": "anthropic",
  "available_providers": ["openai", "anthropic", "google", "ollama"]
}
```

## Implementation Details

### Core Files
- `llm_skill.py` - Main skill orchestration
- `providers.py` - Provider detection & config
- `models.py` - Model definitions & aliases
- `executor.py` - Execution logic (interactive/non-interactive)
- `input_handler.py` - Input type detection

### Key Functions

#### `detect_providers()`
- Scans environment for provider API keys
- Returns dict of available providers

#### `get_model_selector(input_text, provider=None)`
- Returns selected model, showing menu if needed
- Respects `last_model` config preference

#### `load_input(input_source)`
- Handles stdin, file paths, or inline text
- Returns content string

#### `execute_llm(content, model, interactive=False)`
- Calls `llm` CLI with appropriate parameters
- Manages stdin/stdout for interactive mode

### Usage in Claude Code

When user invokes this skill, Claude should:
1. Parse input for model specification (e.g., `--model gpt-4o`)
2. Call skill with content and optional model parameter
3. Wait for provider/model selection if needed
4. Execute and return results
5. For interactive mode, maintain conversation loop

## Error Handling

- If no providers available: Suggest installing API keys
- If model not found: Show available models for chosen provider
- If llm CLI not installed: Suggest installation via `pip install llm`
- If file not readable: Fall back to treating as inline text

## Configuration

Users can pre-configure preferences:
```json
{
  "last_model": "claude-sonnet-4.5",
  "default_provider": "anthropic",
  "interactive_mode": false,
  "available_providers": ["openai", "anthropic"]
}
```

## Slash Command Integration

Support `/llm` command:
```
/llm process this text
/llm --interactive
/llm --model gpt-4o analyze this
```


================================================================================

## 6. Expert Skill: agency-docs-updater
> **Path within category:** `agency-docs-updater/SKILL.md`


# Agency Docs Updater

Execute ALL steps automatically in sequence. Only pause if a step fails and cannot be recovered. Read `references/learnings.md` before starting for known pitfalls.

**Configuration**: paths are read from `.env` in the skill root (see `.env.example`). Defaults work for the standard setup. Key env vars: `VAULT_DIR`, `DOCS_SITE_DIR`, `YOUTUBE_UPLOADER_DIR`, `PRESENTATIONS_DIR`, `SKILLS_REPO_DIR`, `SKILLS_LOCAL_DIR`, `ZOOM_CREDENTIALS_DIR`, `GITHUB_REPO`, `SITE_DOMAIN`.

**Dependencies** (verify these exist before running):
- [zoom](https://github.com/glebis/claude-skills/tree/main/zoom) — Zoom recording download (`scripts/zoom_meetings.py`)
- [fathom](https://github.com/glebis/claude-skills/tree/main/fathom) — Fathom video fallback (`scripts/download_video.py`)
- [nano-banana](https://github.com/glebis/claude-skills/tree/main/nano-banana) — thumbnail overlay generation (`scripts/generate_image.sh`)
- [calendar-sync](~/.claude/skills/calendar-sync) — local-only, calendar event sync (`sync.sh`)
- [youtube-uploader](https://github.com/glebis/youtube-uploader) — video processing, upload, and YouTube API auth

## Step 0: Parse Arguments & Load Config

Load `.env` from skill root. Then split `args` by whitespace:
- 8-digit token (`YYYYMMDD`) → `DATE`
- "yesterday" → `DATE = $(date -v-1d +%Y%m%d)`
- "today" or missing → `DATE = $(date +%Y%m%d)`
- 2-digit token (`NN`) or `lab-NN` → `LAB_FILTER`

Expand env vars for paths used in subsequent steps:
```bash
VAULT_DIR="${VAULT_DIR:-$HOME/Brains/brain}"
DOCS_SITE_DIR="${DOCS_SITE_DIR:-$HOME/Sites/agency-docs}"
YOUTUBE_UPLOADER_DIR="${YOUTUBE_UPLOADER_DIR:-$HOME/ai_projects/youtube-uploader}"
SKILLS_REPO_DIR="${SKILLS_REPO_DIR:-$HOME/ai_projects/claude-skills}"
SKILLS_LOCAL_DIR="${SKILLS_LOCAL_DIR:-$HOME/.claude/skills}"
ZOOM_CREDENTIALS_DIR="${ZOOM_CREDENTIALS_DIR:-$HOME/.zoom_credentials}"
PRESENTATIONS_DIR="${PRESENTATIONS_DIR:-$HOME/ai_projects/claude-code-lab}"
GITHUB_REPO="${GITHUB_REPO:-glebis/agency-docs}"
SITE_DOMAIN="${SITE_DOMAIN:-agency-lab.glebkalinin.com}"
```

## Step 1: Find Fathom Transcript

If `LAB_FILTER` is set: `${VAULT_DIR}/${DATE}-claude-code-lab-${LAB_FILTER}.md`
If empty: glob `${VAULT_DIR}/${DATE}-claude-code-lab-*.md` (pick most recent by mtime).

If missing: run `${SKILLS_LOCAL_DIR}/calendar-sync/sync.sh`, re-check, stop if still missing.

Extract from YAML frontmatter and store:
- `FATHOM_FILE`, `SHARE_URL`, `MEETING_TITLE`, `DATE`, `LAB_NUMBER`
- `VIDEO_NAME` = `${DATE}-claude-code-lab-${LAB_NUMBER}`
- `TRANSCRIPT_LANG` = auto-detect from first ~50 lines (Cyrillic ratio > 0.3 → `ru`, else `en`)

**Determine `MEETING_NUMBER`**: check existing MDX files in `${DOCS_SITE_DIR}/content/docs/claude-code-internal-${LAB_NUMBER}/meetings/` for a placeholder with today's date. If found, use that number. Otherwise, check file content sizes to find the next empty slot. Store as zero-padded two-digit string (e.g. `04`). This variable is used in Steps 3b, 4b, 5, 6, and 8.

## Step 2: Download Video

Skip if `${VAULT_DIR}/${VIDEO_NAME}.mp4` exists and is > 1MB.

**Note**: Zoom recordings may take ~15 minutes to process after a meeting ends. If the Zoom API returns no recordings, wait and retry before falling back to Fathom.

**Primary — Zoom:**
```bash
python3 ${SKILLS_REPO_DIR}/zoom/scripts/zoom_meetings.py recordings \
  --start ${DATE:0:4}-${DATE:4:2}-${DATE:6:2} \
  --end $(date -j -v+1d -f %Y%m%d ${DATE} +%Y-%m-%d) \
  --show-downloads 2>&1
```
Find the MP4 URL, then:
```bash
TOK=$(python3 -c "import json,pathlib; print(json.load(open(pathlib.Path('${ZOOM_CREDENTIALS_DIR}')/'oauth_token.json'))['access_token'])")
curl -L -H "Authorization: Bearer ${TOK}" -o ${VAULT_DIR}/${VIDEO_NAME}.mp4 "${MP4_DOWNLOAD_URL}"
```

**Fallback — Fathom** (if no Zoom recording):
```bash
cd ${VAULT_DIR} && python3 ${SKILLS_LOCAL_DIR}/fathom/scripts/download_video.py \
  "${SHARE_URL}" --output-name "${VIDEO_NAME}"
```

## Step 3: Upload to YouTube

```bash
cd ${YOUTUBE_UPLOADER_DIR} && \
python3 process_video.py \
  --video ${VAULT_DIR}/${VIDEO_NAME}.mp4 \
  --fathom-transcript ${FATHOM_FILE} \
  --title "${MEETING_TITLE}" \
  --upload
```

Run with `run_in_background: true` (10-30 min). On failure: `--resume-from upload`.

Extract `YOUTUBE_URL` from stdout (`✓ YouTube video: ...`) or `processed/metadata/${VIDEO_NAME}.json`.
Extract `VIDEO_ID` from the URL (the part after `?v=` or last path segment).

### Step 3a: Verify Upload (REQUIRED)

After extracting `VIDEO_ID`, verify the video actually exists on YouTube before proceeding. Videos can silently fail processing or get auto-deleted by YouTube's content review.

```python
cd ${YOUTUBE_UPLOADER_DIR} && PYTHONPATH=. python3 -c "
from auth import get_authenticated_service
import sys, time

youtube = get_authenticated_service()
video_id = '${VIDEO_ID}'

# Poll up to 5 minutes for video to become available
for attempt in range(10):
    resp = youtube.videos().list(part='status,processingDetails', id=video_id).execute()
    if not resp['items']:
        if attempt < 9:
            print(f'Video not yet available (attempt {attempt+1}/10), waiting 30s...')
            time.sleep(30)
            continue
        print(f'FATAL: Video {video_id} not found after 5 minutes. Upload may have failed.')
        sys.exit(1)

    status = resp['items'][0]['status']
    processing = resp['items'][0].get('processingDetails', {})
    upload_status = status.get('uploadStatus', 'unknown')
    privacy = status.get('privacyStatus', 'unknown')
    rejection = status.get('rejectionReason', None)

    print(f'Upload status: {upload_status}, Privacy: {privacy}')
    if rejection:
        print(f'REJECTED: {rejection}')
        sys.exit(1)
    if upload_status in ('processed', 'uploaded'):
        print(f'✓ Video {video_id} verified OK')
        sys.exit(0)
    if upload_status == 'failed':
        print(f'FATAL: Upload failed — {status.get(\"failureReason\", \"unknown\")}')
        sys.exit(1)

    print(f'Status: {upload_status}, waiting 30s...')
    time.sleep(30)

print('FATAL: Video not ready after 5 minutes')
sys.exit(1)
"
```

If verification fails: delete the failed video metadata (`rm processed/metadata/${VIDEO_NAME}.json`), re-upload with `--resume-from upload`, and re-verify. Do NOT proceed to MDX or thumbnail steps with an unverified VIDEO_ID.

**Start Step 4 in parallel** — summary doesn't depend on YouTube URL.

### Step 3b: Lab-Style Thumbnail (REQUIRED)

**Always run this step** — it replaces the generic thumbnail from `process_video.py` with the branded lab template. The generic thumbnail is NOT acceptable for publishing.

**Prerequisites**: `VIDEO_ID` must be known (wait for Step 3 to complete if needed).

Follow `references/thumbnail-guide.md` for the full workflow:
1. Generate Nano Banana overlay image (topic-specific prompt from the guide's prompt patterns)
2. Read/inspect raw image to confirm background color, then recolor lines to orange (#e85d04)
3. Write a **temporary** HTML file (e.g. `/tmp/lab-meeting-${MEETING_NUMBER}.html`) based on `${YOUTUBE_UPLOADER_DIR}/templates/images/lab-meeting.html` — update meeting number, topic hero text, bullet descriptions, date. **Do not edit the original template in-place.**
4. Render with Playwright at 1280×720 → `${YOUTUBE_UPLOADER_DIR}/processed/thumbnails/${VIDEO_NAME}.jpg`
5. Read/inspect the rendered thumbnail to verify layout before uploading
6. Upload to YouTube: use `VIDEO_ID` extracted from Step 3

Do NOT skip this step or rely on the `process_video.py` thumbnail.

## Step 4: Generate Fact-Checked Summary

Read `${FATHOM_FILE}`. Generate a structured summary **in `${TRANSCRIPT_LANG}`**:
- `##` section headers, bullet points, code examples where relevant
- Technical terms in English (MCP, Skills, Claude Code, etc.)
- **Exclude personal scheduling details**
- Sanitize for MDX: escape `<`, `>`, and bare `{` characters that would break MDX compilation

Fact-check Claude Code feature claims using `claude-code-guide` subagent (if available; skip fact-checking if the agent is not accessible). Save corrected summary to scratchpad as `summary.md`.

## Step 4b: Update YouTube Metadata

**After both Step 3 and Step 4 complete.** `VIDEO_ID`, `MEETING_NUMBER`, and `LAB_NUMBER` must all be determined before this step. Read `references/youtube-api.md` for description format and API snippets.

Generate YouTube description from the summary. Use the language-appropriate template:

- **If `TRANSCRIPT_LANG=en`**: English labels ("In this video:", "Course materials and session notes:")
- **If `TRANSCRIPT_LANG=ru`**: Russian labels ("В этом видео:", "Материалы и конспект занятия:")

Do NOT mix languages in a single description.

Meeting page URL: `https://${SITE_DOMAIN}/claude-code-lab-${LAB_NUMBER}/meetings/${MEETING_NUMBER}`

Update title, description, tags via YouTube API, then add video to playlist "Claude Code Lab ${LAB_NUMBER}" (auto-created if it does not exist).

## Step 5: Generate MDX

```bash
python3 ${SKILLS_LOCAL_DIR}/agency-docs-updater/scripts/update_meeting_doc.py \
  ${FATHOM_FILE} "${YOUTUBE_URL}" ${SCRATCHPAD}/summary.md
```

**Before running**: check if a placeholder MDX already exists for today's date (`grep -l` in `meetings/`). If so, use `-n ${MEETING_NUMBER} --update` to target it.

**After running**:
1. Strip appended Marp content (everything after summary's closing `---` before `<!-- _class: lead -->`) — MDX breaks on HTML comments (`<!-- -->`), unescaped `<`, and bare `{` characters
2. Check for presentation file: look in `${PRESENTATIONS_DIR}/presentations/lab-${LAB_NUMBER}/` and `${PRESENTATIONS_DIR}/lesson-generator/` for files matching `${DATE}`. If found, copy to `${DOCS_SITE_DIR}/public/${DATE}-claude-code-lab-${LAB_NUMBER}.html` and add link in MDX
3. Replace frontmatter placeholders (`[Название встречи]`, `[Краткое описание встречи]`, `[Дата встречи]`)
4. If `TRANSCRIPT_LANG=en`, rewrite the MDX entirely with English labels — the script defaults to Russian and the translation fallback produces broken mixed-language output
5. Verify: `cd ${DOCS_SITE_DIR} && npm run build 2>&1 | tail -5`

## Step 6: Commit and Push

Only stage pipeline files — never `git add .`:
```bash
cd ${DOCS_SITE_DIR}
git fetch origin main
BEHIND=$(git rev-list --count HEAD..origin/main)
if [ "$BEHIND" -gt 0 ]; then
  git stash push -m "agency-docs-updater: temp stash"
  git pull --rebase origin main
  git stash pop || true
fi
git add content/docs/claude-code-internal-${LAB_NUMBER}/meetings/${MEETING_NUMBER}.mdx
# Only stage presentation HTML if it was copied
[ -f public/${DATE}-claude-code-lab-${LAB_NUMBER}.html ] && git add public/${DATE}-claude-code-lab-${LAB_NUMBER}.html
git commit -m "Add Lab ${LAB_NUMBER} Meeting ${MEETING_NUMBER}"
git push
```

Store `COMMIT_HASH=$(git rev-parse HEAD)` for Step 7.

## Step 7: Wait for Vercel Deploy

```bash
TIMEOUT=300; ELAPSED=0
until [ "$(gh api repos/${GITHUB_REPO}/commits/${COMMIT_HASH}/status --jq '.state' 2>/dev/null || echo 'pending')" != "pending" ]; do
  sleep 15; ELAPSED=$((ELAPSED+15))
  [ "$ELAPSED" -ge "$TIMEOUT" ] && echo "Deploy timeout after ${TIMEOUT}s" && break
done
DEPLOY_STATE=$(gh api repos/${GITHUB_REPO}/commits/${COMMIT_HASH}/status --jq '.state')
echo "Deploy state: ${DEPLOY_STATE}"
```

Run with `run_in_background: true`. If state is `failure` or `error`: check Vercel logs (`vercel logs`), fix locally, re-push, restart this step.

## Step 8: Verify in Browser

Open `https://${SITE_DOMAIN}/claude-code-lab-${LAB_NUMBER}/meetings/${MEETING_NUMBER}` in a browser (via chrome automation tools or manually). Verify YouTube embed is visible. If not: check VIDEO_ID, wait for YouTube processing, or re-upload.

## Pipeline Report

After completion, report: Fathom path, video path, YouTube URL, MDX path, commit hash, deploy status, embed verification.


================================================================================

## 7. Expert Skill: health-data
> **Path within category:** `health-data/SKILL.md`


# Apple Health Data Query Skill

Query and analyze health data from the local SQLite database containing 6.3M+ records across 43 health metrics.

## Database Location

```
~/data/health.db
```

## Query Methods

### 1. Python Script (Recommended for Common Queries)

Use `scripts/health_query.py` for pre-built queries with automatic formatting:

```bash
# Daily summary
python ~/.claude/skills/health-data/scripts/health_query.py --format markdown daily --date 2025-11-29

# Weekly trends
python ~/.claude/skills/health-data/scripts/health_query.py --format json weekly --weeks 4

# Sleep analysis
python ~/.claude/skills/health-data/scripts/health_query.py --format fhir sleep --days 7

# Latest vitals
python ~/.claude/skills/health-data/scripts/health_query.py vitals

# Activity rings
python ~/.claude/skills/health-data/scripts/health_query.py --format json activity --days 30

# Workout history
python ~/.claude/skills/health-data/scripts/health_query.py workouts --days 30 --type Running

# Custom SQL
python ~/.claude/skills/health-data/scripts/health_query.py --format json query "SELECT * FROM workouts LIMIT 5"
```

**Output formats:** `markdown`, `json`, `fhir`, `ascii`

### 2. Direct SQL (For Custom/Ad-hoc Queries)

For flexible queries, run SQL directly against the database. See `references/schema.md` for table structures and query templates.

```bash
sqlite3 ~/data/health.db "SELECT AVG(value) FROM health_records WHERE record_type LIKE '%HeartRate%' AND start_date LIKE '2025-11%'"
```

## Pre-built Queries

### Daily Health Summary

Get today's key metrics:
```bash
python ~/.claude/skills/health-data/scripts/health_query.py daily
```

Returns: steps, calories, heart rate (avg/min/max), exercise minutes, distance, activity ring status.

### Weekly Trends

Compare week-over-week performance:
```bash
python ~/.claude/skills/health-data/scripts/health_query.py weekly --weeks 4
```

Returns: average daily steps, resting HR, exercise minutes, workout count per week.

### Sleep Analysis

Analyze sleep patterns:
```bash
python ~/.claude/skills/health-data/scripts/health_query.py sleep --days 14
```

Returns: nightly duration, sleep stages (Core, Deep, REM), average sleep hours.

### Latest Vitals

Get most recent vital readings:
```bash
python ~/.claude/skills/health-data/scripts/health_query.py vitals
```

Returns: Heart Rate, HRV, Resting HR, Blood Oxygen, Respiratory Rate with timestamps.

### Activity Rings

Track ring completion:
```bash
python ~/.claude/skills/health-data/scripts/health_query.py activity --days 30
```

Returns: daily ring values/goals, completion percentages, perfect day count.

### Workout History

Review exercise sessions:
```bash
python ~/.claude/skills/health-data/scripts/health_query.py workouts --days 30 --type Running
```

Returns: workout type, duration, distance, calories, summary by type.

## Output Formats

### Markdown (default)

Human-readable tables and lists. Best for reports and summaries.

### JSON

Structured data for programmatic use:
```json
{
  "date": "2025-11-29",
  "metrics": {
    "steps": 8542,
    "active_calories": 450.5,
    "heart_rate": {"avg": 72.3, "min": 52, "max": 145}
  }
}
```

### FHIR R4

Healthcare interoperability format. Outputs as FHIR Bundle with Observation resources using LOINC codes. See `references/fhir_mappings.md` for code mappings.

### ASCII

Terminal-friendly output with bar charts and statistics:
```
============================================================
  DAILY SUMMARY - 2025-11-29
============================================================

METRICS
----------------------------------------
  steps                      2620
  active_calories           234.5
  heart_rate           avg:  67.5  min:  52  max: 108

ACTIVITY RINGS
----------------------------------------
  move       [███████░░░░░░░░░░░░░]  36.7% (238/650)
  exercise   [░░░░░░░░░░░░░░░░░░░░]   0.0% (0/35)
  stand      [████████████████████] 100.0% (10/10)
```

## Common SQL Patterns

For ad-hoc queries, use these patterns from `references/schema.md`:

**Heart rate by hour (circadian pattern):**
```sql
SELECT strftime('%H', start_date) as hour, ROUND(AVG(value), 1) as avg_hr
FROM health_records
WHERE record_type = 'HKQuantityTypeIdentifierHeartRate'
AND value BETWEEN 40 AND 200
GROUP BY hour ORDER BY hour;
```

**Steps per day this month:**
```sql
SELECT DATE(start_date) as day, SUM(value) as steps
FROM health_records
WHERE record_type = 'HKQuantityTypeIdentifierStepCount'
AND start_date >= DATE('now', 'start of month')
GROUP BY day ORDER BY day;
```

**Sleep quality (deep + REM hours):**
```sql
SELECT DATE(start_date) as night,
       ROUND(SUM(duration_minutes)/60.0, 1) as quality_hours
FROM sleep_sessions
WHERE sleep_stage IN ('Deep', 'REM')
GROUP BY night ORDER BY night DESC LIMIT 14;
```

**Workout summary:**
```sql
SELECT REPLACE(workout_type, 'HKWorkoutActivityType', '') as type,
       COUNT(*) as count, ROUND(SUM(duration_minutes)) as total_min
FROM workouts
WHERE start_date >= DATE('now', '-30 days')
GROUP BY type ORDER BY count DESC;
```

## Record Types Available

The database contains 43 health metric types including:

**Vitals:** Heart Rate, HRV, Resting HR, Blood Oxygen, Respiratory Rate, Blood Pressure

**Activity:** Steps, Distance, Active Calories, Basal Calories, Flights Climbed, Exercise Time, Stand Time

**Mobility:** Walking Speed, Step Length, Walking Asymmetry, Stair Speed, Walking Steadiness

**Body:** Weight, BMI, Body Fat %

**Audio:** Environmental Noise, Headphone Exposure

**Other:** VO2 Max, Time in Daylight, UV Exposure

## Data Coverage

- **Records:** 6.3M+ measurements
- **Date range:** 2015-10-13 to present
- **Workouts:** 1,435 sessions
- **Sleep sessions:** 40,514 records
- **Activity days:** 1,875 daily summaries

## Resources

### scripts/

- `health_query.py` - Main query tool with Markdown/JSON/FHIR output

### references/

- `schema.md` - Database schema, record type mappings, SQL query templates
- `fhir_mappings.md` - LOINC codes and FHIR R4 templates

## Troubleshooting

**Database not found:**
Ensure `~/data/health.db` exists. Run the import script from `/Users/server/apple_health_export/`:
```bash
python import_health.py --status
```

**No data for date range:**
Check available date range:
```sql
SELECT MIN(start_date), MAX(start_date) FROM health_records;
```

**Outlier values:**
Filter physiologically valid ranges (e.g., heart rate 40-200 bpm):
```sql
WHERE value BETWEEN 40 AND 200
```


================================================================================

## 8. Expert Skill: tg-responder
> **Path within category:** `tg-responder/SKILL.md`


# tg-responder — Telegram Communications Assistant

Review pending response drafts and manage the Telegram response queue.

## Commands

### review — Approve pending drafts

Read the responder queue and present drafts for approval:

```bash
python3 ~/.claude/skills/tg-responder/scripts/schema.py  # ensure DB exists
```

Then query the database:

```sql
-- Pending drafts needing approval
SELECT o.id, o.chat_id, o.draft_text, o.draft_reason, o.source,
       i.sender_name, i.text as original_text, i.urgency, i.category,
       datetime(i.received_at, 'unixepoch') as received
FROM outbox o
JOIN inbox i ON o.inbox_id = i.id
WHERE o.status = 'draft'
ORDER BY
  CASE i.urgency WHEN 'urgent' THEN 0 WHEN 'normal' THEN 1 ELSE 2 END,
  o.created_at ASC;
```

For each draft, present to the user:
1. **Original message** — who sent it, when, what they said
2. **Draft response** — the proposed reply
3. **Options**: approve (send as-is), edit (modify then send), skip

To approve and send a draft:
1. Update outbox: `UPDATE outbox SET status = 'approved', final_text = draft_text, approved_at = strftime('%s','now') WHERE id = ?`
2. Send via telegram skill: `python3 ~/.claude/skills/telegram/scripts/telegram_fetch.py send --chat-id CHAT_ID --text "THE_TEXT"`
3. Update outbox with sent status and message_id

To skip: `UPDATE outbox SET status = 'skipped', updated_at = strftime('%s','now') WHERE id = ?`

### status — Queue statistics

```sql
-- Inbox stats
SELECT status, count(*) FROM inbox GROUP BY status;

-- Outbox stats
SELECT status, count(*) FROM outbox GROUP BY status;

-- Recent activity
SELECT sender_name, route, status, datetime(created_at, 'unixepoch')
FROM inbox ORDER BY created_at DESC LIMIT 10;
```

Report: pending count, drafts waiting, sent today, failed items.

### follow-ups — Track unanswered outbound messages

Scan for people who haven't replied, send reminders with exponential backoff.

```bash
# Scan for new unanswered messages (needs Telethon session — stop daemon first)
python3 ~/.claude/skills/tg-responder/scripts/follow_ups.py scan

# Process due reminders (drafts to Telegram or outbox)
python3 ~/.claude/skills/tg-responder/scripts/follow_ups.py remind

# List active follow-ups
python3 ~/.claude/skills/tg-responder/scripts/follow_ups.py list

# Archive expired follow-ups
python3 ~/.claude/skills/tg-responder/scripts/follow_ups.py archive

# Run all (scan + check replies + remind + archive)
python3 ~/.claude/skills/tg-responder/scripts/follow_ups.py all
```

Also query directly:
```sql
SELECT sender_name, outbound_text, reminder_count, max_reminders,
       datetime(outbound_at, 'unixepoch') as sent,
       datetime(next_reminder_at, 'unixepoch') as next_ping,
       status
FROM follow_ups
WHERE status = 'active'
ORDER BY next_reminder_at;
```

Schedule: exponential (3d → 6d → 12d), fixed (every Nd), or custom per contact.
After max_reminders → archived. If they reply → auto-resolved.

## Database

Located at `~/Brains/data/telegram/responder.db`.

## Config

Located at `~/.claude/skills/tg-responder/config.yaml`. Edit contacts, modes, and ignore lists there.

## Worker

Start: `python3 ~/.claude/skills/tg-responder/scripts/worker.py`
One-shot: `python3 ~/.claude/skills/tg-responder/scripts/worker.py --once`


================================================================================

## 9. Expert Skill: telegram-post
> **Path within category:** `telegram-post/SKILL.md`

# Telegram Post Skill

Create, preview, and send formatted Telegram posts from draft markdown files. Built for [@klodkot](https://t.me/klodkot) and Gleb Kalinin's other Telegram channels.

**Note:** Channel configurations (footers, tags, language defaults) are specific to Gleb's channels. To use for your own channels, edit `CHANNEL_CONFIG` in `scripts/post.py`.

**Configured channels:** [@klodkot](https://t.me/klodkot), @mentalhealthtech, @toolbuildingape, @opytnymputem

## When to Use

Use this skill when:
- User asks to create a draft for a Telegram channel
- User asks to "post to Telegram" or "send to saved messages" from a draft file
- User wants to preview a draft before sending
- Draft files in `Channels/*/drafts/` need to be sent

## Commands

### `create` -- Create a new draft

```bash
# Default: klodkot channel
python3 scripts/post.py create "remotion-video-creation" --topic "Remotion Agent Skill" --source "https://example.com"

# Other channel
python3 scripts/post.py create "therapy-app-review" -c mental-health-tech --topic "Therapy apps"

# With video
python3 scripts/post.py create "demo-post" --video demo.mp4 --source "https://example.com"
```

Creates `Channels/{channel}/drafts/YYYYMMDD-{slug}.md` with proper frontmatter. Returns file path and tags reference for the channel.

Options:
- `--channel, -c`: Channel name (default: klodkot). Use `list` to see all
- `--topic, -t`: Topic for frontmatter
- `--source, -s`: Source URL
- `--video, -v`: Video filename (just name, not path)
- `--language, -l`: Override channel default (ru/en)

### `send` -- Send a draft

```bash
# Preview first (always do this)
python3 scripts/post.py send "Channels/klodkot/drafts/20260209-post.md" --dry-run

# Send to Saved Messages (default)
python3 scripts/post.py send "Channels/klodkot/drafts/20260209-post.md"

# Send to specific chat
python3 scripts/post.py send "draft.md" --chat "@klodkot"
python3 scripts/post.py send "draft.md" -c "Tool Building Ape"
```

### `list` -- List available channels

```bash
python3 scripts/post.py list
```

Returns: klodkot, mental-health-tech, tool-building-ape, opytnym-putem with language and tags info.

## Draft File Format

```markdown

## Post Title

Content with **bold** and *italic* and [links](url).


================================================================================

## 10. Expert Skill: telegram-telethon
> **Path within category:** `telegram-telethon/SKILL.md`


## Claude Behavior Guidelines

### Draft vs Send: Follow User's Intent

| User says | Claude does | Clarify? |
|-----------|-------------|----------|
| "драфт", "draft", "сделай драфт" | `draft` | No |
| "отправь", "пошли", "send" | `send` | No |
| "напиши сообщение" (ambiguous) | Ask what user wants | Yes |

### Key Rules

1. **Explicit draft → draft**: "драфт", "draft" → use `draft` command immediately
2. **Explicit send → send**: "отправь", "пошли", "send" → use `send` command immediately
3. **Ambiguous → clarify**: If neither "draft" nor "send" verb present, ask: "Создать драфт или сразу отправить?"

### Examples

**User:** "сделай драфт для lv: привет"
**Claude:** Uses `draft --chat "lv" --text "привет"` immediately

**User:** "отправь сообщение Маше: встретимся в 5?"
**Claude:** Uses `send --chat "Маша" --text "встретимся в 5?"` immediately

**User:** "напиши сообщение для Маши: встретимся в 5?"
**Claude:** Asks "Создать драфт или сразу отправить?"

# Telegram Telethon Skill

Full Telethon API wrapper with daemon mode and Claude Code integration. Supports interactive setup, background message monitoring, and automatic Claude session spawning per chat.

## Package Layout

```
telegram-telethon/
├── SKILL.md                          # This file
├── pyproject.toml                    # Installable Python package
├── scripts/
│   ├── tg.py                         # Main CLI (messages, media, drafts, etc.)
│   └── tgd.py                        # Daemon controller
├── src/telegram_telethon/            # Importable package
│   ├── core/                         # auth, config
│   ├── modules/                      # messages, media
│   ├── daemon/                       # runner, handlers, claude_bridge
│   └── utils/                        # formatting
└── tests/                            # pytest unit + integration tests
```

Scripts import from `src/telegram_telethon`. Install the package in editable mode so `tg.py`/`tgd.py` can resolve imports:

```bash
cd telegram-telethon
pip install -e .
# or with dev tools (pytest, coverage):
pip install -e ".[dev]"
```

## Relationship to `telegram` Skill

The separate `telegram` skill (single-script `telegram_fetch.py` backed by `telegram_dl`) overlaps on list/recent/search/send/edit/download/thread but differs:

With the publish/markdown/schedule ports now complete, **`telegram-telethon` is a superset of `telegram`** on everything except the external `telegram_dl` auth dependency. Use this skill for:

- `publish` — draft→channel workflow (frontmatter, media albums, post-publish move + index update, post-flight lint)
- `--markdown` on `send` / `publish` — markdown→Telegram HTML conversion
- `--schedule` on `send` / `publish` — ISO / relative / natural-language scheduled delivery
- Daemon mode + Claude Code spawning, voice transcription (Telegram/Groq/Whisper), `delete` / `forward` / `mark-read`, local `draft` / `drafts` / `draft-send`, `lint-channel`, non-interactive auth setup.

## Prerequisites

### Interactive Setup (Terminal)

Run setup wizard on first use:

```bash
python3 scripts/tg.py setup
```

This guides through:
1. Getting API credentials from https://my.telegram.org/auth
2. Phone number verification
3. 2FA (if enabled)
4. Optional daemon trigger configuration

### Non-Interactive Setup (Claude Code)

For use from Claude Code or scripts without TTY:

```bash
# Step 1: Provide credentials and trigger code send
python3 scripts/tg.py setup --api-id 12345678 --api-hash abc123... --phone +1234567890

# Step 2: User receives code on phone, then complete auth
python3 scripts/tg.py setup --api-id 12345678 --api-hash abc123... --phone +1234567890 --code 12345

# If 2FA enabled, add password
python3 scripts/tg.py setup --api-id 12345678 --api-hash abc123... --phone +1234567890 --code 12345 --password mypassword
```

The script auto-detects TTY and switches between interactive/non-interactive modes.

## Quick Start

```bash
# Check connection status
python3 scripts/tg.py status

# List chats
python3 scripts/tg.py list

# Get recent messages from a chat
python3 scripts/tg.py recent "John Doe" --limit 20

# Search messages
python3 scripts/tg.py search "meeting notes"

# Configure daemon triggers interactively
python3 scripts/tg.py daemon-config

# Start daemon (foreground with logs)
python3 scripts/tgd.py start --foreground

# Start daemon (background)
python3 scripts/tgd.py start

# View daemon logs
python3 scripts/tgd.py logs
```

## CLI Commands

### Message Operations

```bash
# List all chats
python3 scripts/tg.py list [--limit 30] [--search "term"]

# Fetch recent messages
python3 scripts/tg.py recent [CHAT] [--limit 50] [--days 7] [--format markdown|json] [--output file.md]

# Search messages by content
python3 scripts/tg.py search QUERY [--chat "Chat Name"] [--limit 50] [--format markdown|json]

# Fetch unread messages
python3 scripts/tg.py unread [--chat "Chat Name"] [--format markdown|json]

# Fetch forum thread
python3 scripts/tg.py thread CHAT_ID THREAD_ID [--limit 100]

# Send message
python3 scripts/tg.py send --chat "Chat Name" --text "Message text" [--reply-to MSG_ID] [--file path] [--topic TOPIC_ID] [--markdown] [--html] [--schedule "+1h" | "tomorrow 10:00" | "2026-04-10T09:30"]

# Edit message
python3 scripts/tg.py edit --chat "Chat Name" --message-id MESSAGE_ID --text "New text"

# Delete messages
python3 scripts/tg.py delete --chat "Chat Name" --message-ids 123 456 789 [--no-revoke]

# Forward messages
python3 scripts/tg.py forward --from "Source" --to "Dest" --message-ids 123 456

# Mark messages as read
python3 scripts/tg.py mark-read --chat "Chat Name" [--max-id MSG_ID]
```

### Draft Operations

```bash
# Save/update a draft message
python3 scripts/tg.py draft --chat "Chat Name" --text "Draft text" [--reply-to MSG_ID] [--no-preview]

# Clear a draft (save empty text)
python3 scripts/tg.py draft --chat "Chat Name" --text ""

# Clear all drafts
python3 scripts/tg.py draft --clear-all

# List all drafts
python3 scripts/tg.py drafts [--limit 50]

# Send a draft as a message (clears the draft)
python3 scripts/tg.py draft-send --chat "Chat Name"
```

**Note:** Use `"me"` as the chat name to target Saved Messages (your own chat). The literal name "Saved Messages" doesn't work as it's localized differently per user.

### Media Operations

```bash
# Download media from chat
python3 scripts/tg.py download "Chat Name" [--limit 5] [--output-dir ~/Downloads] [--message-id ID] [--type voice|video|photo]

# Transcribe a single voice message (MESSAGE_ID required)
python3 scripts/tg.py transcribe "Chat Name" MESSAGE_ID [--method telegram|groq|whisper]

# Batch-transcribe recent voice messages (omit MESSAGE_ID, use --batch)
python3 scripts/tg.py transcribe "Chat Name" --batch [--limit 10] [--method telegram|groq|whisper]
```

### Publish a Draft to a Channel

End-to-end publish workflow: parse a draft markdown file, resolve the destination channel from folder structure or frontmatter `channel:`, upload media (single file or album), post-process to move the draft to `published/` and insert an entry in the channel index.

```bash
# Dry-run preview
python3 scripts/tg.py publish --draft "Channels/klodkot/drafts/20260416-post.md" --dry-run

# Publish now
python3 scripts/tg.py publish --draft "20260416-post"  # slug works too

# Publish scheduled for later
python3 scripts/tg.py publish --draft "..." --schedule "tomorrow 10:00"
```

The result JSON includes `published`, `channel`, `message_id`, `media_count`, `moved_to`, and — crucially — `lint_warnings` when the final body contains leaked markdown/HTML that Telegram wouldn't render. Post-publish bookkeeping failures (e.g. index write error) surface as `warnings` but don't roll back the send.

### Markdown Formatting on Send

Pass `--markdown` to convert a markdown-flavored message into Telegram HTML before sending:

```bash
python3 scripts/tg.py send --chat "@mychannel" --markdown \
  --text $'## Release\n\n**v2** ships _today_. See [docs](https://example.com).\n\n* fast\n* stable'
```

Rules (applied in order): `## Header` → bold line; `* item` / `- item` at line start → `→ item`; `**bold**` → `<b>`; `_italic_` → `<i>`; `[text](url)` → `<a href>`. Pre-existing HTML passes through unchanged, so the flag is safe to add to content that was already authored as HTML.

Pair with `lint-channel` below to catch cases where `--markdown` was forgotten.

### Sending Pre-written HTML

Pass `--html` to send text that already contains Telegram-compatible HTML tags (`<b>`, `<i>`, `<a href>`, `<code>`, `<pre>`, `<u>`, `<s>`, `<tg-spoiler>`, `<blockquote>`):

```bash
python3 scripts/tg.py send --chat "@mychannel" --html \
  --text '<b>Release v2</b> ships today. See <a href="https://example.com">docs</a>.'
```

Unlike `--markdown` (which converts markdown syntax to HTML), `--html` sends the text as-is with `parse_mode='html'`. Use `--html` when you have already authored HTML content or when programmatically building messages with tags.

### Scheduled Delivery

Pass `--schedule` with one of three formats (naive times default to Europe/Berlin):

```bash
# Relative: send in one hour
python3 scripts/tg.py send --chat "@mychannel" --text "..." --schedule "+1h"

# Natural: send tomorrow morning
python3 scripts/tg.py send --chat "@mychannel" --text "..." --schedule "tomorrow 09:30"

# Absolute: send at a specific time
python3 scripts/tg.py send --chat "@mychannel" --text "..." --schedule "2026-04-20T15:00"
```

The response includes ``"scheduled_for": "<iso datetime>"`` when the message is queued for later. Telegram displays scheduled messages in the chat's scheduled-messages view.

### Lint Published Messages

Scan a channel (or a single message) for unrendered markdown/HTML that leaked into the raw message text — i.e. the sender forgot `--markdown` or the HTML conversion failed, so readers see literal `**bold**`, `<b>…</b>`, `[text](url)`, or `## Header` in the post.

```bash
# Scan last 50 messages in @mychannel
python3 scripts/tg.py lint-channel --chat "@mychannel"

# Scan last 200 messages
python3 scripts/tg.py lint-channel --chat "@mychannel" --limit 200

# Lint a single message by ID
python3 scripts/tg.py lint-channel --chat "@mychannel" --message-id 1234

# Machine-readable output for pipelines / CI
python3 scripts/tg.py lint-channel --chat "@mychannel" --json
```

The detector lives in `modules/lint.py` as a pure function (`detect_unrendered_markup(text, entities)`), so it can also be called directly on drafts or wired into a post-flight check after publishing. Content inside `MessageEntityCode`/`MessageEntityPre` spans is ignored (inline code / code blocks are expected to contain raw characters).

### Obsidian Integration

`--to-daily` and `--to-person` are flags on the read commands (`recent`, `search`, `unread`), not standalone subcommands:

```bash
# Append recent messages to today's daily note (Daily/YYYYMMDD.md in the active vault)
python3 scripts/tg.py recent "Chat Name" --to-daily

# Append search results to today's daily note
python3 scripts/tg.py search "query" --to-daily

# Append recent messages to a person's note
python3 scripts/tg.py recent "Chat Name" --to-person "Person Name"
```

The target vault path is resolved by the formatting helpers in `utils/formatting.py`; there are currently no `--vault` or `--section` overrides on the CLI.

### Voice Transcription

The skill supports three transcription methods with automatic fallback:

1. **Telegram API** (default) - Uses Telegram Premium's server-side transcription
2. **Groq** - Uses Groq's Whisper API (requires `GROQ_API_KEY` environment variable)
3. **Whisper** - Uses local OpenAI Whisper model (requires `pip install openai-whisper`)

```bash
# Use Telegram's transcription (Premium feature)
python3 scripts/tg.py transcribe "Chat" 123

# Force Groq transcription
python3 scripts/tg.py transcribe "Chat" 123 --method groq

# Force local Whisper
python3 scripts/tg.py transcribe "Chat" 123 --method whisper
```

## Daemon Mode

The daemon monitors Telegram for messages matching configured triggers and can:
- Reply with static text
- Spawn Claude Code sessions to handle requests
- Resume existing Claude sessions per-chat
- Queue requests to prevent rate limiting

### Trigger Configuration

Triggers are stored in `~/.config/telegram-telethon/daemon.yaml`:

```yaml
triggers:
  # Respond to /claude command in DMs
  - chat: "@myusername"
    pattern: "^/claude (.+)$"
    action: claude
    reply_mode: inline

  # Respond to @Bot mentions in a group
  - chat: "AI Assistants"
    pattern: "@Bot (.+)$"
    action: claude
    reply_mode: new

  # Simple ping-pong in any chat
  - chat: "*"
    pattern: "^/ping$"
    action: reply
    reply_text: "pong"

claude:
  allowed_tools:
    - Read
    - Edit
    - Bash
    - WebFetch
  max_turns: 10
  timeout: 300

queue:
  max_concurrent: 1
  timeout: 600
```

### Trigger Fields

| Field | Description |
|-------|-------------|
| `chat` | Chat name, `@username`, or `*` for all chats |
| `pattern` | Regex pattern (capture group 1 becomes Claude prompt) |
| `action` | `claude`, `reply`, or `ignore` |
| `reply_mode` | `inline` (reply to message) or `new` (separate message) |
| `reply_text` | Static text for `reply` action |

### Claude Integration

When action is `claude`:
1. Text captured by regex group 1 is sent to Claude Code via `claude -p "..." --output-format json`
2. Claude sessions persist per-chat in `sessions.json`
3. Subsequent messages from same chat resume session via `--resume <session_id>`
4. Responses are sent back to Telegram as reply or new message

## Session Persistence

Claude sessions are saved to `~/.config/telegram-telethon/sessions.json`:
- Each chat_id maps to a Claude session_id
- Sessions survive daemon restarts
- Track message count and last used timestamp

To reset: delete chat entry from `sessions.json` or configure a `/reset` trigger.

## Example Configurations

### Personal AI Assistant

Respond to all DMs to yourself:

```yaml
triggers:
  - chat: "@yourusername"
    pattern: "(.+)"
    action: claude
    reply_mode: inline
```

### Group Bot with Mention Trigger

Only respond when @mentioned:

```yaml
triggers:
  - chat: "Dev Team"
    pattern: "@AssistantBot (.+)"
    action: claude
    reply_mode: inline
```

### Multi-Action Setup

```yaml
triggers:
  - chat: "*"
    pattern: "^/ask (.+)"
    action: claude
    reply_mode: inline

  - chat: "*"
    pattern: "^/ping$"
    action: reply
    reply_text: "pong"

  - chat: "Noisy Group"
    pattern: ".*"
    action: ignore
```

## File Structure

```
~/.config/telegram-telethon/
├── config.yaml        # API credentials (api_id, api_hash, phone)
├── daemon.yaml        # Daemon triggers and Claude config
├── session.session    # Telethon session file
├── sessions.json      # Claude session persistence
└── daemon.log         # Daemon log file
```

## Development

```bash
# Install with dev dependencies
cd telegram-telethon
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=telegram_telethon

# Run specific test file
pytest tests/unit/test_claude_bridge.py -v
```

## Example User Requests

Mapping natural-language asks to commands:

| User says | Command |
|-----------|---------|
| "Is Telegram connected?" | `status` |
| "What chats do I have?" | `list` |
| "Find chat named X exactly" | `list --search "X"` (increase `--limit` if not found) |
| "Show recent messages from John" | `recent "John" --limit 20` |
| "Messages from the last week in Group Y" | `recent "Group Y" --days 7` |
| "Search Telegram for 'deadline'" | `search "deadline"` |
| "Unread messages from Group Z" | `unread --chat "Group Z"` |
| "Mark Group Z as read" | `mark-read --chat "Group Z"` |
| "Get thread 174 in Lab" | `thread <chat_id> 174 --limit 100` |
| "Send 'hi' to John" / "отправь John: hi" | `send --chat "John" --text "hi"` |
| "Post a markdown-formatted note to @channel" | `send --chat "@channel" --markdown --text "..."` |
| "Schedule this for tomorrow at 10am" | `send --chat "..." --text "..." --schedule "tomorrow 10:00"` |
| "Send this in an hour" | `send --chat "..." --text "..." --schedule "+1h"` |
| "Reply thanks to message 12345" | `send --chat "..." --text "thanks" --reply-to 12345` |
| "Send image.jpg to John" | `send --chat "John" --file image.jpg` |
| "Save a draft for John: hi" / "сделай драфт" | `draft --chat "John" --text "hi"` |
| "List my drafts" | `drafts` |
| "Send the draft for John" | `draft-send --chat "John"` |
| "Delete messages 123, 456 from John" | `delete --chat "John" --message-ids 123 456` |
| "Forward msg 789 from John to Maria" | `forward --from "John" --to "Maria" --message-ids 789` |
| "Edit message 76 in @channel" | `edit --chat "@channel" --message-id 76 --text "..."` |
| "Download last 5 voice notes from John" | `download "John" --type voice --limit 5` |
| "Transcribe voice message 512 from John" | `transcribe "John" 512` |
| "Batch-transcribe recent voices from John" | `transcribe "John" --batch --limit 10` |
| "Add John's messages to daily note" | `recent "John" --to-daily` |
| "Add messages to a person's note" | `recent "Chat" --to-person "Person Name"` |
| "Publish this draft to the klodkot channel" | `publish --draft "20260416-post"` |
| "Preview a draft before publishing" | `publish --draft "..." --dry-run` |
| "Publish this at 10am tomorrow" | `publish --draft "..." --schedule "tomorrow 10:00"` |
| "Check if @mychannel has unrendered markup" | `lint-channel --chat "@mychannel"` |
| "Lint message 1234 in @mychannel" | `lint-channel --chat "@mychannel" --message-id 1234` |
| "Start the Telegram daemon" | `python3 scripts/tgd.py start` (or `--foreground`) |
| "Show daemon logs" | `python3 scripts/tgd.py logs` |
| "Configure daemon triggers" | `daemon-config` |

**Saved Messages:** Use `"me"` (not "Saved Messages") — the label is localized per user.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Config not found" | Run `python3 scripts/tg.py setup` |
| "Session expired" | Delete `session.session` and re-run setup |
| `ModuleNotFoundError: telegram_telethon` | Run `pip install -e .` from the skill directory |
| "Claude timeout" | Increase `timeout` in `daemon.yaml` |
| "Queue full" | Reduce request rate or wait |
| "No trigger matched" | Check `pattern` regex and `chat` name match |
| Chat not found by name | Increase `--limit` on `list` (default 30); may not be in recent dialogs |


================================================================================

## 11. Expert Skill: balanced
> **Path within category:** `balanced/SKILL.md`


# Balanced Dialog

Engage in constructive, evidence-based dialogue. Multiple output modes available.

## Onboard Mode

Trigger: `/balanced onboard` or `/balanced setup`. Walk the user through all available modes and let them pick a default.

### Flow

1. Display this overview using AskUserQuestion:

```
Balanced Dialog — available modes:

1. FULL (default)  — 4-move structured analysis
2. INTERACTIVE (i) — Socratic Q&A, one move at a time
3. TLDR            — 3-5 line insight box, action-oriented
4. STEELMAN        — strongest argument + strongest counter
5. DECISION        — tradeoff table + the call

Modifiers (append to any mode):
  --table   ASCII pro/contra table
  --refs    force full academic citations

Which mode should be your default? (1-5, or press Enter for FULL)
```

2. Save the user's choice to the skill config file at `~/.claude/skills/balanced/config.json`:
   ```json
   {"default_mode": "full", "default_modifiers": []}
   ```

3. Then ask via AskUserQuestion:
   ```
   Default modifiers? (comma-separated, or Enter for none)
   Options: --table, --refs
   ```

4. Update config.json with the chosen modifiers.

5. Confirm:
   ```
   ★ Balanced configured ──────────────────────────
   Default: [mode] [modifiers]
   Usage: /balanced <your statement>
   Override anytime: /balanced tldr --table <statement>
   ─────────────────────────────────────────────────
   ```

### Config Loading

On every invocation, check if `~/.claude/skills/balanced/config.json` exists. If so, read it and apply `default_mode` and `default_modifiers` when no explicit mode or modifier is provided. Explicit arguments always override config.

## Mode Selection

- **Passive mode** (default): `/balanced <statement>`. Full 4-move analysis in a single structured pass.
- **Interactive mode**: `/balanced i <statement>`. Socratic Q&A using AskUserQuestion, one move at a time.
- **TL;DR mode**: `/balanced tldr <statement>`. 3-5 lines max. One key fact, one challenge, one action. Output in insight box format:
  ```
  ★ Balanced ─────────────────────────────────────
  [key fact]. [challenge to assumption].
  → Action: [concrete next step].
  ─────────────────────────────────────────────────
  ```
- **Steelman mode**: `/balanced steelman <statement>`. Only moves 1+2. Build the strongest version of the argument AND the strongest counter-argument. No action steps. For preparing to defend a position.
- **Decision mode**: `/balanced decision <statement>`. Only move 4 (refinement) with an explicit tradeoff table. For when analysis is done and the call needs to be made.

## Output Modifiers

Append these flags to any mode:

- **`--table`**: Output pro/contra analysis as an ASCII table. Apply whenever the analysis has clear opposing factors. Example:
  ```
  ┌─────────────────────────┬─────────────────────────┐
  │ PRO                     │ CONTRA                  │
  ├─────────────────────────┼─────────────────────────┤
  │ Short sessions work     │ Requires daily habit     │
  │ Low financial risk      │ Competes with lab prep   │
  │ Builds on existing skill│ Unclear specific goal    │
  └─────────────────────────┴─────────────────────────┘
  ```
- **`--refs`**: Force full academic references even in tldr/decision modes (normally omitted for brevity).

## Four Moves

### 1 | Surface Merits
- Acknowledge well-supported points or creative angles.
- State why they are non-trivial. No generic praise.
- **Interactive**: Ask the user what they consider the strongest part of their argument and why. Then offer the analysis.

### 2 | Rigorous Challenge
- Question assumptions and potential biases.
- Test logic for gaps, fallacies, or over-generalization.
- Offer counter-evidence or rival explanations.
- **Interactive**: Present the strongest counter-argument found. Use AskUserQuestion to ask the user how they would respond. Then evaluate their response.

### 3 | Expansion
- Suggest alternative framings, methods, or resources.
- When helpful, pose clarifying questions rather than assume.
- **Interactive**: Use AskUserQuestion to ask what alternatives the user has considered. Then suggest framings they may have missed.

### 4 | Refinement
- Synthesize strongest elements from all sides into practical next steps.
- Flag residual uncertainty and cite sources.
- **Interactive**: Present a draft synthesis. Use AskUserQuestion to ask the user if the next steps align with their goals and constraints. Adjust based on their response.

## Interactive Mode Flow

When in interactive mode:
1. Begin by restating the user's position in one sentence. Use AskUserQuestion to confirm accuracy.
2. Walk through each move sequentially. Each move gets its own AskUserQuestion exchange.
3. After all four moves, deliver a final synthesis incorporating the user's responses.
4. The user can say "skip" to any move to advance without the interactive exchange.

## Meta-Rules

- No flattery. No needless pessimism.
- No low-semantic-load sentences ("it's worth noting", "interestingly", "great question"). No opinion statements.
- Maintain neutral, analytical tone. Quantify confidence when possible (e.g., "~70% confident based on available evidence").
- Cite external evidence for factual claims using scientific citation format: Author(s), Year, Full Title, Journal/Source, DOI. When referencing a DOI, perform a web search to validate it exists.
- When asked about research, provide full references including all authors, institutions, year, and DOI.
- Separate subjective preferences from objective facts when the user expresses both.
- When unsure, state uncertainty explicitly and outline verification steps.


================================================================================

## 12. Expert Skill: jtbd
> **Path within category:** `jtbd/SKILL.md`


# JTBD Project Describer

## Purpose

Conduct a focused Jobs-to-Be-Done interview for one project and emit a decision-grade artifact bundle. The bundle contains a machine-readable `jtbd.json`, a shareable `one-pager.md`, and a `messaging-angles.md` derived from Switch forces. Ingest voice transcripts or review exports when available.

## When to invoke

- "Describe my project in JTBD."
- "Turn this interview transcript into a JTBD brief."
- "Mine these reviews for jobs."
- "I need messaging from this product idea."
- "Help me articulate what I'm actually building."
- "Update my JTBD brief with new data."
- "Decompose this job into outcomes."
- "Generate a GTM brief from this JTBD."

If the user wants a full design spec (what to build, scope, components), prefer `skill-studio` — it's the heavier tool. `jtbd` is the quick, rigorous record.

## Mode selection

Pick one at the start. Ask the user only if ambiguous.

| Mode | Input | Output |
|---|---|---|
| **Interview** (default) | live conversation | full artifact bundle |
| **Transcript ingest** | path to a voice interview transcript | full artifact bundle + confidence flags |
| **Review mining** | path to reviews (CSV/JSON) | `review-brief.md` pre-seed → then Interview |
| **Update** | path to existing `~/jtbd/<slug>/jtbd.json` | updated artifact bundle |

## Scope discipline

One project per session. If the user starts describing a second project, stop them: "That sounds like a separate project — let's finish this one first, then run `/jtbd` again for the next."

If the user drifts into implementation details, features, or tech stack: "Interesting, but let's stay at the job level — what is the person trying to accomplish?"


## Granularity Gate (pre-save validator)

Before drafting the JSON, score the interview output 0–2 on five dimensions. Any score <1 blocks save. Use `references/granularity_fixes.md` for rewrite prompts.

| Dimension | 0 (fail) | 1 (ok) | 2 (strong) |
|---|---|---|---|
| **Actor specificity** | "users" / "people" | a role | a named actor with context |
| **Context / trigger** | "always" / none | a situation | a specific moment |
| **Current workaround** | "nothing" / "various" | named alternative | described attempt + why it fails |
| **Measurable outcome** | "better" / "improved" | directional metric | quantified target |
| **Evidence quote** | none | paraphrase | verbatim quote |

If any dimension scores 0, ask one targeted follow-up question and re-score. Don't interrogate — one rewrite pass, then accept what you have and flag the weak dimensions in `evidence.weaknesses[]`.

For deterministic scoring on ingest paths, call `scripts/validate_granularity.py` with the draft JSON.


## Output schema

### Core (always filled)

```json
{
  "name": "project-slug",
  "hook": "One sentence: what this is for whom, concretely.",
  "jtbd": {
    "situation": "When [specific context/trigger]...",
    "motivation": "I want to [action/goal]...",
    "outcome": "So I can [measurable result]..."
  },
  "problem": {
    "what_hurts": "Specific pain point with evidence."
  },
  "needs": {
    "functional": ["what it must do"],
    "emotional": ["how user wants to feel"]
  },
  "switch_forces": {
    "push": "What's frustrating about today.",
    "pull": "What's attractive about the new.",
    "habit": "What keeps them stuck.",
    "anxiety": "What they fear about switching."
  },
  "outputs": ["what the project produces/delivers"],
  "evidence": {
    "source": "interview | voice_transcript | reviews",
    "quotes": ["verbatim quotes if available"],
    "weaknesses": ["dimensions that scored 0 or 1 in granularity gate"]
  }
}
```

### Extended (include only when naturally surfaced)

```json
{
  "problem": { "cost_today": "What the pain costs (time, money, stress)." },
  "needs": { "social": ["relational/status needs"] },
  "before_after": {
    "before": "Visible + felt state before.",
    "after": "Visible + felt state after."
  },
  "scenarios": [{ "title": "Short label", "vignette": "1-2 sentence day-in-the-life story" }],
  "trigger": { "type": "manual | scheduled | event", "detail": "e.g. after every client call" },
  "version": 1,
  "guardrails": ["what it must NOT do"],
  "odi": {
    "outcomes": [
      { "statement": "Minimize the time it takes to...", "importance": 8.5, "satisfaction": 3.2, "opportunity_score": 13.8 }
    ]
  },
  "open_questions": ["follow-ups the interviewer didn't resolve"]
}
```

See `references/odi.md` for the importance/satisfaction/opportunity formula and when ODI is worth adding.


## Review-Mining Intake

When the user provides a reviews export:

1. Run `scripts/mine_reviews.py <path>` — clusters reviews by pain, outcome, and workaround.
2. The script emits `review-brief.md` in the output folder using `templates/review-brief.md` as a pre-seed.
3. Present the brief to the user. Ask: "Does this match your sense? Any missing patterns?"
4. Use the brief as Pass 0 before the regular interview — skip Pass 1 questions that the reviews already answered.
5. Set `evidence.source = "reviews"`.

See `references/review_taxonomy.md` for the clustering taxonomy.


## ODI Scoring Mode (optional)

Trigger when the user asks for prioritization, "what to build next," or roadmap input. Add the `odi` extended block.

1. Derive candidate outcome statements from the interview.
2. Ask the user to rate each outcome on importance (1–10) and current-solution satisfaction (1–10).
3. Run `scripts/odi_score.py` to compute opportunity scores.
4. Sort descending. Top 3 go into `odi.outcomes[]`.

Only add ODI when the user has 3+ candidate outcomes — below that, skip it.


================================================================================

## 13. Expert Skill: vision-bench
> **Path within category:** `vision-bench/SKILL.md`


# Vision Bench — LLM Image Evaluation

Compare images by scoring them with one or more vision LLM judges against structured rubric criteria.

## Quick Start

```bash
# Install dependencies
pip install pyyaml openai anthropic mistralai

# Score a single image
python bench.py image.png --criteria photorealism --judge gemini-2.5-flash

# Compare two AI-generated images
python bench.py img_a.png img_b.png \
  --criteria text_to_image \
  --prompt "a fox in a snowy forest" \
  --judge gpt-4o

# Multi-judge consensus
python bench.py img.png \
  --criteria portrait \
  --judges gpt-4o gemini-2.5-flash claude-opus-4-5-20251022

# OpenRouter models (any vision-capable model)
python bench.py img_a.png img_b.png \
  --criteria artistic_style \
  --judges "openrouter/meta-llama/llama-4-maverick" "openrouter/mistralai/pixtral-large-2411"

# List all presets
python bench.py --list-presets

# Save report to file
python bench.py img.png --criteria chart_analysis --save report.md
```

## Presets

| Preset | Use Case |
|--------|----------|
| `text_to_image` | Compare AI image generators (Midjourney, DALL-E, Flux) |
| `photorealism` | How convincingly an image looks like a photo |
| `artistic_style` | Style consistency, composition, color harmony |
| `portrait` | AI-generated portrait quality and realism |
| `product_photo` | E-commerce product image quality |
| `document_ocr` | Document text extraction and layout understanding |
| `chart_analysis` | Chart and data visualization comprehension |
| `invoice` | Financial document field extraction accuracy |
| `ui_screenshot` | App/web screenshot understanding |
| `scientific` | Scientific/medical image accuracy |
| `alt_text` | Accessibility image description quality |

Custom criteria: pass any `.yaml` file as `--criteria path/to/my.yaml`.

## Judge Providers

| Prefix | Provider | Example |
|--------|----------|---------|
| `gpt-`, `o1`, `o3`, `o4` | OpenAI | `gpt-4o` |
| `claude-` | Anthropic | `claude-sonnet-4-5-20251022` |
| `gemini-` | Google Gemini | `gemini-2.5-flash` |
| `pixtral-`, `mistral-`, `ministral-` | Mistral | `pixtral-12b-2409` |
| `openrouter/` | OpenRouter (any model) | `openrouter/meta-llama/llama-4-maverick` |

## API Keys

Keys are loaded from `secrets.enc.yaml` (SOPS + age encrypted) with fallback to environment variables.

Supported keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`

To encrypt your own keys:
```bash
sops --config .sops.yaml --encrypt --input-type yaml --output-type yaml secrets.yaml > secrets.enc.yaml
```

## Output Formats

`--output markdown` (default) · `--output json` · `--output table`

## Files

- `bench.py` — CLI entry point
- `judge.py` — Multi-provider LLM judge logic
- `report.py` — Report generation
- `vault.py` — SOPS secrets decryption
- `criteria/` — 11 YAML preset files
- `.sops.yaml` — Age key config for encryption
- `secrets.enc.yaml` — Encrypted API keys


================================================================================

## 14. Expert Skill: session-anonymizer
> **Path within category:** `session-anonymizer/SKILL.md`


# Therapy Anonymizer

Three-layer PII detection and anonymization for therapy session transcripts. Supports Russian and English. Fully local by default — no data leaves the machine.

## Architecture

Three detection layers run in sequence, each catching what others miss:

| Layer | Tool | Catches | Size | Speed |
|-------|------|---------|------|-------|
| 1 | Natasha | Russian names, locations, organizations | 27 MB | instant |
| 2 | OpenAI Privacy Filter (opf) | Phones, accounts, addresses, emails | 2.8 GB | ~1.5s |
| 3 | Ollama LLM | Medications, dates, contextual IDs | 2.5-7 GB | ~10s |

Spans from all layers are merged, overlaps resolved, and a unified redacted output is produced.

## Prerequisites

```bash
pip install natasha setuptools pymorphy2-dicts-ru
pip install 'opf @ git+https://github.com/openai/privacy-filter.git'
ollama pull qwen3:4b
```

Each layer is optional — the script gracefully skips unavailable layers and warns.

## Usage

### Single file

```bash
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py session.txt
```

### Stdin pipe

```bash
cat session.txt | python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py
```

### Batch processing

```bash
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py --batch ~/sessions/ -o ~/sessions_clean/
```

### JSON report

```bash
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py session.txt --json
```

### Pseudonyms instead of tags

```bash
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py session.txt --pseudonyms
```

### Select layers / model

```bash
# Fast — Natasha only
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py session.txt --layers natasha

# LLM only — maximum coverage
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py session.txt --layers ollama --model gemma4:e2b
```

### Encrypt output (AES-256)

```bash
python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py session.txt -o clean.txt --encrypt "password"
```

## Invoking from Claude Code

To anonymize text already in context, pipe it through the script:

```bash
echo '<text>' | python3 ~/.claude/skills/therapy-anonymizer/scripts/anonymize.py --json
```

For files, pass the path directly. Always recommend manual review after automated anonymization.

## Limitations

- Contextual identifiers ("the only red-haired architect in Kostroma") are NOT detected by any automated tool
- OPF is English-focused — Russian coverage is partial
- Medications detected only by Layer 3 (requires Ollama)
- Does not assess re-identification risk from combinations of non-PII fields

## Guardrails

- NEVER send raw transcripts to cloud services
- Cloud verification only on already-anonymized text
- Always recommend manual review for therapy data
- Never log original PII values


================================================================================

## 15. Expert Skill: wispr-analytics
> **Path within category:** `wispr-analytics/SKILL.md`


# Wispr Analytics

Extract and analyze Wispr Flow dictation history from the local SQLite database. Combine quantitative metrics with LLM-powered qualitative analysis for self-reflection, work pattern recognition, and mental health awareness.

## Data Source

Wispr Flow stores all dictations in SQLite at:
```
~/Library/Application Support/Wispr Flow/flow.sqlite
```

Key table: `History` with fields: `formattedText`, `timestamp`, `app`, `numWords`, `duration`, `speechDuration`, `detectedLanguage`, `isArchived`.

The user has ~8,500+ dictations since Feb 2025, bilingual (Russian/English), across apps: iTerm2, ChatGPT, Arc browser, Claude Desktop, Windsurf, Telegram, Obsidian, Perplexity.

## Extraction Script

Run `scripts/extract_wispr.py` to pull data from the database:

```bash
# Get today's data as JSON with stats + text samples
python3 scripts/extract_wispr.py --period today --mode all --format json

# Get markdown stats for the last week
python3 scripts/extract_wispr.py --period week --format markdown

# Get text samples only for LLM analysis
python3 scripts/extract_wispr.py --period month --mode mental --texts-only

# Save to file
python3 scripts/extract_wispr.py --period week --format markdown --output /path/to/output.md
```

### Period Options
- `today` -- current day (default)
- `yesterday` -- previous day
- `week` -- last 7 days
- `month` -- last 30 days
- `YYYY-MM-DD` -- specific date
- `YYYY-MM-DD:YYYY-MM-DD` -- date range

### Mode Options
- `all` -- full analysis (default)
- `technical` -- filters to coding/AI tool dictations
- `soft` -- filters to communication/writing dictations
- `trends` -- focus on volume/frequency patterns
- `mental` -- all text, framed for wellbeing reflection

### Comparison & Graphs
- `--compare` -- auto-compare with the equivalent previous period (week vs previous week, month vs previous month)
- `--graphs PATH` -- generate an HTML dashboard with Chart.js graphs (implies --compare). Graphs include: daily words overlay, hourly activity, category breakdown, top apps, language distribution

```bash
# Compare this month vs previous month (markdown)
python3 scripts/extract_wispr.py --period month --compare --format markdown

# Generate visual dashboard for week comparison
python3 scripts/extract_wispr.py --period week --compare --graphs /tmp/wispr-week.html

# Compare and save both markdown + graphs
python3 scripts/extract_wispr.py --period month --compare --format markdown --output report.md --graphs report.html
```

## Workflow

### Step 1: Extract Data

Run the extraction script with the requested period and mode. Use `--format json` for full data or `--texts-only` for LLM analysis focus.

### Step 2: Present Quantitative Stats

Display the quantitative summary first:
- Total dictations, words, speech time
- Category breakdown (coding, ai_tools, communication, writing, other)
- Language distribution
- Hourly activity pattern
- Daily trends (for multi-day periods)
- Top apps

### Step 3: Perform Qualitative Analysis

Read `references/analysis-prompts.md` to load the appropriate analysis template for the requested mode. Then analyze the text samples using that template.

For each mode:

**Technical**: Focus on what was worked on, technical decisions, context-switching patterns, productivity assessment.

**Soft**: Focus on communication style shifts, language-switching patterns, audience adaptation, interpersonal dynamics.

**Trends**: Focus on volume changes, time-of-day shifts, app migration, behavioral change hypotheses.

**Mental**: Focus on energy proxies, sentiment signals, rumination detection, activity pattern changes. Frame all observations as invitations for self-reflection, never as diagnoses. Use language like "you might notice..." or "this pattern could suggest..."

**All**: Combine all four perspectives into a unified reflection.

### Step 4: Output

Default output location: `meta/wispr-analytics/YYYYMMDD-period-mode.md` in the vault.

File format:
```markdown

# Wispr Flow Analytics: [period]

## Quantitative Summary
[stats from Step 2]

## Analysis
[qualitative analysis from Step 3]

## Reflection Prompts
[3-5 questions based on observations]
```

If the user requests console-only output, skip file creation and display directly.

## App Category Mapping

The extraction script categorizes apps:
- **coding**: iTerm2, cmuxterm, VS Code, Windsurf, Zed, Cursor, Terminal
- **ai_tools**: ChatGPT, Claude Desktop, Perplexity, OpenAI Atlas, Codex
- **communication**: Telegram, Messages, Slack, Zoom
- **writing**: Obsidian, Notes, Chrome, Arc browser

## Dictionary Management

Manage Wispr Flow's dictionary for better recognition accuracy. The dictionary JSON is version-controlled in `~/ai_projects/claude-skills/wispr-analytics/data/dictionary.json`.

### Dictionary Script

Run `scripts/wispr_dictionary.py` for all dictionary operations:

```bash
# Check database health and dictionary stats
python3 scripts/wispr_dictionary.py check

# List all entries (safe while Wispr is running)
python3 scripts/wispr_dictionary.py list
python3 scripts/wispr_dictionary.py list --filter "claude"

# Export dictionary to JSON (safe while running)
python3 scripts/wispr_dictionary.py export

# Suggest new entries by analyzing ASR vs formatted text differences
python3 scripts/wispr_dictionary.py suggest --days 30 --min-freq 3

# Add a single term (requires Wispr Flow to be QUIT)
python3 scripts/wispr_dictionary.py add "Gastown"
python3 scripts/wispr_dictionary.py add "cloud code" "Claude Code"

# Remove an entry (requires Wispr Flow to be QUIT)
python3 scripts/wispr_dictionary.py remove "old term"

# Import from JSON (requires Wispr Flow to be QUIT)
python3 scripts/wispr_dictionary.py import --dry-run
python3 scripts/wispr_dictionary.py import
```

### Dictionary Safety Rules

**CRITICAL**: Wispr Flow must be quit before any write operations (add, remove, import). The script enforces this automatically. Read operations (export, list, suggest, check) are safe while Wispr is running.

Writing to the SQLite database while Wispr Flow has it open causes index corruption. Always:
1. Check if Wispr is running: `pgrep -f "Wispr Flow"`
2. If running, ask user to quit first (Cmd+Q)
3. After writes, run `check` to verify integrity
4. Restart Wispr Flow

### Dictionary Entry Types

- **Recognition terms** (phrase only): teaches Wispr to hear the word correctly (e.g., "Gastown", "LLM", "subagent")
- **Replacement rules** (phrase → replacement): auto-corrects mishears (e.g., "cloud code" → "Claude Code", "клод дизайн" → "Claude Design")
- **Snippets** (isSnippet=true): text expansion shortcuts (e.g., "my email" → "glebis@gmail.com")

### Proactive Dictionary Improvement Workflow

When running analytics, also check for dictionary improvement opportunities:

1. Run `suggest` to find recurring ASR corrections
2. Compare `asrText` vs `formattedText` for patterns
3. Look for Russian/English code-switching mishears
4. Check for new technical terms the user started using
5. Export updated dictionary and commit to git

## Notes

- For analytics: the database is read-only; analytics never modifies Wispr data
- For dictionary: writes require Wispr Flow to be quit first
- Text samples are capped at 100 per extraction to manage context window
- For multi-day periods, daily trend tables help visualize changes
- Bilingual dictations are common; analysis should honor both Russian and English
- The `asrText` field contains raw speech recognition before formatting -- useful for detecting speech patterns vs formatted output
- Dictionary JSON is stored at `~/ai_projects/claude-skills/wispr-analytics/data/dictionary.json` for version control


================================================================================

## 16. Expert Skill: decision-toolkit
> **Path within category:** `decision-toolkit/SKILL.md`


# Decision Toolkit

## Overview

Create structured decision support materials that help humans think through significant choices systematically. This skill produces interactive tools, not just analysis — empowering the decision-maker rather than deciding for them.

## Philosophy

### Principles

1. **Guide, don't decide** — Tools illuminate the decision space; humans choose
2. **One thing at a time** — Reduce cognitive load through progressive disclosure
3. **Multiple lenses** — Same decision viewed through different frameworks reveals blind spots
4. **Biases visible** — Make cognitive biases explicit and checkable
5. **Actionable output** — End with concrete next steps, not abstract conclusions

### Accessibility First

- Support screen readers (semantic HTML, ARIA labels)
- Keyboard navigable (tab order, focus states)
- High contrast by default (WCAG AA minimum)
- Reduced motion option
- Works without JavaScript (graceful degradation)
- Mobile-friendly touch targets (44px minimum)

### Cognitive Inclusivity

Different people process decisions differently:

| Style | Accommodation |
|-------|---------------|
| **Analytical** | Numbers, matrices, weighted scores |
| **Intuitive** | Gut-check prompts, "how does this feel?" |
| **Visual** | Diagrams, progress bars, color coding |
| **Verbal** | Written summaries, question prompts |
| **Sequential** | Step-by-step wizard flow |
| **Global** | Dashboard overview option |

## When to Use

Invoke this skill when user faces:
- Collaboration/partnership decisions
- Career or job changes
- Investment of significant time/money
- Project prioritization
- Technology/tool selection
- Any choice with multiple factors and uncertainty

**Not for**: Trivial decisions, emergency responses, or when user just needs information.

## Decision Types

### Type 1: Opportunity Evaluation
*Should I pursue this opportunity?*
- Partnership, job offer, investment, project

### Type 2: Resource Allocation
*Where should I invest my time/money/attention?*
- Prioritization, budgeting, focus areas

### Type 3: Risk Assessment
*What could go wrong and is it worth it?*
- New ventures, changes, experiments

### Type 4: Trade-off Navigation
*Which option among alternatives?*
- Tool selection, hire decisions, strategic choices

## The Decision Journey

Nine steps, each focused on one dimension:

```
┌─────────────────────────────────────────────────────────────┐
│  1. CONTEXT         What is the decision?                   │
│  2. FIRST PRINCIPLES Does this solve a real problem?        │
│  3. TIMING          Is now the right moment?                │
│  4. STAKEHOLDERS    Who else is involved? Are they stable?  │
│  5. BIASES          What might cloud my judgment?           │
│  6. OPPORTUNITY COST What am I giving up?                   │
│  7. SCENARIOS       What could happen?                      │
│  8. QUESTIONS       What do I still need to learn?          │
│  9. SYNTHESIS       Summary + decision                      │
└─────────────────────────────────────────────────────────────┘
```

## Output Formats

### 1. Interactive HTML Guide (Primary)
Step-by-step wizard with:
- Progress indicator
- One question per screen
- State persistence across steps
- Final summary aggregating all inputs
- Keyboard navigation
- Print-friendly CSS

### 2. Markdown Framework
For offline/text-based use:
- Structured prompts
- Checkbox-style bias audit
- Fill-in-the-blank templates

### 3. Voice Summary
For audio consumption:
- 5-7 paragraph executive summary
- Orpheus TTS markup for emotional texture
- Key decision + rationale

### 4. PDF Report
For documentation/sharing:
- Professional formatting
- All frameworks applied
- Appendix with raw analysis

## Frameworks Reference

### First Principles Test
```
1. What problem does this solve?
2. Can I solve it myself?
3. Is this the best solution?
4. What assumptions am I making?
5. If starting fresh today, would I choose this?
```

### Bias Checklist
```
□ FOMO — Am I afraid of missing out?
□ Sunk Cost — Am I factoring past investment?
□ Authority — Am I deferring to credentials?
□ Social Proof — Am I following the crowd?
□ Commitment — Do I feel locked in by past statements?
□ Optimism — Am I assuming problems will resolve?
□ Recency — Am I overweighting recent events?
□ Confirmation — Am I seeking validating info only?
□ Shiny Object — Is novelty distracting me?
□ Loss Aversion — Am I overweighting potential losses?
```

### Opportunity Cost Calculator
```
Hours/week × Weeks × Hourly rate = Direct cost
+ What else could those hours produce?
+ What relationships/opportunities might suffer?
= True opportunity cost
```

### Scenario Matrix
```
| Scenario | Probability | Outcome | Expected Value |
|----------|-------------|---------|----------------|
| Worst    | X%          | ...     | ...            |
| Bad      | X%          | ...     | ...            |
| Neutral  | X%          | ...     | ...            |
| Good     | X%          | ...     | ...            |
| Best     | X%          | ...     | ...            |
```

### Pre-mortem
```
Imagine it's [future date]. This decision failed. Why?

Possible causes:
1. ...
2. ...
3. ...

Which causes are within my control?
Which warning signs should I watch for?
```

### 10-10-10 Framework
```
How will I feel about this decision in:
- 10 minutes?
- 10 months?
- 10 years?
```

### Regret Minimization
```
Imagine you're 80 looking back.
Would you regret doing this?
Would you regret NOT doing this?
```

## Implementation Guide

### Step 1: Gather Context

Ask user for:
- What is the decision?
- What are the options?
- What's the timeline?
- What's at stake?
- Any relevant background?

Or extract from existing documents (meeting transcripts, notes).

### Step 2: Choose Output Format

Based on user preference and context:
- Complex decision + time available → Interactive HTML
- Quick analysis → Markdown framework
- On-the-go consumption → Voice summary
- Need to share with others → PDF report

### Step 3: Generate Tool

Use templates in `templates/` directory:
- `decision-guide-template.html` — Full interactive wizard
- `decision-framework.md` — Text-based analysis
- `decision-voice-summary.md` — Audio script template

### Step 4: Customize

Replace placeholders:
- `{{DECISION_TITLE}}` — What's being decided
- `{{CONTEXT}}` — Background information
- `{{OPTIONS}}` — Available choices
- `{{STAKEHOLDERS}}` — People/teams involved
- `{{TIMELINE}}` — Relevant dates
- `{{FACTORS}}` — Key evaluation criteria

### Step 5: Apply Branding (Optional)

If using Agency brand:
- Import brand-agency skill CSS variables
- Use neobrutalism styling
- Apply Geist/EB Garamond typography

## Accessibility Implementation

### Semantic HTML
```html
<main role="main" aria-label="Decision Guide">
  <nav aria-label="Progress">
    <ol role="list">...</ol>
  </nav>
  <section aria-labelledby="step-title">
    <h1 id="step-title">...</h1>
  </section>
</main>
```

### Keyboard Navigation
```javascript
// Ensure all interactive elements are focusable
// Tab order follows visual order
// Enter/Space activate buttons
// Arrow keys navigate options
```

### Screen Reader Announcements
```html
<div role="status" aria-live="polite" id="announcer">
  <!-- Announce step changes, selections, results -->
</div>
```

### Color Contrast
```css
/* Minimum 4.5:1 for normal text, 3:1 for large text */
--text-on-light: #000000;  /* 21:1 on white */
--text-on-dark: #ffffff;   /* 21:1 on black */
--text-on-primary: #ffffff; /* Check each color */
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Cultural Considerations

### Individualist Framing
- "What do YOU want?"
- Personal goals and values
- Individual opportunity cost

### Collectivist Framing
- "How does this affect your team/family?"
- Relationship implications
- Group harmony considerations

### Power Distance Awareness
- Some cultures defer to authority figures
- Bias check should include "Am I deferring inappropriately?"
- Include stakeholder perspectives explicitly

### Uncertainty Tolerance
- Some prefer detailed scenario analysis
- Others find it anxiety-inducing
- Offer both detailed and simplified views

## Example Invocations

### From Meeting Transcript
```
User: Analyze this meeting transcript and create a decision toolkit
Claude: [Extracts decision, stakeholders, options from transcript]
        [Generates interactive HTML guide]
        [Creates voice summary]
```

### From Scratch
```
User: I need to decide whether to take a new job offer
Claude: [Asks clarifying questions]
        [Generates decision framework]
        [Customizes for career decision type]
```

### Quick Analysis
```
User: Help me think through this partnership decision, just give me the frameworks
Claude: [Provides markdown framework]
        [Skips interactive tool]
        [Focuses on key questions]
```

## Files

- `SKILL.md` — This file
- `templates/decision-guide-template.html` — Interactive wizard template
- `templates/decision-framework.md` — Text-based analysis template
- `templates/decision-voice-summary.md` — Audio script template
- `references/bias-encyclopedia.md` — Detailed bias descriptions
- `references/framework-deep-dives.md` — Extended framework explanations

## Integration

Works well with:
- **brand-agency** — Apply visual branding
- **transcript-analyzer** — Extract decisions from meetings
- **pdf-generation** — Create shareable reports
- **elevenlabs-tts** — Generate audio summaries

## Learnings

### 2026-01-09
**Context**: Initial skill creation from Synthius decision session

**Key Insight**: Dashboard-everything-at-once overwhelms. Step-by-step wizard with one concept per screen dramatically improves usability.

**Architecture**: 9-step journey covering all major decision dimensions. State object persists selections across steps. Summary aggregates everything.

**Accessibility Note**: High contrast neobrutalism actually helps accessibility — clear borders, distinct states, no subtle gradients.


================================================================================

## 17. Expert Skill: recording
> **Path within category:** `recording/SKILL.md`


# Recording Mode

Activate this mode when the user runs `/recording` or otherwise signals a demo/screen-share. Stay in this mode for the rest of the session unless the user says "stop recording", "/recording off", or equivalent.

## Core rule

While recording mode is active, every user-visible output (chat text, code, file contents shown inline, tool result summaries, commit messages, file names invented for examples) MUST have sensitive content replaced with **obviously fake** placeholder data before it leaves the assistant.

This applies to text the model generates. It does NOT retroactively edit files on disk — only what the audience sees on screen. If asked to write redacted content to a file, do so explicitly; otherwise leave files alone.

## What to redact

Replace these categories:

- **Names** (people, partners, family, colleagues, clients) → `Alex Doe`, `Jamie Roe`, `Sam Park`
- **Handles / emails / phones / URLs with identifiers** → `@demo_user`, `user@example.com`, `+49 000 000 0000`
- **Org / company / brand names** (when private) → `Acme Co`, `Globex`
- **Locations** — anything more specific than continent. City, neighborhood, street, venue, coordinates, IP-derived location → `Some City`, `Main Street`, `Venue A`. Even "Berlin" gets replaced if it could identify the user.
- **Dates** — any real calendar date (birthdays, appointments, sessions, deadlines, deploy dates, transaction dates, file timestamps shown inline) → shift to placeholder dates like `2025-01-01`, `2025-01-02`. Keep relative ordering and weekday if it matters to the demo. Today's actual date should be replaced too if it appears in output.
- **Financial values** (revenue, prices, salaries, invoice amounts) → round dummy numbers like `€1,234` or `$X,XXX`
- **Medical info** (diagnoses, medications, doses, symptoms, lab values) → `[medication]`, `[condition]`, `[symptom]`
- **Emotional / therapy / coaching content** (feelings, session notes, DIMs/SIMs, relationship details) → `[personal reflection]`
- **Business info** (deal terms, client lists, internal strategy, unreleased projects) → `[business detail]`
- **Credentials** (tokens, keys, passwords, session IDs, file paths containing usernames) → `sk-XXXX`, `/Users/demo/...`
- **Genetic / health data** specific to the user → `[genetic marker]`

When in doubt, redact. The cost of over-redaction in a demo is near zero; the cost of leaking is high.

## Style of replacement

- Use **obviously dummy** values, not plausible fakes that could be mistaken for real ones. `Alex Doe` not `Andrey Volkov`. `Acme Co` not `Northwind Studio`.
- Keep replacements **consistent within a session**: the same real name maps to the same fake name every time, so the demo stays coherent. Maintain this mapping mentally for the duration of recording mode.
- Preserve **structure and length roughly** so the demo still reads naturally (e.g. a real email becomes a fake email, not `[REDACTED]`).
- Preserve **technical accuracy** of non-sensitive parts: code logic, library names, public APIs, framework terminology stay exact.

## What NOT to redact

- Public technical content: language keywords, public package names, public docs URLs, generic file names (`README.md`, `package.json`).
- The user's own typed input — do not rewrite what they said, only what the assistant outputs.
- Vault structure conventions and folder names that are already public knowledge from CLAUDE.md.

## Tool calls

Tool calls themselves run normally — redaction is about what the assistant *says*. But:

- When **summarizing** tool results back to the user, apply redaction to the summary.
- When **quoting** file contents inline (e.g. showing a snippet of a daily note), redact the snippet.
- Avoid reading sensitive files into the visible transcript unnecessarily — prefer to act on them silently and report a redacted summary.

## Toggle behavior

`/recording` is a **toggle**. Calling it flips the current state:

- If recording mode is OFF, `/recording` turns it ON. Reply with one short redacted line confirming it's on.
- If recording mode is ON, `/recording` turns it OFF. Reply with one short line confirming it's off, then resume normal output.

Track the current state across the session. Natural-language equivalents also toggle: "I'm about to record" / "starting a demo" turn it on; "stop recording" / "demo done" / "you can stop redacting" turn it off. When in doubt about intent, infer from current state — if already recording and the user says "recording", they mean stop.

## Self-check before sending

Before emitting any message while recording mode is active, scan the draft for:
1. Any proper noun that isn't a public technical term.
2. Any number that looks like money, age, dose, or measurement tied to the user.
3. Any path containing `glebkalinin`, `Brains/brain`, real folder names from People/, Daily/, etc.
4. Any emotional or medical vocabulary tied to a first-person subject.

If any hit, redact and re-check. Only then send.


================================================================================

## 18. Expert Skill: gws
> **Path within category:** `gws/SKILL.md`


# Google Workspace CLI (gws)

CLI for Gmail, Calendar, Drive, Sheets, Docs, Slides, Tasks, People, Chat, Meet, Forms, Keep, Admin, and cross-service workflows.

Binary: `/opt/homebrew/bin/gws`

## Command Pattern

```
gws <service> <resource> [sub-resource] <method> [flags]
```

Every command accepts:
- `--params <JSON>` — URL/query parameters
- `--json <JSON>` — request body (POST/PATCH/PUT)
- `--upload <PATH>` — file to upload as media content
- `--output <PATH>` — path for binary responses (downloads)
- `--format json|table|yaml|csv` — output format (default: json)
- `--page-all` / `--page-limit N` — auto-paginate
- `--dry-run` — validate locally without sending

## Quick Reference — Helper Commands (prefer these)

| Command | Purpose | R/W |
|---|---|---|
| `gws gmail +triage [--max N] [--query Q]` | Unread inbox summary | R |
| `gws gmail +send --to EMAIL --subject S --body T` | Send plaintext email | W |
| `gws gmail +watch --project GCP` | Stream new emails (Pub/Sub) | R |
| `gws calendar +agenda [--today\|--tomorrow\|--week\|--days N]` | Upcoming events | R |
| `gws calendar +insert --summary T --start ISO --end ISO` | Create event | W |
| `gws drive +upload FILE [--parent ID] [--name N]` | Upload file | W |
| `gws sheets +read --spreadsheet ID --range R` | Read range (e.g. `Sheet1!A1:D10`) | R |
| `gws sheets +append --spreadsheet ID --values "a,b,c"` | Append row (or `--json-values`) | W |
| `gws docs +write --document ID --text T` | Append text to doc | W |
| `gws chat +send --space spaces/ID --text T` | Post to Chat space | W |
| `gws workflow +standup-report` | Today's meetings + open tasks | R |
| `gws workflow +meeting-prep [--calendar ID]` | Next meeting details | R |
| `gws workflow +email-to-task --message-id ID` | Email → Task | W |
| `gws workflow +weekly-digest` | Week's meetings + unread | R |
| `gws workflow +file-announce --file-id ID --space SPACE` | Announce file in Chat | W |

## Common Patterns

### Gmail
```bash
# Triage unread (table for humans)
gws gmail +triage --max 10 --format table

# Search
gws gmail users messages list --params '{"userId":"me","q":"from:amazon newer_than:7d","maxResults":5}'

# Read full message
gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}'

# Read headers only (faster)
gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"metadata","metadataHeaders":["Subject","From","Date"]}'

# Archive (remove INBOX)
gws gmail users messages modify --params '{"userId":"me","id":"MSG_ID"}' --json '{"removeLabelIds":["INBOX"]}'

# Trash
gws gmail users messages trash --params '{"userId":"me","id":"MSG_ID"}'

# Bulk label
gws gmail users messages batchModify --params '{"userId":"me"}' --json '{"ids":["ID1","ID2"],"addLabelIds":["Label_123"]}'
```

### Calendar
```bash
# Today (Europe/Berlin default works with RFC3339 +02:00/+01:00)
gws calendar +agenda --today --format table

# Create simple event
gws calendar +insert \
  --summary 'AGENCY Meetup' \
  --start '2026-04-14T18:00:00+02:00' \
  --end '2026-04-14T19:00:00+02:00' \
  --location 'https://us02web.zoom.us/j/8991032224' \
  --description 'Zoom: https://us02web.zoom.us/j/8991032224'

# Event WITH Google Meet link (helper doesn't support — use raw)
gws calendar events insert \
  --params '{"calendarId":"primary","conferenceDataVersion":1}' \
  --json '{
    "summary":"Sync",
    "start":{"dateTime":"2026-04-15T14:00:00+02:00"},
    "end":{"dateTime":"2026-04-15T15:00:00+02:00"},
    "conferenceData":{"createRequest":{"requestId":"req-'$(date +%s)'","conferenceSolutionKey":{"type":"hangoutsMeet"}}}
  }'

# Update event
gws calendar events patch --params '{"calendarId":"primary","eventId":"EID"}' --json '{"summary":"New title"}'

# Delete
gws calendar events delete --params '{"calendarId":"primary","eventId":"EID"}'

# List all calendars
gws calendar calendarList list --format table
```

### Drive
```bash
# Upload to root
gws drive +upload ./report.pdf

# Upload to folder
gws drive +upload ./data.csv --parent FOLDER_ID --name 'Sales Data.csv'

# Search files
gws drive files list --params '{"q":"name contains \"report\" and mimeType=\"application/pdf\"","pageSize":10}'

# Download
gws drive files get --params '{"fileId":"FID","alt":"media"}' --output ./local.pdf

# Create folder
gws drive files create --json '{"name":"MyFolder","mimeType":"application/vnd.google-apps.folder"}'

# Share with user
gws drive permissions create --params '{"fileId":"FID"}' --json '{"role":"reader","type":"user","emailAddress":"user@example.com"}'
```

### Sheets
```bash
# Read
gws sheets +read --spreadsheet SID --range 'Sheet1!A1:D10' --format table

# Append single row (simple values)
gws sheets +append --spreadsheet SID --values 'Alice,100,true'

# Append multiple rows
gws sheets +append --spreadsheet SID --json-values '[["a","b"],["c","d"]]'
```

### Tasks
```bash
gws tasks tasklists list
gws tasks tasks list --params '{"tasklist":"@default"}'
gws tasks tasks insert --params '{"tasklist":"@default"}' --json '{"title":"My task","notes":"Details","due":"2026-04-20T00:00:00Z"}'
gws tasks tasks patch --params '{"tasklist":"@default","task":"TID"}' --json '{"status":"completed"}'
```

### Chat
```bash
# Find space
gws chat spaces list --format table

# Post message
gws chat +send --space spaces/AAAAxxxx --text 'Hello team!'
```

### People / Contacts
```bash
gws people people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses","pageSize":100}'
gws people people searchContacts --params '{"query":"John","readMask":"names,emailAddresses"}'
```

## Critical Notes

- **userId**: Every Gmail raw call needs `"userId":"me"` in params.
- **RFC3339 times**: Calendar uses full ISO with offset (`2026-04-14T18:00:00+02:00`). "Z" for UTC.
- **Meet links**: `+insert` does NOT add conferencing — use raw `events.insert` with `conferenceDataVersion=1` and `conferenceData.createRequest`.
- **Pagination**: `--page-all` emits NDJSON (one JSON object per page). `--page-limit N` caps pages.
- **Schema discovery**: `gws schema <service>.<resource>.<method>` — e.g. `gws schema gmail.users.messages.list`.
- **Filters**: `gmail.settings.basic` scope required — special manual OAuth flow (see `references/api_reference.md`).
- **Write confirmation**: Always confirm with user before `+send`, `+insert`, `+email-to-task`, `+file-announce`, `drive files delete`, `events delete`, `messages trash`.
- **Format choice**: `--format table` for human-readable summaries; default `json` for scripting/piping to `jq`.

## OAuth Setup

- GCP project: `n8n-automations-454016`
- Credentials: `~/.config/gws/credentials.json`
- Configured scopes: `gmail.modify`, `gmail.settings.basic`, `drive`, `spreadsheets`, `tasks`, `calendar`, `documents`, `chat.messages`, `contacts.readonly`
- `gmail.settings.basic` scope needs manual OAuth (Python localhost listener on port 8085) — `gws auth login --scopes` cannot request it directly.

## Full API Reference

For full command inventory, all raw API calls, pagination, labels, drafts, filters, and admin APIs, see `references/api_reference.md`.


================================================================================

## 19. Expert Skill: linear
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


================================================================================

## 20. Expert Skill: codex
> **Path within category:** `codex/SKILL.md`


# Codex Skill Guide

## Running a Task
1. **Do NOT specify a model by default.** The Codex CLI is configured with a ChatGPT account, and explicit model flags (`-m gpt-5-codex`, `-m gpt-5`, `-m o4-mini`) all fail with "not supported when using Codex with a ChatGPT account." Omitting `-m` lets Codex use its default model, which works. Only add `-m` if the user explicitly requests a specific model.
2. Select the sandbox mode required for the task; default to `--sandbox read-only` unless edits or network access are necessary.
3. Assemble the command with the appropriate options:
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `--full-auto`
   - `-C, --cd <DIR>`
   - `--skip-git-repo-check`
   - `-m, --model <MODEL>` (only if user explicitly requests)
   - `--config model_reasoning_effort="<high|medium|low>"` (only if user explicitly requests)
4. Always use --skip-git-repo-check.
5. When continuing a previous session, use `codex exec --skip-git-repo-check resume --last` via stdin. When resuming don't use any configuration flags unless explicitly requested by the user. Resume syntax: `echo "your prompt here" | codex exec --skip-git-repo-check resume --last 2>/dev/null`. All flags have to be inserted between exec and resume.
6. **IMPORTANT**: By default, append `2>/dev/null` to all `codex exec` commands to suppress thinking tokens (stderr). Only show stderr if the user explicitly requests to see thinking tokens or if debugging is needed.
7. Run the command, capture stdout/stderr (filtered as appropriate), and summarize the outcome for the user.
8. **After Codex completes**, inform the user: "You can resume this Codex session at any time by saying 'codex resume' or asking me to continue with additional analysis or changes."

### Quick Reference
| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Permit network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Resume recent session | Inherited from original | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` (no flags allowed) |
| Run from another directory | Match task needs | `-C <DIR>` plus other flags `2>/dev/null` |

## Following Up
- After every `codex` command, immediately use `AskUserQuestion` to confirm next steps, collect clarifications, or decide whether to resume with `codex exec resume --last`.
- When resuming, pipe the new prompt via stdin: `echo "new prompt" | codex exec resume --last 2>/dev/null`. The resumed session automatically uses the same model, reasoning effort, and sandbox mode from the original session.
- Restate the chosen model, reasoning effort, and sandbox mode when proposing follow-up actions.

## Error Handling
- Stop and report failures whenever `codex --version` or a `codex exec` command exits non-zero; request direction before retrying.
- Before you use high-impact flags (`--full-auto`, `--sandbox danger-full-access`, `--skip-git-repo-check`) ask the user for permission using AskUserQuestion unless it was already given.
- When output includes warnings or partial results, summarize them and ask how to adjust using `AskUserQuestion`.


================================================================================

## 21. Expert Skill: deep-research
> **Path within category:** `deep-research/SKILL.md`


# Deep Research Skill

## Purpose

This skill enables comprehensive, internet-enabled research on any topic using OpenAI's Deep Research API (o4-mini-deep-research model). It intelligently enhances user research prompts through interactive clarifying questions, ensures research parameters are saved for reproducibility, and executes deep research with full web search capabilities.

## When to Use This Skill

Trigger this skill when:
- User requests research on a specific topic
- User asks for analysis, investigation, or comprehensive information gathering
- User wants exploration of a subject with web search and reasoning
- User provides a brief research query that could be refined
- User wants to understand current state, trends, or comparisons in a field

Example user requests:
- "Research the most effective open-source RAG solutions with high benchmark performance"
- "What are the latest AI developments in 2025?"
- "I need a comprehensive analysis of distributed database systems"
- "Find best practices for implementing vector search"
- "Investigate how AI is impacting the software engineering industry"

## Workflow Overview

```
User Input
    ↓
Assessment: Prompt too brief?
    ↓
YES → Ask Enhancement Questions → Collect Answers
    ↓                               ↓
    └───────→ Construct Enhanced Prompt ←──┘
                    ↓
            Save to Timestamped File
                    ↓
            Execute deep_research.py
                    ↓
            Output Report + Sources
                    ↓
            Present to User
```

## How Claude Should Use This Skill

**Important for Token Efficiency:**
Deep research takes 10-20 minutes to complete. The skill is designed to run synchronously (blocking) without intermediate status checks. This approach minimizes token usage during the wait. Claude should:
1. Start the research
2. Wait for completion (subprocess blocks automatically)
3. Present final results once complete

No need for periodic polling or status updates during execution.

### Step 1: Accept Research Request

Receive the user's research prompt. This can range from brief ("Latest AI trends") to highly detailed ("Impact of language models on developer productivity with focus on 2024-2025").

### Step 2: Execute the Orchestration Script

Run the skill's main orchestration script with the user's research prompt:

```bash
python3 scripts/run_deep_research.py "Your research prompt here"
```

The script is located at `scripts/run_deep_research.py` within the skill's installation.

### Step 3: Script Execution Flow

The script automatically:

1. **Assesses prompt completeness**: Checks if prompt is too brief or generic (< 15 words or starts with "what is", "how to", etc.)

2. **Asks clarifying questions** (if needed):
   - Presents 2-3 focused questions relevant to the research type
   - Detects if research is technical or general based on keywords
   - Allows users to select from predefined options (1-4) or provide custom text
   - Questions cover: Scope/Timeframe, Depth level, Focus areas

3. **Enhances the prompt**: Combines original prompt with user's answers into structured research parameters

4. **Saves prompt file**: Writes enhanced prompt to `research_prompt_YYYYMMDD_HHMMSS.txt` for reproducibility

5. **Executes deep research**: Runs the core `deep_research.py` script with:
   - Model: o4-mini-deep-research (configurable via `--model`)
   - Timeout: 1800 seconds / 30 minutes (configurable via `--timeout`)
   - Tools: Web search enabled by default

### Step 4: Present Results to User

The script automatically:
- **Saves markdown file**: Research report with sources saved to `research_report_YYYYMMDD_HHMMSS.md`
- **Prints to terminal**: Complete research report with markdown formatting
- **Lists web sources**: Numbered URLs referenced in the research
- **Confirms completion**: Path where research files were saved

**Token Efficiency Note**: Deep research takes 10-20 minutes. The script runs synchronously (blocking) without intermediate polling, minimizing token usage during the wait.

## Bundled Resources

### Scripts

#### `scripts/run_deep_research.py` (Main Entry Point)

The orchestration script that handles:
- Prompt quality assessment
- Interactive enhancement questions (with smart detection for technical vs. general research)
- Prompt saving and timestamping
- Execution of core deep research

**Key Features:**
- Smart enhancement: Only asks questions if prompt is brief/generic
- Template-based questions: Different question sets for technical vs. general research
- Flexible input: Numbered options + custom text input
- Error handling: Helpful messages if deep_research.py is not found

**Available options:**
```
python3 run_deep_research.py <prompt> [OPTIONS]
  --no-enhance              Skip enhancement questions
  --model <model>           Model to use (default: o4-mini-deep-research)
  --timeout <seconds>       Timeout in seconds (default: 1800)
  --output-dir <path>       Where to save prompt file
```

#### `assets/deep_research.py`

Core script that interfaces with OpenAI's Deep Research API. Handles:
- API authentication via OPENAI_API_KEY
- Request creation and execution
- **Automatic markdown saving**: Saves timestamped report files by default
- Output formatting (report + sources with metadata)
- Error handling and retries

**New command-line options:**
```
--output-file <path>      Custom output file path
--no-save                 Disable automatic markdown saving
```

### References

#### `references/workflow.md`

Detailed workflow documentation covering:
- Complete skill workflow with examples
- Prompt enhancement strategies
- Research parameters explanation
- Integration guidance for Claude
- Command-line interface reference
- Error handling and troubleshooting
- Tips for effective research

## Key Behaviors

### Smart Prompt Enhancement

The skill intelligently determines whether enhancement is needed:
- **Triggers enhancement** for prompts with < 15 words or generic starts
- **Skips enhancement** for detailed, specific prompts
- **Allows users** to disable with `--no-enhance` flag
- **Template-aware**: Uses different questions for technical vs. general research

### Research Parameters

Enhanced prompts include:
- Original user query with full context
- Scope and timeframe preferences
- Desired depth level (summary, technical, implementation, comparative)
- Specific focus areas (performance, cost, security, etc.)

These parameters help the deep research model deliver more targeted, relevant results.

### Reproducibility

Every research execution:
- Saves the exact prompt used to a timestamped file
- Enables tracing research decisions
- Allows follow-up research using same/modified prompts
- Maintains audit trail of research parameters

## Examples

### Brief Prompt with Enhancement

**User:** "Research the most effective opensource RAG solutions"

**Script behavior:**
1. Detects brief prompt (12 words) + technical keywords ("opensource", "RAG")
2. Asks technical research questions:
   - Technology scope: Open-source only? (User: Yes)
   - Key metrics: Performance/benchmarks? (User: Speed and Accuracy)
   - Use cases: Production deployment? (User: Multiple aspects)
3. Enhances to detailed prompt with parameters
4. Saves and executes deep research
5. Returns comprehensive report with comparative benchmarks and source URLs

### Detailed Prompt Without Enhancement

**User:** "Analyze the impact of large language models on software developer productivity in 2024-2025, focusing on code generation tools, pair programming, and productivity metrics."

**Script behavior:**
1. Detects detailed prompt (24 words) with specific scope/focus
2. Skips enhancement questions
3. Saves and executes deep research immediately
4. Returns focused analysis aligned with user specifications

## Requirements

- Python 3.7+
- OpenAI API key (set via `OPENAI_API_KEY` environment variable or `.env` file)
- Internet connection (for web search)
- 30+ minutes for research completion (configurable timeout)

## Token-Efficient Workflow

### Long-Running Task Optimization

Deep research queries typically take **10-20 minutes** to complete. This skill is optimized to minimize token usage during long waits:

**How it works:**
1. **Synchronous execution**: The script runs as a blocking subprocess (no background polling)
2. **No intermediate checks**: Claude waits silently for completion without status updates
3. **Single output**: Results are presented once at the end
4. **Automatic saving**: Markdown files are saved automatically, no manual intervention needed

**Token savings:**
- Traditional approach: Checking status every 30 seconds = ~40 checks × 500 tokens = ~20,000 tokens wasted
- This approach: Single wait = ~1,000 tokens total

### Automatic File Management

The skill automatically generates and saves files:

**Generated files:**
- `research_prompt_YYYYMMDD_HHMMSS.txt` - Enhanced research prompt with parameters
- `research_report_YYYYMMDD_HHMMSS.md` - Complete markdown report with:
  - Research sections (historical, cognitive, cultural, etc.)
  - Numbered source citations
  - Metadata footer (date, model)

**Customization options:**
```bash
# Custom output location
python3 deep_research.py --prompt-file prompt.txt --output-file my_research.md

# Disable automatic saving (terminal output only)
python3 deep_research.py --prompt-file prompt.txt --no-save
```

## Troubleshooting

### Missing OPENAI_API_KEY

**Error:** "Missing OPENAI_API_KEY"

**Solution:**
- Set environment variable: `export OPENAI_API_KEY="your-key"`
- Or create `.env` file in working directory with `OPENAI_API_KEY=your-key`

### deep_research.py Not Found

**Error:** "Could not find deep_research.py"

**Solution:**
- Ensure skill is properly installed with assets
- Script searches in: skill assets folder → current directory → parent directory

### Research Timeout

**Error:** Request times out after 30 minutes

**Solution:**
- Increase timeout: `--timeout 5400` (90 minutes)
- Simplify prompt to reduce research scope
- Run during off-peak hours for potentially faster API responses


================================================================================

## 22. Expert Skill: elevenlabs-tts
> **Path within category:** `elevenlabs-tts/SKILL.md`


# ElevenLabs Text-to-Speech

## Overview

Generate professional audio files from text using ElevenLabs' advanced text-to-speech API. The skill provides pre-configured voice presets with sensible defaults, voice parameter customization, and direct access to the `scripts/elevenlabs_tts.py` script for programmatic control.

## Quick Start

To generate audio from text:

1. Ensure the `.env` file contains a valid `ELEVENLABS_API_KEY`
2. Execute the script with text: `python scripts/elevenlabs_tts.py "Your text here"`
3. Specify voice and output: `python scripts/elevenlabs_tts.py "Text" --voice adam --output audio/output.mp3`

## Voice Presets

Seven pre-configured voices are available. See `references/api_reference.md` for complete voice descriptions:

- `rachel` (default) - Clear, professional female
- `adam` - Deep, authoritative male
- `bella` - Warm, friendly female
- `elli` - Young, enthusiastic female
- `josh` - Friendly, conversational male
- `arnold` - Deep, powerful male
- `ava` - Expressive, dynamic female

## Parameters

### Text
The text to convert to speech. Any length is supported.

### Voice Selection
Specify voice using preset name (e.g., `rachel`, `adam`) or direct ElevenLabs voice ID.

### Voice Parameters
- **stability** (0.0-1.0, default 0.5): Lower values create expressive variation; higher values ensure consistency
- **similarity_boost** (0.0-1.0, default 0.75): Higher values maintain closer adherence to voice characteristics

### Output
Specify the output file path. Default is `output.mp3`. Directories are created automatically.

## Usage Examples

### Basic Python Usage
```python
from scripts.elevenlabs_tts import generate_speech

path = generate_speech(
    text="Hello, this is a test message",
    voice_id="rachel"
)
```

### Command Line
```bash
# With default voice
python scripts/elevenlabs_tts.py "Generate this text"

# With custom voice and stability
python scripts/elevenlabs_tts.py "Different voice" --voice adam --stability 0.7

# To custom output path
python scripts/elevenlabs_tts.py "Save here" --output audio/narration.mp3

# List available voices
python scripts/elevenlabs_tts.py "" --list-voices
```

## Implementation Notes

- The script handles API communication with error reporting
- Output directories are created automatically if they don't exist
- Returns absolute path to generated audio file
- Uses `eleven_monolingual_v1` model by default (can be overridden)

## Resources

- `scripts/elevenlabs_tts.py` - Main Python script for text-to-speech generation. Can be imported as a module or executed from command line.
- `references/api_reference.md` - Detailed API documentation including voice descriptions, parameter explanations, and usage examples.
- `.env` and `.env.example` - Environment configuration for storing API credentials securely.


================================================================================

## 23. Expert Skill: meta
> **Path within category:** `meta/SKILL.md`


# Meta Skill - Command Handler

⚠️ **IMPORTANT**: This skill is a COMMAND HANDLER registration. It tells the bot to handle `/meta` commands by spawning Claude Code Agent SDK sessions in the telegram_agent directory.

## What This Does

Registers `/meta` as a command handler that:
1. Takes the user's prompt after `/meta`
2. Spawns a Claude Code Agent SDK session
3. Sets working directory to `~/ai_projects/telegram_agent`
4. Returns responses in Telegram

## Implementation

The actual command handler needs to be registered in the telegram bot codebase at:
- `src/bot/handlers/claude_commands.py` - Add meta command handler
- `src/bot/bot.py` - Register the command

## Usage Pattern

User types in Telegram:
```
/meta fix the rate limiting bug
/meta add better logging
/meta refactor authentication
```

Bot spawns Claude Agent SDK with:
- Working directory: `~/ai_projects/telegram_agent`
- Prompt: User's text after `/meta`
- Same infrastructure as `/claude` command

## Example User Requests

- `/meta fix bug in message handler`
- `/meta add error recovery to file sending`
- `/meta refactor the session management`
- `/meta improve the keyboard layout`

## Implementation Notes

Must use `ClaudeCodeService` with custom `cwd` parameter:
```python
service.execute_prompt(
    prompt=user_prompt,
    cwd="/Users/server/ai_projects/telegram_agent"
)
```


================================================================================

## 24. Expert Skill: context-builder
> **Path within category:** `context-builder/SKILL.md`


# Context Builder

Generate interactive context-building prompts for consulting clients. These prompts are designed to be run in Claude Code -- they guide a team through structured questions using AskUserQuestion, generate output files per section, and compile everything into a reusable CLAUDE.md.

## Workflow

### Phase 1: Intake (AskUserQuestion)

Ask all intake questions using AskUserQuestion with closed-list options. Gather:

**Question 1: Company identifier**
- Options: "I have a website URL", "I have a company name", "I have both"
- Follow up to get the actual URL/name

**Question 2: Who will use this prompt?**
- Options: "Specific person (name + role)", "A team (no specific person)", "Unknown / TBD"
- If specific person: follow up for name and role

**Question 3: Primary consulting focus** (multiSelect)
- "AI automation of current operations"
- "Existential strategy (what survives AI)"
- "New business models / pivots"
- "Product development with AI"

**Question 4: Industry**
- "Marketing / Advertising"
- "Manufacturing / Construction"
- "SaaS / Software"
- "Professional Services / Consulting"
- (Other)

**Question 5: Existing context in vault?**
- "Yes, there's a call transcript"
- "Yes, there are notes/files"
- "No existing context"
- If yes: ask for filename or search term to locate it

**Question 6: Session language**
- "Russian (questions in Russian, output in English)"
- "English throughout"
- "Other"

### Phase 2: Research (automated)

Run these research steps in parallel where possible:

1. **Web research**: Use WebSearch and WebFetch (via Task agent) to gather:
   - What the company does, products/services
   - Target market, company size, geography
   - Tech stack, partnerships
   - Recent news, funding, team info
   - Competitive landscape

2. **Vault search**: Search the Obsidian vault for:
   - Transcripts mentioning the company name (Grep in vault root and Daily/)
   - People files for contacts at the company (People/ folder)
   - Any existing notes or research

3. **Transcript analysis** (if found): Extract from call transcripts:
   - Team members and their roles
   - Current AI tool usage
   - Pain points and concerns mentioned
   - Specific processes described
   - Questions raised by the team

### Phase 3: Section Selection (AskUserQuestion)

Present a curated set of sections based on the consulting focus. Use AskUserQuestion with multiSelect to let the user pick which sections to include.

#### Section Library

Draw from `references/section-library.md` for the full section catalog. Default section sets by focus:

**AI Automation focus:**
1. Process Inventory, 2. Pain Points & Waste, 3. Current Tech Stack, 4. AI Opportunity Mapping, 5. People & Org, 6. Data Reality Check, 7. Quick Wins

**Existential Strategy focus:**
1. Revenue & Service Map, 2. The Existential Question, 3. Client Value Chain, 4. New Business Models, 5. Data & Knowledge Assets, 6. People & Org, 7. Quick Wins & Pilots

**Full Assessment (both):**
All 10 sections from the library.

After section selection, ask:

**Express mode grouping**: Present a suggested grouping of selected sections into 4 Express mega-sections. Let user confirm or adjust.

### Phase 4: Generation

Generate two files:

#### 1. The Context-Builder Prompt

Save to: `Claude-Drafts/{company-slug}-context-prompt.md`

**Structure** (follow the template in `references/prompt-template.md`):

```

# AI Transformation Context Builder -- {Company Name}

## About {Company}
  [Generated from research -- company description, size, market, positioning]

## Current State
  **What's working:** [from research + transcript]
  **The gap:** [from research + transcript]
  [If existential concerns found: **Existential context:**]

## Mode Selection
  [Express vs Deep Dive with section descriptions]

## How This Works
  [Standard interactive session instructions]

## Session Resumability
  [Standard resumability logic]

## Interactive Flow
  [Selected sections with tailored questions]

## Output Files
  [One file per section + final CLAUDE.md]

## Relevant Frameworks
  [Selected from references/frameworks.md based on focus]
```

#### 2. Instruction File (optional)

If the prompt will be sent to someone external, generate a short instruction file:
`Claude-Drafts/{company-slug}-context-instructions.md`

Containing:
- What this file is and how to use it
- Prerequisites (Claude Code or similar)
- The two modes explained simply
- What they'll get on output
- Privacy note (they can share as much or as little as they want)

### Phase 5: Delivery (AskUserQuestion)

**Question: What to do with the generated files?**
- "Save to vault only"
- "Save and send via Telegram"
- "Save and let me review first"

If Telegram: ask for the recipient handle/name, then send using the telegram skill (intro message + file).

## Key Principles

- **Maximize closed-list questions**: Every AskUserQuestion should have concrete options. Minimize free-text input.
- **Research before asking**: Don't ask the user things that can be found via web search or vault search.
- **Tailor sections to context**: If the transcript reveals specific concerns (e.g., existential fears, specific tech stack), customize the section questions to reference those specifics.
- **Bake in discovered context**: The generated prompt's "About" and "Current State" sections should be rich with researched details so the person running the prompt gets a warm start.
- **Language awareness**: If session language is Russian, all AskUserQuestion interactions during prompt execution should be in Russian, but output files in English.

## Resources

### references/
- `section-library.md` -- Full catalog of available sections with question templates
- `prompt-template.md` -- Structural template for the generated prompt
- `frameworks.md` -- Consulting frameworks to selectively include


================================================================================

## 25. Expert Skill: skill-studio
> **Path within category:** `skill-studio/SKILL.md`


# Skill Studio

## Purpose

Conduct a structured JTBD interview that captures what to build, for whom, and why — then emit a one-page `design.md` + `design.svg` spec. Sits between "should I automate this?" (automation-advisor) and "how do I package this as a skill?" (skill-creator).

## Architecture

This skill wraps an external CLI tool (`skill-studio`) installed via pip. The CLI handles session state, coverage tracking, and export. The skill orchestrates the CLI — it does not bundle scripts directly.

## When to use

Trigger on any of: "help me design...", "build a skill for...", "design an automation for...", "I want a bot/agent/workflow that...", "scope a new shortcut". Also trigger when the user describes a recurring pain and asks how to automate it.

## Prerequisites

- `skill-studio` CLI on PATH (`pip install -e .` inside the skill directory, or `skill-studio init` for guided setup)
- Python 3.11+
- Text mode needs no API key — the interview runs natively inside Claude Code
- Voice mode (`--voice`) needs `DAILY_API_KEY`, `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, and an LLM provider key (`OPENROUTER_API_KEY` by default). If any key is missing, suggest text mode instead.

To verify the CLI is available, run `skill-studio --help`. If the command is not found, install it from the skill's base directory: `pip install -e <skill-studio-base-dir>`.

## Interview protocol (text mode)

Follow these steps in order.

### Step 0 — (Optional) Seed from a prior session

If the user provides a prior session (Claude Code transcript, another skill-studio session, or arbitrary transcript path), seed the interview instead of starting blank:

```bash
skill-studio propose-from-session <session_id>
# or: skill-studio propose-from-session --path <file>
# add --bundle-only to skip the LLM call and inspect the raw extract
```

This runs in two stages:
1. **Deterministic ingest** (no LLM) — regex-extracts models tried, cost events, prompt changes, pain snippets, and hashes. A 50k-token transcript compresses to ~30 lines of JSON.
2. **Single LLM call** — over that compact bundle only, proposes a partial DesignJSON patch with a `rationale` map citing which signals justified each field.

**The proposal is NOT applied automatically.** Present it to the user (with the rationale) and ask for approval. Offer: `approve as-is`, `edit inline`, `discard and start fresh`, `approve partial` (keep some fields, re-interview others).

`propose-from-session` does not create a session. After approval, run `new-session` (Step 1) to create one, then pipe the approved patch to `apply-patch`, and continue the interview loop from the next uncovered target.

### Step 1 — Start the session

Presets: `ai-agent` (default), `life-automation`, `knowledge-work`, `custom`.
Depth: `sprint` (0.60, ~5–7 questions), `standard` (0.80, ~15–20 questions, default), `deep` (0.92, ~25–35 questions).

Styles (shape how questions are phrased):
- `scenario-first` (default) — "Walk me through a specific time when..."
- `socratic` — "Why does that matter? What would happen if...?"
- `metaphor-first` — "If this automation were a [thing], what would it be?"
- `form` — One direct question per field, no preamble.

Run:

```bash
skill-studio new-session --preset <preset> --depth <depth> --style <style>
```

Output:

```
session_id: <uuid>
opening: <question text>
```

Store the `session_id`. Present the opening question to the user as a direct text message.

### Step 2 — Interview loop

For every user answer:

**a. Extract a JSON patch.** Emit a JSON object containing only the DesignJSON fields the answer addresses. Use only fields from the schema below — never hallucinate fields or values. If nothing schema-relevant was said, emit `{}`.

Example patch:

```json
{"jtbd.situation": "When I finish a coaching call and need to write up notes", "problem.what_hurts": "Manual note-taking takes 20 minutes and I lose details"}
```

Example with list fields:

```json
{"needs.functional": ["transcribe audio", "extract action items"], "guardrails": ["never send notes without review"]}
```

Example with object-list field (`scenarios`):

```json
{"scenarios": [{"title": "Post-coaching rush", "vignette": "Call ends at 14:00, next meeting at 14:15 — I scribble three bullet points and lose the rest by evening."}]}
```

**DesignJSON fields:**

| Field | Type | Notes |
|-------|------|-------|
| `hook` | str | One-sentence pitch of the automation |
| `problem.what_hurts` | str | Specific pain |
| `problem.cost_today` | str | What the pain costs right now |
| `needs.functional` | list[str] | What it must do |
| `needs.emotional` | list[str] | How the user wants to feel |
| `needs.social` | list[str] | Relational / status needs |
| `jtbd.situation` | str | When this happens |
| `jtbd.motivation` | str | What the user wants |
| `jtbd.outcome` | str | So they can... |
| `before_after.before_external` | str | Visible state before |
| `before_after.before_internal` | str | Felt state before |
| `before_after.after_external` | str | Visible state after |
| `before_after.after_internal` | str | Felt state after |
| `scenarios` | list[{title, vignette}] | Concrete day-in-the-life stories |
| `trigger.type` | `manual` / `scheduled` / `event` | |
| `trigger.detail` | str | e.g. "7:45am weekdays" |
| `inputs` | list[str] | Data / services consumed |
| `capabilities` | list[str] | What it does |
| `outputs` | list[str] | What it produces |
| `guardrails` | list[str] | Safety rails; negative-space rules |
| `cta` | str | Next action at end of design |
| `concept_imagery.metaphor` | str | Visual / verbal handle |

**b. Apply the patch.**

```bash
echo '<patch_json>' | skill-studio apply-patch <session_id>
```

Output:

```
coverage: 0.42
next_target: jtbd.situation
```

**c. Check stop conditions.** End the loop if either:
- `coverage >= threshold` (sprint=0.60, standard=0.80, deep=0.92)
- User says "done", "wrap up", or "stop"

**d. Ask the next question.** Target the `next_target` field, in the active style. Never re-ask a field already past 0.5 coverage. Present the question as direct text to the user.

### Step 3 — Export

```bash
skill-studio done <session_id>
```

Prints the paths to `design.md` and `design.svg`. Present both paths to the user.

## Voice mode

For voice interviews, skip the manual loop and delegate to the built-in pipeline:

```bash
skill-studio new --voice --preset <preset> --depth <depth>
```

This spins up a Daily room (auto-opens in the browser), runs Groq Whisper STT -> interview loop -> Deepgram TTS, and auto-exports on session end.

If voice mode fails due to missing API keys, fall back to text mode and inform the user. To configure keys, run `skill-studio init`.

## Other commands

- `skill-studio list` — list all sessions
- `skill-studio export <id> md-svg` — regenerate `design.md` + `design.svg`
- `skill-studio coverage <id>` — per-field confidence JSON
- `skill-studio next-target <id>` — ask-this-next hint
- `skill-studio init` — full first-run wizard (prereq checks + keys + paths)
- `skill-studio setup` — narrower key-rotation flow (sops-only)

## Sessions

Each interview writes to `$SKILL_STUDIO_HOME/sessions/<uuid>/` (default: `~/.skill-studio/sessions/<uuid>/`):

- `design.json` — canonical schema (single source of truth)
- `transcript.md` — full Q&A log
- `design.md`, `design.svg` — exported artifacts

## Troubleshooting

- **`skill-studio: command not found`** — Run `pip install -e <skill-studio-base-dir>` and retry.
- **`apply-patch` returns an error** — Verify the JSON patch is valid (keys must match schema fields above). Run `skill-studio coverage <session_id>` to inspect current state.
- **Session not found** — Always run `new-session` before the first `apply-patch`. There is no implicit session creation. Run `skill-studio list` to check existing sessions.
- **Voice mode key errors** — Run `skill-studio init` to configure missing keys, or fall back to text mode.

## Notes

- The interview loop runs entirely inside Claude Code for text mode. No Anthropic API key is required.
- Voice mode LLM provider is swappable via `LLM_PROVIDER=anthropic` (default is `openrouter`).


================================================================================

## 26. Expert Skill: lab-retro
> **Path within category:** `lab-retro/SKILL.md`


# Claude Code Lab — Final Retrospective

This skill walks a Claude Code Lab graduate through four sequential exercises that consolidate their learning, capture their best work, plan next steps, and collect structured feedback for the organizer.

## How to run

Default flow: run all four parts in order. The user can also jump to a specific part with `/lab-retro 2` (or just say "part 3").

Between parts, briefly summarize what just happened and ask "ready for part N?" so the user controls the pace.

All artifacts are saved into a single folder `lab-retro-output/` in the current working directory:
- `01-progress.md`
- `02-best-prompt.md`
- `03-month-plan.md`
- `04-feedback.json` + `04-feedback-report.md`

Create the folder if missing.


## Part 2 — Best prompt

**Goal:** turn one prompt the participant is proud of into a reusable Skill.

Ask the participant: *"Скопируйте или опишите ваш самый полезный промт из лабы."*

Then `AskUserQuestion`:

1. **"Для какой задачи был промт?"** (singleSelect)
   - Автоматизация рутины
   - Создание контента/документации
   - Анализ данных/исследование
   - Прототипирование/разработка
   - Личный workflow / PKM

2. **"Что сделало его эффективным?"** (multiSelect)
   - Хороший контекст в CLAUDE.md
   - Чёткие критерии успеха
   - Разбиение на шаги
   - Использование Skills/MCP
   - Примеры в промте
   - Ограничения и анти-критерии

Reformat the prompt as a proper Skill (frontmatter + body), suggest an `description` line that would trigger it, and save to `lab-retro-output/02-best-prompt.md`. Suggest where to put it (`~/.claude/skills/<name>/SKILL.md`).


## Part 4 — Feedback for the organizer

**Goal:** structured feedback that goes back to the lab organizer.

`AskUserQuestion`:

1. **"Оцените лабу в целом (NPS)"** (singleSelect: 0–10)
2. **"Самая ценная встреча?"** (singleSelect: M01 / M03 / M05 / M07 / M09 / M11)
3. **"Самая ценная тема за все 6 недель?"** (multiSelect)
   - Основы Claude Code
   - Промтинг и контекст
   - Архитектура и субагенты
   - MCP / Skills / Hooks
   - Agent SDK и деплой
   - Evals и качество
   - AI-гигиена
4. **"Что улучшить?"** (free text)
5. **"Главное препятствие, с которым вы столкнулись?"** (free text)
6. **"Согласны ли поделиться отзывом публично?"** (singleSelect: да / да-анонимно / нет)

Save TWO files:
- `lab-retro-output/04-feedback.json` — structured for the organizer
- `lab-retro-output/04-feedback-report.md` — human-readable summary for the participant

**Then submit to the public proxy** (no secrets needed):

```bash
curl -sS -X POST https://lab-feedback-proxy.vercel.app/api/feedback \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg name "<participant name>" --slurpfile notes lab-retro-output/04-feedback.json '{name:$name, notes:($notes[0]|tostring)}')"
```

The proxy forwards to Baserow table 746002 with a server-side token. Response is `{"ok":true,"row_id":<N>}`. Confirm row ID with the participant.

If the request fails, fall back to local files only and tell the participant: "submit failed — your feedback is saved locally in `lab-retro-output/04-feedback.json`, send it to the organizer manually."


================================================================================

## 27. Expert Skill: github-gist
> **Path within category:** `github-gist/SKILL.md`


# GitHub Gist Publisher

Publish any file as a GitHub Gist for easy sharing.

## Prerequisites

Uses `gh` CLI by default. Ensure you're authenticated:

```bash
gh auth status
# If not authenticated: gh auth login
```

Fallback: Set `GITHUB_GIST_TOKEN` env var with gist scope.

## Usage

```bash
# Publish file as secret (unlisted) gist - DEFAULT
python3 scripts/publish_gist.py /path/to/file.md

# Publish as public gist (visible in your profile)
python3 scripts/publish_gist.py /path/to/file.md --public

# Custom description
python3 scripts/publish_gist.py /path/to/file.md -d "My awesome note"

# Override filename in gist
python3 scripts/publish_gist.py /path/to/file.md -f "readme.md"

# From stdin
echo "Hello" | python3 scripts/publish_gist.py - -f "hello.txt"

# Just get URL
python3 scripts/publish_gist.py /path/to/file.md --url-only

# Create and open in browser
python3 scripts/publish_gist.py /path/to/file.md --open
```

## Options

| Flag | Description |
|------|-------------|
| `--public` | Create public gist (default is secret/unlisted) |
| `-d, --description` | Gist description |
| `-f, --filename` | Override filename |
| `--url-only` | Output only URL |
| `--open` | Open in browser |
| `--api` | Force API instead of gh CLI |

## Output

```json
{
  "url": "https://gist.github.com/user/abc123",
  "id": "abc123",
  "public": false,
  "filename": "file.md"
}
```

## Example

Session log published with this skill: https://gist.github.com/glebis/3faaae6b907123929220e81add51a567


================================================================================

## 28. Expert Skill: wispr-fix
> **Path within category:** `wispr-fix/SKILL.md`


# Wispr Fix: Dictation Correction Queue

Queue dictation corrections instantly during work. Apply them all at once when convenient.

## Invocation Patterns

### Explicit add
User says: `/wispr-fix "Clauthe Code" "Claude Code"`
Action: Run the add command.

### Auto-detect pattern
User writes: `wispr fix: X -> Y`
Action: Parse X and Y, run the add command.

### Flush / dry-run / list
User says: `/wispr-fix flush`, `/wispr-fix dry-run`, `/wispr-fix list`
Action: Run the corresponding command.

## Commands

All commands use the script at `~/.claude/skills/wispr-fix/scripts/wispr-fix.sh`.

### Queue a correction
```bash
~/.claude/skills/wispr-fix/scripts/wispr-fix.sh add "<mishear>" "<correction>"
```
Use `--exact` to skip case variant generation (auto-applied for single words).

### List pending corrections
```bash
~/.claude/skills/wispr-fix/scripts/wispr-fix.sh list
```

### Remove a queued correction
```bash
~/.claude/skills/wispr-fix/scripts/wispr-fix.sh remove "<mishear>"
```
Supports fuzzy matching on the mishear string.

### Preview what flush will do
```bash
~/.claude/skills/wispr-fix/scripts/wispr-fix.sh dry-run
```

### Apply all queued corrections
```bash
~/.claude/skills/wispr-fix/scripts/wispr-fix.sh flush
```
Options: `--force-quit` (force-kill Wispr if graceful quit fails), `--no-restart` (don't restart Wispr after).

**IMPORTANT:** Flush will quit Wispr Flow, apply all corrections to the SQLite database, and restart it. Always inform the user before running flush.

### Restore from backup
```bash
~/.claude/skills/wispr-fix/scripts/wispr-fix.sh restore latest
```

## Argument Parsing

When the user invokes `/wispr-fix` with arguments:

| Input | Action |
|-------|--------|
| `"X" "Y"` or `X Y` (two quoted/unquoted args) | `add "X" "Y"` |
| `flush` | `flush` |
| `flush --force-quit` | `flush --force-quit` |
| `dry-run` | `dry-run` |
| `list` | `list` |
| `remove "X"` | `remove "X"` |
| `restore latest` | `restore latest` |
| (no args) | `list` (show current queue) |

## Auto-Detect Pattern

When you see `wispr fix: X -> Y` in user text (the `wispr fix:` prefix is required):
1. Parse X (everything between `wispr fix:` and `->`)
2. Parse Y (everything after `->`)
3. Trim whitespace from both
4. Run `add "X" "Y"`
5. Confirm to the user: "Queued: 'X' -> 'Y'"

## Notes
- Corrections are queued instantly — no Wispr restart needed
- Flush quits Wispr, backs up DB, applies corrections, verifies integrity, exports dictionary, restarts Wispr
- The queue persists between sessions at `~/.claude/skills/wispr-fix/queue.jsonl`
- Applied corrections are logged in `queue.applied.jsonl`
- Backups are stored in `~/Library/Application Support/Wispr Flow/backups/` (last 10 retained)


================================================================================

## 29. Expert Skill: brand-agency
> **Path within category:** `brand-agency/SKILL.md`


# Agency Brand Styling

## Overview

To access Agency's official brand identity and style resources, use this skill. The style is based on neobrutalism aesthetic with bold colors, hard shadows, and strong typography.

## Brand Guidelines

### Colors

**Main Colors:**

- Background Light: `#ffffff` - Light backgrounds
- Foreground Dark: `#000000` - Primary text and dark elements
- Muted: `#e5e5e5` - Subtle backgrounds, secondary elements

**Primary Palette:**

- Primary (Orange): `#e85d04` - Main accent, CTAs, highlights
- Secondary (Yellow): `#ffd60a` - Secondary accent, warnings, attention
- Accent (Blue): `#3a86ff` - Links, interactive elements, info

**Chart/Extended Colors:**

- Chart Green: `#38b000` - Success states, positive indicators
- Chart Red: `#d62828` - Error states, destructive actions

### Typography

**Font Stack:**

- **Headings**: Geist ExtraBold (weight 800), fallback: Arial
- **Body Text**: EB Garamond, fallback: Georgia
- **Monospace/Code**: Geist Mono, fallback: Courier New

**Google Fonts Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Geist:wght@800&family=Geist+Mono:wght@400;500&display=swap');
```

**CSS Variables:**
```css
:root {
  --font-body: 'EB Garamond', Georgia, serif;
  --font-heading: 'Geist', Arial, sans-serif;
  --font-mono: 'Geist Mono', 'Courier New', monospace;
}
```

### Neobrutalism Style

**Shadows:**
- Hard shadow offset: `4px 4px 0px 0px #000000`
- No blur (stdDeviation: 0)
- CSS: `box-shadow: 4px 4px 0px 0px #000000;`
- SVG filter: `<feDropShadow dx="4" dy="4" stdDeviation="0" flood-color="#000000"/>`

**Borders:**
- Width: 3px
- Color: `#000000`
- Style: solid
- Border radius: 0 (no rounded corners)

**Key Principles:**
- High contrast between elements
- Bold, saturated colors
- No gradients (flat colors only)
- Strong black outlines
- Offset hard shadows
- Zero border radius

## Application Guidelines

### SVG Graphics

To create SVG in Agency brand style:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="150%" height="150%">
      <feDropShadow dx="4" dy="4" stdDeviation="0" flood-color="#000000" flood-opacity="1"/>
    </filter>
  </defs>

  <circle cx="200" cy="200" r="80"
    fill="#e85d04"
    stroke="#000000"
    stroke-width="3"
    filter="url(#shadow)"/>
</svg>
```

### Presentations (Marp/PowerPoint)

**Slide backgrounds by type:**
- Title slides: Primary Orange `#e85d04`
- Content slides: Light `#ffffff` or Muted `#e5e5e5`
- Accent slides: Secondary Yellow `#ffd60a`, Accent Blue `#3a86ff`
- Dark slides: Foreground `#000000`

**Text colors:**
- On light backgrounds: `#000000`
- On dark/colored backgrounds: `#ffffff`

### Web/HTML

```css
:root {
  /* Colors */
  --color-background: #ffffff;
  --color-foreground: #000000;
  --color-primary: #e85d04;
  --color-secondary: #ffd60a;
  --color-accent: #3a86ff;
  --color-success: #38b000;
  --color-error: #d62828;
  --color-muted: #e5e5e5;

  /* Typography */
  --font-body: 'EB Garamond', Georgia, serif;
  --font-heading: 'Geist', Arial, sans-serif;
  --font-mono: 'Geist Mono', 'Courier New', monospace;

  /* Shadows */
  --shadow: 4px 4px 0px 0px #000000;
  --shadow-sm: 2px 2px 0px 0px #000000;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: 800;
}

/* Body */
body {
  font-family: var(--font-body);
  color: var(--color-foreground);
  background: var(--color-background);
}

/* Buttons */
.btn {
  background: var(--color-primary);
  color: white;
  border: 3px solid var(--color-foreground);
  box-shadow: var(--shadow);
  border-radius: 0;
  font-family: var(--font-heading);
  font-weight: 800;
}

/* Cards */
.card {
  background: var(--color-background);
  border: 3px solid var(--color-foreground);
  box-shadow: var(--shadow);
  border-radius: 0;
}

/* Code */
code, pre {
  font-family: var(--font-mono);
  background: var(--color-foreground);
  color: white;
  border: 3px solid var(--color-foreground);
}
```

## Color Usage Quick Reference

| Context | Color | Hex |
|---------|-------|-----|
| Primary action | Orange | `#e85d04` |
| Secondary action | Yellow | `#ffd60a` |
| Links/Info | Blue | `#3a86ff` |
| Success | Green | `#38b000` |
| Error/Danger | Red | `#d62828` |
| Text (light bg) | Black | `#000000` |
| Text (dark bg) | White | `#ffffff` |
| Muted/Disabled | Gray | `#e5e5e5` |

## Assets

**Logo:** `assets/logo.svg` - Agency logo in neobrutalism style (terminal window with code symbols and geometric shapes)

## Social Media Templates

ASCII-art style HTML templates for social media using Geist Mono font. Render to PNG using Playwright.

### Available Templates

| Template | Size | Platform |
|----------|------|----------|
| `instagram/story-announcement` | 1080x1920 | IG Story |
| `instagram/story-quote` | 1080x1920 | IG Story |
| `instagram/post-title` | 1080x1350 | IG Post |
| `instagram/post-tips` | 1080x1350 | IG Post |
| `instagram/post-event` | 1080x1350 | IG Post |
| `youtube/thumbnail` | 1280x720 | YT Thumbnail |
| `youtube/shorts-cover` | 1080x1920 | YT Shorts |
| `social/cover-banner` | 1584x396 | LinkedIn/FB |
| `social/tiktok` | 1080x1920 | TikTok |
| `social/twitter-post` | 1200x675 | X/Twitter |
| `social/pinterest-pin` | 1000x1500 | Pinterest |

### Usage

```bash
# Render all templates
node scripts/render-templates.js

# Render specific template
node scripts/render-templates.js --template instagram/story-announcement

# Custom output path
node scripts/render-templates.js -t youtube/thumbnail -o my-thumbnail.png

# List available templates
node scripts/render-templates.js --list
```

### ASCII Style Elements

Templates use ASCII box-drawing characters for decoration:

```
Frames:   ┌─────┐  ╔═════╗  ┏━━━━━┓
          │     │  ║     ║  ┃     ┃
          └─────┘  ╚═════╝  ┗━━━━━┛

Lines:    ─ │ ═ ║ ━ ┃

Arrows:   → ← ↑ ↓ ▶ ◀ ▲ ▼

Shapes:   ● ○ ■ □ ▲ △ ★ ☆ ◆ ◇

Blocks:   █ ▓ ▒ ░
```

### Template Files

Located in: `assets/templates/`


================================================================================

## 30. Expert Skill: google-image-search
> **Path within category:** `google-image-search/SKILL.md`


# Google Image Search Skill

Search for images using Google Custom Search API with intelligent scoring and LLM-based selection.

## When to Use

- Finding images to illustrate technical articles or research
- Adding visuals to presentations
- Enriching Obsidian notes with relevant images
- Batch image search for multiple topics
- Generating image search configs from plain text lists

## Requirements

- Google Custom Search API key and Search Engine ID
- OpenRouter API key (for LLM selection)
- llm CLI installed at `/opt/homebrew/bin/llm`

Store credentials in `.env`:
```
Google-Custom-Search-JSON-API-KEY=your_key
Google-Custom-Search-CX=your_cx
OPENROUTER_API_KEY=your_openrouter_key
```

## Modes of Operation

### 1. Simple Query

Search for a single term:

```bash
python3 ~/.claude/skills/google-image-search/scripts/google_image_search.py \
  --query "neural interface wearable device" \
  --output-dir ./images \
  --num-results 5
```

### 2. Batch Processing

Process multiple queries from JSON config:

```bash
python3 ~/.claude/skills/google-image-search/scripts/google_image_search.py \
  --config image_queries.json \
  --output-dir ./images \
  --llm-select
```

### 3. Generate Config from Terms

Create JSON config from a list of terms using LLM:

```bash
python3 ~/.claude/skills/google-image-search/scripts/google_image_search.py \
  --generate-config \
  --terms "AlterEgo wearable" "sEMG electrodes" "BCI headset" \
  --output my_queries.json
```

### 4. Enrich Obsidian Note

Extract visual terms from note, find images, and insert below headings:

```bash
python3 ~/.claude/skills/google-image-search/scripts/google_image_search.py \
  --enrich-note ~/Brains/brain/Research/neural-interfaces.md
```

This mode:
1. Detects Obsidian vault and attachments folder
2. Uses LLM to extract visual-worthy terms from note
3. Searches for images for each term
4. Downloads best images to attachments folder
5. Inserts image embeds below relevant headings
6. Creates backup before modifying note

## Key Options

| Option | Description |
|--------|-------------|
| `--query TEXT` | Simple single query |
| `--config FILE` | JSON config for batch |
| `--generate-config` | Generate config from `--terms` |
| `--enrich-note FILE` | Enrich Obsidian note |
| `--output-dir DIR` | Where to save images |
| `--urls-only` | Return URLs only, no download |
| `--llm-select` | Use LLM to pick best image (default: on) |
| `--no-llm-select` | Disable LLM selection |
| `--num-results N` | Results per query (default: 5) |
| `--dry-run` | Show what would be done |

## JSON Config Format

Each entry supports:

```json
{
  "id": "unique-id",
  "heading": "Display Heading",
  "description": "Context for what image to find",
  "query": "Google search query",
  "numResults": 5,
  "selectionCriteria": "What makes a good image",
  "requiredTerms": ["must", "have"],
  "optionalTerms": ["bonus", "terms"],
  "excludeTerms": ["stock", "clipart"],
  "preferredHosts": ["official-site.com"],
  "selectionCount": 2
}
```

See `references/api_config_reference.md` for full documentation.

## Scoring System

Images are scored based on:
- **Required terms**: -80 if missing, +30 if all present
- **Optional terms**: +5 per match
- **Exclude terms**: -50 per match
- **Preferred hosts**: +25 if trusted, -5 if unknown
- **MIME type**: +5 for PNG/JPEG, -10 for GIF
- **Resolution**: +10 for high res, -10 for low res
- **File size**: -5 if very small

## LLM Selection

After scoring, LLM picks the best image from top candidates based on:
- Title and URL metadata
- Scoring reasons
- Selection criteria

The LLM evaluates authenticity, clarity, and relevance for technical audiences.

## Obsidian Integration

When in an Obsidian vault:
- Auto-detects vault root via `.obsidian` folder
- Uses configured attachments folder (default: `Attachments`)
- Generates Obsidian-style embeds: `![[image.png|alt text]]`
- Creates backup before modifying notes

## Script Files

| File | Purpose |
|------|---------|
| `google_image_search.py` | Main entry point |
| `api.py` | Google Custom Search API |
| `config.py` | Credentials and config handling |
| `download.py` | Image download with magic bytes |
| `evaluate.py` | Keyword-based scoring |
| `llm_select.py` | LLM selection and term extraction |
| `obsidian.py` | Vault detection and enrichment |
| `output.py` | Markdown output generation |


================================================================================

## 31. Expert Skill: presentation-generator
> **Path within category:** `presentation-generator/SKILL.md`


# Presentation Generator

## Overview

Create stunning presentations in neobrutalism style with Agency brand colors. Generate interactive HTML presentations with smooth scrolling navigation, export individual slides as PNG, or create PDF documents.

**Output formats:**
- **HTML** - Interactive presentation with navigation dots, keyboard support, smooth scrolling
- **PNG** - Individual slide images via Playwright (1920x1080)
- **PDF** - Multi-page document via Playwright

## Quick Start

### 1. Create presentation from JSON/YAML content

```bash
node scripts/generate-presentation.js --input content.json --output presentation.html
```

### 2. Export to PNG slides

```bash
node scripts/export-slides.js presentation.html --format png --output ./slides/
```

### 3. Export to PDF

```bash
node scripts/export-slides.js presentation.html --format pdf --output presentation.pdf
```

## Brand Integration

This skill references `brand-agency` for consistent styling:

### Colors (from brand-agency)

| Color | Hex | Usage |
|-------|-----|-------|
| Primary (Orange) | `#e85d04` | Title slides, CTAs, accents |
| Secondary (Yellow) | `#ffd60a` | Highlights, accent slides |
| Accent (Blue) | `#3a86ff` | Info slides, links |
| Success (Green) | `#38b000` | Positive content |
| Error (Red) | `#d62828` | Warnings, emphasis |
| Foreground | `#000000` | Text, borders |
| Background | `#ffffff` | Light slides |

### Typography

- **Headings**: Geist ExtraBold (800)
- **Body**: EB Garamond
- **Code/ASCII**: Geist Mono

## Slide Types

### 1. Title Slide (`--title`)
Full-screen title with subtitle, colored background (primary/secondary/accent/dark).

### 2. Content Slide (`--content`)
Heading + body text + optional bullet list.

### 3. Two-Column Slide (`--two-col`)
Split layout for comparisons, text + image, before/after.

### 4. Code Slide (`--code`)
Dark background, syntax-highlighted code block with title.

### 5. Stats Slide (`--stats`)
Big numbers with labels (e.g., "14 templates | 4 formats | 1 skill").

### 6. Task Grid Slide (`--grid`)
Grid of cards with numbers, titles, descriptions.

### 7. ASCII Art Slide (`--ascii`)
Decorative slide with ASCII box-drawing characters.

### 8. Image Slide (`--image`)
Full-bleed or contained image with optional caption.

## ASCII Decorations

Use ASCII box-drawing characters for tech aesthetic:

```
Frames:   ┌─────┐  ╔═════╗  ┏━━━━━┓
          │     │  ║     ║  ┃     ┃
          └─────┘  ╚═════╝  ┗━━━━━┛

Lines:    ─ │ ═ ║ ━ ┃ ━━━ ───

Arrows:   → ← ↑ ↓ ▶ ◀ ▲ ▼

Shapes:   ● ○ ■ □ ▲ △ ★ ☆ ◆ ◇

Blocks:   █ ▓ ▒ ░
```

## Content Format

### JSON format:

```json
{
  "title": "Presentation Title",
  "footer": "Company / Date",
  "slides": [
    {
      "type": "title",
      "bg": "primary",
      "title": "Main Title",
      "subtitle": "Subtitle text"
    },
    {
      "type": "content",
      "title": "Section Title",
      "body": "Introduction paragraph",
      "bullets": ["Point 1", "Point 2", "Point 3"]
    },
    {
      "type": "code",
      "title": "Code Example",
      "language": "javascript",
      "code": "const x = 42;"
    },
    {
      "type": "stats",
      "items": [
        {"value": "14", "label": "templates"},
        {"value": "4", "label": "formats"},
        {"value": "∞", "label": "possibilities"}
      ]
    }
  ]
}
```

### YAML format:

```yaml
title: Presentation Title
footer: Company / Date
slides:
  - type: title
    bg: primary
    title: Main Title
    subtitle: Subtitle text

  - type: content
    title: Section Title
    body: Introduction paragraph
    bullets:
      - Point 1
      - Point 2
```

## Interactive Features

Generated HTML includes:

- **Navigation dots** - Fixed right sidebar with clickable dots
- **Keyboard navigation** - Arrow keys, Page Up/Down, Home/End
- **Smooth scrolling** - CSS scroll-snap and smooth behavior
- **Intersection Observer** - Active slide highlighting
- **Responsive** - Works on various screen sizes (optimized for 16:9)

## Usage Examples

### Create workshop summary:

```bash
# Generate from today's session
node scripts/generate-presentation.js \
  --title "Claude Code Lab — Day Summary" \
  --footer "29.11.2025" \
  --slides slides-content.json \
  --output workshop-summary.html
```

### Quick presentation from markdown:

```bash
# Convert markdown outline to presentation
node scripts/md-to-slides.js notes.md --output presentation.html
```

### Batch export:

```bash
# Export all slides as PNGs
node scripts/export-slides.js presentation.html --format png --output ./export/

# Result: slide-01.png, slide-02.png, etc.
```

## File Structure

```
presentation-generator/
├── SKILL.md              # This file
├── templates/
│   ├── base.html         # Base HTML template
│   ├── slides/           # Slide type partials
│   │   ├── title.html
│   │   ├── content.html
│   │   ├── code.html
│   │   ├── stats.html
│   │   ├── two-col.html
│   │   ├── grid.html
│   │   └── ascii.html
│   └── styles.css        # Neobrutalism styles
├── scripts/
│   ├── generate-presentation.js  # Main generator
│   ├── export-slides.js          # PNG/PDF export
│   └── md-to-slides.js           # Markdown converter
└── output/               # Generated files
```

## Dependencies

- Node.js 18+
- Playwright (`npm install playwright`)

## Tips

1. **Use ASCII sparingly** - Great for tech/dev presentations, can feel dated otherwise
2. **Stick to brand colors** - Don't mix custom colors, use the 5-color palette
3. **Big text on title slides** - h1 should be 4-5rem minimum
4. **One idea per slide** - Neobrutalism works best with focused content
5. **Test interactivity** - Always preview HTML before exporting


================================================================================

## 32. Expert Skill: wow-digest
> **Path within category:** `wow-digest/SKILL.md`


# wow-digest

## Purpose

Pull last 24h of newsletters (email) and Telegram channel posts, filter noise,
score survivors for genuine surprise against the user's focus and recent research,
and append 3-7 WOW items to today's daily note.

## Workflow

1. Run `scripts/ingest.py` to pull and normalize candidates from all sources
2. Run `scripts/enrich.py` to fetch full content for link-only newsletters (LinkedIn, beehiiv, Substack)
3. Run `scripts/salience_filter.py` to drop obvious noise (marketing, payments, greetings)
4. Run `scripts/wow_score.py` on filtered candidates to score and select WOW items
4. Append selected items to today's daily note under `## Reading`
5. Save raw candidates to `.wow-eval/candidates/YYYYMMDD.jsonl` for replay
6. Archive processed newsletter emails via GWS
7. During eval phase: run `scripts/feedback.py` to collect human verdicts

## Manual run

```bash
python3 scripts/ingest.py --days 1 --output /tmp/wow-candidates.jsonl
python3 scripts/enrich.py --input /tmp/wow-candidates.jsonl --output /tmp/wow-enriched.jsonl
python3 scripts/salience_filter.py --input /tmp/wow-enriched.jsonl --output /tmp/wow-filtered.jsonl
python3 scripts/wow_score.py --input /tmp/wow-filtered.jsonl --output /tmp/wow-selected.json
# Then the skill appends to daily note and archives emails
```

## Dry-Run Mode

When the user says `/wow-digest --dry-run` or "preview the digest", run the full pipeline but:
1. Do NOT append to daily note
2. Do NOT archive emails
3. Instead, print the selected items with scores and hooks directly in the conversation

This lets the user preview what would be appended without side effects.

## Context Sourcing

The scoring prompt uses three context signals from the vault (`~/Brains/brain/`):

- **`{focus}`** — From `My Focus.md`, sections `## Current`, `## Base`, `## Primary` (stops at `## Nice to have`). This tells the scorer what the user cares about right now.
- **`{research}`** — From `ai-research/*.md` files (last 30 days), parsed from filenames (`YYYYMMDD-topic.md`) and `research_topic:` frontmatter. Shows what the user has already investigated.
- **`{recent_topics}`** — From `Daily/YYYYMMDD.md` headings (last 7 days), excluding `## do` and `## log`. Shows recent daily note themes.

If these files don't exist, scoring still works but with degraded personalization.

## Dedup

Ingestion deduplicates against the last 7 days of `.wow-eval/candidates/*.jsonl` using SHA-256 hashes of `title|source_name` (case-insensitive). Same article shared to multiple channels or re-sent in a newsletter won't appear twice. Pass `--no-dedup` to `ingest.py` to skip.

## Config

Edit `config/sources.yaml` to add/remove email patterns or Telegram channels.
Edit `config/wow_prompt.txt` to tune the scoring prompt.

## Output Format

After scoring, append to today's daily note (`Daily/YYYYMMDD.md`) ABOVE the `- - -` separator, below any existing content:

```markdown
## Reading

- **[Title]** (Source) — hook explaining WHY it's surprising
- **[Title]** (Source) — hook
...

_WOW digest · N candidates → M selected · YYYY-MM-DD_
```

CRITICAL: Always run `date +"%Y%m%d"` to get today's date. Never assume.

If `## Reading` already exists in the daily note, append items to it rather than creating a duplicate section.

## Archive

After appending to daily note, archive processed newsletter emails:
1. Collect all `message_id` values from email candidates
2. Run GWS batchModify to remove INBOX label

```bash
gws gmail users messages batchModify \
  --params '{"userId":"me"}' \
  --json '{"ids":["ID1","ID2",...],"removeLabelIds":["INBOX"]}'
```

## Eval Mode (first 2 weeks)

During eval phase, do NOT auto-archive. Instead:

1. Run ingest + scoring as normal
2. Present the selected items to the user with FULL CONTENT, not just titles. For each item show:
   - Title + source
   - The snippet (first 300-500 chars of actual content)
   - The LLM's hook and challenged_assumption
   - WOW score breakdown (relevance, surprise, bridge_value, predictability)
3. Show all items in a single text block first so the user can read the content
4. Then ask via AskUserQuestion: "Was this actually WOW?" with options: wow / meh / noise / already_knew
5. Record feedback via `scripts/feedback.py`
6. Show current feedback stats
7. Only archive after user confirms

CRITICAL: The user CANNOT judge WOW from titles alone. Always show the snippet content.
If the snippet is empty or too short, fetch the full email body via GWS before presenting.

To check if eval mode is active:
- If `.wow-eval/feedback.jsonl` has fewer than 50 entries → eval mode
- If 50+ entries → auto mode (archive without asking)


================================================================================

## 33. Expert Skill: firecrawl-research
> **Path within category:** `firecrawl-research/SKILL.md`


# FireCrawl Research

## Overview

Enrich research documents by automatically searching and scraping web sources using the FireCrawl API. Extract research topics from markdown files and generate comprehensive research documents with source material.

## When to Use This Skill

Use this skill when the user:
- Says "Research this topic using FireCrawl"
- Requests to enrich notes or documents with web sources
- Wants to gather information about topics listed in a markdown file
- Needs to search and scrape multiple topics systematically

## How It Works

### 1. Topic Extraction

The script automatically extracts research topics from markdown files using two methods:

**Method 1: Headers**
```markdown
## Spatial Reasoning in AI
### Computer Vision Applications
```
Both `Spatial Reasoning in AI` and `Computer Vision Applications` become research topics.

**Method 2: Research Tags**
```markdown
- [research] Large Language Models for robotics
- [search] Theory of Mind in autonomous driving
```
Both tagged items become research topics.

### 2. Search and Scrape

For each topic:
1. Searches FireCrawl with the topic as query
2. Retrieves up to N results (default: 5)
3. Automatically scrapes full content from each result
4. Extracts markdown-formatted content (main content only)

### 3. Output Generation

Creates new markdown files in the specified output directory:
- One file per topic
- Filename: `{topic}_{timestamp}.md`
- Contains: title, date, sources count, full scraped content
- Each source includes: title, URL, markdown content

## Usage

### Basic Usage

```bash
python scripts/firecrawl_research.py research.md
```

Outputs to current directory.

### Specify Output Directory

```bash
python scripts/firecrawl_research.py research.md ./output
```

Creates files in `./output/` folder.

### Limit Results Per Topic

```bash
python scripts/firecrawl_research.py research.md ./output 3
```

Retrieves maximum 3 results per topic.

## Configuration

### API Key Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add FireCrawl API key:
   ```
   FIRECRAWL_API_KEY=fc-your-actual-api-key
   ```

The script automatically loads the API key from the skill's `.env` file.

### Rate Limiting

The script includes automatic rate limiting for FireCrawl's free tier:
- **Free tier limit:** 5 requests/minute
- **Built-in delay:** 12 seconds between topics
- Prevents API errors and credit exhaustion

When processing multiple topics, expect:
- 5 topics: ~1 minute
- 10 topics: ~2 minutes
- 20 topics: ~4 minutes

## Workflow Example

**User request:** "Research these AI topics using FireCrawl"

**Input file (`ai-research.md`):**
```markdown
# AI Research Topics

## Spatial Reasoning in Vision-Language Models

- [research] Embodied AI for robotics
- [research] Computer Use Agents
```

**Command:**
```bash
python scripts/firecrawl_research.py ai-research.md ./research_output 5
```

**Output:**
```
research_output/
├── Spatial_Reasoning_in_Vision-Language_Models_20251122_140530.md
├── Embodied_AI_for_robotics_20251122_140542.md
└── Computer_Use_Agents_20251122_140554.md
```

Each file contains:
- Topic title
- Timestamp
- Source count
- Full scraped content from up to 5 sources
- Source URLs

## Common Patterns

### Pattern 1: Quick Research
Extract topics from existing notes, research them, save to current folder:
```bash
python scripts/firecrawl_research.py my-notes.md
```

### Pattern 2: Organized Research
Create dedicated output folder for research results:
```bash
python scripts/firecrawl_research.py topics.md ./research_results
```

### Pattern 3: Deep Dive
Increase results per topic for comprehensive coverage:
```bash
python scripts/firecrawl_research.py topics.md ./deep_research 10
```

### Pattern 4: Obsidian Vault Integration
Direct output to vault's research folder:
```bash
python scripts/firecrawl_research.py topics.md ~/Brains/brain/Research
```

## Error Handling

### "API key not found"
Create `.env` file in skill folder with `FIRECRAWL_API_KEY=...`

### "Rate limit exceeded"
- Free tier: 5 req/min
- Script has 12s delay built-in
- If still hitting limit, reduce topics or wait between runs

### "Insufficient credits"
- Check FireCrawl account credits
- Upgrade plan or wait for credit reset

### "No topics found"
Add topics to markdown using:
- `## Header format`
- `- [research] Topic format`
- `- [search] Topic format`

## Script Details

**Location:** `scripts/firecrawl_research.py`

**Dependencies:**
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests to FireCrawl API

**Install dependencies:**
```bash
pip install python-dotenv requests
```

**FireCrawl Features Used:**
- `/v1/search` endpoint - Search with automatic scraping
- `scrapeOptions.formats: ['markdown']` - Markdown output
- `scrapeOptions.onlyMainContent: true` - Filter noise

## Academic Writing Templates

This skill includes templates for writing scientific papers in markdown format.

### Available Templates

**1. Pandoc Scholarly Paper** (`assets/templates/pandoc-scholarly-paper.md`)
- Standard academic paper format
- Compatible with Pandoc converter
- Supports citations via BibTeX
- Exports to PDF, DOCX, HTML

**2. MyST Scientific Paper** (`assets/templates/myst-scientific-paper.md`)
- MyST (Markedly Structured Text) format
- Advanced cross-referencing
- Professional scientific publishing
- Multi-format export (PDF, LaTeX, DOCX)

### Using Templates

**Copy template to your project:**
```bash
cp assets/templates/pandoc-scholarly-paper.md my-paper.md
# or
cp assets/templates/myst-scientific-paper.md my-paper.md
```

**Edit content:**
- Update YAML frontmatter (title, authors, affiliations)
- Write your content in sections
- Add citations using `[@AuthorYear]` (Pandoc) or `{cite}\`AuthorYear\`` (MyST)

**Convert to PDF/DOCX:**
```bash
python scripts/convert_academic.py my-paper.md pdf
python scripts/convert_academic.py my-paper.md docx
python scripts/convert_academic.py my-paper.md pdf --myst  # For MyST
```

### Bibliography Generation

Convert FireCrawl research results into BibTeX bibliography entries:

```bash
python scripts/generate_bibliography.py research_output/*.md -o references.bib
```

**What it does:**
- Extracts URLs and titles from FireCrawl markdown files
- Generates BibTeX `@misc` entries
- Creates citation keys automatically
- Adds access dates

**Example workflow:**
```bash
# 1. Research topics
python scripts/firecrawl_research.py topics.md ./research

# 2. Generate bibliography
python scripts/generate_bibliography.py research/*.md -o refs.bib

# 3. Copy template
cp assets/templates/pandoc-scholarly-paper.md paper.md

# 4. Edit paper.md (add content, cite sources)

# 5. Convert to PDF
python scripts/convert_academic.py paper.md pdf
```

### Citation Examples

**Pandoc syntax:**
```markdown
Recent research [@Smith2024] shows...
Multiple studies [@Jones2023; @Brown2024] indicate...
```

**MyST syntax:**
```markdown
Recent research {cite}`Smith2024` shows...
Multiple studies {cite}`Jones2023,Brown2024` indicate...
```

### Example Bibliography File

An example bibliography is provided in `assets/references.bib` with common entry types:
- Journal articles (`@article`)
- Conference papers (`@inproceedings`)
- Books (`@book`)
- PhD theses (`@phdthesis`)
- Web resources (`@misc`)
- Preprints (`@article` with arXiv)

## Tips

1. **Organize topics hierarchically** - Use `##` for main topics, `###` for subtopics
2. **Use descriptive names** - Topic text becomes filename, make it clear
3. **Batch processing** - Group related topics in one file for efficiency
4. **Output organization** - Create separate folders for different research projects
5. **Content review** - Results are truncated at 3000 chars/source for readability
6. **Academic workflow** - Use bibliography generator to cite research sources in papers
7. **Template customization** - Modify templates for your field's citation style

## Limitations

- **No summarization** - Returns raw scraped content, not summaries
- **No deduplication** - Duplicate sources may appear across topics
- **No quality ranking** - All results treated equally
- **New files only** - Does not append to existing files
- **Free tier constraints** - Rate limiting affects processing speed


================================================================================

## 34. Expert Skill: telegram
> **Path within category:** `telegram/SKILL.md`


# Telegram Message Skill

Fetch, search, download, send, and publish Telegram messages with flexible filtering and output options.

## Prerequisites

Authentication must be configured in `~/.telegram_dl/`. Run `setup` command to check status or get instructions:

```bash
python3 scripts/telegram_fetch.py setup
```

If not configured, follow these steps:
1. Get API credentials from https://my.telegram.org/auth
2. Clone telegram_dl: https://github.com/glebis/telegram_dl
3. Run `python telegram_dl.py` and follow interactive prompts
4. Verify with `python3 scripts/telegram_fetch.py setup`

## Quick Start

Run the script at `scripts/telegram_fetch.py` with appropriate commands:

```bash
# List available chats
python3 scripts/telegram_fetch.py list

# Get recent messages
python3 scripts/telegram_fetch.py recent --limit 20

# Search messages
python3 scripts/telegram_fetch.py search "meeting"

# Get unread messages
python3 scripts/telegram_fetch.py unread
```

## Commands

### List Chats

To see available Telegram chats:

```bash
python3 scripts/telegram_fetch.py list
python3 scripts/telegram_fetch.py list --limit 50
python3 scripts/telegram_fetch.py list --search "AI"
python3 scripts/telegram_fetch.py list --search "claude code глеб + саши" --exact
```

**Options:**
- `--search "text"`: Filter by substring match (case-insensitive)
- `--exact`: Require exact name match instead of substring (use with --search)
- `--limit N`: Max chats to retrieve (default: 30, increase if chat not found)

**Important:** If you're looking for a specific chat by exact name and it's not found, increase `--limit` to 100 or 200, as the chat may not be in the most recent 30.

Returns JSON with chat IDs, names, types, and unread counts.

### Fetch Recent Messages

To get recent messages:

```bash
# From all chats (last 50 messages across top 10 chats)
python3 scripts/telegram_fetch.py recent

# From specific chat
python3 scripts/telegram_fetch.py recent --chat "Tool Building Ape"
python3 scripts/telegram_fetch.py recent --chat-id 123456789

# With limits
python3 scripts/telegram_fetch.py recent --limit 100
python3 scripts/telegram_fetch.py recent --days 7
```

### Search Messages

To search message content:

```bash
# Global search across all chats
python3 scripts/telegram_fetch.py search "project deadline"

# Search in specific chat
python3 scripts/telegram_fetch.py search "meeting" --chat-id 123456789

# Limit results
python3 scripts/telegram_fetch.py search "important" --limit 20
```

### Fetch Unread Messages

To get only unread messages:

```bash
python3 scripts/telegram_fetch.py unread
python3 scripts/telegram_fetch.py unread --chat-id 123456789
```

### Send Messages

To send a message to a chat:

```bash
# Send to existing chat by name
python3 scripts/telegram_fetch.py send --chat "John Doe" --text "Hello!"

# Send to username (works even without prior conversation)
python3 scripts/telegram_fetch.py send --chat "@username" --text "Hello!"

# Reply to a specific message (use message ID from recent/search output)
python3 scripts/telegram_fetch.py send --chat "Tool Building Ape" --text "Thanks!" --reply-to 12345

# Send to a forum topic (for groups with topics enabled)
python3 scripts/telegram_fetch.py send --chat "Group Name" --text "Hello topic!" --topic 12

# Send with markdown formatting (converts **bold**, _italic_, [links](url) to Telegram HTML)
python3 scripts/telegram_fetch.py send --chat "@username" --text "**Bold** and _italic_ text" --markdown
```

**Formatting (`--markdown` flag):**
- Without `--markdown`: text is sent as-is (plain text, no formatting)
- With `--markdown`: converts markdown to Telegram HTML (`**bold**` -> bold, `_italic_` -> italic, `[text](url)` -> link, `## Header` -> bold, `* item` -> arrow list)
- **IMPORTANT**: Always use `--markdown` when sending draft content that contains markdown formatting
- The `publish` command handles markdown conversion automatically; the `send` command does NOT unless `--markdown` is specified

### Send Files

To send images, documents, or videos:

```bash
# Send an image
python3 scripts/telegram_fetch.py send --chat "John Doe" --file "/path/to/image.jpg"

# Send document with caption
python3 scripts/telegram_fetch.py send --chat "@username" --file "report.pdf" --text "Here's the report"

# Reply with media
python3 scripts/telegram_fetch.py send --chat "Group" --file "screenshot.png" --reply-to 12345
```

**Chat resolution order:**
1. `@username` - Resolves Telegram username directly
2. Numeric ID - Resolves chat by Telegram ID
3. Name match - Fuzzy search in existing dialogs

Returns JSON with send status, resolved chat name, message ID, and file info (for media).

### Edit Messages

To edit an existing message:

```bash
# Edit a message by ID
python3 scripts/telegram_fetch.py edit --chat "@mentalhealthtech" --message-id 76 --text "Updated text"

# Edit in a group/channel
python3 scripts/telegram_fetch.py edit --chat "Mental health tech" --message-id 123 --text "Corrected content"
```

**Note:** You can only edit your own messages. Telegram formatting (**bold**, etc.) is preserved.

Returns JSON with edit status and message ID.

### Download Attachments

To download media files from a chat:

```bash
# Download last 5 attachments from a chat (default)
python3 scripts/telegram_fetch.py download --chat "Tool Building Ape"

# Download last 10 attachments
python3 scripts/telegram_fetch.py download --chat "Project Group" --limit 10

# Download to custom directory
python3 scripts/telegram_fetch.py download --chat "@username" --output "/path/to/folder"

# Download from specific message
python3 scripts/telegram_fetch.py download --chat "John Doe" --message-id 12345
```

**Default output:** `~/Downloads/telegram_attachments/`

Returns JSON with download results (file names, paths, sizes).

### Fetch Forum Thread Messages

To get messages from a specific forum thread (topics in groups):

```bash
# Fetch from thread 174 in Claude Code Lab
python3 scripts/telegram_fetch.py thread --chat-id -1003237581133 --thread-id 174

# Fetch with custom limit
python3 scripts/telegram_fetch.py thread --chat-id -1003237581133 --thread-id 174 --limit 50

# Save to file
python3 scripts/telegram_fetch.py thread --chat-id -1003237581133 --thread-id 174 -o ~/thread.md

# Append to daily note
python3 scripts/telegram_fetch.py thread --chat-id -1003237581133 --thread-id 174 --to-daily

# JSON output
python3 scripts/telegram_fetch.py thread --chat-id -1003237581133 --thread-id 174 --json
```

**Messages are sorted newest first** (reverse chronological order).

**How to find thread ID:**
- Forum topic IDs appear in the thread URL: `https://t.me/c/CHAT_ID/THREAD_ID`
- Use `recent` command on the chat to see message IDs in threads

Returns markdown or JSON with all messages from the specified thread.

### Publish Draft to Channel

To publish a draft from the klodkot channel to Telegram:

```bash
# Dry run (preview without sending)
python3 scripts/telegram_fetch.py publish --draft "Channels/klodkot/drafts/20260122-anthropic-consciousness-question.md" --dry-run

# Publish to channel
python3 scripts/telegram_fetch.py publish --draft "Channels/klodkot/drafts/20260122-anthropic-consciousness-question.md"
```

**Workflow:**
1. Parses draft frontmatter and body
2. Validates channel field (must be "klodkot")
3. Extracts media references from frontmatter `video:` field and wikilinks
4. Resolves media paths in `Channels/klodkot/attachments/` or `Sources/`
5. Strips draft headers (e.g., "# Title - Telegram Draft")
6. Appends footer if not present: "**[КЛОДКОТ](https://t.me/klodkot)** — Claude Code и другие агенты: инструменты, кейсы, вдохновение"
7. Sends to @klodkot channel (multiple media as album)
8. Updates frontmatter with `published_date`, `telegram_message_id`
9. Moves file from `drafts/` to `published/`
10. Updates channel index with new entry at top

**Media handling:**
- Frontmatter: `video: filename.mp4`
- Wikilinks: `[[filename.mp4]]`, `[[image.png|alt text]]`
- Multiple media sent as Telegram album

**Safety:**
- `--dry-run` shows preview without sending
- Validates before sending
- Rollback on send failure (file not moved)
- Warnings on post-publish errors (file sent but move/index update failed)

**Returns:** JSON with publish status, message ID, warnings (if any)

## Output Options

### Default (Markdown to stdout)

By default, outputs formatted markdown suitable for Claude to read and summarize.

### JSON Format

Add `--json` flag for structured data:

```bash
python3 scripts/telegram_fetch.py recent --json
```

### Append to Obsidian Daily Note

Add messages to today's daily note in the vault:

```bash
python3 scripts/telegram_fetch.py recent --to-daily
python3 scripts/telegram_fetch.py search "project" --to-daily
```

Appends to `~/Brains/brain/Daily/YYYYMMDD.md`

### Append to Person's Note

Add messages to a specific person's note:

```bash
python3 scripts/telegram_fetch.py recent --chat "John Doe" --to-person "John Doe"
```

Creates or appends to `~/Brains/brain/{PersonName}.md`

### Save to File (Token-Efficient)

Save messages directly to file without consuming context tokens:

```bash
# Save 100 messages to markdown file
python3 scripts/telegram_fetch.py recent --chat "AGENCY: Community" --limit 100 -o ~/chat_archive.md

# Save with media files downloaded to same folder
python3 scripts/telegram_fetch.py recent --chat "Project Group" --limit 50 -o ~/project/archive.md --with-media

# Save search results to file
python3 scripts/telegram_fetch.py search "meeting" -o ~/meetings.md
```

Returns JSON with save status (file path, message count, media download results) - minimal token usage.

## Example User Requests

When user asks:

- "Show my recent Telegram messages" -> `recent --limit 20`
- "What Telegram messages did I get today?" -> `recent --days 1`
- "Search Telegram for messages about the project" -> `search "project"`
- "Get unread messages from Tool Building Ape" -> `unread` + filter output
- "Add my Telegram messages to daily note" -> `recent --to-daily`
- "What chats do I have on Telegram?" -> `list`
- "Find the exact chat named X" -> `list --search "X" --exact --limit 200`
- "Send hello to John on Telegram" -> `send --chat "John" --text "Hello!"`
- "Message @username on Telegram" -> `send --chat "@username" --text "..."`
- "Reply to that message with thanks" -> `send --chat "..." --text "Thanks!" --reply-to <id>`
- "Send this image to John" -> `send --chat "John" --file "/path/to/image.jpg"`
- "Send report.pdf with caption" -> `send --chat "..." --file "report.pdf" --text "Here's the report"`
- "Send to topic 12 in Group" -> `send --chat "Group" --text "..." --topic 12`
- "Download attachments from Tool Building Ape" -> `download --chat "Tool Building Ape"`
- "Download last 10 files from Project Group" -> `download --chat "Project Group" --limit 10`
- "Save last 100 messages from AGENCY to file" -> `recent --chat "AGENCY: Community" --limit 100 -o ~/agency.md`
- "Archive chat with media" -> `recent --chat "Group" -o ~/archive.md --with-media`
- "Edit that message" -> `edit --chat "..." --message-id <id> --text "new text"`
- "Fix the typo in message 123" -> `edit --chat "..." --message-id 123 --text "corrected text"`
- "Is Telegram configured?" -> `setup`
- "How do I set up Telegram?" -> `setup` (returns instructions if not configured)
- "Publish this draft to klodkot" -> `publish --draft "Channels/klodkot/drafts/...md"`
- "Preview this draft before publishing" -> `publish --draft "..." --dry-run`

## Rate Limiting

The script includes built-in rate limiting (0.1s between messages) and handles Telegram's FloodWaitError automatically with backoff.

## Dependencies

Requires Python packages:
- `telethon` - Telegram API client
- `pyyaml` - YAML parsing for draft frontmatter

Install with: `pip install telethon pyyaml`


================================================================================

## 35. Expert Skill: site-diagnosis
> **Path within category:** `site-diagnosis/SKILL.md`


# Site Diagnosis — Pre-Consultation Questionnaire

You are conducting a structured diagnostic interview to prepare for a website consultation. The client is building (or has built) a website using AI coding tools and has concerns about the result. Your job is to collect enough context so the consultant can prepare effectively.

## How This Works

Walk the client through 5 rounds of questions using AskUserQuestion. Round 0 picks the language; Rounds 1–4 cover the diagnostic themes. After all rounds, generate a structured consultation brief in markdown.

Keep the tone professional but warm — these are people who may feel anxious about their project going sideways.

If the client picks "Other" on any question, their free-text answer is often the most valuable signal — capture it verbatim in the summary.

## Round 0: Language

Ask this question alone, before anything else:

**Question 0 — "Language / Язык"**
- header: "Язык"
- question: "На каком языке вам удобнее проходить анкету? / Which language do you prefer?"
- options:
  - "Русский" — Russian
  - "English" — English
- multiSelect: false

Store the chosen language. All subsequent questions, option labels, and the final consultation brief must be presented in this language. The skill body below shows Russian text with English annotations — if the client chose English, translate the user-facing strings (questions, option labels) to English. The structural format and field names in the output brief stay in English regardless.

## Round 1: Project & Background

Ask these 3 questions together:

**Question 1 — "Что вы делаете?"**
- header: "Проект"
- question: "Какой сайт вы делаете или уже сделали?"
- options:
  - "Лендинг / одностраничник" — single page, usually for a product or service launch
  - "Сайт-визитка / портфолио" — personal or business card site, portfolio
  - "Интернет-магазин" — e-commerce with catalog and payments
  - "Блог / контентный сайт" — content-driven, articles, media
- multiSelect: false

**Question 2 — "Ваш технический уровень"**
- header: "Опыт"
- question: "Как бы вы описали свой технический уровень?"
- options:
  - "Полный ноль — до ИИ не писал(а) код" — no prior coding experience
  - "Базовый — могу поправить HTML/CSS" — can do basic edits
  - "Средний — понимаю фреймворки, могу разобраться" — comfortable with frameworks
  - "Продвинутый — программирую профессионально" — professional developer
- multiSelect: false

**Question 3 — "Какие ИИ-инструменты используете?"**
- header: "Инструменты"
- question: "Какими ИИ-инструментами вы пользуетесь для создания сайта?"
- options:
  - "Claude (Code, Projects, чат)" — Anthropic's Claude in any form
  - "Cursor / Windsurf / другая ИИ-IDE" — AI-powered code editors
  - "Bolt / Lovable / v0" — no-code AI builders
  - "ChatGPT / Codex" — OpenAI tools
- multiSelect: true

## Round 2: Current State & Pain Points

**Question 4 — "На каком этапе проект?"**
- header: "Этап"
- question: "На каком этапе сейчас находится ваш сайт?"
- options:
  - "В самом начале — есть идея, мало кода" — early stage
  - "В процессе — основная часть сделана, но не готово" — mid-build
  - "Почти готов — доделываю детали" — nearly done
  - "Уже запущен — но хочу улучшить" — live, needs improvement
- multiSelect: false

**Question 5 — "Что беспокоит больше всего?"**
- header: "Боли"
- question: "Что вас больше всего беспокоит в текущем состоянии сайта?"
- options:
  - "Дизайн — выглядит 'как от ИИ', непрофессионально" — generic AI look
  - "Код — не понимаю что там внутри, боюсь сломать" — black box code
  - "Администрирование — непонятно как обновлять контент" — content management
  - "Производительность — медленно грузится, ошибки" — performance issues
- multiSelect: true

**Question 6 — "Что нравится в текущем результате?"**
- header: "Плюсы"
- question: "Есть ли что-то, что вам нравится в том, что уже получилось?"
- options:
  - "Да, базовая структура и логика хорошие" — good foundation
  - "Да, отдельные страницы/секции удались" — some parts work well
  - "Скорее нет — хочу переделать существенную часть" — mostly unhappy
  - "Сложно оценить — поэтому и нужна консультация" — can't tell, need expert eye
- multiSelect: false

## Round 3: Design & Technical Details

**Question 7 — "Проблемы с дизайном"**
- header: "Дизайн"
- question: "Какие проблемы с дизайном вы видите?"
- options:
  - "Выглядит шаблонно / скучно" — looks templated, generic
  - "Цвета и шрифты не сочетаются" — poor color/typography choices
  - "Неудобная навигация, непонятная структура" — bad UX/IA
  - "Плохо выглядит на телефоне" — not mobile-friendly
- multiSelect: true

**Question 8 — "Где размещён сайт?"**
- header: "Хостинг"
- question: "Где размещён (или планируется разместить) ваш сайт?"
- options:
  - "Vercel / Netlify / Cloudflare Pages" — modern JAMstack hosting
  - "Свой сервер / VPS" — self-hosted
  - "Пока нигде — только локально" — local only
  - "Не знаю / не уверен(а)" — don't know
- multiSelect: false

**Question 9 — "Технологии"**
- header: "Стек"
- question: "Знаете ли вы, какие технологии использует ваш сайт?"
- options:
  - "React / Next.js" — React ecosystem
  - "HTML/CSS/JS без фреймворка" — vanilla stack
  - "Другой фреймворк (Vue, Svelte, Astro...)" — other framework
  - "Не знаю — ИИ сам выбрал" — AI chose, client doesn't know
- multiSelect: false

## Round 4: Goals & Expectations

**Question 10 — "Как планируете обновлять контент?"**
- header: "Контент"
- question: "Как вы планируете обновлять контент на сайте после запуска?"
- options:
  - "Буду просить ИИ вносить изменения" — ask AI to edit
  - "Хочу CMS (админку), чтобы самому менять" — wants a CMS
  - "Буду редактировать код вручную" — manual code edits
  - "Пока не думал(а) об этом" — hasn't considered this yet
- multiSelect: false

**Question 11 — "Что хотите получить от консультации?"**
- header: "Цель"
- question: "Какой результат консультации был бы для вас идеальным?"
- options:
  - "Конкретный план — что исправить и в каком порядке" — actionable fix plan
  - "Оценку — стоит ли продолжать или лучше начать заново" — go/no-go assessment
  - "Обучение — научиться лучше работать с ИИ-инструментами" — learn to use AI better
  - "Помощь с конкретной проблемой (расскажу подробнее)" — specific problem
- multiSelect: true

**Question 12 — "Что ещё важно знать?"**

This is a free-text question. Do NOT use AskUserQuestion here — instead, ask the client directly in conversation text (in their chosen language):

Russian: "Последний вопрос! Пожалуйста, напишите свободным текстом всё, что считаете важным: ссылку на сайт или репозиторий, примерный бюджет на доработку, конкретные страницы или элементы, которые беспокоят, референсы (сайты, которые нравятся) — любые детали, которые помогут подготовиться к консультации."

English: "Last question! Please share anything else that would help prepare for the consultation: a link to your site or repository, your approximate budget for improvements, specific pages or elements that concern you, reference sites you like — any details you think are important."

Wait for the client's free-text response before generating the summary.

## Generating the Summary

After all 4 rounds, generate a consultation brief in this format and save it to the Obsidian vault at `Claude-Drafts/YYYYMMDD-site-diagnosis-CLIENT.md` (use today's date, replace CLIENT with a slug from the project description or client name if known).

```markdown

# Site Diagnosis Brief

## Client Profile
- **Technical level**: [answer]
- **AI tools**: [answer]

## Project
- **Type**: [answer]
- **Stage**: [answer]
- **Tech stack**: [answer]
- **Hosting**: [answer]

## Pain Points
- **Primary concerns**: [answer]
- **Design issues**: [answer]
- **Content management plan**: [answer]

## What's Working
[answer]

## Consultation Goals
[answer]

## Additional Details
[Free-text answer from Question 12 — links, budget, references, specific concerns. Capture verbatim, then add any structured observations below.]

## Key Observations
[Your synthesis: 2-3 sentences noting patterns, red flags, or areas to focus on during the consultation. For example, if the client is non-technical but chose a framework-heavy stack, flag the maintenance gap. If they want a CMS but are on a static site, note the mismatch.]

## Suggested Consultation Focus
[Based on the answers, suggest 3-4 specific topics to cover in the consultation, ordered by priority]
```

After saving, tell the user where the file is and offer a brief summary of what you noticed — the patterns, mismatches, or key risks that stand out from the answers.


================================================================================

## 36. Expert Skill: fathom
> **Path within category:** `fathom/SKILL.md`


# Fathom Meeting Fetcher

Fetches meeting data directly from Fathom API including transcripts, AI summaries, action items, and participant info.

## Usage

```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `--list` | List recent meetings with IDs |
| `--id <id>` | Fetch specific meeting by recording ID |
| `--today` | Fetch all meetings from today |
| `--since <date>` | Fetch meetings since date (YYYY-MM-DD) |

### Options

| Option | Description |
|--------|-------------|
| `--analyze` | Run transcript-analyzer on fetched meetings |
| `--download-video` | Download video recording (requires ffmpeg) |
| `--output <path>` | Output directory (default: ~/Brains/brain) |
| `--limit <n>` | Max meetings to list (default: 10) |

## Examples

### List recent meetings
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --list
```

### Fetch today's meetings
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --today
```

### Fetch and analyze
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --today --analyze
```

### Fetch since date
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --since 2025-01-01
```

### Fetch specific meeting
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --id abc123def456
```

### Download video with meeting
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --id abc123def456 --download-video
```

## Output Format

Each meeting is saved as markdown with:

```markdown

# Meeting Title

## Summary
{AI-generated summary from Fathom}

## Action Items
- [ ] Item 1 (@assignee)
- [ ] Item 2

## Transcript
**Speaker Name**: What they said...
```

## File Naming

Files are saved as: `YYYYMMDD-meeting-title-slug.md`

Example: `20250106-weekly-standup.md`

## Prerequisites

Install dependencies (first time):
```bash
pip install requests python-dotenv
```

For video download (optional):
```bash
# ffmpeg required for video downloads
brew install ffmpeg  # macOS
# or apt install ffmpeg (Linux)
```

## Configuration

API key stored in `~/.claude/skills/fathom/scripts/.env`:
```
FATHOM_API_KEY=your-api-key
```

## Integration

- **transcript-analyzer**: Use `--analyze` flag to automatically process transcripts
- **video-downloader**: Use `--download-video` flag to download meeting recordings
  - Validates downloaded videos using ffprobe
  - Automatically retries up to 3 times if download fails
  - Videos saved as .mp4 next to meeting markdown files
- Replaces Dropbox sync workflow (direct API access)


================================================================================

## 37. Expert Skill: rag-eval
> **Path within category:** `rag-eval/SKILL.md`


# rag-eval

## Purpose

Replace the "tweak → squint → swap model → burn credits" loop with a single command that runs a grid of eval variants on the user's gold-set, ranks them by a cost-aware score, and returns structured feedback on architecture, stack, and likely-issues. Draws on evidence-based RAG practices and learns from the user's past runs.

## When to use

Trigger on: "help me test a RAG", "tune my RAG", "my RAG is bad", "compare retrieval prompts", "how do I eval this", "what's the best embedding model for X", "my RAG eval is expensive". Also trigger when the user reports burning OpenRouter / OpenAI credits with no clear signal of improvement.

## Prerequisites — gather before running

Collect these from the user before the first sweep. Many are optional with sensible defaults; always confirm the ones that gate cost.

1. **RAG codebase root** — path to the repo/module under test.
2. **Gold-set** — at least 10 Q&A pairs. If missing, offer to generate a starter gold-set from the user's dataset (LLM-synthesized, human-reviewed). See `references/best-practices.md`.
3. **Dataset** — the corpus the RAG retrieves over.
4. **Budget cap** — hard dollar limit per run (default: $2 if user doesn't specify). **Always confirm before any sweep.**
5. **Provider keys** — `OPENROUTER_API_KEY` or `OPENAI_API_KEY` (read from env).
6. **Vector-store config** — collection name, embedding model, chunk size (read from repo; confirm if ambiguous).
7. **Eval history path** (optional) — defaults to `.rag-eval/history.jsonl` in the repo root.

## Workflow

Follow this order. Refer to `references/best-practices.md` for the canonical checklist and `references/evidence-base.md` for the research-backed defaults.

### Step 0 — (Optional) Ingest a prior iteration session

When the user provides a session ID (Claude Code transcript, skill-studio session, or a Fathom meeting), run the **deterministic ingest** *first* — no LLM calls. This extracts only the useful signals (models tried, prompt variants, cost events, eval results) as compact JSON, so the rest of the skill works off a tiny structured bundle instead of a long raw transcript.

```bash
python scripts/session_ingest.py <session_id> > /tmp/rag-eval-bundle.json
# or with a direct path:
python scripts/session_ingest.py --path /path/to/transcript.jsonl > /tmp/rag-eval-bundle.json
```

The bundle includes: `models_tried`, `prompts_tried` (hashes only), `iterations`, `total_cost_usd`, `summary_stats`. Feed this into Step 1 — do not paste the raw transcript.

**Why this matters:** transcripts can be 100k+ tokens of noise. The ingest script does regex extraction only, keeping the LLM budget for the actual audit + sweep planning. This is a hard requirement, not an optimization.

### Step 1 — Audit the stack

Read `references/best-practices.md` and inspect the user's repo + vector-store config. Produce a structured report covering:
- Architecture (retrieval type: dense / hybrid / rerank; chunking strategy; prompt structure)
- Tech stack (embedding model, LLM, vector store)
- Resources (dataset size, gold-set size, prior eval runs)
- Risks (known anti-patterns, missing pieces)

Present the report to the user and ask which issues to address first.

### Step 2 — Propose a sweep plan

Based on the audit, propose 3–8 variants to test. Keep the grid small on the first run (default: 2 prompts × 2 models × 1 retrieval variant = 4 cells). Estimate cost using gold-set size × variants × avg tokens × provider pricing. **Present the cost estimate and wait for user confirmation before running.**

### Step 3 — Run the sweep

Use `scripts/eval_sweep.py` (see the script header for invocation). It reads a config YAML, runs each variant against the gold-set, records per-variant cost and answer quality, and appends to `history.jsonl`.

**Guardrails:**
- Never exceed the budget cap — halt mid-sweep if reached.
- Never mutate the user's repo. Write all artifacts under `.rag-eval/` (gitignore it).
- Confirm before any sweep estimated to exceed the user's cap.

### Step 4 — Rank and report

After the sweep, rank variants by a cost-aware score: `quality × (1 / log(1 + cost))`. Present:
- Top 3 variants with quality metrics and cost
- What changed vs the previous best
- Concrete next experiment to try

Write the full report to `.rag-eval/reports/<timestamp>.md`.

### Step 5 — Self-improve

Before each subsequent run, read `history.jsonl` and factor in what the user has already tried. Avoid re-testing rejected variants. Surface patterns ("models A, B, C all underperformed on multi-hop queries — next try a reranker").

## Reusable resources

- `scripts/eval_sweep.py` — grid-search runner. Reads `eval_config.yaml`, writes results to `history.jsonl`.
- `references/best-practices.md` — evidence-based RAG checklist the agent uses as an anchor.
- `references/evidence-base.md` — pointers to recent RAG research and when each technique helps.
- `assets/eval_config.template.yaml` — starter config to copy into the user's repo.
- `assets/gold_set.template.jsonl` — 3 example Q&A pairs to show the gold-set format.

## Notes

- **Cost is the main failure mode.** Never run without a confirmed budget. Err on the side of smaller sweeps; users can always run again.
- **No repo mutation.** All outputs go under `.rag-eval/` in the target repo.
- **When uncertain about best practices, do web research.** Use `tavily-search` or `firecrawl-research` to pull current evidence, then synthesize into the audit report.
- **Defer to the user.** Before changing any file in the target repo, always confirm.


================================================================================

## 38. Expert Skill: temple-generator
> **Path within category:** `temple-generator/SKILL.md`


# Temple Generator

Generate a 3D interactive knowledge visualization from any Obsidian vault. The output is a single HTML file (Three.js) with concentric entity rings, audio, discovery mechanics, and multi-scale semantic zoom.

## When to Use

- User wants to visualize any Obsidian vault as a 3D knowledge map
- User wants to compare two vaults/document sets visually
- User wants to regenerate the temple from scratch with fresh vault analysis

## Architecture

Two-part system:
1. **Generation pipeline** (this skill): discovers structure, names it, scores confidence, exports a scene package
2. **Runtime renderer** (template): handles navigation, transitions, audio, discovery

Pre-generate meaning. Runtime-render experience.

## Workflow

### Step 1: Scan the Vault

Run `python3 ~/.claude/skills/temple-generator/scripts/extract_entities.py <vault_path>`.

This produces `vault-scan.json` with:
- Files: path, title, tags, outgoing links, backlink counts, word count, folder, frontmatter
- Graph: adjacency list with bidirectional link counts
- Centrality: degree centrality per node
- Clusters: detected groups of tightly linked notes

### Step 2: Read the Scan + Sample Notes

1. Read `vault-scan.json`
2. Read the top ~20 nodes by centrality (first 100 lines each)
3. Read `references/classification-guide.md` for entity type heuristics
4. Read 3-5 representative notes to calibrate the vault's "voice" (formal/informal, domain jargon, language)

### Step 3: Classify Entities

Using `references/classification-guide.md`, assign each significant node to an entity type. Maintain two vocabularies:

- **canonical**: neutral labels for portability (`anxiety-management`, `fermentation-process`)
- **poetic**: mythic/art labels for the installation (`The Ferment Gate`, `The Cortisol Throne`)

Target counts per type (adjust for vault size):

| Type | Small vault (< 100) | Medium (100-500) | Large (500+) |
|------|---------------------|-------------------|--------------|
| Gods | 2-3 | 3-5 | 5-7 |
| Demigods | 3-7 | 5-12 | 8-15 |
| Tensions | 2-4 | 3-7 | 5-9 |
| Narratives | 2-5 | 5-10 | 8-12 |
| Blind spots | 1-3 | 3-5 | 4-7 |
| Spirits | 1-3 | 3-5 | 3-5 |
| Research | 5-15 | 10-25 | 15-30 |
| Values | 2-5 | 3-8 | 5-10 |
| Trails | 2-5 | 3-8 | 5-10 |
| Questions | 3-6 | 5-10 | 8-12 |
| Depths | 2-5 | 5-10 | 8-15 |
| Crystals | 1-3 | 2-5 | 3-6 |

### Step 4: Build Abstraction Levels

Levels are **confidence-gated** — only include a level if the vault supports it.

**Level 0 — Entities** (always exists): individual nodes with positions, connections, descriptions.

**Level 1 — Domains** (requires >= 3 meaningful clusters): groups of related entities. Each domain has:
- `canonical` + `poetic` name
- member entity keys
- centroid position (weighted average of member positions)
- representative exemplar (most central member)
- description (1-2 sentences in vault voice)
- confidence score (0-1)

**Level 2 — Axes** (requires >= 2 interpretable opposing pairs): fundamental tensions. Each axis has:
- two poles with names and descriptions
- member domains per pole
- axis description
- confidence score

**Level 3 — Comparison** (requires two vaults + sufficient alignment): shared/unique analysis.

Read `references/merge-algorithm.md` for dual-graph logic.

### Step 5: Generate Scene Package

Follow the schema in `references/entity-schema.md` to produce `temple-data.json`.

Include:
- `entities`: all classified nodes
- `levels`: abstraction layers with zoom thresholds
- `mappings`: entity → domain → axis crosswalks
- `comparison`: (if dual-graph) shared/unique/alignment data
- `audio`: motif hints per type and level
- `style`: poetic vocabulary, intro text, color palette, layer definitions
- `confidence`: per-abstraction and per-alignment scores

### Step 6: Generate HTML

1. Copy `~/.claude/skills/temple-generator/assets/temple-template.html` to the output location
2. If `--inline` flag: embed the JSON data as `const TEMPLE_DATA = {...};` inside the HTML
3. Otherwise: place `temple-data.json` alongside the HTML

### Step 7: Report

Show the user:
- Entity counts by type
- Abstraction levels generated (with confidence scores)
- Top 5 gods/central entities
- Detected tensions
- If dual-graph: overlap percentage and shared domains

## Dual-Graph Mode

When `--compare vault_path_2` is provided:

1. Scan both vaults independently (Step 1)
2. Classify entities for each vault (Steps 2-3)
3. Run merge algorithm from `references/merge-algorithm.md`
4. Generate merged scene package with source attribution
5. Template renders shared scaffold with divergence offsets

## Quality Guidelines

- Skip trivial notes (daily todos, admin logs, empty stubs)
- Prefer nodes that reveal the vault's actual concerns, not its filing system
- Write in the vault's own voice, calibrated from sample notes
- If a level lacks confidence, omit it rather than fabricating structure
- Each abstraction level must be backed by membership weights, exemplars, and provenance
- "The abstraction hierarchy should be semantic, not just geometric"

## Audio Guidance for Template

The template's audio system should respect hierarchical continuity across zoom levels:
- L0 (close): localized, identity-rich — entity whispers and textures
- L1 (medium): regional harmonic beds, cluster pulses
- L2 (far): sparse drones, tension-based tonal movement
- L3 (comparison): stereo/dialogic between two vault voices

Zoom should feel like changing resolution, not changing universes. Motifs relate across scales.


================================================================================

## 39. Expert Skill: sorted
> **Path within category:** `sorted/SKILL.md`


# Sorted — Freelancer Tax & Invoicing Automation

Automates [getSorted.de](https://app.getsorted.de/) via real Chrome Beta browser for invoicing, expense tracking, and German tax report submissions.

## Prerequisites

- Chrome Beta with `--remote-debugging-port=9222` (use `/real-browser` launch sequence)
- Google account session persisted in `~/.chrome-beta-profile`
- `agent-browser` CLI installed

## Commands

### `invoice create`

Create a new invoice on Sorted.

**Required params:** client name, amount
**Optional:** hours, rate, description, due date, service date, client type (business/person)

### `invoice download <invoice-number>`

Download a properly formatted PDF from Sorted (not browser print).

### `invoice send <invoice-number> --email <email>`

Send invoice via email directly from Sorted (paid plan only). On free plan, downloads PDF and sends via Telegram instead.

### `invoice list`

List all invoices with status (paid/unpaid).

### `expense add`

Add an expense entry.

### `tax status`

Show current tax obligations, deadlines, and overdue reports.

### `tax preview <report-type> <period>`

Preview a tax report before submission.

### `tax submit <report-type> <period>`

Submit a tax report to Finanzamt via ELSTER (requires paid plan).

## Sorted Navigation

App URL: `https://app.getsorted.de/`

| Section | Sidebar link | Purpose |
|---------|-------------|---------|
| Dashboard | Sorted (logo) | Overview: taxes owed, income, expenses |
| Taxes | Taxes | Tax reports, deadlines, submissions |
| Income | Income | Invoice list, create/edit invoices |
| Expenses | Expenses | Expense tracking, receipts |
| Tax consultant | Tax consultant | Advisor connection |
| Personal details | Profile → Personal details | Freelancer info, Steuernummer |
| Bank accounts | Profile → Bank accounts (Beta) | Connected banks |
| Subscription | Profile → Subscription | Plan management |
| Import | Profile → Import your data | Bulk data import |
| Settings | Profile → Settings | App preferences |

## Tax Report Types

| Report | German name | Frequency | Description |
|--------|------------|-----------|-------------|
| Advance VAT | Umsatzsteuer-Voranmeldung (UStVA) | Quarterly | VAT collected on invoices |
| EU Summary | Zusammenfassende Meldung (ZM) | Quarterly | Revenue from EU customers |
| Annual Returns | EÜR + Einkommensteuererklärung | Yearly | Profit/loss + income tax |

## Invoice Creation Flow

### Step-by-step browser automation:

1. **Navigate:** `Income` → click `Add` → `Create invoice`
2. **Set client:** Click `Client details` area on invoice preview
   - Search existing clients or click `Add new client`
   - Choose `Business` or `Private person`
   - Fill: name, VAT/TIN, street, city, zip, country (autocomplete dropdown — type then click match), email (optional)
   - Click `Save` in dialog
3. **Set invoice date:** Click the date next to "Invoice date" (defaults to today)
4. **Set service date (REQUIRED):** Click the empty area to the right of invoice date labeled "Service date"
   - This is a **date range picker** — select start date, then end date
   - If same-day service, click the same date twice
   - **Without service date, Save will fail silently** — the field shows "Required" in red
   - The clickable element has class `clickable` and is positioned at ~x:734 y:413 on the invoice preview
   - If snapshot doesn't show it, use JS: find div with text "Service dateRequired" and click it
5. **Set due date:** Click "Select date" under "Due date" → pick from calendar
6. **Add line item:** Click `Add a line`
   - Fields: description (text), quantity (number), unit dropdown (h/pcs/etc), rate (number)
   - Click on collapsed values to re-edit them
7. **VAT:** Automatically 0% for Kleinunternehmer accounts. Shows "Service not taxable in Germany" in notes
8. **Save:** Click `Save` button. Title changes from "Add invoice" to "Edit invoice" on success

### Gotchas

- **Service date is mandatory** but easy to miss — it's not highlighted until you try to save
- **German number formatting:** dots are thousands separators (1.000 = one thousand), commas are decimals
- **Collapsed fields:** After saving, line item fields collapse to display-only. Click the displayed value to re-open the editable field
- **Invoice number:** Auto-generated sequentially (e.g., 2025-03-21). Can be edited by clicking it

## Invoice PDF Download Flow

**CRITICAL: Do NOT use Chrome CDP `Page.printToPDF` — it captures the entire page including sidebar and settings panel. Always use Sorted's native PDF.**

### Step-by-step:

1. Open the invoice (click from Income list, or navigate after creating)
2. Click `Save and send` button (top right, teal button)
3. An **"Email invoice"** dialog appears with:
   - To field (email)
   - Subject (auto-filled)
   - Message textarea
   - **Attachments section** at the bottom showing the PDF filename
4. Click the PDF link (e.g., `ALL3 DOO BELGRADE-2025-03-21-20260506.pdf`)
   - It's a `generic` element with `cursor:pointer` and `onclick`
   - The text matches pattern: `{CLIENT_NAME}-{INVOICE_NUMBER}-{DATE}.pdf`
5. PDF downloads to `~/Downloads/`
6. Close the dialog (click `Close` or `×`)

### Email sending (paid plan)

On paid plans, the "Email invoice" dialog is fully functional:

1. Fill `To` field with client email (`@e49`)
2. Edit `Subject` if needed (auto-filled as "Gleb Kalinin sent you an invoice (#INVOICE-NUMBER)")
3. Write a `Message` in the textarea
4. Toggle "Send a copy to my email" checkbox (checked by default)
5. Click `Email invoice` button (`@e15`) to send

On the **free plan**, the dialog shows "Sending invoices by email is not available in your plan" with a "Change my plan" link. The PDF download still works regardless.

### Fallback: Telegram delivery (free plan)

When email sending is unavailable, download the PDF and send via Telethon (see "Sending Invoice After Download" section below).

### PDF filename pattern
```
{CLIENT_NAME}-{INVOICE_NUMBER}-{YYYYMMDD}.pdf
```
Example: `ALL3 DOO BELGRADE-2025-03-21-20260506.pdf`

## Client Management

Existing clients are stored and reusable. When creating an invoice:
- The client picker shows all saved clients
- Search by name in the search box
- Edit/delete clients via small buttons next to each name

### Client fields (Business)
- Business name (required)
- VAT number / TIN (optional)
- Street & Number
- City
- Zip Code
- Country (autocomplete — type and click match)
- Email

### Client fields (Private person)
- First name, Last name
- Address fields same as business

## Sending Invoice After Download

After downloading the PDF, send via Telegram using Telethon:

```python
from telethon.sync import TelegramClient
import json
from pathlib import Path

config = json.loads((Path.home() / '.telegram_dl' / 'config.json').read_text())
session = str(Path.home() / '.telegram_dl' / 'user')

with TelegramClient(session, config['api_id'], config['api_hash']) as client:
    client.send_file("username", "/path/to/invoice.pdf", caption="message")
```

## Gleb's Sorted Account Details

- **Status:** Kleinunternehmer (no VAT charged)
- **Finanzamt:** Berlin - Wedding
- **VAT-ID:** DE369692682
- **Tax Number:** 2337201265
- **Bank:** Revolut Bank UAB, Zweigniederlassung
- **IBAN:** DE38 1001 0178 8157 1777 30
- **BIC/SWIFT:** REVODEB2
- **Plan:** Free (invoicing works, tax submission requires upgrade)

## Browser Session Setup

Always use the `/real-browser` skill's launch sequence. Session name should be unique per run:

```bash
SESSION=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 6)
agent-browser --cdp 9222 --session "$SESSION" open "https://app.getsorted.de/"
```

Google login is persisted — no need to re-authenticate each time.


================================================================================

## 40. Expert Skill: zoom
> **Path within category:** `zoom/SKILL.md`


# Zoom Skill

Manage Zoom meetings and cloud recordings via the Zoom API.

## Features

- **Meetings**: List, create, update, delete scheduled meetings
- **Recordings**: List cloud recordings with transcripts, summaries, and download links

**Note:** All times passed to create/update commands are interpreted as **local time**. The script auto-detects your timezone if not explicitly specified with `--timezone`.

## Prerequisites

This skill uses two authentication methods:

| Feature | Auth Type | Credentials File |
|---------|-----------|------------------|
| Meetings | Server-to-Server OAuth | `~/.zoom_credentials/credentials.json` |
| Recordings | User OAuth (General App) | `~/.zoom_credentials/oauth_token.json` |

Check status:

```bash
python3 scripts/zoom_meetings.py setup
```

## Setup

### Part 1: Server-to-Server OAuth (for Meetings)

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us/) → Develop → Build App
2. Select **Server-to-Server OAuth**
3. Name it (e.g., "Claude Zoom Meetings")
4. Copy **Account ID**, **Client ID**, **Client Secret**
5. Add scopes:
   - `meeting:read:meeting:admin`
   - `meeting:read:list_meetings:admin`
   - `meeting:write:meeting:admin`
   - `user:read:user:admin`
6. Activate the app
7. Save credentials:

```bash
mkdir -p ~/.zoom_credentials
cat > ~/.zoom_credentials/credentials.json << 'EOF'
{
  "account_id": "YOUR_ACCOUNT_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
EOF
```

### Part 2: General App OAuth (for Recordings)

Server-to-Server apps cannot access cloud recordings. You need a separate General App:

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us/) → Develop → Build App
2. Select **General App**
3. Set redirect URL: `http://localhost:8888/callback`
4. Copy **Client ID** and **Client Secret**
5. Add scopes:
   - `cloud_recording:read:list_user_recordings`
   - `cloud_recording:read:list_recording_files`
6. Activate the app
7. Authorize (one-time browser flow):

```bash
# Open this URL in browser (replace CLIENT_ID):
https://zoom.us/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8888/callback

# After authorizing, you'll be redirected to:
# http://localhost:8888/callback?code=AUTHORIZATION_CODE

# Exchange the code for tokens (replace values):
python3 -c "
import requests, json
resp = requests.post('https://zoom.us/oauth/token',
    auth=('CLIENT_ID', 'CLIENT_SECRET'),
    data={'grant_type': 'authorization_code', 'code': 'AUTH_CODE', 'redirect_uri': 'http://localhost:8888/callback'})
data = resp.json()
data['client_id'] = 'CLIENT_ID'
data['client_secret'] = 'CLIENT_SECRET'
data['expires_at'] = __import__('time').time() + data.get('expires_in', 3600)
with open(__import__('pathlib').Path.home() / '.zoom_credentials/oauth_token.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Saved!')
"
```

## Quick Start

```bash
# Check setup
python3 scripts/zoom_meetings.py setup

# List upcoming meetings
python3 scripts/zoom_meetings.py list

# Create a meeting
python3 scripts/zoom_meetings.py create "Team Standup" --start "2025-01-15T10:00:00" --duration 30

# List recordings
python3 scripts/zoom_meetings.py recordings --start 2025-01-01
```

## Commands

### Meetings

```bash
# List meetings
python3 scripts/zoom_meetings.py list                      # upcoming
python3 scripts/zoom_meetings.py list --type previous      # past
python3 scripts/zoom_meetings.py list --limit 10 --json

# Get meeting details
python3 scripts/zoom_meetings.py get MEETING_ID

# Create meeting (times are treated as LOCAL time)
python3 scripts/zoom_meetings.py create "Topic"                              # instant
python3 scripts/zoom_meetings.py create "Topic" --start "2025-01-15T14:00:00" # scheduled (local time)
python3 scripts/zoom_meetings.py create "Topic" --duration 60 --timezone "Europe/Berlin"
python3 scripts/zoom_meetings.py create "Topic" --agenda "Discussion points" --waiting-room
python3 scripts/zoom_meetings.py create "Topic" --invite "user@example.com"  # send invite
python3 scripts/zoom_meetings.py create "Topic" --invite "a@x.com" --invite "b@x.com"  # multiple

# Update meeting
python3 scripts/zoom_meetings.py update MEETING_ID --topic "New Topic"
python3 scripts/zoom_meetings.py update MEETING_ID --start "2025-01-16T10:00:00"

# Delete meeting (requires meeting:delete:meeting:admin scope)
python3 scripts/zoom_meetings.py delete MEETING_ID
```

### Recordings

```bash
# List all recordings (default: last 30 days)
python3 scripts/zoom_meetings.py recordings

# With date range
python3 scripts/zoom_meetings.py recordings --start 2025-01-01 --end 2025-01-31

# Show download URLs
python3 scripts/zoom_meetings.py recordings --show-downloads

# Get specific meeting's recordings
python3 scripts/zoom_meetings.py recording MEETING_ID

# JSON output
python3 scripts/zoom_meetings.py recordings --json
```

## Output Formats

### Markdown (default)

```markdown
# Zoom Meetings (3 upcoming)

## Weekly Team Sync
**ID:** 123456789
**Start:** 2025-01-15 14:00:00 UTC
**Duration:** 60 minutes
**Join URL:** https://zoom.us/j/123456789
```

### JSON

Add `--json` for structured output suitable for piping to other tools.

## Recording File Types

| Type | Description |
|------|-------------|
| MP4 | Video recording |
| M4A | Audio only |
| TRANSCRIPT | Text transcript (VTT) |
| CHAT | Chat messages |
| TIMELINE | Speaker timeline |
| SUMMARY | AI meeting summary |

## Example User Requests

| User says | Command |
|-----------|---------|
| "List my Zoom meetings" | `list` |
| "Show past meetings" | `list --type previous` |
| "Create a meeting for tomorrow at 2pm" | `create "Meeting" --start "2025-01-15T14:00:00"` |
| "Show my Zoom recordings" | `recordings --start 2025-01-01` |
| "Get the recording for meeting X" | `recording MEETING_ID` |

## Dependencies

```bash
pip install requests
```

## Files

| File | Purpose |
|------|---------|
| `~/.zoom_credentials/credentials.json` | S2S OAuth credentials |
| `~/.zoom_credentials/token.json` | S2S cached token |
| `~/.zoom_credentials/oauth_token.json` | User OAuth tokens (auto-refreshes) |

## API Reference

- [Zoom Meeting APIs](https://developers.zoom.us/docs/api/meetings/)
- [Zoom API Reference](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/)


================================================================================

## 41. Expert Skill: doctorg
> **Path within category:** `doctorg/SKILL.md`


# Doctor G -- Evidence-Based Health Research

Answer health and wellness questions using only trusted, evidence-based sources with explicit evidence strength ratings.

## Usage

```bash
# Quick answer (WebSearch only, ~30s)
/doctorg Is creatine safe for daily use?

# Deep research (WebSearch + Tavily, ~90s)
/doctorg --deep Huberman vs Attia on fasted training

# Full investigation (WebSearch + Tavily + Firecrawl, ~3min)
/doctorg --full What does current evidence say about GLP-1 agonists for non-diabetic weight loss?

# Without personal health context
/doctorg --no-personal Best stretching protocol for lower back pain
```

## Depth Levels

| Level | Flag | Tools | Time | Use When |
|-------|------|-------|------|----------|
| Quick | *(default)* | WebSearch | ~30s | Simple factual questions |
| Deep | `--deep` | WebSearch + Tavily | ~90s | Competing claims, nuanced topics |
| Full | `--full` | WebSearch + Tavily + Firecrawl | ~3min | Controversial topics, need primary sources |

## How It Works

### 1. Parse Query & Detect Topic Category

Classify the question into one of:
- **Nutrition/Supplements** (examine.com gets priority)
- **Exercise/Training** (PubMed + ACSM get priority)
- **Sleep** (focus sleep-specific databases)
- **Disease/Condition** (condition-specific orgs + clinical guidelines)
- **Medication/Treatment** (FDA, EMA, Cochrane get priority)
- **Mental Health** (APA, mental health orgs)
- **General Wellness** (broad search across all tiers)

### 2. Search Evidence Sources (Tiered)

Search sources in priority order. See `references/sources.md` for complete domain list.

**Tier 1 -- Primary Research** (highest weight):
- PubMed/PMC, Cochrane Library, WHO, ClinicalTrials.gov

**Tier 2 -- Clinical/Institutional** (high weight):
- Mayo Clinic, Hopkins Medicine, Cleveland Clinic, Harvard Health
- Condition-specific: AHA, ACS, ADA, Alzheimer's Association

**Tier 3 -- Expert Analysis** (medium weight):
- Examine.com, STAT News, Health News Review
- Consensus.app, Epistemonikos

**Tier 4 -- Quality Journalism** (context/framing):
- The Atlantic, NYT, NPR, Guardian, FiveThirtyEight

#### Search Strategy by Depth

**Quick** (default):
```
WebSearch(query, allowed_domains=[Tier 1 + Tier 2 domains])
WebSearch(query + "systematic review OR meta-analysis", allowed_domains=[Tier 1])
```

**Deep** (--deep):
All Quick searches PLUS:
```
tavily-search(query, include_domains=[Tier 1-3])
WebSearch(query + "expert opinion OR position statement", allowed_domains=[Tier 2-3])
WebSearch(query + "risks OR side effects OR contraindications")
```

**Full** (--full):
All Deep searches PLUS:
```
firecrawl-research for top 2-3 most relevant results from Tier 1
WebSearch for competing/contrarian viewpoints
WebSearch(query + "retracted OR debunked OR misleading")
```

### 3. Pull Personal Health Context (unless --no-personal)

Query Apple Health database for relevant metrics:

```bash
python ~/ai_projects/claude-skills/health-data/scripts/health_query.py --format json vitals
python ~/ai_projects/claude-skills/health-data/scripts/health_query.py --format json daily
python ~/ai_projects/claude-skills/health-data/scripts/health_query.py --format json sleep --days 7
python ~/ai_projects/claude-skills/health-data/scripts/health_query.py --format json workouts --days 30
```

Select ONLY metrics relevant to the query:
- Exercise question -> recent workouts, activity, resting HR, VO2 max
- Sleep question -> sleep data, HRV
- Nutrition question -> weight trends, activity level
- Heart question -> HR, HRV, resting HR, blood pressure

### 4. Synthesize with Evidence Grading

Rate each claim using simplified GRADE scale:

| Rating | Meaning | Based On |
|--------|---------|----------|
| **Strong** | Consistent evidence from systematic reviews/meta-analyses or multiple large RCTs | Level I-II evidence |
| **Moderate** | Supported by well-designed studies but some inconsistency or limitations | Level II-III evidence |
| **Weak** | Limited evidence, small studies, or conflicting results | Level III-IV evidence |
| **Minimal** | Expert opinion, case reports, or preliminary/animal studies only | Level V evidence |
| **Contested** | Active scientific debate with credible evidence on both sides | Mixed levels |

### 5. Format Output

```markdown
# [Topic Title]

**Short answer**: [1-2 sentence direct answer]

## [Expert/Position A] (if comparing viewpoints)
- Key claim 1
- Key claim 2
- Has **evolved stance**: [if applicable]

## [Expert/Position B]
- Key claim 1
- Key claim 2

## Where They Actually Agree (if comparing)
- Agreement point 1
- Agreement point 2

## What Research Shows

| Claim | Evidence Strength |
|-------|------------------|
| Claim 1 | **Strong** |
| Claim 2 | **Weak** (reason) |
| Claim 3 | **Contested** |

## For You Specifically (if --personal context available)

[Personalized interpretation based on user's health data]

[Specific actionable recommendation]

## Sources
- [Source 1 title](url) -- Tier, year
- [Source 2 title](url) -- Tier, year

## Limitations
- [Any caveats about the evidence or this analysis]
```

**Output rules**:
- NEVER give medical diagnoses or replace professional advice
- ALWAYS include disclaimer: "This is research synthesis, not medical advice"
- When evidence is **Weak** or **Minimal**, explicitly say so
- When claims are **Contested**, present both sides fairly
- Prefer recent sources (last 5 years) over older ones
- Flag if key studies have been retracted or challenged
- Include the "For You Specifically" section only when health data adds meaningful context

### 6. Disclaimer (always append)

```

================================================================================

## 42. Expert Skill: gpt-image-2
> **Path within category:** `gpt-image-2/SKILL.md`


# GPT Image 2 — Interactive Image Generation

Generate and edit images via OpenAI's GPT Image 2 API with an interactive, guided workflow.

## Interactive Flow

When the user invokes this skill, guide them through these steps using AskUserQuestion. Do not skip steps — the interactive flow is the core experience.

### Step 1: What are we making?

Ask the user what they want to create. Offer these options:

- **Single image** — one image from a text prompt
- **Photo edit** — transform an existing photo into a style
- **Carousel** — 5-10 cohesive slides for LinkedIn/Instagram
- **Variants** — multiple versions of the same concept
- **Quick generate** — skip questions, just run the prompt

If the user already provided a clear prompt (e.g. "generate an editorial image of a rocket"), skip to Step 3.

### Step 2: Style selection

Show the user available presets grouped by category. Read `presets.yaml` and present them:

**Visual styles** (no text in image):
editorial, blueprint, ink, risograph, wireframe, constellation, brutalist, grain

**Text-heavy** (leverages GPT Image 2 text rendering):
infographic, slide, diagram, poster, menu, manga

**Community favorites:**
trading-card, pixar, app-mockup, isometric, action-figure, cinematic, panorama

**Custom** — user describes their own style

Ask: "Which style? Or describe your own."

### Step 3: Platform & sizing

Ask where this will be used:
- YouTube thumbnail (1280×720)
- Instagram square (1080×1080)
- Slides/presentation (1920×1080)
- Blog hero (1200×630)
- X/Twitter (1600×900)
- Story (1080×1920)
- Custom size
- No resize (use API default)

### Step 4: Draft first, then final

**Always generate a draft first** unless the user says "skip draft" or uses `--draft false`.

1. Generate with `--draft` (quality=low, ~$0.006/image)
2. Show the image to the user using the Read tool
3. Ask: "Like this direction? I can: (a) generate final quality, (b) adjust the prompt, (c) try a different style, (d) regenerate with a new seed"
4. If approved, generate final with `--quality high` (~$0.21/image)
5. Use `--seed` from the draft to maintain composition when upgrading to final

This draft→final flow saves ~97% on iteration costs.

### Step 5: Show result and offer next actions

After generation, always:
1. Show the image using the Read tool
2. Open it with `open <path>` for full-resolution preview
3. Report the cost
4. Offer: "Want to (a) generate variants, (b) edit this further, (c) use as reference for more images, (d) done?"

## Carousel Workflow

When the user wants a carousel (5-10 slides):

### 1. Story arc
Ask: "What's the story? Give me the key message and I'll draft a 10-slide arc."

Then propose a slide-by-slide plan like:
```
Slide 1: [Cover] — hook headline + hero image
Slide 2: [Problem] — bold statement
Slide 3: [Context] — illustration + explanation
...
Slide 10: [CTA] — call to action with URL
```

Ask the user to approve or modify the plan.

### 2. Style consistency
Use the same preset + seed range across all slides. For carousels:
- Pick one visual style for all slides
- Use `--seed` to lock composition patterns
- Include pagination dots in prompts (e.g., "10 small dots at bottom, third dot highlighted orange")
- Maintain consistent color palette and typography

### 3. Draft batch
Generate all slides as drafts first ($0.006 × 10 = $0.06 total). Show them all to the user as a contact sheet or one by one. Ask which ones to regenerate or adjust.

### 4. Final batch
Only generate finals for approved slides. Offer to generate all at once with `-y` flag.

## Photo Edit Workflow

When the user wants to transform a photo:

1. Ask for the source image (file path or clipboard)
2. For clipboard: save with `osascript` to a temp file
3. Show available styles and ask which to try
4. Generate a draft edit first
5. Show result, ask if they want adjustments
6. Generate final when approved

Use `--edit <path>` for the API call.

## Cost Awareness

Always communicate costs before generating:

| Quality | Per image | 10-slide carousel |
|---------|-----------|-------------------|
| `--draft` (low) | $0.006 | $0.06 |
| medium | $0.05 | $0.50 |
| high (default) | $0.21 | $2.10 |
| high + thinking | $0.25-0.42 | $2.50-4.20 |

Thinking mode adds 20-100% cost. Only suggest it for text-heavy or complex compositions.

The script auto-confirms when cost < $0.50. Above that, it prompts the user.

## Prompt Engineering Tips

When helping users write prompts, apply these patterns:

1. **Structure**: Scene → Subject → Detail → Lighting → Constraint
2. **Front-load the subject**: put the main thing first
3. **For text in images**: quote exact text with single quotes: `'with the headline "Hello World"'`
4. **Character consistency**: maintain a 5-tuple: age + appearance + hairstyle + distinctive features + clothing
5. **Style tags at end**: append tags like `editorial-magazine`, `studio-product` to converge batches
6. **Use `--seed` for iteration**: lock composition, vary only the prompt details

## CLI Reference

```bash
# Basic generation
scripts/gpt_image_2.py "prompt" output.png

# With preset and platform
scripts/gpt_image_2.py --preset editorial --platform square "subject" out.png

# Draft mode (~$0.006/image)
scripts/gpt_image_2.py --draft "prompt" out.png

# With thinking for complex layouts
scripts/gpt_image_2.py --thinking medium --preset diagram "OAuth flow" out.png

# Seed for reproducibility
scripts/gpt_image_2.py --seed 42 "prompt" out.png

# Edit existing photo
scripts/gpt_image_2.py --edit photo.png "transform into constellation style" out.png

# Variants with contact sheet
scripts/gpt_image_2.py --n 4 --preset ink "mountain" out.png

# Cost estimate
scripts/gpt_image_2.py --estimate --n 10 --quality high "batch test"

# Skip confirmation
scripts/gpt_image_2.py -y --n 10 "batch" out.png

# Dry run (show prompt without API call)
scripts/gpt_image_2.py --dry-run --preset editorial "test" out.png
```

## Files

- `scripts/gpt_image_2.py` — main CLI (Python, requires PyYAML)
- `presets.yaml` — 21 style presets (visual + text-heavy + community)
- `platforms.yaml` — 8 platform sizing presets
- `references/api_reference.md` — full API documentation
- `~/.config/gpt-image-2/config.yaml` — user defaults
- `~/.config/gpt-image-2/history.jsonl` — generation log
- `~/.config/gpt-image-2/last.json` — last run (for `again`)


================================================================================

## 43. Expert Skill: session-search
> **Path within category:** `session-search/SKILL.md`


# Session Search

Search Claude Code session transcripts by combining keyword pre-filtering with semantic evaluation. Finds previous sessions about specific topics, debugging conversations, research tasks, or any past work.

## Workflow

### Step 1: Run the search script

Execute `scripts/search.py` with the user's query:

```bash
python3 scripts/search.py "<query>" [max_results] [max_age_days]
```

- `query` (required): Natural language search query
- `max_results` (optional, default 10): Maximum results to return
- `max_age_days` (optional, default 90): How far back to search

The script performs keyword pre-filtering across all sessions, then extracts meaningful excerpts from top candidates. Output contains a `SESSIONS_DATA` JSON block.

### Step 2: Evaluate results semantically

After receiving the script output, evaluate each session's relevance to the query. Consider:

- **Synonym matching**: "bug" matches "error", "issue", "problem", "fix"
- **Related concepts**: "debugging" matches sessions with test failures or error messages
- **Tool patterns**: "refactoring" matches Edit-heavy sessions
- **Domain context**: "obsidian" matches vault-related work

Assign a relevance score (0-10) to each session based on excerpt content and query intent.

### Step 3: Present results

Display the top results (up to `max_results`) sorted by relevance, formatted as:

```
### [Relevance: N/10] Project — Date
Summary of what the session was about (1-2 sentences based on excerpts)
`claude --resume <session-id>`
```

If no relevant results are found, report that and suggest alternative queries.

## Session Storage

Sessions are stored as JSONL files in `~/.claude/projects/`. Each file contains events with user/assistant messages and tool calls. The search script handles file discovery and text extraction automatically.

## Customization

To search older sessions or get more results:

```
/session-search "query" 20 180
```
(20 results, 180 days lookback)


================================================================================

## 44. Expert Skill: pdf-generation
> **Path within category:** `pdf-generation/SKILL.md`


# PDF Generation

## Overview

Generate professional PDFs from markdown files using Pandoc with Eisvogel template styling. Supports English and Russian documents with customizable themes, table of contents, and professional typography including EB Garamond font for Russian text.

## Quick Start

Basic commands:

```bash
# Desktop/Print PDF (A4 format)
pandoc doc.md -o doc.pdf --pdf-engine=xelatex --toc --toc-depth=2 -V geometry:margin=2.5cm -V fontsize=11pt -V documentclass=article

# Mobile-friendly PDF (6x9 phone screen optimized)
pandoc doc.md -o doc-mobile.pdf --pdf-engine=xelatex --toc --toc-depth=2 -V geometry:paperwidth=6in -V geometry:paperheight=9in -V geometry:margin=0.5in -V fontsize=10pt -V linestretch=1.2

# Russian PDF with EB Garamond
pandoc doc-ru.md -o doc.pdf --pdf-engine=xelatex --toc --toc-depth=2 -V geometry:margin=2.5cm -V fontsize=11pt -V documentclass=article -V mainfont="EB Garamond"

# Russian Mobile PDF
pandoc doc-ru.md -o doc-mobile.pdf --pdf-engine=xelatex --toc --toc-depth=2 -V geometry:paperwidth=6in -V geometry:paperheight=9in -V geometry:margin=0.5in -V fontsize=10pt -V linestretch=1.2 -V mainfont="EB Garamond"
```

## Document Theme Colors

- **White Papers** - Blue (1e3a8a)
- **Marketing** - Green (059669)
- **Research** - Purple (7c3aed)
- **Technical** - Gray (374151)

## YAML Frontmatter Example

```yaml
```

See references/frontmatter_templates.md for complete templates.


## Markdown Formatting Best Practices

For optimal PDF rendering, ensure:

1. **Blank lines before lists** - Required for proper list rendering
2. **Blank lines after headings** - Improves spacing
3. **Nested list indentation** - Use 3 spaces for sub-items

### Common Claude Code Pattern

Lists after colons need blank lines:

```markdown
Your data spans 9 years with complete tracking:

- Item 1
- Item 2
```

Without blank line after colon, renders as inline text.

### Automatic Fix

Use preprocessing script:

```bash
scripts/fix_markdown.py input.md output.md
```

Automatically detects and fixes:
- Lists after colons (Claude Code format)
- Lists after headings
- Nested list spacing

## Layout Options

### Desktop/Print Layout (A4)
- Paper: 210mm x 297mm (A4)
- Margins: 2.5cm
- Font size: 11pt
- Best for: Printing, reading on large screens, archival

### Mobile Layout (Phone-optimized)
- Paper: 6in x 9in (phone aspect ratio)
- Margins: 0.5in (minimal for screen space)
- Font size: 10pt with 1.2 line spacing
- Best for: Phone/tablet reading, Telegram/messaging apps

**Default for Telegram Bot**: Use mobile layout for all PDFs sent via Telegram unless user explicitly requests print/desktop version.

## Generation Workflows

### Workflow 1: Simple PDF

1. Check context (Telegram = mobile, otherwise desktop)
2. Check if Russian (use EB Garamond if yes)
3. Run appropriate pandoc command
4. Verify output

### Workflow 2: Professional Title Page

1. Add YAML frontmatter with theme color
2. Include metadata (title, author, date)
3. Choose layout (mobile vs desktop)
4. Generate with xelatex

### Workflow 3: Using Script

```bash
scripts/generate_pdf.py doc.md -t white-paper
scripts/generate_pdf.py doc.md -t marketing --russian
scripts/generate_pdf.py doc.md --mobile  # Mobile layout
```

## Resources

- **scripts/generate_pdf.py** - Automated generation
- **references/frontmatter_templates.md** - YAML templates
- **references/pandoc_reference.md** - Command reference

## Troubleshooting

Install pandoc: `brew install pandoc`
Install LaTeX: `brew install --cask mactex`
## Mobile-Friendly PDFs

For phone and tablet reading, use the mobile layout option:

```bash
# Using script (recommended)
scripts/generate_pdf.py doc.md --mobile

# Direct pandoc command
pandoc doc.md -o doc-mobile.pdf \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 \
  -V geometry:paperwidth=6in \
  -V geometry:paperheight=9in \
  -V geometry:margin=0.5in \
  -V fontsize=10pt \
  -V linestretch=1.2 \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue
```

**Mobile layout features**:
- 6x9 inch page size (optimal for mobile screens)
- 10pt font (readable on smaller screens)
- 0.5in margins (maximizes content area)
- 1.2 line spacing (improved readability)
- Auto-generated `-mobile.pdf` filename suffix

**When to use mobile layout**:
- Sharing research via Telegram/messaging apps
- Reading on phones or tablets
- Creating portable reference documents
- Quick consumption on the go

**Default context**: Mobile layout is used by default when generating PDFs through the Telegram bot for optimal mobile reading experience.


================================================================================

## 45. Expert Skill: chrome-history
> **Path within category:** `chrome-history/SKILL.md`


# Chrome History Query Skill

Search and filter your Chrome browsing history using natural language queries.

## What It Does

1. Parses natural language queries to understand date ranges and filters
2. Queries Chrome's SQLite history database
3. Filters out noise (social media, email, redirects)
4. Groups results by type (reading, research, tools, events)
5. Returns formatted markdown with links

## Supported Queries

### Date Range
- "yesterday" → previous day only
- "today" → today only
- "last week" → past 7 days
- "last month" → past 30 days
- "last 2 weeks" → past 14 days

### Content Filters
- "articles I read" → reading cluster (news, blogs, essays)
- "scientific articles" → research cluster (papers, docs)
- "code/research" → GitHub, Stack Overflow, docs

### Keyword Filtering
- "articles about AI" → finds pages mentioning AI
- "scientific articles about climate" → finds research pages mentioning climate

### Site-Specific
- "reddit threads" → reddit.com only
- "on medium" → medium.com only
- "twitter posts" → twitter.com only

## Example Queries

```
"articles I read yesterday"
"articles about AI I read yesterday"
"scientific articles for the last week"
"research about machine learning this week"
"reddit threads last month"
"code repos I visited yesterday"
"on medium this week"
```

## Usage

Run directly with a query:
```bash
python3 ~/.claude/skills/chrome-history/chrome_history_query.py "articles I read yesterday"
```

Or integrate into Claude Code when user asks:
- "Show me articles I read yesterday"
- "What scientific papers did I look at last week?"
- "Show reddit threads I visited last month"
- "Articles about AI from yesterday?"

## Configuration

- **Chrome History**: `~/Library/Application Support/Google/Chrome/Default/History`
- **Vault Location**: `/Users/glebkalinin/Brains/brain`
- **Filtered Sites**: Social media, email, Google redirect wrappers
- **Clustering**: Automatic by domain type (reading, research, tools, events)

## Exclusions

Automatically filters out:
- Social media: Facebook, Instagram, Twitter, TikTok, Reddit, LinkedIn
- Email: Gmail, Outlook
- Shopping: Amazon, eBay
- Google redirects: google.com/url wrappers
- Utility sites: FreeFeed, YouTube

## Output Format

Results grouped by content type with timestamps:

```
## Chrome History: articles about AI yesterday

*Found 5 items*

### Reading (3)
- 14:22 [The more that people use AI...](url)
- 16:38 [AI makes you smarter but...](url)

### Research (2)
- 11:23 [GitHub: AI project](url)
```


================================================================================

## 46. Expert Skill: tdd
> **Path within category:** `tdd/SKILL.md`


# Test-Driven Development — Multi-Agent Orchestration

Enforce disciplined RED-GREEN-REFACTOR cycles using **separate subagents** for test writing and implementation. The core innovation: **the Test Writer never sees implementation code, and the Implementer never sees the specification.** This prevents the LLM from leaking implementation intent into test design.

## When to Use

- User requests TDD, test-first, or red-green-refactor workflow
- User says `/tdd` with a feature description or bug report
- User wants to add a feature with test coverage enforced from the start
- User wants to fix a bug by first writing a reproducing test

## Invocation Modes

| Invocation | Behavior |
|-----------|----------|
| `/tdd <feature>` | Interactive mode — pause for approval at slices and each RED checkpoint |
| `/tdd --auto <feature>` | Autonomous mode — run all slices without pausing; stop ONLY on unrecoverable errors |
| `/tdd --resume` | Resume from `.tdd-state.json` in project root |
| `/tdd --dry-run <feature>` | Validation mode — runs Phase 0 + Phase 1 fully, renders all prompts, but skips `Task()` calls. No code is written. |

In `--auto` mode, skip all `[HUMAN CHECKPOINT]` steps. Print status lines instead:

```
[auto] RED  slice 1/4: "validates email format" — test failing as expected
[auto] GREEN slice 1/4: passing (attempt 1)
[auto] REFACTOR slice 1/4: 1 suggestion applied, 0 skipped
```

Stop and ask the user ONLY when:
- Implementation fails after 5 attempts
- Regressions cannot be auto-fixed after 3 attempts
- A script error makes it impossible to continue (missing binary, permission denied, etc.)

In `--dry-run` mode, validate the entire orchestration pipeline without executing any subagents or writing any code:

1. **Phase 0 runs fully**: detect framework, verify baseline, extract API, discover docs, create state file
2. **Phase 1 runs fully**: decompose into slices (still requires user approval)
3. **For each slice**: render all three agent prompts (Test Writer, Implementer, Refactorer) with actual variables. Print rendered prompts to the user with character counts.
4. **No `Task()` calls are made**. No test files are written. No implementation code is generated.
5. **Validate**: check that all template variables resolve (no `{UNRESOLVED}` placeholders), all scripts execute without error, and the state file is well-formed.
6. **Report summary**:

```
DRY RUN COMPLETE: {feature name}

Phase 0:
  Framework: {framework}
  Language: {language}
  Baseline: {pass|greenfield}
  API surface: {line count} lines
  Doc context: {line count} lines (or "none")

Phase 1:
  Slices: {N} ({layer breakdown})

Prompts rendered: {N * 3} (all variables resolved)
  Test Writer:   {char count} chars
  Implementer:   {char count} chars
  Refactorer:    {char count} chars

State file: .tdd-state.json written
No code was modified.
```

This mode is useful for:
- Validating that scripts work in the project's environment
- Reviewing prompt content before committing to a full TDD run
- Testing skill changes without side effects

## Architecture Overview

```
ORCHESTRATOR (you, reading this file)
├─ Phase 0: Setup — detect framework, extract API, create state file
├─ Phase 1: Decompose into vertical slices → user approves
│
├─ FOR EACH SLICE:
│   ├─ Phase 2 (RED):    Task(Test Writer)  ← spec + API only
│   ├─ Phase 3 (GREEN):  Task(Implementer)  ← failing test + error only
│   └─ Phase 4 (REFACTOR): Task(Refactorer) ← all code + green results
│
└─ Summary
```

### Context Boundaries (the key constraint)

| Agent | Sees | Does NOT See |
|-------|------|-------------|
| **Test Writer** | Slice spec, public API signatures, framework conventions, layer constraints | Implementation code, other slices, implementation plans |
| **Implementer** | Failing test code, test failure output, file tree, existing source, layer constraints | Original spec, slice descriptions, future plans |
| **Refactorer** | All implementation + all tests + green results, layers touched | Original spec, decomposition rationale |

## Workflow

### Phase 0: Setup (once per session)

**Step 1**: Detect framework and test runner.

```
Check for: package.json (jest/vitest), pyproject.toml/pytest.ini (pytest),
go.mod (go test), Cargo.toml (cargo test), Gemfile (rspec), composer.json (phpunit)
```

If ambiguous, ask: "What command runs your tests? (e.g., `npm test`, `pytest`)"

**Step 2**: Detect language from source files (for agent prompts):

```
TypeScript (.ts/.tsx), JavaScript (.js/.jsx), Python (.py), Go (.go), Rust (.rs), Ruby (.rb), PHP (.php)
```

**Step 3**: Verify green baseline.

```bash
bash ~/.claude/skills/tdd/scripts/run_tests.sh {FRAMEWORK} "{TEST_COMMAND}"
```

Parse the JSON output.

- If `status` is `"pass"`: proceed.
- If `status` is `"fail"`: stop — "Existing tests are failing. TDD starts from a green baseline."
- If `status` is `"error"` AND `total` is 0: **greenfield project** — no tests exist yet. This is fine. Proceed.

**Step 4**: Extract the public API surface.

```bash
bash ~/.claude/skills/tdd/scripts/extract_api.sh {SOURCE_DIR}
```

Save the output — this is what the Test Writer will see. If empty (greenfield), that's expected.

**Step 5**: Discover project documentation.

```bash
bash ~/.claude/skills/tdd/scripts/discover_docs.sh {PROJECT_ROOT} --lang {LANGUAGE}
```

This searches for:
- **Documentation files**: README, ARCHITECTURE.md, docs/ folder, DESIGN.md, SPEC files, ADRs
- **API specifications**: OpenAPI/Swagger, GraphQL schemas, .proto files
- **Source docstrings**: JSDoc, Python docstrings, Go doc comments, Rust `///` comments

Save the output as `{DOC_CONTEXT}`. This feeds into:
- **Phase 1** — so slice decomposition is informed by documented behavior and API contracts
- **Phase 2** — so the Test Writer writes tests aligned with documented intent, not just code signatures

If empty (no docs found), that's fine — proceed without doc context.

**Step 6**: Create the state file `.tdd-state.json` in the project root:

```json
{
  "feature": "user's feature description",
  "framework": "jest|vitest|pytest|go|cargo|rspec|phpunit",
  "language": "typescript|javascript|python|go|rust|ruby|php",
  "test_command": "the full test command",
  "source_dir": "src/",
  "doc_context": "output from discover_docs.sh (or empty string)",
  "auto_mode": false,
  "dry_run": false,
  "slices": [],
  "current_slice": 0,
  "phase": "setup",
  "layer_map": {},
  "files_modified": [],
  "test_files_created": []
}
```

Each slice in the `slices` array includes a `layer` field: `"domain"`, `"domain-service"`, `"application"`, or `"infrastructure"`. See Phase 1 for how layers are assigned.

The `layer_map` maps directory prefixes to layers. Built during Phase 1 from project structure:

```json
{
  "layer_map": {
    "src/domain/": "domain",
    "src/services/": "domain-service",
    "src/application/": "application",
    "src/infrastructure/": "infrastructure",
    "src/adapters/": "infrastructure",
    "src/controllers/": "infrastructure"
  }
}
```

If the project has no clear directory-layer mapping (flat structure), set `layer_map` to `{}` and skip path-based validation.

**Step 5a** (auto-detect layer_map): If `layer_map` is empty, scan the source directory for common DDD/layered architecture directory names and auto-populate:

```
Common directory → layer mappings (check if directories exist):
  */domain/       → "domain"
  */models/       → "domain"          (ORM models often serve as domain entities)
  */entities/     → "domain"
  */value_objects/ → "domain"
  */services/     → "application"     (unless clearly infrastructure)
  */application/  → "application"
  */use_cases/    → "application"
  */core/         → "application"
  */infrastructure/ → "infrastructure"
  */adapters/     → "infrastructure"
  */controllers/  → "infrastructure"
  */api/          → "infrastructure"
  */bot/          → "infrastructure"  (Telegram/Discord bot handlers)
  */handlers/     → "infrastructure"
  */repositories/ → "infrastructure"  (concrete repo implementations)
```

Only add entries for directories that actually exist in the source tree. If fewer than 2 directories match, leave `layer_map` empty (flat project). Present the auto-detected map to the user for confirmation:

```
Auto-detected layer map from directory structure:
  src/models/     → domain
  src/services/   → application
  src/core/       → application
  src/bot/        → infrastructure
  src/api/        → infrastructure

Does this mapping look correct? (adjust if needed)
```

**Update state**: `"phase": "setup"`. Write state file immediately.


### Dry-Run Phase Override (Phase 2–4)

In `--dry-run` mode, **replace Phases 2–4 entirely** with the following for each slice:

1. Refresh API surface (`extract_api.sh`)
2. Render the **Test Writer prompt** with all variables filled in. Print it under a `### Test Writer Prompt (slice N)` heading.
3. Render the **Implementer prompt** using placeholder test code: `"(dry-run: test code would be generated by Test Writer)"` for `{FAILING_TEST_CODE}` and `"(dry-run: no test output)"` for `{TEST_FAILURE_OUTPUT}`.
4. Render the **Refactorer prompt** using placeholder values: `"(dry-run: no green output)"` for `{GREEN_TEST_OUTPUT}`, `"(dry-run: code from Test Writer)"` for `{ALL_TEST_CODE}`, `"(dry-run: code from Implementer)"` for `{ALL_IMPLEMENTATION_CODE}`.
5. For each rendered prompt, verify no `{UNRESOLVED_VARIABLE}` patterns remain (regex: `\{[A-Z][A-Z_]+\}`). Report any unresolved variables as errors.
6. Print character counts for each prompt.
7. Move to next slice (no `Task()` calls, no file writes, no test runs).

After all slices are processed, print the dry-run summary and exit. Do NOT clean up the state file — it's useful for subsequent `--resume`.


### Phase 3: GREEN — Minimal Implementation

**Step 1**: Read the failing test file and the test failure output (the full `raw_tail` from the RED phase run_tests.sh result).

**Step 2**: Build the file tree of source files (not test files, not node_modules, etc.):

```bash
find {SOURCE_DIR} -type f \( -name '*.ts' -o -name '*.js' -o -name '*.py' -o -name '*.go' -o -name '*.rs' -o -name '*.rb' -o -name '*.php' \) | grep -v test | grep -v spec | grep -v node_modules | grep -v __pycache__ | grep -v vendor | grep -v target | grep -v dist | grep -v build | head -50
```

**Step 3**: Read existing source files that the test imports or references.

**Step 4**: Read the prompt template from `references/agent_prompts.md` -> "Implementer Agent" section. Fill in:

- `{LANGUAGE}`: Detected language
- `{FAILING_TEST_CODE}`: The complete test file content
- `{TEST_FAILURE_OUTPUT}`: The `raw_tail` from run_tests.sh JSON output
- `{FILE_TREE}`: Source file listing from Step 2
- `{EXISTING_SOURCE}`: Content of relevant source files (if any — may be empty for greenfield)
- `{LAYER}`: The slice's layer tag from Phase 1
- `{LAYER_DEPENDENCY_CONSTRAINT}`: Layer-specific dependency constraint (see agent_prompts.md -> Layer-Specific Constraint Lookup)

On retries (attempt > 1), also fill in the `{?PREVIOUS_ATTEMPT}` section:
- `{PREVIOUS_ATTEMPT_DESCRIPTION}`: the `explanation` field from the failed attempt
- `{PREVIOUS_ATTEMPT_ERROR}`: the `raw_tail` from the test run after the failed attempt

**CRITICAL**: Do NOT include the slice specification, feature description, or any future plans. The Implementer works from the test alone.

**Step 5**: Launch the Implementer agent:

```
Task(subagent_type="general-purpose", prompt=<constructed prompt>)
```

**Step 6**: Parse the JSON response. **Validate layer boundaries**, then apply file changes.

**Step 6a** (Layer path validation): If `layer_map` is not empty, check each file path in the response against the current slice's layer:

```
For each file in response.files:
  inferred_layer = lookup file.path against layer_map (longest prefix match)
  if inferred_layer exists AND inferred_layer != current_slice.layer:
    if inferred_layer is OUTER relative to current_slice.layer:
      REJECT: "Implementer created/modified {file.path} which belongs to
      the {inferred_layer} layer, but this is a {current_slice.layer} slice.
      Inner layers must not depend on outer layers."
      → Re-launch Implementer with appended constraint:
        "Do NOT create or modify files in {inferred_layer} directories.
        This slice is {current_slice.layer} only."
    if inferred_layer is INNER relative to current_slice.layer:
      ALLOW: outer layers may touch inner-layer files (e.g., adding a port interface)
```

Layer ordering for "outer" check: domain < domain-service < application < infrastructure.

If `layer_map` is empty (flat project), skip this validation.

**Step 6b**: Apply validated file changes:

For each file in the response `files` array:
- If `action` is `"create"` or `"overwrite"`: Use the Write tool to create or overwrite the file with the complete content
- If `action` is `"edit"` (used for existing files over 200 lines): Use the Edit tool with `old_string` → `new_string` to apply the changes. The Implementer returns only the changed functions with surrounding context — identify the insertion point or the function being replaced, and use Edit tool accordingly. If the edit target is ambiguous, fall back to reading the full file and using Write.
- For existing files over 200 lines where the Implementer returned full content anyway (action = "overwrite"), prefer using Edit tool to apply only the diff — this prevents accidental reformatting of untouched code

**Step 7**: Run the specific test:

```bash
bash ~/.claude/skills/tdd/scripts/run_tests.sh {FRAMEWORK} "{TEST_COMMAND_FOR_SPECIFIC_TEST}"
```

**Step 8**: RETRY LOOP (if test still fails):

```
attempt = 1
max_attempts = 5
previous_explanation = null
previous_error = null

while status != "pass" AND attempt <= max_attempts:
    previous_explanation = explanation from last Implementer response
    previous_error = raw_tail from last test run

    Launch FRESH Task(Implementer) with:
      - same test code + file tree + existing source (re-read!)
      - NEW failure output
      - PREVIOUS_ATTEMPT section filled in

    Apply changes (Write tool for each file)
    Re-run test
    attempt += 1

if still failing after max_attempts:
    STOP. Present to user:
    "Implementation failed after 5 attempts. Last error: {raw_tail}"
    Ask: "Adjust the test, try a different approach, or debug manually?"
```

Each retry is a **fresh** Task call with only the previous attempt's explanation and error. This prevents the Implementer from going down rabbit holes while giving it enough context to try a different strategy.

**Step 9**: Once the specific test passes, run the FULL test suite:

```bash
bash ~/.claude/skills/tdd/scripts/run_tests.sh {FRAMEWORK} "{FULL_TEST_COMMAND}" --all
```

**Step 10**: Handle regressions:

| Result | Action |
|--------|--------|
| All pass | Proceed to REFACTOR |
| Regressions found | Auto-fix: launch a fresh Implementer with the regression test failures. Apply. Re-run full suite. Repeat up to 3 times. If still failing after 3 regression-fix attempts, STOP and present to user. |

**Step 11** (interactive mode only — skip in `--auto`): Present to the user:

```
GREEN: Test passing with minimal implementation.

Implementation: {explanation from agent response}
Files changed: {list}
All tests: {passed} passing, {failed} failing

Proceed to REFACTOR phase? (or adjust?)
```

**Update state**: `"phase": "green"`, update `files_modified`. Write state immediately.

**Step 12** (domain/domain-service slices only): Layer purity check before REFACTOR:

For each new/modified file in a `domain` or `domain-service` layer slice:
- **Import scan**: Read all import/require statements. Check each imported module against `layer_map`. Flag any import from an outer layer as a violation.
- **Constructor check**: Verify constructor takes NO parameters typed from outer layers (no ORM sessions, HTTP clients, framework configs)
- **Static call check**: No static method calls to outer-layer code
- If violations found, fix them now (move the dependency to a port interface) before entering REFACTOR

**Step 13**: Full-repo import scan (all layers, runs once per slice):

Scan ALL source files (not just session-modified) for dependency direction violations:

```bash
# For each source file, extract imports and check against layer_map
# Language-specific patterns:
#   Python: from X import Y, import X
#   TypeScript/JS: import ... from 'X', require('X')
#   Go: import "X"
```

For each file:
1. Determine its layer from `layer_map` (skip if no match)
2. For each import, determine the imported module's layer from `layer_map`
3. If imported layer is OUTER relative to file's layer → violation

Report violations to the user before REFACTOR:

```
Layer scan found N dependency direction violation(s):
- domain/user.py imports infrastructure/db.py (domain → infrastructure)
- domain/services/registration.py imports adapters/email.py (domain-service → infrastructure)
```

In `--auto` mode: attempt auto-fix (replace concrete import with port interface). In interactive mode: present violations and ask user how to proceed.

This supplements the Refactorer's import checking (which only sees session files) with a repo-wide scan. Static tools miss ~23% of violations (Pruijt et al., 2017) — combining textual + structural checks improves coverage.


### Phase 5: Next Slice or Complete

If more slices remain -> increment `current_slice` in state, return to Phase 2.

If all slices complete -> present summary:

```
TDD Complete: {feature name}

Slices implemented: N
Tests written: N
Files created/modified: {list}
All tests passing: yes
```

Clean up: remove `.tdd-state.json` (in `--auto` mode, remove silently; in interactive, ask user).


## Edge Cases

### Greenfield Projects

No source files, no tests, no test configuration. Handle gracefully:

1. **Phase 0 Step 3**: If run_tests.sh returns `status: "error"` with `total: 0`, check if any test files exist. If none, this is greenfield — proceed.
2. **Phase 0 Step 4**: extract_api.sh will return empty output. Pass `"(No existing API — this is a new project)"` to the Test Writer.
3. **Phase 2**: The Test Writer will create test files from scratch. May need to set up the test framework config (e.g., `jest.config.js`, `pytest.ini`). If the first test run fails with a framework error (not a test failure), create minimal framework config and retry.

### Bug Fix TDD

1. Write a test demonstrating the bug (should FAIL showing the bug exists)
2. Confirm failure matches the reported bug — human checkpoint
3. Fix: minimal code to make test pass (GREEN phase as normal)
4. Verify: no regressions

### Existing Code (Characterization Tests)

1. Write a test for CURRENT behavior (should PASS — this is a characterization test)
2. Modify the test for DESIRED behavior (should FAIL)
3. Proceed with GREEN -> REFACTOR

### User-Provided Tests

If user provides test code:
1. Run to confirm it fails (RED confirmed)
2. Skip to Phase 3 (GREEN) — user-provided tests are authoritative
3. Do not modify without asking

### Flaky Tests

If a test sometimes passes/fails: stop, report, fix the flaky test before continuing.


## Layer Reference

See `references/layer_guide.md` for layer definitions, dependency rules, test strategies by layer, and detection heuristics.

## Anti-Patterns to Avoid

See `references/anti_patterns.md`. Critical ones:
- Never modify a test to make it pass (change implementation, not tests)
- Never write implementation before tests
- Never write all tests at once (vertical slicing)
- Never test implementation details
- Never skip the RED phase
- Never let domain code import infrastructure (dependency direction violation)
- Never mock domain objects — construct real instances instead


================================================================================

## 47. Expert Skill: session-finder
> **Path within category:** `session-finder/SKILL.md`


# Session Finder

Semantic search across Claude Code sessions using Gemini embeddings.

## Commands

### Index sessions
```bash
python3 ~/.claude/skills/session-finder/scripts/session_finder.py index [--max-age-days 90]
```

### Search
```bash
python3 ~/.claude/skills/session-finder/scripts/session_finder.py search "query" [--top 5]
```

### Open best match directly
```bash
python3 ~/.claude/skills/session-finder/scripts/session_finder.py open "query"
```

### Stats
```bash
python3 ~/.claude/skills/session-finder/scripts/session_finder.py stats
```

## How it works

1. **Document extraction** — deterministic, no LLM. Each session JSONL is parsed into a structured document:
   - `away_summary` events (pre-existing Claude recaps) if available
   - First user message (task description)
   - Follow-up user messages (condensed)
   - First assistant response
   - Tools used
   - Project name
2. **Embedding** — documents are embedded with `gemini-embedding-exp-03-07` via `llm` CLI
3. **Storage** — SQLite at `~/.claude/session-finder.db`
4. **Search** — query is embedded, cosine similarity ranks all sessions, top match is the default to open

## Workflow

When user asks to find a session:
1. Run `search` with their query
2. Present results with confidence scores
3. Offer to resume the top match via `claude --resume <id>`


================================================================================

## 48. Expert Skill: sketch
> **Path within category:** `sketch/SKILL.md`

# Sketch - Collaborative SVG Canvas

## Description
Opens a Fabric.js-based SVG editor in the browser for collaborative visual prototyping. Claude can write and read SVG through MCP tools while the user edits interactively. Changes sync in real-time via WebSocket.

## Tools Available (via sketch-mcp-server)
- `sketch_open_canvas` - Open a named canvas (creates if new), launches browser editor
- `sketch_get_svg` - Read current SVG from a canvas
- `sketch_set_svg` - Replace entire canvas with new SVG
- `sketch_add_element` - Add SVG elements without clearing existing content
- `sketch_add_textbox` - Add a fixed-width text area (Textbox) with word wrapping
- `sketch_lock_objects` - Lock all current objects (non-selectable, non-movable)
- `sketch_unlock_objects` - Unlock all objects
- `sketch_save_template` - Save canvas as reusable JSON template (preserves Textbox widths + lock state)
- `sketch_load_template` - Load a saved JSON template into a canvas
- `sketch_list_templates` - List all saved templates
- `sketch_clear_canvas` - Clear canvas to blank state (use before streaming)
- `sketch_focus_canvas` - Bring canvas window to foreground
- `sketch_list_canvases` - List all active canvases
- `sketch_close_canvas` - Close a canvas and its browser tab

## Usage Patterns

### Quick sketch
1. `sketch_open_canvas` with a name
2. `sketch_set_svg` or `sketch_add_element` to draw
3. User edits in browser
4. `sketch_get_svg` to see changes

### Streaming (real-time build-up)
1. `sketch_open_canvas` with a name
2. `sketch_focus_canvas` to bring window to front
3. `sketch_clear_canvas` to start fresh
4. Call `sketch_add_element` multiple times -- each fragment appears instantly
5. User watches the UI build up in real-time

### Multiple canvases
Each canvas opens in its own browser tab. Use different names for different drawings.

### SVG tips
- Use standard SVG elements: `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<path>`, `<text>`, `<polygon>`, `<polyline>`
- Include `xmlns="http://www.w3.org/2000/svg"` on the root `<svg>` element
- Set `width` and `height` on the root SVG (default: 1200x800)
- Colors: use hex colors (`#ff0000`) -- avoid `rgba()` as Fabric.js SVG parser may not handle it
- Text: `<text x="100" y="100" font-size="24">Hello</text>`
- Images: `<image href="data:image/png;base64,..." width="200" height="200"/>`
- Avoid `<defs>`, `<linearGradient>`, `<filter>` -- Fabric.js has limited support for these


================================================================================

## 49. Expert Skill: timebuzzer-led
> **Path within category:** `timebuzzer-led/SKILL.md`


# timeBuzzer LED

Control the timeBuzzer hardware LED over MIDI. The device has 3 RGB segments controllable independently or together.

## Requirements

- timeBuzzer device connected via USB-C
- `python-rtmidi` installed (`pip install python-rtmidi`)
- timeBuzzer app may be running (MIDI port is shared)

## Script

Single CLI: `scripts/buzzer_led.py`

### Color commands

```bash
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py color red
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py color --hex "#FF8800"
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py rgb 255 100 0
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py off
```

Named colors: red, orange, yellow, green, cyan, blue, purple, magenta, pink, white, warm, off.

### Effects

```bash
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py pulse blue --bpm 30 --seconds 5
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py strobe red --count 5 --interval 0.15
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py rainbow --seconds 5
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py fade warm --seconds 2
```

### Status signals (parallel to `hue` skill)

```bash
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py signal success
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py signal thinking --seconds 5
```

| signal | color | effect |
|---|---|---|
| success/done | green | solid |
| error | red | strobe |
| warning | orange | pulse |
| thinking | blue | pulse |
| working | cyan | pulse |
| idle | warm | solid |
| attention | magenta | strobe |
| focus | purple | solid |

### Per-segment control

```bash
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py segment 0 255 0 0   # seg 0 red
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py segment 1 0 255 0   # seg 1 green
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py segment 2 0 0 255   # seg 2 blue
```

## Protocol details

- USB MIDI device (vendor 0x16D0, product 0x1170)
- Sends/receives MIDI CC on channel 12 (status byte 187/0xBB)
- LED output: CC 70-78 for 3 segments x 3 channels (R, G, B)
- Values: 0-127 (half of standard 0-255 RGB)
- The timeBuzzer app controls LED based on active project color; this script overrides it directly

## Syncing with Hue

Use the same signal vocabulary as the `hue` skill. Example combined command:

```bash
python3 ~/.claude/skills/timebuzzer-led/scripts/buzzer_led.py signal success &
python3 ~/.claude/skills/hue/scripts/hue.py signal success --group 1
```


================================================================================

## 50. Expert Skill: gmail
> **Path within category:** `gmail/SKILL.md`


# Gmail Search Skill

Search and fetch emails via Gmail API with flexible query options and output formats.

## Prerequisites

Credentials must be configured in `~/.gmail_credentials/`. Run `setup` to check status:

```bash
python3 scripts/gmail_search.py setup
```

### Obtaining Gmail API Credentials

#### 1. Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click project dropdown -> "New Project"
3. Name it (e.g., "Gmail Agent Skill") -> Create

#### 2. Enable Gmail API

1. Navigate to "APIs & Services" -> "Library"
2. Search for "Gmail API"
3. Click it and press "Enable"

#### 3. Configure OAuth Consent Screen

1. Go to "OAuth consent screen" (left sidebar)
2. Choose "External" user type
3. Fill in required fields:
   - App name: Gmail Agent Skill
   - User support email: your email
   - Developer email: your email
4. Click "Save and Continue", skip Scopes
5. On "Test users" page, add your Gmail address
6. Complete all steps

#### 4. Publish the Test App

**Important:** Without this step, you'll get "Error 403: access_denied".

1. Go back to "OAuth consent screen"
2. Under "Publishing status", click "Publish App"
3. Confirm the dialog

This keeps the app in test mode (not production) but allows your test users to authenticate. You'll see an "unverified app" warning during login - click "Advanced" -> "Go to Gmail Agent Skill (unsafe)" to proceed.

**Note:** Test tokens expire after 7 days. Production requires Google verification.

#### 5. Create OAuth Credentials

1. Go to "Credentials" (left sidebar)
2. Click "Create Credentials" -> "OAuth client ID"
3. Select "Desktop app" as application type
4. Name it (e.g., "Gmail Agent Client")
5. Click "Create"

#### 6. Get Your Credentials

1. Client ID will be displayed - copy it
2. Client Secret: Click the download icon or view details to get the secret

#### 7. Save Credentials

Create `~/.gmail_credentials/credentials.json`:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["http://localhost"]
  }
}
```

#### 8. Authenticate

```bash
python3 scripts/gmail_search.py auth
```

This opens a browser. Click through the "unverified app" warning ("Advanced" -> "Go to Gmail Agent Skill"), approve access, and you're ready.

## Quick Start

```bash
# Check setup status
python3 scripts/gmail_search.py setup

# Authenticate (opens browser)
python3 scripts/gmail_search.py auth

# Search emails
python3 scripts/gmail_search.py search "meeting notes"

# Search with filters
python3 scripts/gmail_search.py search --from "boss@company.com" --unread
```

## Commands

### Setup

Check configuration status:

```bash
python3 scripts/gmail_search.py setup
python3 scripts/gmail_search.py setup --json
```

### Authenticate

Authenticate with Gmail (opens browser for OAuth):

```bash
python3 scripts/gmail_search.py auth
```

### Scope

View or change API permission scope:

```bash
# View current scope
python3 scripts/gmail_search.py scope

# Change scope (requires re-auth)
python3 scripts/gmail_search.py scope --set readonly
python3 scripts/gmail_search.py scope --set modify
python3 scripts/gmail_search.py scope --set full
```

**Available scopes:**
- `readonly` - Read emails only (default, recommended)
- `modify` - Read + modify labels, mark read/unread
- `full` - Full access including delete

### Search

Search emails with free-text query or filters:

```bash
# Free-text search (uses Gmail search syntax)
python3 scripts/gmail_search.py search "project deadline"
python3 scripts/gmail_search.py search "from:john@example.com subject:invoice"

# Using helper flags
python3 scripts/gmail_search.py search --from "john@example.com"
python3 scripts/gmail_search.py search --to "me@example.com"
python3 scripts/gmail_search.py search --subject "Weekly Report"
python3 scripts/gmail_search.py search --label "INBOX"
python3 scripts/gmail_search.py search --label "work"

# Date filters (YYYY/MM/DD format)
python3 scripts/gmail_search.py search --after 2024/01/01
python3 scripts/gmail_search.py search --before 2024/12/31
python3 scripts/gmail_search.py search --after 2024/01/01 --before 2024/06/30

# Status filters
python3 scripts/gmail_search.py search --unread
python3 scripts/gmail_search.py search --starred
python3 scripts/gmail_search.py search --has-attachment

# Combined filters
python3 scripts/gmail_search.py search "invoice" --from "billing@" --has-attachment --after 2024/01/01

# Limit results
python3 scripts/gmail_search.py search "meeting" --limit 50

# Include full body (default shows snippet only)
python3 scripts/gmail_search.py search "contract" --full

# Include attachment info
python3 scripts/gmail_search.py search --has-attachment --attachments

# JSON output
python3 scripts/gmail_search.py search "project" --json
```

### Download Attachments

Download attachments from a specific message:

```bash
# Download to default location (~/Downloads/gmail_attachments/)
python3 scripts/gmail_search.py download MESSAGE_ID

# Download to custom directory
python3 scripts/gmail_search.py download MESSAGE_ID --output /path/to/folder

# JSON output
python3 scripts/gmail_search.py download MESSAGE_ID --json
```

Get message ID from search results (shown in output).

### Labels

List all available Gmail labels:

```bash
python3 scripts/gmail_search.py labels
python3 scripts/gmail_search.py labels --json
```

## Output Formats

### Markdown (default)

```markdown
# Gmail Search Results (3 messages)

## Weekly Report
**From:** boss@company.com
**To:** me@example.com
**Date:** Mon, 25 Nov 2024 10:00:00 +0000
**ID:** `18abc123def`

> Here's the weekly report summary...


================================================================================

## 51. Expert Skill: meeting-processor
> **Path within category:** `meeting-processor/SKILL.md`


# Meeting Processor

Intelligent meeting transcript processor that auto-detects meeting type and applies type-specific extraction with optional interactive clarification.

## When to Use

- After syncing Fathom or Granola transcripts (`/fathom --today`, `/granola export`)
- When asked to process, analyze, or summarize a meeting transcript
- When a new meeting transcript appears in the vault root matching `YYYYMMDD-*.md`
- For coaching sessions, delegate to `coaching-session-summarizer` skill instead

## Prerequisites

```bash
pip install openai pyyaml
```

Requires `CEREBRAS_API_KEY` environment variable (uses Cerebras API with llama-3.3-70b).

## Supported Meeting Types

| Type | Description | Key Extractions |
|------|-------------|-----------------|
| **leadgen** | Sales/business development calls | Commitments, pain points, budget, timeline, decision makers, deal stage, sentiment |
| **partnership** | Collaboration/partnership exploration | Opportunity overview, value proposition, strategic alignment, technical needs, fit assessment |
| **coaching** | Coaching/mentoring sessions | Insights, decisions, action items, themes, emotional arc, techniques, session quality |
| **internal** | Internal team meetings | Coming soon |

## Usage

### Interactive Mode (default)

Run the processor, which auto-detects meeting type and asks clarifying questions:

```bash
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --mode interactive
```

**Interactive flow:**
1. Script analyzes transcript and detects meeting type
2. Extracts structured data via LLM
3. Identifies missing/ambiguous fields
4. Returns questions as JSON (exit code 2 signals interaction needed)
5. Parse the JSON between `__INTERACTIVE_QUESTIONS__` markers
6. Use AskUserQuestion to collect answers for each question
7. Save answers to a temp JSON file and re-run with `process_with_answers.py`

**Handling interactive questions:**

When the script exits with code 2, parse the output for questions JSON. Each question has:
- `question`: The question text
- `header`: Short label (used as answer key)
- `options`: Array of `{label, description}` for AskUserQuestion

After collecting answers, create two temp files:
- `questions.json` — the original questions context (includes `partial_data`, `meeting_type`, `transcript_file`)
- `answers.json` — map of `{header_lowercase: selected_label}`

Then run:
```bash
python3 ~/.claude/skills/meeting-processor/scripts/process_with_answers.py questions.json answers.json
```

### Batch Mode

Extract only high-confidence information without user interaction:

```bash
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --mode batch
```

### Force Meeting Type

Skip auto-detection:

```bash
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --type leadgen
python3 ~/.claude/skills/meeting-processor/scripts/process.py <transcript-file> --type partnership
```

## Output

Analysis is appended to the transcript file as a `## Meeting Analysis` section. Frontmatter is updated with `meeting_type`, `processed_date`, and `processing_mode`.

### Leadgen Output Structure

- **Commitments & Actions** — with deadlines and owners
- **Follow-up** — next meeting date if scheduled
- **Client Context** — pain points, budget, timeline, decision makers
- **Deal Assessment** — stage (cold/warm/hot), probability (1-5), blocker, sentiment

### Partnership Output Structure

- **Opportunity** — description and value proposition for both sides
- **Commitments & Actions** — with deadlines and owners
- **Follow-up** — next meeting date if scheduled
- **Partnership Context** — strategic alignment, technical needs, resources, challenges
- **Opportunity Assessment** — fit (strong/medium/weak), readiness, success factors, sentiment


================================================================================

## 52. Expert Skill: youtube-transcript
> **Path within category:** `youtube-transcript/SKILL.md`


# YouTube Transcript

## Overview

Extract YouTube video transcripts, metadata, and chapters using yt-dlp. Output formatted as Markdown with YAML frontmatter, saved to ~/Brains/brain/ (Obsidian vault).

## Quick Start

To extract a transcript from a YouTube video:

```bash
python scripts/extract_transcript.py <youtube_url>
```

Optional: Specify custom output filename:

```bash
python scripts/extract_transcript.py <youtube_url> custom_filename.md
```

## Output Format

### YAML Frontmatter

The generated Markdown includes comprehensive metadata:

- `title` - Video title
- `channel` - Channel name
- `url` - YouTube URL
- `upload_date` - Upload date (YYYY-MM-DD)
- `duration` - Video duration (HH:MM:SS)
- `description` - Video description (truncated to 500 chars)
- `tags` - Array of video tags
- `view_count` - View count
- `like_count` - Like count

### Body Structure

Transcript organized by video chapters (if available):

```markdown
## Chapter Title

**00:05:23** Transcript text for this segment.

**00:05:45** Next segment text.
```

If no chapters exist, all content appears under "## Transcript" heading.

Timestamps formatted as HH:MM:SS for consistency.

## Workflow

1. Extract metadata and subtitles using yt-dlp
2. Parse VTT subtitle format to extract timestamps and text
3. Group transcript segments by video chapters (if present)
4. Format as Markdown with YAML frontmatter
5. Save to ~/Brains/brain/ with sanitized filename based on video title
6. Clean up temporary subtitle files

## Deduplication

To remove duplicates from existing transcript files:

```bash
python scripts/deduplicate_transcript.py <markdown_file>
```

This removes transcript entries that are prefixes of subsequent entries (common in VTT files where subtitles accumulate).

## Requirements

Ensure yt-dlp is installed:

```bash
pip install yt-dlp
```

## Limitations

- Extracts subtitles in English first, falls back to Russian if English unavailable
- Requires video to have subtitles (auto-generated or manual)
- Does not download video or audio files
- Description truncated to 500 characters in frontmatter


================================================================================

## 53. Expert Skill: transcript-analyzer
> **Path within category:** `transcript-analyzer/SKILL.md`


# Transcript Analyzer

## Overview

Analyze meeting transcripts using AI to automatically extract and categorize:
- **Decisions** - Explicit agreements or choices made
- **Action Items** - Tasks assigned to people
- **Opinions** - Viewpoints expressed but not agreed upon
- **Questions** - Unresolved questions raised
- **Terms** - Domain-specific terminology for glossary

## Prerequisites

Before first use, install dependencies:

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm install
```

## Usage

To analyze a transcript:

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- <transcript-file> -o <output.md> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `<file>` | Transcript file to analyze (first positional arg) |
| `-o, --output <path>` | Write markdown to file instead of stdout |
| `--include-transcript` | Include full transcript in output [default: off] |
| `--no-extractions` | Exclude extractions section |
| `--no-glossary` | Exclude glossary section |
| `--glossary <path>` | Custom glossary JSON path |
| `--skip-glossary` | Don't preload glossary terms |
| `--max-terms <num>` | Limit glossary suggestions |
| `--chunk-size <num>` | Override chunk size (default: 3000) |

## Examples

### Basic Analysis

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /path/to/meeting.md -o /path/to/analysis.md
```

### Include Original Transcript

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /path/to/meeting.md -o /path/to/analysis.md --include-transcript
```

### Extractions Only (No Glossary)

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /path/to/meeting.md -o /path/to/analysis.md --no-glossary
```

### Analyze Specific Section

To analyze only part of a transcript, extract the section first:

```bash
sed -n '50,100p' /path/to/meeting.md > /tmp/section.md
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /tmp/section.md -o /path/to/section-analysis.md
```

## Output Format

The tool generates markdown with:

1. **YAML Frontmatter** - Processing metadata:
   - chunks processed
   - extractions count by type
   - new terms discovered
   - model used (llama-3.3-70b via Cerebras)
   - token usage (input/output/total)

2. **Extractions** - Categorized findings with confidence scores:
   - Each extraction includes speaker (if identified), source snippet, and related terms

3. **Glossary** - Approved terms from existing glossary + suggested new terms with definitions

## Configuration

The skill uses Cerebras API with the key stored in `scripts/.env`:

```
CEREBRAS_API_KEY=<your-key>
```

## Scripts

- `scripts/cli.ts` - Main CLI entry point
- `scripts/src/lib/extract-service.ts` - AI processing logic using Cerebras
- `scripts/src/lib/markdown.ts` - Markdown output generation
- `scripts/src/lib/term-utils.ts` - Term deduplication utilities
- `scripts/src/lib/mockExtractor.ts` - Mock mode for testing
- `scripts/src/types/index.ts` - TypeScript type definitions
- `scripts/data/glossary.json` - Default glossary storage


================================================================================

## 54. Expert Skill: nano-banana
> **Path within category:** `nano-banana/SKILL.md`


# Nano Banana - Gemini Image Generation

Generate and edit images from text prompts via Google's Gemini image generation API.

## When to Use

- User requests image generation, creation, or production from a text description
- Editing existing images with text instructions
- Style-transfer: generate new images that match the aesthetic of a reference
- Creating illustrations for presentations, articles, thumbnails, social posts
- Batch variations of the same concept

## First-Time Setup

```bash
scripts/nano_banana.py init
```

Wizard checks dependencies (sops, age, magick), verifies the API key, and saves defaults to `~/.config/nano-banana/config.yaml`.

## Quick Start

```bash
# Simple generation
scripts/nano_banana.py "a minimalist illustration of a rocket" ./rocket.png

# With style preset
scripts/nano_banana.py --preset editorial "interconnected nodes" ./nodes.png

# YouTube thumbnail (auto-cropped to 1280x720)
scripts/nano_banana.py --preset grain --platform youtube "coffee on desk" ./thumb.png

# Generate 4 variants + contact sheet
scripts/nano_banana.py --preset wireframe "a crystal" ./crystal.png --n 4

# Edit existing image
scripts/nano_banana.py --edit ./old.png "make the background deep teal" ./new.png

# Style reference (match aesthetic of existing image)
scripts/nano_banana.py --reference ./style.png "a new mountain landscape" ./mountain.png

# Re-roll last prompt
scripts/nano_banana.py again

# View history
scripts/nano_banana.py history -n 10
```

## Requirements

- `GEMINI_API_KEY` — auto-decrypted from `secrets.enc.yaml` via SOPS + age. Fallback: `export GEMINI_API_KEY=...`
- `sops`, `age` — for key decryption
- `magick` (ImageMagick) — for platform fit + contact sheets
- `python3` with `pyyaml`

## Models

| Model | Alias | Nano Banana Name | Use When |
|-------|-------|-----------------|----------|
| `gemini-3.1-flash-image-preview` (default) | `flash` | **Nano Banana 2** | Best instruction following, fast |
| `gemini-3-pro-image-preview` | `pro` | **Nano Banana Pro** | Highest quality, text in images |
| `gemini-2.5-flash-image` | `flash-2.5` | **Nano Banana** (original) | Legacy |

Use via `--model flash|pro|flash-2.5` or full ID.

## Style Presets

```bash
scripts/nano_banana.py list-presets
scripts/nano_banana.py --preset editorial "your subject" out.png
```

| Preset | Style |
|--------|-------|
| `editorial` | Thin lines on black, muted palette, technical diagram feel |
| `blueprint` | White/cyan lines on dark navy, engineering drawing |
| `ink` | Japanese sumi-e ink wash, organic brushstrokes, monochrome |
| `risograph` | Flat colors, grain, terracotta + sage, zine aesthetic |
| `wireframe` | 3D wireframe mesh, glowing edges on black |
| `constellation` | Star map dots connected by faint lines, celestial |
| `brutalist` | Bold shapes, thick borders, hard shadows, flat colors |
| `grain` | Film grain photo, high ISO, warm cinematic tones |

Defined in `presets.yaml` — edit to add your own.

## Platform Presets

```bash
scripts/nano_banana.py list-platforms
scripts/nano_banana.py --platform youtube "your subject" out.png
```

Generated image is automatically resized + center-cropped to target dimensions.

| Platform | Size |
|----------|------|
| `youtube` | 1280×720 |
| `youtube-short` | 1080×1920 |
| `slides` | 1920×1080 |
| `blog` | 1200×630 |
| `x` | 1600×900 |
| `square` | 1080×1080 |
| `story` | 1080×1920 |
| `pinterest` | 1000×1500 |

## Features

### Variants + Contact Sheet
`--n N` generates N variants in parallel and assembles them into a contact sheet:
```bash
scripts/nano_banana.py --preset ink "mountain" ./mt.png --n 6
# Creates mt-01.png ... mt-06.png + mt-contact.png
```

### Edit Mode
Pass an existing image and the prompt becomes the edit instruction:
```bash
scripts/nano_banana.py --edit ./thumb.png "remove the watermark, warmer colors" ./clean.png
```

### Reference Images (Style Anchor)
Use one or more reference images to guide the aesthetic without editing them:
```bash
scripts/nano_banana.py --reference ./episode1.png --reference ./episode2.png \
  "episode 3: data drift" ./ep3.png
```

### Projects + Metadata
Organize outputs by project:
```bash
scripts/nano_banana.py --project lab-04/meeting-02 --preset editorial "MCP loops" ./overlay.png
# Saves to ~/nano-banana/outputs/lab-04/meeting-02/20260414-<subject>.png + .json sidecar
```

### Re-roll + History
```bash
scripts/nano_banana.py again              # rerun last prompt
scripts/nano_banana.py history -n 20      # show last 20 generations
scripts/nano_banana.py history --project lab-04
```

### Dry Run
Preview the composed prompt without calling the API:
```bash
scripts/nano_banana.py --preset editorial --platform youtube "subject" --dry-run
```

## Transient Errors & Retry

The API occasionally returns `500/INTERNAL` or empty candidates. The script retries up to 4 times with exponential backoff (2s, 4s, 8s, 16s). Permanent errors (4xx, safety violations) fail fast without retry.

## Prompt Tips

- Specify visual style: "photograph", "flat illustration", "watercolor", "3D render"
- Include composition: "centered", "white background", "wide shot"
- Name colors: "blue and white color scheme", "warm earth tones"
- For text rendering, use `--model pro` and quote exact text: `'with the text "Hello"'`

See `references/api_reference.md` for full API documentation.

## Files

- `scripts/nano_banana.py` — main CLI (Python)
- `scripts/generate_image.sh` — thin bash wrapper (back-compat)
- `presets.yaml` — style presets
- `platforms.yaml` — platform sizing presets
- `secrets.enc.yaml` — encrypted API key (SOPS + age)
- `~/.config/nano-banana/config.yaml` — user defaults (from `init`)
- `~/.config/nano-banana/history.jsonl` — generation log
- `~/.config/nano-banana/last.json` — last run (for `again`)


================================================================================
