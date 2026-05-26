---
name: list-affitor-skill
description: "Turn a repeatable AI prompt or workflow into a structured, publish-ready skill for"
---

# list-affitor-skill

> **Path within category:** `skills/meta/list-affitor-skill/SKILL.md`


# List Affitor Skill

Turn a repeatable AI prompt or workflow into a structured, publish-ready skill for
[list.affitor.com](https://list.affitor.com). The output is a complete SKILL.md file
that works in any AI agent — plus the listing fields to publish it on LIST.

## Stage

This skill belongs to Stage S8: Meta

## When to Use

- User has a prompt they keep reusing and wants to turn it into a shareable skill
- User wants to create a new skill for the Affitor skills directory
- User wants to write a SKILL.md file in the standard format
- User says "make this a skill" or "write a skill for X"
- User wants to package an AI workflow so others can replicate it

## Input Schema

```
{
  raw_prompt: string       # (required) The prompt, workflow description, or detailed explanation of what the skill does
  failure_modes: string    # (optional) What goes wrong when the output is bad — helps write better Instructions and Error Handling
  niche: string            # (optional) Category hint, e.g., "content", "research", "seo"
  examples: string         # (optional) Example input/output pairs the user already has
}
```

## Workflow

### Step 1: Understand What the Prompt Actually Does

Before writing anything, analyze the user's raw prompt or workflow description:

1. **Task type** — Is this content creation, research, analysis, planning, automation, or something else?
2. **Variable inputs** — What changes each time? (product name, URL, audience, topic, etc.)
3. **Fixed structure** — What stays the same? (output format, sections, tone, constraints)
4. **Quality differentiator** — What makes a good output vs. a bad one?
5. **Failure modes** — Where does the AI tend to go wrong without explicit guidance?

If the user gave a vague description instead of an actual prompt, ask:
- "What do you typically paste into ChatGPT/Claude for this?"
- "What does the output look like when it works well?"
- "What goes wrong when it doesn't?"

If the user says "just do it", infer from context and proceed.

### Step 2: Determine Skill Metadata

Based on the analysis, determine:

| Field | How to decide |
|-------|--------------|
| `name` | Short, action-oriented. "Comparison Post Writer" not "A Skill for Writing Comparison Posts" |
| `slug` | kebab-case of name, e.g., `comparison-post-writer` |
| `category` | One of: research, content, seo, landing, distribution, analytics, automation, meta |
| `level` | beginner (1-step, no tools), intermediate (multi-step, 1 tool), advanced (complex workflow, multiple tools) |
| `stage` | S1-Research, S2-Content, S3-Blog, S4-Landing, S5-Distribution, S6-Analytics, S7-Automation, S8-Meta |
| `tags` | 3-6 lowercase tags relevant to the skill's domain |
| `tools` | What external tools the skill needs: `web_search`, `web_fetch`, `code_execution`, none |

### Step 3: Write the SKILL.md

Create a complete SKILL.md following this exact structure. Every section is required.

**Frontmatter (YAML)**
```yaml
```

**Title and Introduction**
One paragraph. What the skill does and what makes the output reliable. No marketing speak.

**When to Use**
3-5 specific trigger scenarios. "Writing a blog post" is too vague. "You need to publish a comparison post for two competing SaaS tools this week" is useful.

**Input Schema**
Typed definition of every variable input. Mark required vs optional.

**Workflow (numbered steps)**
This is the core. Each step must be concrete enough that any AI model produces consistent output:

- **Action** — what to do
- **Approach** — how to do it specifically
- **Quality bar** — what good looks like

Bad: "3. Write the pros and cons"
Good: "3. Write at least 3 pros and 2 cons. Each must reference a specific feature, not a vague category. 'Exports to 12 formats including PDF and DOCX' not 'Great export options'."

**Output Schema**
Typed fields that other skills can consume via conversation context. Include `output_schema_version: "1.0.0"`.

**Output Format**
A markdown code block showing the exact template with `[placeholder]` brackets. This is the single most important section for consistency.

**Error Handling**
3-5 named failure modes with specific recovery behavior. What happens when input is missing, ambiguous, or the task can't be completed?

**Examples**
2-3 concrete examples showing:
- User input
- Key decisions made during the workflow
- What the output looks like (excerpt, not full)

**Flywheel Connections**
- Feeds Into: which skills consume this skill's output
- Fed By: which skills produce input for this skill
- Feedback Loop: how community engagement improves the skill
- `chain_metadata` YAML block with `skill_slug`, `stage`, `timestamp`, `suggested_next`

**Quality Gate**
5-7 numbered checklist items that must all pass before the output is delivered. These are the self-validation checks the AI runs silently.

**References**
Links to supplementary reference files if applicable.

### Step 4: Write the LIST Description

Separately from the SKILL.md, write a community-facing description for the listing on list.affitor.com. This is what people see in the feed — it sells the skill, not documents it.

Structure:
1. **Opening** (2 sentences) — what the skill does, who it's for
2. **When to Use** (3 bullets) — specific scenarios
3. **What Makes It Different** (brief) — why this skill vs. just prompting
4. **Instructions summary** — condensed version of the workflow
5. **Input Required** — what the user needs to provide
6. **Output Format** — what the skill produces (show template)
7. **Example** — one concrete input/output
8. **Tips** (3-5) — practical advice for getting the best results

This is NOT the SKILL.md content — it's a human-friendly summary for discovery.

### Step 5: Assemble Output

Present two clearly separated outputs:

1. **SKILL.md** — the full file, ready to save to `skills/{stage}/{slug}/SKILL.md`
2. **LIST Submission** — listing fields + description for list.affitor.com

### Step 6: Self-Validation

Before presenting output, verify:

- [ ] SKILL.md has all required sections (frontmatter, intro, when-to-use, input schema, workflow, output schema, output format, error handling, examples, flywheel, quality gate)
- [ ] Every workflow step has action + approach + quality bar
- [ ] Output Format uses a code block with `[placeholder]` brackets
- [ ] At least 2 examples with concrete input/output
- [ ] Error handling covers realistic failure modes, not hypothetical ones
- [ ] Quality gate items are testable (not "make sure it's good")
- [ ] Description is specific enough that someone knows if it's relevant before clicking
- [ ] Frontmatter `name` matches the slug exactly

## Output Schema

Other skills consume these fields from conversation context:

```
{
  output_schema_version: "1.0.0"
  skill_md: string           # Complete SKILL.md file content (ready to write to disk)
  listing: {
    name: string             # "Comparison Post Writer"
    slug: string             # "comparison-post-writer"
    description: string      # Community-facing description for list.affitor.com
    content: string          # Full SKILL.md content (for the content field)
    category: string         # "content", "research", "seo", etc.
    level: string            # "beginner", "intermediate", "advanced"
    tags: string[]           # ["content", "comparison", "seo", "blog"]
  }
  metadata: {
    stage: string            # "S2-Content"
    tools_needed: string[]   # ["web_search"] or []
    estimated_time: string   # "15 min"
  }
}
```

## Output Format

The skill produces two outputs:

### Output 1: SKILL.md File

```

# [Skill Name]

[1 paragraph intro]

## Stage

This skill belongs to Stage [S1-S8]: [Stage Name]

## When to Use

- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

## Input Schema

[typed input definition]

## Workflow

### Step 1: [Action]
[Instructions with approach and quality bar]

### Step 2: [Action]
[Instructions]

...

## Output Schema

[typed output definition with output_schema_version]

## Output Format

[code block template with [placeholders]]

## Error Handling

- **[Failure mode 1]:** [Recovery behavior]
- **[Failure mode 2]:** [Recovery behavior]

## Examples

**Example 1: [Scenario]**
[Input, decisions, output excerpt]

**Example 2: [Scenario]**
[Input, decisions, output excerpt]

## Flywheel Connections

### Feeds Into
- [skill] ([stage]) — [how]

### Fed By
- [skill] ([stage]) — [how]

### Feedback Loop
[How community engagement improves this skill]

chain_metadata YAML block

## Quality Gate

1. [Testable check]
2. [Testable check]
...

## References

- [reference files if applicable]
```

### Output 2: LIST Submission Fields

```
## Listing Fields (for list.affitor.com)

| Field | Value |
|-------|-------|
| Name | [Skill Name] |
| Slug | [slug] |
| Category | [category] |
| Level | [level] |
| Tags | [tag1, tag2, tag3] |
