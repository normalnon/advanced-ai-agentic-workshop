---
name: comparison-post-writer
description: "Write high-converting 'X vs Y' comparison blog posts that rank on Google and help readers make a confident buying decision. Each post includes a fe..."
---

# comparison-post-writer

> **Path within category:** `skills/blog/comparison-post-writer/SKILL.md`


# Comparison Post Writer

Write high-converting "X vs Y" comparison blog posts that rank on Google and help readers make a confident buying decision. Each post includes a feature comparison table, individual product breakdowns, pros and cons, a clear winner recommendation, and affiliate CTAs placed at maximum-intent moments.

## When to Use

- User wants to compare two or three competing products side by side
- User has two affiliate programs and wants a single article that covers both
- User says "vs", "versus", "compare", "which is better", "side by side"
- User wants to capture high-intent search traffic (X vs Y searches convert at 2-3x the rate of generic reviews)
- User has a product from S1 and wants to frame it against competitors

## Workflow

### Step 1: Identify Products to Compare

Parse the user's request for product names. You need a minimum of 2 and a maximum of 3 products.

**If only 1 product is provided:**
- Use `web_search` to find the top 1-2 competitors
- Search: `"[product name] alternatives" OR "[product name] vs" site:g2.com OR site:capterra.com OR site:trustradius.com`
- Pick the competitors with the most head-to-head search volume

**If 3+ products are provided:**
- Keep all 3 if they are genuinely comparable
- If the user listed 4+, ask which 2-3 to focus on — more than 3 makes the comparison unwieldy

**Affiliate priority**: The user's affiliate product goes first (featured position). If both products have affiliate links, feature the higher-commission one in the "winner" slot unless the product genuinely loses on quality.

### Step 2: Research Both Products

For each product, use `web_search` to gather:
1. **Pricing**: starting price, tiers, free trial availability
2. **Key features**: 8-12 features that matter to buyers
3. **Target audience**: who uses this product and why
4. **Known weaknesses**: common complaints on G2, Capterra, Reddit, or Trustpilot
5. **Unique differentiator**: one thing this product does better than everyone else
6. **Search volume signal**: `"[product A] vs [product B]"` — check if autocomplete shows this is a real query

Search queries to run per product:
- `"[product name] review [year]"`
- `"[product name] pricing"`
- `"[product name] pros cons"`

### Step 3: Build the Comparison Framework

Determine the 6-10 comparison dimensions that matter most for this product category. These should be:
- Directly relevant to buyer decisions (not vanity features)
- Measurable or clearly differentiable between products
- Things that appear in search queries ("does X have [feature]?")

**Example dimensions by category:**
- Email tools: deliverability, automation, templates, integrations, pricing/contacts ratio, free plan
- SEO tools: keyword database size, backlink data, site audit depth, reporting, API access, pricing
- Video tools: resolution, AI avatars, voice cloning, templates, render speed, watermark on free plan
- Project management: task limits on free, Gantt chart, time tracking, automations, integrations, mobile app

Assign a winner per dimension based on research. Mark ties where genuine.

### Step 4: Determine the Narrative Angle

Choose one of three angles based on what the data shows:

| Angle | When to use | Headline formula |
|---|---|---|
| **Clear winner** | One product is genuinely better for most users | "[A] vs [B]: [A] Wins for Most, But [B] Is Better If..." |
| **It depends** | Products serve different audiences | "[A] vs [B]: Which Is Right for You? (Honest Comparison)" |
| **Upset** | Lesser-known product beats the market leader | "[A] vs [B]: Why [Lesser-Known] Is Actually Better in [Year]" |

Default to "clear winner" — readers want a recommendation, not a non-answer.

### Step 5: Write the Article

Write the full comparison post following this exact structure:

**1. FTC Disclosure** (3 lines, above the fold)
Read `shared/references/ftc-compliance.md` and use the medium format. Insert immediately after the title.

**2. Introduction** (150-250 words)
- Open with the core tension: why this is a hard choice
- State who each product is best suited for (one sentence each)
- End with: "By the end of this post, you'll know exactly which one to pick."
- Include target keyword naturally in the first 100 words

**3. Quick Verdict Box** (immediately after intro)
A scannable summary for readers who won't read the full article:
```
**Quick Verdict**
- Best overall: [Product A] — [one-line reason]
- Best for [use case]: [Product B] — [one-line reason]
- Best for budget: [Product X]
- Skip if: [edge case where neither works]
```

**4. Product Overviews** (200-300 words each)
One H2 section per product:
- What it is and what it does
- Who built it and when (brief credibility context)
- The one thing it does better than anyone else
- Starting price and free trial info
- Affiliate CTA: `[Try [Product] free →](affiliate_url)`

**5. Feature Comparison Table**
A full markdown table with all comparison dimensions:
```
| Feature | [Product A] | [Product B] |
|---|---|---|
| [Dimension 1] | ✅ Yes | ❌ No |
| [Dimension 2] | ⭐ Better | Good |
| Price | $X/mo | $Y/mo |
```
Use ✅ / ❌ / ⚠️ (partial) for binary features. Use descriptive text for nuanced ones. Bold the winner per row.

**6. Deep-Dive Sections** (one H2 per key dimension, 3-4 total)
Pick the 3-4 dimensions that drive 80% of buying decisions. For each:
- Explain what the feature does and why it matters
- Compare both products specifically (not generically)
- Include a sub-verdict: "Winner: [Product] because..."

**7. Pricing Breakdown**
- Table showing all pricing tiers for both products
- Calculate cost at 3 usage levels: starter, growing, scale
- Highlight free plan differences
- Note which has better value per feature

**8. Pros and Cons**
Two H3 sections (one per product), each with 4-6 bullet points per list.

**9. Who Should Choose Each Product**
Two H3 sections with bullet lists:
- "Choose [Product A] if you..."
- "Choose [Product B] if you..."
Be specific — job titles, use cases, budget ranges, team sizes.

**10. The Verdict** (200-300 words)
- State the winner clearly: "[Product A] is the better choice for most people."
- Explain why in 2-3 sentences
- Acknowledge the exception case where [Product B] wins
- Final affiliate CTA (strong format): `**Get started with [Product A] →**(affiliate_url)`
- If [Product B] also has affiliate link: secondary CTA below

**11. FAQ Section** (5-7 questions)
Address the real questions people type into Google:
- "Is [Product A] better than [Product B]?"
- "Which is cheaper, [A] or [B]?"
- "Does [Product A] offer a free trial?"
- "Can I switch from [Product B] to [Product A]?"
- "Which has better customer support?"

### Step 6: Format Output

Produce output in three parts:

**Part 1: SEO Metadata**
```
Title: [title]
Slug: [product-a]-vs-[product-b]
Meta Description: [150-160 chars comparing both products with clear angle]
Target Keyword: [product-a] vs [product-b]
Secondary Keywords: [product-a] review, [product-b] alternatives, best [category] tool, [product-a] pricing
Word Count: [actual]
Format: comparison
Winner: [product name]
