---
name: listicle-generator
description: "Write 'Top N Best [Category]' roundup articles that rank on Google, capture featured snippets, and drive affiliate conversions across multiple prod..."
---

# listicle-generator

> **Path within category:** `skills/blog/listicle-generator/SKILL.md`


# Listicle Generator

Write "Top N Best [Category]" roundup articles that rank on Google, capture featured snippets, and drive affiliate conversions across multiple products. Each list entry is a self-contained mini-review with features, pricing, pros/cons, audience fit, and a CTA. The article is structured to win both the featured snippet and the "People Also Ask" box.

## When to Use

- User wants to cover an entire product category with multiple affiliate links
- User says "best", "top", "roundup", "list of", or mentions a number with a category
- User wants to capture high-volume generic keywords ("best email marketing tools") vs. specific product searches
- User has multiple affiliate programs in the same category and wants one article to cover them all
- User wants an article format that benefits from regular updates (add/remove products as market evolves)

## Workflow

### Step 1: Determine List Parameters

Parse the user's request for:
- **Category**: what type of product (e.g., "email marketing tools", "AI video generators")
- **List size (N)**: explicitly stated number, or auto-select based on category depth
  - Niche/specialized categories: 5-7 products
  - Broad/competitive categories: 7-10 products
  - Very broad (e.g., "project management tools"): 10-12 products
- **Target audience**: inferred from category + any context clues (beginners, enterprises, specific industries)
- **Year**: always use current year in the title for freshness signal

**If no affiliate product is specified:**
- Ask: "Which product are you promoting? I'll feature it prominently in the list."
- If user says to proceed anyway, generate a balanced list and note where they should insert their affiliate link.

### Step 2: Research the Product Landscape

Use `web_search` to build the product list:

1. **Seed query**: `"best [category] tools [year]" site:g2.com OR site:capterra.com OR site:trustradius.com`
2. **Validate with traffic**: `"best [category]"` — check autocomplete for common phrasings
3. **Find affiliate programs**: `"[category] affiliate program"` — identify which products offer commissions

For each candidate product, gather:
- Product name and one-line description
- Starting price and free plan availability
- G2/Capterra rating (if available)
- The one thing it does best (unique angle)
- Who it's primarily designed for

**Affiliate prioritization rules:**
- Position the user's affiliate product at #1 or #2 (never lower than #3 unless it genuinely cannot be defended in the top 3)
- #1 position gets the most clicks — use it for the highest-commission or best-converting product
- If the user has multiple affiliate programs, spread them in positions 1, 2, and 4
- Non-affiliate products fill the remaining slots to make the list credible and balanced

### Step 3: Plan the Article Structure

Map out every section before writing:

**Article structure:**
1. Title (with year, number, category)
2. FTC disclosure
3. Introduction (150-200 words)
4. "At a Glance" summary table
5. Evaluation criteria (H2)
6. Individual product entries × N (H2 each)
7. Comparison table (all products × key dimensions)
8. How to Choose (H2)
9. FAQ (H2)
10. Final Recommendation (H2)

**Per-entry structure** (400-600 words each):
- H2: `[Rank]. [Product Name] — [One-line Value Prop]`
- Opening paragraph: what it is, who made it, why it's on this list
- Key features section (3-5 bullet points)
- Pricing table (free / starter / pro / enterprise)
- Pros list (4-5 bullets)
- Cons list (2-3 bullets — be honest, builds trust)
- Best for: one sentence naming the ideal user
- Affiliate CTA button: `[Try [Product] free →](url)`

### Step 4: Write the Full Article

**Title formula:** `[N] Best [Category] Tools in [Year] (Ranked and Reviewed)`
Alternative: `Best [Category] Software: Top [N] Picks for [Year]`

**Introduction (150-200 words):**
- Open with the core problem this category solves
- Mention how many tools you evaluated and your selection criteria
- Name-drop 2-3 products from the list to signal comprehensiveness
- End with a transition: "Here are the [N] best options I found."

**"At a Glance" Table** (immediately after intro, captures featured snippet):
```
| Tool | Best For | Starting Price | Free Plan |
|---|---|---|---|
| [Product 1] | [Use case] | $X/mo | ✅ |
| [Product 2] | [Use case] | $Y/mo | ❌ |
```

**Evaluation Criteria (H2, before the list):**
List the 4-6 criteria used to rank products. This builds credibility and explains why your #1 pick is #1.
Example criteria: ease of use, feature depth, pricing value, customer support quality, integration ecosystem, scalability.

**Individual Product Entries:**
Write each entry following the per-entry structure above. Vary the opening sentence — don't start every entry the same way. Include specific, verifiable details (actual feature names, real pricing tiers, concrete limitations) — not generic praise.

**Master Comparison Table:**
After all product entries, include a comprehensive feature matrix:
```
| Feature | [P1] | [P2] | [P3] | [P4] | [P5] |
|---|---|---|---|---|---|
| Free plan | ✅ | ❌ | ✅ | ⚠️ | ✅ |
| [Key feature] | ✅ | ✅ | ❌ | ✅ | ❌ |
| [Key feature] | ⭐ Best | Good | Limited | Good | Basic |
| Starting price | $X | $Y | $Z | $A | Free |
```

**How to Choose (H2, 300-400 words):**
A decision framework for readers who are still unsure after reading the list:
- "If you're a beginner with a tight budget → [Product X]"
- "If you need [specific feature] → [Product Y]"
- "If you're scaling a team → [Product Z]"
- "If you're migrating from [common competitor] → [Product A]"

**FAQ Section (5-7 questions):**
- "What is the best [category] tool?"
- "What is the cheapest [category] tool?"
- "What [category] tool has the best free plan?"
- "Is [top product] worth it?"
- "How do I choose [category] software?"

**Final Recommendation (H2):**
- Restate the #1 pick with a 2-sentence reason
- Give a backup pick for a different audience
- Strong CTA: `**Start with [Product] — it's free to try.** [Get started →](affiliate_url)`

### Step 5: Format Output

**Part 1: SEO Metadata**
```
Title: [title with year and number]
Slug: best-[category-slug]-tools
Meta Description: [150-160 chars, include number + year + top product name]
Target Keyword: best [category] tools
Secondary Keywords: [category] software, [product 1] review, [product 2] alternatives, top [category] [year]
Word Count: [actual]
Format: listicle
Products: [N]
