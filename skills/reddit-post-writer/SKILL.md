---
name: reddit-post-writer
description: "Write Reddit posts and comments that earn upvotes by leading with genuine value."
---

# reddit-post-writer

> **Path within category:** `skills/content/reddit-post-writer/SKILL.md`


# Reddit Post Writer

Write Reddit posts and comments that earn upvotes by leading with genuine value.
The affiliate recommendation comes second — after trust is built. Reddit users
have a finely tuned spam detector. This skill helps affiliates write like Redditors,
not marketers.

## Stage

This skill belongs to Stage S2: Content

## When to Use

- User wants to drive affiliate traffic from Reddit
- User wants to recommend a product in a relevant subreddit
- User is active in a community and wants to add a helpful product mention
- User has a genuine experience with a product and wants to share it naturally
- User asks how to participate on Reddit without getting banned for self-promotion

## Input Schema

```
{
  product: {
    name: string              # (required) "Notion"
    description: string       # (optional) What the product does
    url: string               # (optional) Affiliate link — used in disclosure only
    reward_value: string      # (optional) Commission — never revealed in post
  }
  subreddit: string           # (optional) Target subreddit, e.g., "r/productivity"
  post_type: string           # (optional, default: auto) "post" | "comment_reply" | "ama_style"
  trigger_question: string    # (optional) Specific Reddit question or post you're replying to
  personal_experience: string # (optional) Real experience with the product to use as anchor
  audience: string            # (optional) Who reads this subreddit — "students", "developers"
  tone: string                # (optional, default: "genuine") "genuine" | "analytical" | "casual"
  problem_focus: string       # (optional) The specific problem this post addresses
}
```

## Workflow

### Step 1: Understand Reddit Culture First

Before writing, confirm the target subreddit context. If subreddit is provided,
use `web_search "reddit r/[subreddit] rules affiliate"` to check:
- Are affiliate links explicitly banned? (many subreddits ban them outright)
- What post formats are most common? (links, text posts, discussions)
- What gets upvoted vs. downvoted in this community?
- Is there a community expectation of neutrality or personal experience?

**Subreddits that generally tolerate product mentions:**
r/productivity, r/entrepreneur, r/Entrepreneur, r/sidehustle, r/personalfinance,
r/freelance, r/marketing, r/SEO, r/webdev, r/startups, r/smallbusiness

**Subreddits that are extremely ban-happy about promotion:**
r/frugal, r/cscareerquestions, r/AskReddit, r/personalfinance (strict on direct links)

If subreddit bans affiliate links: do NOT write a post with a link. Instead, write
a post that mentions the product by name with a note like "Search for [product]
affiliate program if interested." Disclose and redirect.

### Step 2: Determine the Post Type

**Option A — Original Post (new thread):**
Best when there's no existing discussion. Write a story, question, or breakdown that
organically leads to a product mention.
- "How I went from X to Y — the exact tools I used"
- "Anyone else use [product] for [use case]? Here's my 6-month review"
- "I tested 5 [category] tools so you don't have to — honest breakdown"

**Option B — Comment Reply (responding to an existing post):**
Highest trust format. Someone asks "what tool do you use for X?" and you reply helpfully.
- Write a substantive answer that doesn't mention the product until the 3rd+ paragraph
- Add value even without the product mention — if removed, the comment should still be helpful
- Product mention: "Personally, I use [product] and it's been solid for [specific use case]"

**Option C — AMA-Style / Experience Share:**
"I've been doing [X] for [N] years. Happy to share what's worked."
- Opens conversation, positions creator as authority
- Product naturally comes up when people ask "what tools do you use?"

If `trigger_question` is provided → use Option B. Otherwise, default to Option A.

### Step 3: Research Product and Find Reddit-Specific Angles

Use `web_search "reddit [product name] review"` to find:
- What real Reddit users are saying about the product (use their language)
- Common objections raised on Reddit (address these proactively)
- How competitors are discussed (context for framing)
- Questions people ask that your post can answer

Also use `web_search "reddit [problem space] best tools"` to understand:
- What alternatives Redditors currently recommend
- How to frame your recommendation as additive, not replacing their preferences
- What not to say (phrases that get downvoted in this community)

### Step 4: Write the Post

**Reddit post structure that converts:**

