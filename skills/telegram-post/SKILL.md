---
name: telegram-post
description: "Create, preview, and send formatted Telegram posts from draft markdown files. Built for [@klodkot](https://t.me/klodkot) and Gleb Kalinin's other T..."
---

# telegram-post

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
