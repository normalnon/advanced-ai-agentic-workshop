---
name: traffic-analyzer
description: "Analyze website traffic, engagement, and traffic sources for any domain. Goes beyond"
---

# traffic-analyzer

> **Path within category:** `skills/research/traffic-analyzer/SKILL.md`


# Traffic Analyzer

Analyze website traffic, engagement, and traffic sources for any domain. Goes beyond
raw data — scores the domain, interprets what the traffic patterns mean for affiliate
promotion, and recommends whether the program is worth your time.

A tool returns numbers. This skill returns a verdict.

**Use cases:**
- Is this affiliate program's website healthy? (High traffic = more brand awareness = easier conversions)
- Where does a competitor get their traffic? (Find channels they're ignoring)
- Compare 2-3 affiliate programs by advertiser website strength
- Validate a niche by checking traffic to the top programs in it

## Stage

This skill belongs to Stage S1: Research

## When to Use

- Before committing to promote an affiliate program — check if the advertiser is legit
- When comparing multiple programs — traffic is a proxy for brand strength
- When `competitor-spy` identifies competitor sites — analyze their traffic sources
- When evaluating a niche — check if the top programs have healthy traffic
- When an advertiser claims "millions of users" — verify with data

## Input Schema

```yaml
domains: string[]             # (required) 1-5 domains to analyze — "heygen.com", "synthesia.io"
compare: boolean              # (optional, default: true if 2+ domains) Side-by-side comparison
focus: string                 # (optional, default: "affiliate") 
                              # "affiliate" — score from promoter perspective
                              # "competitor" — analyze as a competitor site
                              # "advertiser" — evaluate advertiser health
```

## Workflow

### Step 1: Gather Traffic Data

**With SimilarWeb API (see `shared/references/social-data-providers.md`):**

If `social_data_config.similarweb` is configured:
- Call SimilarWeb API for each domain
- Returns: global rank, country rank, visits, pages/visit, avg duration, bounce rate, traffic sources

**Without API (web_search fallback):**

For each domain:
1. `web_search "[domain] traffic similarweb"` → often shows rank and visit estimates in snippets
2. `web_search "[domain] site traffic statistics"` → third-party reports
3. `web_search "site:[domain]"` → Google index count as proxy for content depth
4. `web_search "[domain] alexa rank"` OR `"[domain] semrush traffic"` → alternative sources
5. `web_fetch "https://www.similarweb.com/website/[domain]/"` → extract visible data from SimilarWeb free page (may be limited)

Note: web_search data is approximate. SimilarWeb API provides exact metrics.

### Step 2: Analyze Core Metrics

For each domain, analyze and interpret:

**Traffic Volume:**
```yaml
global_rank: number            # Lower = better. <10K = major site, <100K = solid, <1M = niche
country_rank: number           # Rank in primary country
monthly_visits: string         # "1.2M", "350K", "45K"
visits_trend: string           # "growing" | "stable" | "declining" (if historical data available)
```

**Engagement Quality:**
```yaml
pages_per_visit: number        # >3 = good engagement, <2 = bouncy
avg_visit_duration: string     # ">3 min" = engaged, "<1 min" = low quality
bounce_rate: number            # <40% = excellent, 40-60% = normal, >60% = concerning
```

**Traffic Sources Breakdown:**
```yaml
direct: number                 # % — brand strength indicator
search: number                 # % — SEO strength
social: number                 # % — social media presence
referral: number               # % — partnership/affiliate ecosystem
paid: number                   # % — ad spend (high paid = advertiser invests in acquisition)
```

### Step 3: Interpret for Use Case

**For affiliate promoters (`focus: "affiliate"`):**

Score the domain as an affiliate promotion target:

| Signal | Good (8-10) | OK (5-7) | Red Flag (1-4) |
|--------|-------------|----------|-----------------|
| Monthly visits | >500K | 50K-500K | <50K |
| Bounce rate | <40% | 40-60% | >70% |
| Search traffic | >30% | 15-30% | <10% (overly dependent on ads) |
| Brand (direct) | >30% | 15-30% | <10% (nobody knows them) |
| Pages/visit | >4 | 2-4 | <2 |

**Why this matters for affiliates:**
- High traffic = people already search for this brand → easier to convert your referrals
- Strong brand (high direct traffic) = trust → higher conversion rate
- Good engagement = product delivers value → lower refund rate → your commissions stick
- Healthy search traffic = sustainable business → long-term commission potential
- High paid traffic = advertiser invests in growth → good sign for program longevity

**For competitor analysis (`focus: "competitor"`):**

- Identify their strongest traffic channel → where are they winning?
- Find their weakest channel → opportunity for you
- Compare bounce rate → are they retaining visitors better than you?
- Check referral traffic → which sites link to them? (potential partnership targets)

**For advertiser evaluation (`focus: "advertiser"`):**

- Is the advertiser's website healthy? (declining traffic = risky to promote)
- Do they invest in marketing? (paid traffic % shows ad budget)
- Is their product sticky? (engagement metrics reveal product quality)
- How established are they? (global rank trajectory)

### Step 4: Generate Traffic Score

Calculate an overall **Traffic Health Score** (0-100):

```
traffic_score = (
  rank_score × 0.20 +           # Based on global rank
  volume_score × 0.25 +          # Based on monthly visits  
  engagement_score × 0.25 +      # Based on bounce rate + pages/visit + duration
  diversity_score × 0.15 +       # Traffic source diversity (not overly dependent on one channel)
  brand_score × 0.15             # Direct traffic % (brand recognition)
)
```

**Score interpretation:**
- **80-100:** Excellent. Strong, established brand. Safe to promote long-term.
- **60-79:** Good. Healthy traffic. Solid promotion candidate.
- **40-59:** Fair. Growing or niche site. Evaluate other factors (commission, product quality).
- **20-39:** Weak. Low traffic or declining. Proceed with caution.
- **0-19:** Red flag. Very low traffic, new, or declining fast. Not recommended unless early-stage with high commission.

### Step 5: Compare (if multiple domains)

If 2+ domains provided, create side-by-side comparison:
- Which has more traffic?
- Which has better engagement?
- Which has more diverse traffic sources?
- Which is growing faster?
- Overall winner with reasoning

### Step 6: Self-Validation

Before presenting output, verify:

- [ ] Data source clearly stated (API vs web_search estimate)
- [ ] Scores are calibrated (not all 8/10 — differentiate clearly)
- [ ] Interpretation matches the focus (affiliate vs competitor vs advertiser)
- [ ] Red flags explicitly called out, not buried
- [ ] Recommendation is actionable and specific

If any check fails, fix before delivering. Do not flag checklist to user.

## Output Schema

```yaml
output_schema_version: "1.0.0"
domains_analyzed:
  - domain: string
    data_source: "similarweb_api" | "web_search_estimate"
    metrics:
      global_rank: number | null
      country_rank: number | null
      country: string | null
      monthly_visits: string
      pages_per_visit: number | null
      avg_duration: string | null
      bounce_rate: number | null
    traffic_sources:
      direct: number | null        # percentage
      search: number | null
      social: number | null
      referral: number | null
      paid: number | null
    traffic_score: number          # 0-100
    verdict: string                # "excellent" | "good" | "fair" | "weak" | "red_flag"
    interpretation: string         # 2-3 sentence analysis based on focus
comparison: object | null          # if 2+ domains
  winner: string
  reasoning: string
recommended_next_skill: string
```

## Output Format

```markdown
## Traffic Analysis: [Domain(s)]

### Data Source
📊 **[SimilarWeb API | Web search estimates (approximate)]**


### [If comparing 2+ domains]

### Head-to-Head: [domain1] vs [domain2]

| Metric | [domain1] | [domain2] | Winner |
|--------|-----------|-----------|--------|
| Traffic Score | XX/100 | XX/100 | [domain] |
| Monthly Visits | X.XM | XXK | [domain] |
| Engagement | X.X pg/visit | X.X pg/visit | [domain] |
| Brand Strength | XX% direct | XX% direct | [domain] |
| SEO | XX% search | XX% search | [domain] |

**Verdict:** [domain1] is the stronger affiliate promotion target because [reasoning].
