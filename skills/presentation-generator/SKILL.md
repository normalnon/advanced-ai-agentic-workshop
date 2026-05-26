---
name: presentation-generator
description: "Create stunning presentations in neobrutalism style with Agency brand colors. Generate interactive HTML presentations with smooth scrolling navigat..."
---

# presentation-generator

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