1. **Title** (for new posts): specific, searchable, sounds like a real person's question or story
   - Good: "I tried 4 project management tools over 2 years — here's what I actually use now"
   - Bad: "The BEST productivity tool I've ever used!! (link in post)"
   - Good: "[6 months update] How I finally stopped context-switching between apps"

2. **Opening paragraph**: establish credibility or relatability. NO product mention here.
   - "I've been freelancing for 3 years and I'm embarrassed by how long I tried to manage
     everything in spreadsheets."

3. **Body**: share the actual useful content — your experience, the problem, what you tried.
   This section should be valuable even without the product mention.

4. **Product introduction** (70-80% through the post): introduce naturally.
   - "Eventually I landed on [product] and I've stuck with it for [X months]."
   - Specific use case: what exactly you use it for, not vague praise
   - ONE honest con: "It's not perfect — the mobile app is weak — but for desktop work
     it's exactly what I needed." Cons dramatically increase trust.

5. **FTC disclosure** (at the bottom):
   - "Full disclosure: the link in my profile leads to an affiliate link. No extra cost
     to you, and I would recommend this tool regardless."
   - Or if not posting a link: "Not affiliated, just a genuine fan."
   - Per `shared/references/ftc-compliance.md` — disclosure is required for Reddit too.

6. **Closing**: invite discussion, not clicks.
   - "Happy to answer questions about my workflow in the comments."
   - Ask a question back: "What does your current setup look like?"

### Step 5: Anti-Spam Checklist

Before finalizing, run through this checklist:

- [ ] Post adds value even if the product mention is removed
- [ ] No exclamation marks in praise ("This tool is AMAZING!!")
- [ ] No superlatives without evidence ("best tool I've ever used" → needs qualifier)
- [ ] Affiliate link goes in comments or profile bio, NOT the main post body (most subreddits)
- [ ] FTC disclosure is present and clear
- [ ] Post doesn't read like a press release
- [ ] Includes at least one real limitation or caveat about the product
- [ ] Tone matches the subreddit (match voice to community)
- [ ] Username context matters — new accounts posting affiliate content get instant downvotes

### Step 6: Add Engagement Strategy

Reddit rewards participation, not broadcasting. Include:
1. **Reply strategy**: when commenters respond, how to keep conversation going naturally
2. **Upvote path**: what type of engagement to solicit (awards, saves, discussion)
3. **Subreddit timing**: best day/time to post in this subreddit
4. **Cross-post candidates**: which other subreddits this post could work in

### Step 7: Self-Validation

Before presenting output, verify:

- [ ] Post adds value even if product mention is removed
- [ ] No exclamation marks in product praise
- [ ] Affiliate link in comments or bio, NOT in post body
- [ ] FTC "Full disclosure: affiliate link" present at bottom
- [ ] At least one real product limitation or caveat mentioned
- [ ] Tone matches target subreddit style

If any check fails, fix the output before delivering. Do not flag the checklist to the user — just ensure the output passes.

## Output Schema

```
{
  output_schema_version: "1.0.0"  # Semver — bump major on breaking changes
  post: {
    type: string              # "post" | "comment_reply" | "ama_style"
    subreddit: string         # "r/productivity"
    title: string | null      # For new posts only
    body: string              # Full post/comment body
    link_placement: string    # Where to put the affiliate link
    disclosure: string        # The disclosure text used
    char_count: number
  }
  subreddit_notes: {
    allows_affiliate_links: boolean
    community_tone: string
    best_post_time: string
    cross_post_subreddits: string[]
  }
  engagement_tips: string[]
  product_name: string
  content_angle: string
}
```

## Output Format

```
## Reddit Post: [Product Name]

**Type:** [New Post / Comment Reply / AMA-style]
**Target Subreddit:** [r/subreddit]
**Subreddit allows affiliate links:** [Yes / No / Link in comments only]


### Post Body

[Full post text, formatted with Reddit markdown — use **bold**, *italic*, > quotes
as appropriate. Paragraphs separated by blank lines.]


### Subreddit Notes

- **Community tone:** [What vibe this subreddit has]
- **Best time to post:** [Day and time]
- **Watch out for:** [Specific rules or sensitivities]


### Engagement Tips

1. [How to respond to likely comments]
2. [How to handle skeptics or downvotes]
3. [When to resurface this content]
