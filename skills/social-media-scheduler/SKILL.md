---
name: social-media-scheduler
description: "Generate a complete 30-day social media content calendar with post copy, hashtags, and scheduling times for LinkedIn, X (Twitter), Facebook, and Re..."
---

# social-media-scheduler

> **Path within category:** `skills/distribution/social-media-scheduler/SKILL.md`


# Social Media Scheduler

Generate a complete 30-day social media content calendar with post copy, hashtags, and scheduling times for LinkedIn, X (Twitter), Facebook, and Reddit. Follows the 80/20 rule: 80% value and engagement content, 20% affiliate promotions. Every post is ready to copy-paste or load into a scheduling tool.

## Stage

S5: Distribution — Social media is the top free traffic channel for affiliate marketers. This skill eliminates "what do I post today?" paralysis by giving you 30 days of content in one shot, optimized for each platform's algorithm and audience behavior.

## When to Use

- User wants a content plan for promoting an affiliate product over 30 days
- User asks for a social media calendar, posting schedule, or content strategy
- User wants platform-specific posts (LinkedIn professional angle, X casual, Reddit community-first)
- User has an audience on one or more social platforms and wants consistent posting
- Chaining from S1 (product research) — user found a product and now wants a social plan

## Input Schema

```yaml
product:
  name: string              # REQUIRED — product being promoted (e.g., "Semrush")
  affiliate_url: string     # REQUIRED — affiliate tracking link
  category: string          # OPTIONAL — e.g., "SEO tool", "AI writing tool"
  key_benefits: string[]    # OPTIONAL — top benefits. Inferred if not provided.
  price: string             # OPTIONAL — e.g., "starts at $119/mo"
  free_trial: boolean       # OPTIONAL — does the product have a free trial?

creator:
  niche: string             # REQUIRED — your content niche (e.g., "SEO for freelancers")
  audience: string          # REQUIRED — who follows you (e.g., "freelance SEO consultants")
  tone: string              # OPTIONAL — "professional" | "casual" | "educational" | "bold"
                            # Default: "educational"
  personal_story: string    # OPTIONAL — brief personal experience with the product

platforms:
  - string                  # REQUIRED — list of platforms: "linkedin" | "x" | "facebook" | "reddit"
                            # Default: ["linkedin", "x"]

calendar:
  start_date: string        # OPTIONAL — ISO date (e.g., "2026-04-01"). Default: next Monday.
  posts_per_week: number    # OPTIONAL — 3-7. Default: 5 (weekdays only)
  promotion_ratio: number   # OPTIONAL — % of posts that are affiliate promo. Default: 20
```

**Chaining context**: If S1 (product research) was run, auto-fill `product.name`, `product.affiliate_url`, `product.key_benefits`. If S3 (blog post) was run, include 2 posts linking to the blog post. If S4 (landing page) was run, include posts driving to the landing page.

## Workflow

### Step 1: Gather Inputs

Collect required fields. If product details are available from S1, use them. Otherwise ask:
- "What product are you promoting and what's your affiliate link?"
- "What's your content niche and who's your target audience?"
- "Which platforms: LinkedIn, X, Facebook, Reddit? (pick 1-4)"

### Step 2: Plan the 30-Day Arc

Divide the month into 4 weeks with a strategic arc:

| Week | Theme | Promo Ratio |
|------|-------|-------------|
| Week 1 | Education + awareness — establish authority, zero sell | 0% |
| Week 2 | Problem agitation — surface pain points the product solves | 10% |
| Week 3 | Solution introduction — introduce product, soft sell | 30% |
| Week 4 | Social proof + urgency — testimonials, results, hard CTA | 40% |

Overall month target: 20% promotional, 80% value/engagement.

**Post type mix** (apply across all 4 weeks):
- 30% Educational (how-to tips, frameworks, industry data)
- 20% Engagement (questions, polls, hot takes, controversial opinions)
- 20% Personal / storytelling (lessons learned, behind the scenes, wins)
- 15% Curated (share tools, articles, resources — without affiliate link)
- 15% Promotional (affiliate link posts — FTC disclosed)

### Step 3: Write Posts Per Platform

Write distinct copy for each platform. Do NOT copy the same post across platforms.

**LinkedIn** (professional, 150-300 words per post):
- Hook line: bold statement or specific number in first line (LinkedIn shows 2 lines before "see more")
- Format: short paragraphs with line breaks, 3-5 bullet points for how-to posts
- Hashtags: 3-5 at end (#SEO #ContentMarketing #FreelanceTips)
- CTA: "Comment below", "Save this for later", "Link in first comment" (for affiliate posts)
- Best posting times: Tue-Thu 8-10am and 12-2pm (user's timezone)

**X / Twitter** (concise, punchy, under 280 characters for single tweets):
- Hook: strong opener, no fluff
- Thread format for educational posts: number each tweet (1/ 2/ 3/)
- Hashtags: 1-2 only (#SEO #AItools)
- CTA: "RT if this helped", "Drop your take", direct link for promo posts
- Best posting times: Mon-Fri 9am and 6pm

**Facebook** (conversational, 100-200 words):
- More personal and community tone than LinkedIn
- Ask questions to drive comments (algorithm rewards comment activity)
- Hashtags: 2-3 only
- Image prompt included (describe what image to use)
- Best posting times: Wed-Fri 1-3pm

**Reddit** (community-first, never salesy):
- Identify 2-3 relevant subreddits for the niche (e.g., r/SEO, r/juststart, r/freelance)
- Lead with genuine value — post as a community member, not a marketer
- Affiliate link goes in comments, not the post body (per most subreddit rules)
- Title: specific and searchable (Reddit posts surface in Google)
- Format: detailed paragraph, then list takeaways
- Disclosure: "(Affiliate link in comments)" in post body
- Post max: 4 Reddit posts per month to avoid spam detection

### Step 4: Format the Calendar

Output a table-based calendar followed by individual post copy blocks.

**Calendar table format:**

```
WEEK 1 — Education & Awareness
| Day | Platform | Type | Topic |
|-----|----------|------|-------|
| Mon Apr 7 | LinkedIn | Educational | 5 SEO mistakes killing your traffic |
| Tue Apr 8 | X | Engagement | Hot take: [opinion] |
...
```

Then write each post in full:

```
[Full post copy, ready to paste]

Hashtags: #tag1 #tag2 #tag3
CTA: [specific action]
Best time to post: [time]
[If promo: Affiliate disclosure included]
