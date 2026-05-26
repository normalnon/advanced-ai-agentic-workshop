---
name: jtbd
description: "Conduct a focused Jobs-to-Be-Done interview for one project and emit a decision-grade artifact bundle. The bundle contains a machine-readable `jtbd..."
---

# jtbd

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
