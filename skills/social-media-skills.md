---
name: social-media-skills
description: Consolidated expert tools and guidelines for social media skills.
---

# 🛠️ Consolidated Skills: SOCIAL-MEDIA-SKILLS
This playbook contains a combined registry of expert capabilities for **social-media-skills**.

## 1. Expert Skill: youtube-thumbnail
> **Path within category:** `skills/youtube-thumbnail/SKILL.md`


# YouTube Thumbnail

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1.

## Step 1. Gather inputs

Check the project for a reference photo config. Look in this order:

1. `thumbnail-config.md` in the project root
2. `brand-kit.md` — look for a reference image path and brand colours
3. `about-me.md` — for the creator's name and positioning

If a reference photo path is stored, pre-fill it. Otherwise ask:

> Upload or provide the path to the reference photo of yourself you want used in the thumbnail. Ideally a clear headshot with distinctive lighting and expression you plan to reuse across videos for brand consistency.

Then call AskUserQuestion:

```json
[
  {
    "question": "What is the video title?",
    "header": "Title",
    "multiSelect": false,
    "options": [
      {"label": "I will type the title", "description": "Type the full working title"},
      {"label": "Suggest one", "description": "Given the topic, propose 3 click-worthy titles first"}
    ]
  },
  {
    "question": "Emotional tone?",
    "header": "Tone",
    "multiSelect": false,
    "options": [
      {"label": "Shock / surprise", "description": "Wide eyes, open mouth, bold reaction"},
      {"label": "Curious / thinking", "description": "Slight smirk, raised eyebrow, gaze off-frame"},
      {"label": "Confident / direct", "description": "Eye contact, calm, assertive"},
      {"label": "Frustrated / strong take", "description": "Intense gaze, hand gesture, tension"}
    ]
  }
]
```

## Step 2. Apply thumbnail best practices

Every thumbnail must follow these rules:

- **Face fills 30 to 50 percent** of the frame. Readable at small sizes.
- **3 to 5 words maximum** of large text. 6 if absolutely necessary.
- **Two colours dominate**. Brand primary + one high-contrast accent (yellow, red, cyan work well).
- **One clear focal element** besides the face. Tool logo, bold number, arrow, or prop.
- **High contrast** between face, text, and background. Test by squinting.
- **Text is not a sentence**. It is a hook phrase. Examples: "I fired my team", "Claude can now...", "Don't do this".
- **No small text, no logos bottom-right** (watch time icon sits there).

## Step 3. Build the thumbnail brief

Output a concise brief the user can review:

```
THUMBNAIL BRIEF: [video title]

Composition: [face position, % of frame, direction of gaze]
Text: "[hook phrase, 3-5 words]"
Text placement: [left, right, top, wraps around face]
Colour palette: [primary hex], [accent hex], [background hex]
Supporting element: [logo / prop / arrow / number]
Emotional tone: [tone from Step 1]
```

Then ask:

> Here's the brief. Say "generate" to output the image prompt or tell me what to change.

## Step 4. Output the Gemini prompt

Once approved, output the image generation prompt in a code block:

```
Using the attached reference photo of me, generate a YouTube thumbnail at 1280 x 720 pixels (16:9).

Composition:
- Place me [left / right / centre] filling [30-50]% of the frame
- My expression: [tone details — e.g., shocked with wide eyes and open mouth]
- My gaze: [direction — e.g., looking directly at camera / looking off-frame toward the text]

Text:
- Display "[hook phrase]" in large bold sans-serif typography
- Text colour: [hex]
- Text outline: [colour, thickness for readability]
- Text placement: [specific area]

Colour palette:
- Primary: [hex]
- Accent: [hex]
- Background: [hex] — [describe treatment: flat, gradient, blurred scene, etc.]

Supporting element: [specific description of the supporting visual]

Constraints:
- Face must be clear and sharp
- Text must be readable at 320px wide (YouTube mobile size)
- No watermarks, no YouTube UI elements, no bottom-right corner text
- High contrast between face, text, and background
```

Tell the user:

> Paste this into a new Gemini chat, attach your reference photo, enable Create Image, and select Nano Banana. Generate at 1280x720.

## Step 5. Offer the next move

> Want me to outline the video next? Hook, mid, CTA from the thumbnail. Or call the create skill if you have one.

## Rules

- 1280x720 pixels (16:9). YouTube's native thumbnail size.
- Never include the reference photo path in the prompt itself — the user attaches the photo separately.
- Never allow more than 6 words of text, 5 is ideal, 3 is best.
- Face must always be a visible focal point. No face-hidden compositions.
- Never use em dashes.
- British English unless voice.md specifies otherwise.
- If brand-kit.md is in the project, read it and use exact brand colours.
- Recommend the user keep a consistent thumbnail style across videos for channel recognition.


================================================================================

## 2. Expert Skill: graphic-designer
> **Path within category:** `skills/graphic-designer/SKILL.md`


# Graphic Designer

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise. Do not explain options. Start immediately.

## Step 1. Read the post

Check the project for the most recent post file. If found, read it. If not, say:

> Paste the post you want a graphic for.

Wait for the post, then call AskUserQuestion:

```json
[
  {
    "question": "What type of graphic fits this post best?",
    "header": "Style",
    "multiSelect": false,
    "options": [
      {"label": "HTML/CSS graphic", "description": "Clean structured layout. Framework, comparison, steps, data. Fully editable, screenshot to export."},
      {"label": "Whiteboard infographic", "description": "Hand-drawn marker style on a whiteboard or notebook page. Recaps the post visually. Generated in Gemini."},
      {"label": "Branded infographic", "description": "Professional infographic using your brand colours. Recaps the post visually. Generated in Gemini."},
      {"label": "You decide", "description": "Analyse the post and pick the best format automatically"}
    ]
  }
]
```

If "You decide": analyse the post. If it contains numbered steps, frameworks, comparisons, or data tables, go Path A (HTML/CSS). If it recaps a workflow, shares tips, teaches a concept, or tells a story, go Path B (image prompt) and pick whichever style fits better.

## Path A: HTML/CSS structured graphic

Design constraints:
- 1200 x 1400 pixels (LinkedIn optimal)
- Dark background (#1a1a2e or user's brand colour) with high contrast text
- Clean sans-serif font (Inter, system-ui)
- White or light text on dark background
- One accent colour for highlights and dividers
- 40px minimum padding on all sides
- No stock photo backgrounds
- Let the post content dictate how many sections the graphic has. 3 steps = 3 blocks. 10 tips = 10 blocks. The constraint is legibility, not a fixed number. Every element must be large enough to read on a mobile screen.

Single self-contained HTML file with inline CSS. Include viewport meta tag.

Extract the core framework or steps from the post. Do not copy the full post. Distil into:
- A short headline (5 to 8 words)
- Key points as visual blocks (Unicode icons fine)
- Footer with author name from about-me.md if available

Save the HTML file. Tell the user:

> Open the HTML in your browser and screenshot it.

## Path B: Image generation prompt

The graphic must recap the post content visually. It is not an abstract illustration or stock photo. It summarises the key information from the post in a visual format the reader can scan.

First, extract the content for the infographic from the post:
- The main headline or hook (shortened to 5 to 10 words)
- 3 to 6 key points, steps, or takeaways (one short line each)
- Any numbers, stats, or data worth highlighting
- A footer line (author name and CTA if appropriate)

Then build the prompt based on the chosen style.

### Style 1: Whiteboard infographic

Use this prompt template. Fill in the content sections from the post.

```
Generate a single image of a physical, hand-drawn infographic on a large whiteboard or notebook page.

Crucial Style Instructions (Read First):
Medium: The image must look like a photograph of a real whiteboard or large paper notepad.
Texture: All elements must look created by hand using colored marker pens (black, blue, red, green) and highlighters (yellow/orange). Lines should be slightly imperfect, wobbly, and have the texture of ink on a surface.
No Digital Fonts: All text, headings, and bullet points must appear handwritten or hand-printed in marker pen.

Layout: Structure the 1080x1350 image as follows:

TITLE (large, bold marker, top of page):
[Insert headline from the post]

CONTENT (hand-drawn sections with marker pen):
[Insert 3 to 6 key points, each as a short hand-written line with a bullet, number, or small icon drawn next to it]

[If there are stats or numbers, draw them large with a circle or box around them]

Use multi-colored markers for emphasis. Keep text large and legible. Make everything look hand-drawn with slight imperfections. Make it look like a photograph of an actual notebook page.

Always include the handwritten text "[Author name from about-me.md] | Repost" at the bottom of the image, in the same hand-drawn marker style.
```

### Style 2: Branded infographic

Ask the user for brand colours if not already known. If about-me.md exists, check there first.

```
Generate a professional infographic image at 1080x1350 pixels.

Style: Clean, modern, editorial. Flat design with sharp edges and strong typography. No 3D effects, no gradients, no stock photos.

Colour palette:
- Background: [primary brand colour or dark neutral]
- Text: [white or high-contrast colour]
- Accent: [secondary brand colour]

Layout:
HEADLINE (top, large bold text):
[Insert headline from the post]

BODY (structured sections, each with an icon or number):
[Insert 3 to 6 key points as short lines, each with a visual marker: numbered circle, checkmark, or simple icon]

[If there are stats, display them as large feature numbers with a label underneath]

FOOTER:
[Author name from about-me.md] | [CTA or tagline if appropriate]

Keep text large and scannable. Maximum 40 words on the entire image. No decorative borders. No watermarks. No logos unless the user provides one.
```

Output the complete prompt in a code block. Tell the user:

> Paste this into Gemini or your image generator. The prompt is ready to go.

## After either path

Say:

> Graphic ready. Say "score my post" when you want feedback before publishing.

## Rules

- Always read the post before designing. The graphic must recap the post content, not illustrate an abstract concept.
- Structured graphics (Path A) must be a single HTML file with inline CSS.
- Image prompts (Path B) must be fully self-contained. The user pastes it cold into Gemini and gets the graphic.
- Extract and distil the post content into the graphic. No copying the full post text.
- Whiteboard style: always hand-drawn marker look, imperfect lines, coloured pens, notebook/whiteboard texture.
- Branded style: always clean, flat, modern, using the user's brand colours.
- Never use em dashes in any output.
- British English throughout.


================================================================================

## 3. Expert Skill: voice-builder
> **Path within category:** `skills/voice-builder/SKILL.md`


# Voice Builder

## CRITICAL: Auto-start on load

The moment this skill is loaded, installed, uploaded, or triggered, you MUST immediately run Step 1 below. This means your very next message to the user is the interview questions. Nothing else.

Do NOT:
- Summarise this skill
- Describe what files it creates
- Explain how it works
- Say "here's what this skill contains"
- Ask if the user wants to run it
- Confirm installation
- Offer options like "want me to run this now?"

Do THIS:
- Go straight to Step 1
- Send the interview questions as your first and only response

This applies whether the user uploaded a .skill file, said "build my voice", pasted samples, or triggered the skill in any other way. No preamble. No summary. Interview first.

## Step 1. Run the About Me interview

You MUST call the AskUserQuestion tool to ask these questions. Do not type the questions as chat text. Use the tool. The tool renders as an interactive form the user fills in, which is a better experience than typing answers into chat.

AskUserQuestion supports a maximum of 4 questions per call, so send two calls: Batch 1 first, wait for answers, then Batch 2.

### Batch 1 (your very first action, no text before it)

Call AskUserQuestion with this exact JSON structure for the questions parameter:

```json
[
  {
    "question": "What is your name and what do you do?",
    "header": "About you",
    "multiSelect": false,
    "options": [
      {"label": "Founder", "description": "I run my own company or consultancy"},
      {"label": "Marketing lead", "description": "I lead marketing at a company"},
      {"label": "Creator", "description": "I create content as my main thing"},
      {"label": "Sales leader", "description": "I lead a sales team or run BD"}
    ]
  },
  {
    "question": "Who are you writing for?",
    "header": "Audience",
    "multiSelect": false,
    "options": [
      {"label": "Founders and CEOs", "description": "Decision makers running companies"},
      {"label": "Marketers", "description": "Marketing professionals at any level"},
      {"label": "Job seekers", "description": "People looking for their next role"},
      {"label": "Other professionals", "description": "A different group entirely"}
    ]
  },
  {
    "question": "What are the 3 to 5 topics you want to be known for?",
    "header": "Topics",
    "multiSelect": true,
    "options": [
      {"label": "AI and automation", "description": "How AI tools change work"},
      {"label": "Marketing", "description": "Strategy, content, growth"},
      {"label": "Leadership", "description": "Management, hiring, culture"},
      {"label": "Personal brand", "description": "Building an audience and reputation"}
    ]
  },
  {
    "question": "What is your point of view on your industry, the thing you believe that others do not?",
    "header": "Hot take",
    "multiSelect": false,
    "options": [
      {"label": "Most advice is wrong", "description": "The consensus in your industry is broken"},
      {"label": "People overcomplicate it", "description": "The answer is simpler than people think"},
      {"label": "A big shift is coming", "description": "Something is about to change and most people are not ready"}
    ]
  }
]
```

### Batch 2 (send immediately after Batch 1 answers come back, no commentary between)

Call AskUserQuestion again with:

```json
[
  {
    "question": "What is the one thing you want people to think when they see your name?",
    "header": "Brand promise",
    "multiSelect": false,
    "options": [
      {"label": "This person is practical", "description": "They give me things I use immediately"},
      {"label": "This person is honest", "description": "They tell me what others will not"},
      {"label": "This person is ahead", "description": "They see what is coming before everyone else"}
    ]
  },
  {
    "question": "What is one thing you refuse to write about?",
    "header": "Off limits",
    "multiSelect": false,
    "options": [
      {"label": "Politics", "description": "No political takes, ever"},
      {"label": "Personal life", "description": "Keep it professional only"},
      {"label": "Competitors", "description": "No naming or shaming other people or brands"}
    ]
  }
]
```

After both batches are answered, move to Step 2. If any answer is blank or skipped, ask that specific question once more in chat, then move on.

## Step 2. Write about-me.md

Create about-me.md in the project root. Use this structure:

```
# About Me

## Name and role
[From question 1]

## Audience
[From question 2, expanded into 2 to 3 sentences on who the reader is]

## Topic pillars
[3 to 5 topics from question 3, one line each]

## Point of view
[From question 4, the contrarian or distinctive belief, written as a clear statement]

## Brand promise
[From question 5, the one thought the author wants to own in the reader's head]

## Off limits
[From question 6, topics or angles never to write about]
```

Keep it under 300 words. Every line should be something Claude would reference when writing.

## Step 3. Ask for the samples

Say this:

> Now paste 3 to 5 pieces of writing you want me to learn from. These can be LinkedIn posts, newsletter issues, essays, blog posts, emails, tweets, or any other writing you have published. They can be yours or someone whose voice you admire. One piece per message or all at once. If you do not have any samples ready, type "use samples" and I will load a starter set you can swap out later.

Wait for the user to paste. Minimum 3 samples before moving to analysis. If they paste fewer than 3, ask for more.

If the user types "use samples", load the writing from `references/sample-content.md` inside this skill folder. Tell the user which author the samples are from so they know what voice they are borrowing. Remind them they can replace these with their own writing later.

## Step 4. Analyse the samples

Read every sample. Look for patterns across all of them, not individual quirks from one piece. Extract:

**Voice signals**
- Average sentence length
- Paragraph rhythm (single line breaks, blank lines, staccato versus flowing)
- Hook or opening style (contrarian, question, data point, story, confession, observation)
- Point of view (first person, second person, observational)
- Tone (deadpan, warm, blunt, playful, clinical)
- Signature phrases or recurring words
- CTA or closing style

**Structural signals**
- Length range
- Lists versus prose
- How they open, how they close
- How they handle transitions

**Topic signals**
- Subjects that come up across multiple samples
- Who the audience appears to be
- What the author stands for

**Absence signals**
- Words and punctuation consistently absent (for example, em dashes in 0 of 5 samples)
- Hook types the author never uses
- Tones the author never hits
- Structures the author avoids

## Step 5. Write voice.md

Create voice.md in the project root. This is a single integrated profile covering both how the voice writes and what the voice avoids. No separate voice file.

```
# Voice Profile

## Who I sound like
[2 to 3 sentences describing the overall voice in plain language]

## Tone
[3 to 5 attributes the voice consistently hits, followed by 1 to 2 tones the voice never hits, drawn from gaps in the samples]

## Sentence rhythm
[Average length, pacing, paragraph structure. Include avoidance patterns: e.g. never staccato fragments, never tricolons, no sentences over 25 words]

## Hook patterns
[3 to 5 hook types observed, with one example each from the samples. Note any hook types absent across all samples, e.g. never rhetorical questions, never "imagine a world where"]

## How I open
[1 to 2 sentences. Note opening moves the voice avoids if a clear pattern of avoidance exists across samples]

## How I close
[1 to 2 sentences, include CTA style. Note closing moves the voice avoids, e.g. never motivational summaries, never "in conclusion"]

## Signature phrases
[Recurring words or phrases from the samples]

## Off-limits
[Words, punctuation, or constructions absent from every sample. Only list items the samples clearly avoid. Examples: no em dashes (0 of 5 samples), no hashtags, no corporate jargon by name]

## What this voice never does
[3 to 5 specific behaviours drawn from gaps in the samples. Be specific. If the samples never use the "not X, but Y" construction, list it. If they avoid a specific vocabulary set, name the words]
```

Fill every section from the actual samples. No generic filler. If a pattern is not present, say so. Do not duplicate audience or topic pillars from about-me.md.

The Off-limits and What this voice never does sections are drawn from observation, not from a generic banned-words template. Every item must be backed by absence across the samples.

## Step 6. Confirm and hand off

Tell the user:

> Your voice profile is built. Two files are now in your project: about-me.md and voice.md. Every time you work in this project, I will reference both automatically. You can open and edit either file anytime.
>
> You are ready to go. Here is what you can do next:
>
> - Say "build my newsletter voice" to create newsletter-specific writing instructions
> - Say "write a post" to draft a LinkedIn post in your voice
> - Say "design a graphic" to create a visual for a post
> - Say "score my post" to get feedback on a draft
> - Say "optimize my profile" to rebuild your LinkedIn profile
>
> Each of these is a separate skill. Pick one and go.

## What this skill produces

Two files in the project root:

1. about-me.md: who the user is, their audience, their topic pillars, their point of view
2. voice.md: the integrated voice profile, covering positive signals (how the voice writes) and absence signals (what the voice avoids) in one document

## Rules

- When this skill triggers, go straight to Step 1. No summary, no explanation, no preamble.
- Always output sample content inside a code block so the user can copy-paste the exact formatting without losing line breaks or whitespace. Use a plain code block (triple backticks with no language tag).
- Work from what is in the samples. Do not invent patterns that are not there.
- Minimum 3 samples for pattern detection. Ask for more if fewer than 3.
- If samples contradict each other, note the contradiction in voice.md rather than smoothing it over.
- Keep about-me.md under 300 words.
- Keep voice.md under 500 words.
- British English throughout unless the samples are clearly American.
- Never use em dashes in any output file or in any draft.
- Do not produce an voice.md file. Absence signals live inside voice.md.


================================================================================

## 4. Expert Skill: quote-post
> **Path within category:** `skills/quote-post/SKILL.md`


# Quote Post

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise.

## Step 1. Get the caption

Ask:

> Paste the caption this quote will accompany. The quote should reinforce the caption's message.

Wait for the caption.

## Step 2. Generate quote options

Return 9 viral motivational quote options, grouped into 3 categories of 3 quotes each:

- **Category 1: Growth and transformation** (e.g., "You don't find the time. You make it.")
- **Category 2: Resilience and grit** (e.g., "Your setback is someone else's setup.")
- **Category 3: Contrarian / bold** (e.g., "Stop asking for permission to start.")

Every quote must:

- Be under 15 words
- Feel human and authentic, not corporate
- Avoid jargon or overly technical language
- Work as a standalone line without context
- Punch hard in the first 3 words

Output format:

```
QUOTE OPTIONS for your caption

1. Growth and transformation
   a. [quote]
   b. [quote]
   c. [quote]

2. Resilience and grit
   a. [quote]
   b. [quote]
   c. [quote]

3. Contrarian / bold
   a. [quote]
   b. [quote]
   c. [quote]
```

Then ask:

> Which one lands best for your audience? Reply with the number and letter (e.g. 2b) or paste your own quote if none hit.

## Step 3. Get the reference image

Once the user has picked a quote, ask:

> Paste or describe the reference image you want to recreate. Pinterest, LinkedIn, or Google Images all work. If you don't have one, I will suggest a style.

If the user describes a style instead of uploading an image, recommend:

- **Notebook / hand-drawn** style (simple sketch, cream background, pen marks)
- **Minimalist editorial** (large serif type, lots of white space, one accent colour)
- **Bold poster** (heavy sans-serif, solid colour block background, high contrast)
- **Polaroid or film photo** with text overlay

## Step 4. Output the Gemini prompt

Output the following prompt in a code block, with the quote filled in:

```
Recreate the attached reference image with the following quote:

"[CHOSEN QUOTE]"

Critical constraints:
- Output at exactly 1080 x 1350 pixels (4:5 vertical)
- Match the style, typography, and colour palette of the reference image
- Keep the quote as the focal point — centred and legible
- Attribute nothing (no names, no handles, no logos)
- Maintain the visual tone of the original but with the new text

The quote must be perfectly spelled and punctuated exactly as written above.
```

Tell the user:

> Paste this into a new Gemini chat with the reference image attached. Create Image mode, Nano Banana model, 1080x1350 output.

## Step 5. Honest expectation-setting

After the prompt, add:

> Quote posts get strong engagement but lower impressions than other formats. It is not the strongest content type. But for the effort, the return is worth it. This takes minutes.

## Rules

- Always generate at 1080x1350. Horizontal quote graphics get lost on the LinkedIn feed.
- Never allow more than 15 words in the final quote. Longer quotes lose readability.
- Never fabricate attribution. Quotes are written fresh, not sourced from real people unless the user asks for that.
- Never use em dashes in any output.
- British English unless voice.md specifies otherwise.
- Tune the quote options to the user's voice if voice.md exists.
- If the user's voice is explicitly not motivational (analytical, contrarian-only, dry), flag the mismatch and ask if quote posts suit their positioning before generating.


================================================================================

## 5. Expert Skill: post-scorer
> **Path within category:** `skills/post-scorer/SKILL.md`


# Post Scorer

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise. Do not explain the scoring method. Start immediately.

## Step 1. Get the post

If the user already pasted a post in the same message, use it. Otherwise say:

> Paste the LinkedIn post you want scored.

Wait for the post.

## Step 2. Load scoring data

The scorer needs two things: the user's voice system and real performance data.

### Voice system

Read about-me.md and voice.md from the project if they exist. If missing, note it and score without voice matching.

### Performance data

Check for cached LinkedIn data in the project or outputs folder. Look for files matching *-all-posts.json or *-posts.txt.

If cached data exists, use it. If not, ask the user:

```json
[
  {
    "question": "To score your post against real data, I need your LinkedIn history. How should I get it?",
    "header": "Data source",
    "multiSelect": false,
    "options": [
      {"label": "Scrape my posts", "description": "Pull my last 100 posts from LinkedIn via Apify. Takes 1 to 2 minutes, costs about $0.50."},
      {"label": "Use Charlie Hills data", "description": "Score against Charlie Hills benchmarks (1,872 avg engagement, 500 posts analysed). Good fallback."},
      {"label": "Skip data scoring", "description": "Score against generic best practices only. Less accurate but instant."}
    ]
  }
]
```

If "Scrape my posts":
1. Ask for their LinkedIn username
2. Call Apify actor apimaestro/linkedin-profile-posts with input: { "username": "[their-username]", "total_posts": 100 }
3. Download results (do NOT use the fields parameter, it strips engagement data)
4. Save as [username]-all-posts.json in the project
5. Proceed to analysis

If "Use Charlie Hills data":
Look for cached Charlie data at **/linkedin-data/charlie-all-posts.json. If found, use it. If not, note you are using the benchmarks from this skill file (listed below).

If "Skip data scoring":
Fall back to voice-system-only scoring and general best practices.

## Step 3. Analyse the top performers

When performance data is available, run this analysis before scoring:

1. Calculate engagement score for every post: total_reactions + (comments x 3)
2. Identify the top 10% of posts by engagement score
3. From those top posts, extract:
   - Hook types that appear most often (contrarian, number-led, bold claim, personal story, question, news)
   - Average post length (word count)
   - Format distribution (text only, image, carousel, video)
   - CTA patterns (newsletter mention, comment gate, repost ask, question, none)
   - Topic clusters that over-index on engagement
   - Sentence rhythm (average sentence length, paragraph breaks per post)
4. Also note the bottom 10% patterns to identify what fails

Save these patterns as a "scoring profile" you reference for each criterion.

## Step 4. Score the post

Score across 5 criteria. Each scored 1 to 10.

### Hook strength (1 to 10)

Compare the draft's opening line to the hook types in the top 10%.
- Does it use a hook type that historically performs for this author?
- Is it specific with a number, name, or concrete detail?
- Would it stop a scroll based on what actually stops scrolls in their data?
- Score 8+ only if the hook type matches a pattern in their top 10%

### Voice match (1 to 10)

If voice.md exists:
- Does the post match tone, rhythm, sentence length from voice.md?
- Does it violate any rule in voice.md's absence patterns section (what the voice never does)?
- Does the sentence length match the average from their top performers?
If no voice files: score against the patterns extracted from their post data.

### Value density (1 to 10)

Compare to the user's top-performing posts:
- Do their best posts teach, give steps, share data, or tell stories?
- Does this draft match that value pattern?
- Is the takeaway specific enough that someone would save or share it?
- Compare word count to their top 10% average. Flag if way over or under.

### Structure and format (1 to 10)

Based on their data:
- What format (text, image, carousel) gets the most engagement for them?
- Does the draft's structure match the line break and paragraph rhythm of top posts?
- Is the post scannable on mobile?
- Does the CTA match patterns from their best performers?

### Publish readiness (1 to 10)

- Did the user actually write this or does it read like unedited AI output?
- Would this post blend naturally into their feed based on their posting history?
- Are there any red flags: banned words listed in voice.md's absence patterns, generic phrases, corporate tone?
- Is it the right length compared to their top performers?

## Step 5. Output the scorecard

Output in a code block:

```
LINKEDIN POST SCORE

Data source: [their posts / Charlie Hills benchmarks / generic]
Posts analysed: [number]
Top 10% avg engagement: [number]

Hook strength:         [X] / 10  [hook type detected]
Voice match:           [X] / 10
Value density:         [X] / 10
Structure and format:  [X] / 10  [format: text/image/carousel]
Publish readiness:     [X] / 10
----------------------------------------
TOTAL:                 [XX] / 50

VERDICT: [One sentence referencing specific data]

TOP PERFORMER COMPARISON:
Your top posts average [X] words, use [hook type] hooks,
and include [CTA pattern]. This draft [matches/differs] because [specific reason].

FIXES:
1. [Specific fix backed by data, e.g. "Your top 10% posts open with numbers. This opens with a question. Switch to a stat."]
2. [Second fix backed by data]
3. [Third fix if needed]
```

Every fix must reference the user's actual data. Not "improve the hook" but "your top 10% posts use number-led hooks (42% of hits). This draft uses a question hook (12% of hits). Lead with the stat instead."

## Step 6. Offer next steps

After the scorecard:

> Want me to rewrite the weakest section using patterns from your top posts, or ship it?

If rewrite requested, apply the fixes and output the revised post in a code block.

## Fallback benchmarks (when no data available)

Use these Charlie Hills benchmarks as the scoring baseline when the user picks "Use Charlie Hills data" and no cached file is found:

Average engagement: 1,872 (reactions + comments x 3)
Average reactions: 808
Average comments: 355
Average reposts: 61
Comment-to-reaction ratio: 44%

Top hook types: number-led (31%), bold claim (27%), contrarian (18%)
Top formats: carousel (33%), image (29%), text only (22%)
Average post length top 10%: 180 to 250 words
CTA rate: 45% mention newsletter
Comment gate rate: 5%

## Rules

- Always try to use real data before falling back to generic advice.
- Every score and every fix must reference specific data points, not subjective opinions.
- Never score higher than 8 unless the draft genuinely matches top 10% patterns.
- Be honest. A generous scorer is useless.
- If data is stale (14+ days old), suggest a refresh before scoring.
- Inform the user before running an Apify scrape (costs money).
- Never use em dashes in any output.
- British English throughout.
- Keep the scorecard compact. It needs to look good on a big screen at events.


================================================================================

## 6. Expert Skill: reels-scripting
> **Path within category:** `skills/reels-scripting/SKILL.md`


# Reels Scripting

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise.

## Prerequisites

This skill needs:

- `APIFY_API_TOKEN` environment variable (Instagram scraping)
- `GOOGLE_AI_API_KEY` environment variable (Gemini 2.5 Flash video analysis)
- Node.js 18+ and the `apify-client` and `@google/generative-ai` packages

If either env var is missing, tell the user to run:

```
! export APIFY_API_TOKEN=your_token
! export GOOGLE_AI_API_KEY=your_key
```

Then stop until both are set.

## Step 1. Get the reference

Ask:

> Paste the reference Reel URL or Notion link. This is the outlier Reel you want to reverse-engineer the format from.

Wait for the URL.

If the user pastes a Notion link, follow it via WebFetch, locate the Instagram Reel URL on the page, and extract it. If no Reel URL is found on the Notion page, ask the user to paste the Reel URL directly.

## Step 2. Get the newsletter topic

Ask:

> What's the topic from your newsletter you want to repurpose into this Reel? Paste the relevant newsletter section, or type the core idea in a sentence.

Wait for the topic. Read newsletter-voice.md, voice.md, and about-me.md from the project if they exist, so the script matches the user's voice.

## Step 3. Scrape and download the Reel

Create `~/Desktop/Reels/` if it does not exist. Write a Node.js script at `~/Desktop/Reels/analyse-reel.js` that:

1. Uses `apify-client` to call `apify/instagram-reel-scraper` with `{ directUrls: [reelUrl], resultsLimit: 1 }`. If that returns no items, fall back to `{ urls: [reelUrl], resultsLimit: 1 }`, then `apify/instagram-scraper` with `{ directUrls: [reelUrl], resultsType: 'posts', resultsLimit: 1 }`.
2. Extracts `videoUrl` from the returned item.
3. Downloads the video to `~/Desktop/Reels/downloads/{username}_{shortCode}.mp4`.
4. Saves raw scrape data to `~/Desktop/Reels/reel_data_{shortCode}.json`.

Run the script. Confirm file size and metadata (views, likes, comments, caption first 200 chars) before continuing.

## Step 4. Analyse with Gemini 2.5 Flash

Extend the Node script (or run a second pass) that:

1. Reads the downloaded `.mp4` as base64.
2. Calls `genAI.getGenerativeModel({ model: 'gemini-2.5-flash' })`.
3. Sends the video with this exact prompt:

```
I'm studying this Reel to write my own script in a similar style for my audience of [AUDIENCE FROM about-me.md].

## Full Transcript
- Transcribe EVERY word with timestamps

## Hook
- Exact first words spoken
- Word count of the hook
- What makes it stop the scroll?

## Language Patterns
- Average sentence length
- You/your vs I/me ratio
- Transitions between points
- Where are the 'just' minimisers?

## Structure
- Total duration
- Section breakdown with timings
- What's the before/after moment?
- What's the CTA?

## One key insight
- The single most important technique to learn from this Reel
```

Save the analysis to `~/Desktop/Reels/analysis_reference_{shortCode}.md`.

## Step 5. Write the new Reel script

Using the analysis from Step 4, the newsletter topic from Step 2, and the user's voice files, write a new Reel script to `~/Desktop/Reels/reel-[slug].md`.

Apply these rules (non-negotiable):

### Hook
- Never open with "I". Use "this", "you", a fact, or a name drop.
- Proven formats: "This changed... forever" / negative flip ("X is useless unless...") / capability statement.
- Hook creates curiosity or pattern interrupt within 3 seconds.
- Mirror the hook's word count and structure from the reference analysis.

### Body
- British English. Short sentences. No em dashes, no semicolons.
- Use "you" and "just" conversationally ("you just drop in...").
- Never merge three or more staccato fragments. Combine into one flowing sentence.
- Never state the conclusion. Let the facts do the work.
- No "link in bio". Use comment automation.

### Comment trigger
- Single caps word only (SCRIPT, WIKI, PROMPTS, VIDEO).
- Must directly relate to what is being promised.
- No quotes, no "below", no trailing punctuation.

### CTA
- "Comment [WORD] and I'll send you [specific thing]"
- Short. No "the link to my full" padding.

### Duration and structure
- Target 30 to 45 seconds total.
- 2 key points maximum, not 3.
- Caption mirrors the script. Update both together.

### Script file structure

```
# Reel: [title]

## Reference analysis
- URL: [reel url]
- Views: [number]
- Key technique: [from Gemini analysis]

## Duration target
30-45 seconds

## Hook (0-3s)
[Exact words]

## Point 1 ([start]-[end]s)
[Exact words]

## Point 2 ([start]-[end]s)
[Exact words]

## CTA ([start]-[end]s)
[Exact words including "Comment [WORD]"]


## Visual notes
[Cuts, B-roll ideas, text overlays]
```

## Step 6. QA loop

Score the script against the rules in Step 5. Every violation must be fixed. Re-score until the script hits 95/100. Never show the user anything below 95.

Common violations to check:
- Opens with "I"
- Staccato fragments of three or more
- States the conclusion
- Multi-word or stylised comment trigger
- Duration over 45 seconds when read aloud
- 3 points instead of 2
- Caption does not mirror script

## Step 7. Offer the pipeline

After the script is approved, offer:

> Two paths from here:
>
> 1. Record it yourself.
> 2. Auto-generate with ElevenLabs (voice) + HeyGen (avatar) + Remotion (motion graphics). If you have the my-video project configured, run `npm run pipeline:claude-routines` with this script config.

## Rules

- Never skip the 95/100 QA gate.
- Always read voice.md and about-me.md before writing. Voice match is non-negotiable.
- Never invent metrics from the reference Reel. Use only what Apify returns.
- British English. No em dashes. No semicolons.
- Every script deliverable includes the exact caption and comment trigger alongside the script. Never deliver just the script.
- If the reference Reel scrape fails across all three actor variants, report the failure and stop. Do not fabricate analysis.
- Gemini 2.5 Flash is the model. Do not substitute without the user's approval.


================================================================================

## 7. Expert Skill: niche-research
> **Path within category:** `skills/niche-research/SKILL.md`


# Niche Research

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise the research method.

## Prerequisites

This skill needs live browsing. Use this order of preference:

1. **Claude for Chrome extension** (preferred). Check that the extension is enabled and Claude has permission to browse on the current tab. If not, tell the user:
   > Enable the Claude for Chrome extension and open a blank tab. I need to drive the browser to scroll Reddit, X, and run Google searches with verified dates.
2. **Playwright MCP** as a fallback if the Claude for Chrome extension is not available.
3. **WebSearch + WebFetch tools** as a last resort (less thorough on feed scrolling).

Pick the best available path and continue.

## Step 1. Gather the niche

Call AskUserQuestion:

```json
[
  {
    "question": "What niche do you want to research?",
    "header": "Niche",
    "multiSelect": false,
    "options": [
      {"label": "I will type my niche", "description": "Type the exact niche phrase after this"},
      {"label": "Pull from about-me.md", "description": "Use the niche and audience already in my voice files"}
    ]
  }
]
```

If the user picks "Pull from about-me.md", read the file from the project root. If the file does not exist or does not name a clear niche, fall back to asking the user to type it.

## Step 2. Browse like a human researcher

Drive the browser through these actions in order. Verify publish dates on every item. Exclude anything older than 7 days from today without exception.

### 2a. Reddit feed scanning

1. Navigate to https://www.reddit.com/ (home feed).
2. Scroll the feed. Load more posts.
3. Open niche-relevant posts. On each post, check the "posted X days ago" timestamp.
4. Discard posts older than 7 days.
5. Repeat with https://www.reddit.com/r/popular/.
6. Also search any niche-specific subreddits that come up while scrolling.

### 2b. X (Twitter) feed scanning

1. Navigate to https://x.com/home (For You feed).
2. Scroll multiple screens.
3. Open full threads for niche-relevant tweets.
4. Check the post timestamp on each thread.
5. Discard posts older than 7 days, even if engagement is high.

### 2c. Google web search

Run these searches one by one, open the top results, verify publish dates.

- `[niche] news` (set Tools → Any time → Past week)
- `[niche] launch` (past week)
- `[niche] controversy` (past week)
- `[niche] research` (past week)
- `[niche] regulation` (past week)

For each promising result:

1. Open the page.
2. Locate the visible publish date.
3. Verify it is within the last 7 days.
4. If the date is missing, unclear, or older than 7 days, exclude it.

## Step 3. Synthesise into themes

Collect a broad pool of verified, in-window items. Group related items into themes. Each theme may combine social discussion and news coverage.

Select themes that show at least two of:

- Strong attention or discussion
- Clear disagreement or debate
- Novel insight or new information
- Real-world implications for the niche

Target 20 themes. Fewer is acceptable if genuinely limited.

## Step 4. Output

First line before the table:

```
As of [DD/MM/YYYY]
```

Then a markdown table with these exact columns:

```
| Theme / Emerging Story | Platforms (Reddit, X, News) | Key Communities / Accounts / Sources | Representative Links | Attention Signals | What's Happening or Being Debated | Why It Matters for [NICHE] | Shareable Angle |
```

No prose outside the table.

## Step 5. Offer the next move

After the table, ask:

> Any row here you want me to turn into a LinkedIn post? Call the post-writer skill with the row number, or the post-formatter skill to apply a framework.

## Rules

- Never invent links, metrics, or dates.
- Exclude anything older than 7 days without exception.
- Verify every publish date before including an item. No shortcuts.
- Table only at the end. No commentary, no summary paragraph.
- If fewer than 20 themes pass the filter, say so. Do not pad with weak items.
- If Claude for Chrome is not available and neither Playwright MCP nor WebSearch can cover feed scrolling properly (Reddit and X), tell the user what is missing rather than faking the scan.
- British English throughout. DD/MM/YYYY date format.
- Never use em dashes.


================================================================================

## 8. Expert Skill: gemini-carousel
> **Path within category:** `skills/gemini-carousel/SKILL.md`


# Gemini Carousel

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise.

## Step 1. Gather inputs

Ask:

> Paste the content you want in the carousel. A post, section of a newsletter, research notes, or a framework all work.

Wait for the content, then call AskUserQuestion:

```json
[
  {
    "question": "Brand style?",
    "header": "Style",
    "multiSelect": false,
    "options": [
      {"label": "Pull from brand-kit.md", "description": "Use the colours and typography in my project brand file"},
      {"label": "I will type brand colours", "description": "I will paste hex codes and font preferences"},
      {"label": "Suggest for me", "description": "Pick a palette and typography based on the content"}
    ]
  },
  {
    "question": "Number of slides?",
    "header": "Slides",
    "multiSelect": false,
    "options": [
      {"label": "6 slides", "description": "Concise, fast read"},
      {"label": "8 slides", "description": "Standard carousel length"},
      {"label": "10 slides", "description": "Deep-dive carousel"}
    ]
  }
]
```

## Step 2. Build the design brief

Analyse the content and produce a slide-by-slide brief with:

- **Slide 1 (Cover)**: hook, large bold text, visual direction
- **Slides 2 to N-1 (Body)**: one idea per slide, max 15 words per slide, visual suggestion
- **Slide N (CTA)**: repost ask, name, link or offer

For each slide include:

- Slide number
- Headline (max 8 words)
- Body text (max 15 words)
- Visual suggestion (icon, colour block, illustration, diagram)

Tell the user:

> Here is the design brief. Tell me what to change, or say "generate" when you are happy.

Wait for approval. Do not proceed until the user explicitly approves.

## Step 3. Output per-slide prompts

Once approved, output one Gemini image generation prompt per slide, each in its own code block, numbered clearly.

Every prompt follows this structure:

```
Act as an expert graphic designer. Create a LinkedIn carousel slide at 1080x1350 pixels (4:5 aspect ratio).

Brand style:
- Primary colour: [HEX]
- Secondary colour: [HEX]
- Accent colour: [HEX]
- Typography: [bold industrial headline font, clean geometric body font]
- Aesthetic: modern, authoritative, high contrast

Slide [N of M]: [slide purpose]

Content:
- Headline: "[headline text]"
- Body: "[body text]"
- Visual element: [specific visual suggestion]

Layout instructions:
- [Headline placement and size]
- [Body placement and size]
- [Visual placement]
- [Background treatment]

Constraints:
- Vertical 4:5 aspect ratio at exactly 1080x1350 pixels
- No watermarks, no logos unless specified above
- Maintain visual consistency with the other slides in the set
```

Tell the user:

> Paste each prompt into a new Gemini chat with Create Image enabled and Nano Banana selected. Generate slides one at a time for maximum control over consistency.

## Step 4. Offer one-shot alternative

After the per-slide prompts, offer:

> Want a single combined prompt that generates the full carousel in one shot? Faster but less visual consistency. Say "combine" and I will rewrite.

## Rules

- Always gate on user approval of the brief before outputting image prompts.
- 1080x1350 pixels per slide. No other aspect ratio.
- Maximum 15 words of body text per slide. Readability loses on the feed.
- Keep the brand style identical across every slide prompt so the set looks like one carousel.
- Cover slide (1) and CTA slide (last) must be visually distinct from body slides.
- Never use em dashes.
- British English unless voice.md specifies otherwise.
- If brand-kit.md exists in the project, read it and use its exact hex codes and typography choices.


================================================================================

## 9. Expert Skill: pinned-comment
> **Path within category:** `skills/pinned-comment/SKILL.md`


# LinkedIn Pinned Comment + Image Prompt Skill

## Why This Skill Exists

The post delivers value. The pinned comment builds personality, trust, and rewatch value. It is where Charlie drops the polished creator mask and talks like a real person.

Funny is subjective and easy to miss. This skill exists to make hilarious pinned comments REPEATABLE so anyone on the team (Smriti, Ansh, etc.) can produce them at Charlie's standard.

## The Core Insight (read this first)

The image carries the joke. The comment captions the image.

If the comment makes sense without the image, the comment is doing too much work. If the image needs the comment to be funny, the image is too weak.

This is why image generation comes FIRST. Always.


## THE 4-LINE RULES (non-negotiable)

- Exactly 4 lines. No more, no less.
- Each line is one complete sentence.
- Each line is 40 characters max.
- Start with 📌 on line 1.
- No P.S. (line 4 IS the punchline)
- No line breaks between sentences (they sit tight together)
- British English throughout
- No em dashes, no hashtags, no semicolons
- Avoid Charlie's banned word list (just, that, very, really, actually, literally, etc.)


## OTHER PROVEN IMAGE GAGS (for reference)

- **Status reversal at the desk:** Laptop in the chair wearing a tie, Charlie on the floor in pyjamas
- **The shrine:** Candles, a rose, a framed Anthropic logo, a handwritten letter "To Dario", Charlie kneeling in prayer
- **The banquet table:** Charlie at the head of the table with a paper crown, every other seat occupied by a tech logo (Stanford, Google, OpenAI, Anthropic, Microsoft)
- **The therapist's couch:** Charlie reclining looking happy, therapist looking concerned, Claude logo framed on the wall behind her
- **The boardroom:** Charlie pointing at a presentation, every "executive" in the room is a tech logo
- **The pub vs the home office:** Charlie smug at a pub table while his laptop visibly works through a window across the street


## OUTPUT FORMAT

When triggered, always output:

1. **The admission** (one sentence, what the post is quietly confessing)
2. **The image prompt** (full paragraph in the standard format)
3. **The 4-line comment** (with 📌)
4. **A one-line note** confirming the comment passed the 5 tests

Optionally provide 2-3 variations if the first attempt is borderline.


================================================================================

## 10. Expert Skill: gemini-infographic
> **Path within category:** `skills/gemini-infographic/SKILL.md`


# Gemini Infographic

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise the process.

## Step 1. Get the source content

Ask:

> Paste the content you want to turn into an infographic. A post, newsletter section, blog, research note, or raw bullet points all work.

Wait for the content.

## Step 2. Build the brief

Analyse the content and produce an infographic brief in plain language. Include:

- **Title** (6 words or fewer, punchy)
- **Subtitle** (optional, one line of context)
- **Core structure**: decide between steps, framework, comparison, stats, or list
- **Key points**: 3 to 7 bullets max, each 10 words or fewer
- **Visual suggestions**: arrows, boxes, highlighted numbers, icons, color accents. Be specific about placement and colour.
- **Footer CTA**: handwritten text reading "Follow [Name] [Tagline] for more helpful content | Repost ♻️"

Tell the user:

> Here is the brief. Tell me what to change, or say "generate" when you're happy.

Wait for approval.

## Step 3. Output the Gemini prompt

Once approved, output the full prompt in a code block, with the brief inserted into the `[INSERT YOUR INFOGRAPHIC CONTENT AND LAYOUT HERE]` placeholder:

```
Generate a single image of a physical, hand-drawn infographic on a large whiteboard or notebook page.

Crucial Style Instructions (Read First):

Medium: The image must look like a photograph of a real whiteboard or large paper notepad.

Texture: All elements must look created by hand using colored marker pens (black, blue, red, green) and highlighters (yellow/orange). Lines should be slightly imperfect, wobbly, and have the texture of ink on a surface.

No Digital Fonts: All text, headings, and bullet points must appear handwritten or hand-printed in marker pen.

Layout: Structure the 1080x1350 image as follows:

[INSERT THE BRIEF HERE — title, subtitle, core structure, key points, visual suggestions]

Use multi-colored markers for emphasis. Keep text large and legible. Make everything look hand-drawn with slight imperfections. Make it look like a photograph of an actual notebook page.

Always include the handwritten text "Follow [Name] [Tagline] for more helpful content | Repost ♻️" at the bottom of the image, in the same hand-drawn marker style.
```

Tell the user:

> Paste this into a new Gemini chat with Create Image enabled and Nano Banana selected. Generate at 1080x1350.

## Step 4. Offer iteration

After the prompt, offer:

> If the first generation misses, tell me what to adjust and I will rewrite the prompt. Common fixes: fewer colours, bigger title, different layout direction.

## Rules

- 1080x1350 pixel output is non-negotiable. Vertical format owns the LinkedIn feed.
- Footer CTA always includes the recycle symbol and "Repost".
- Never use em dashes in any output.
- Keep bullets under 10 words. Longer text loses legibility at the whiteboard scale.
- Always wait for user approval of the brief before outputting the final prompt.
- British English unless voice.md says otherwise.
- If the user has brand-kit.md or colours.md in the project, bake their brand colours into the visual suggestions.


================================================================================

## 11. Expert Skill: newsletter-voice
> **Path within category:** `skills/newsletter-voice/SKILL.md`


# Newsletter Voice

## Prerequisites check

The moment this skill is triggered, check the project root for voice.md and about-me.md.

If either file is missing, tell the user:

> Newsletter voice sits on top of your general voice profile. Run voice-builder first (upload the skill or say "build my voice"), then come back here once about-me.md and voice.md are in the project.

Then stop. Do not continue until both files exist.

If both files exist, read them fully, then go straight to Step 1.

## Step 1. Check for samples

Ask the user in chat:

> Do you have 2 to 3 past newsletter issues I can learn from?
>
> Yes: paste them here (one per message or all at once)
> No: type "archetype" and I will build from a template tuned to your voice

Wait for response.

If the user pastes 2 or more newsletters, go to Step 2a.
If the user types "archetype", go to Step 2b.
If the user pastes 1 newsletter, ask for at least one more. If they only have one, offer: "One sample is not enough for pattern detection. Want me to switch to archetype mode and use your one newsletter as a reference point?"

## Step 2a. Sample-based analysis

Read every newsletter fully. Look for patterns across issues, not one-off quirks. Extract:

**Opening formula**
- What the first 3 sentences do (specific result, cultural observation, claim, scene, question)
- Length of the opening section before the first structural break
- Credibility move (how the author establishes authority early)
- Value promise (what the reader is told they will get)

**Section structure**
- Problem or contrast setup
- Named framework or free prose
- Numbered steps, methods, or continuous argument
- Examples and evidence patterns
- Bonus or extension section
- Closing formula and signoff

**Data philosophy**
- Specific numbers per issue (count them)
- Source attribution style (linked, named, uncredited)
- Example-to-abstraction ratio
- Limitation or failure acknowledgements

**Formatting**
- Header usage (frequency, hierarchy)
- List usage (numbered, bulleted, arrows)
- Bold and italic usage
- Prompt, code block, or blockquote formatting
- Visual markers (arrows, checkmarks, emojis if any)

**Length**
- Word count range across samples
- Section word counts

**Voice markers unique to newsletter format**
- Pro tips or callouts (frequency, format)
- Forward-looking closings
- Signoff phrase if consistent across samples
- Meta-transparency (does the author reflect on the process or ask for feedback)

**Absence signals**
- Words, constructions, or structures absent from every sample
- Closing moves the author never uses
- Topics the author never touches

Then go to Step 3.

## Step 2b. Archetype selection

Call the AskUserQuestion tool with a single question:

```json
[
  {
    "question": "Which newsletter archetype fits what you want to write?",
    "header": "Archetype",
    "multiSelect": false,
    "options": [
      {"label": "Data tutorial", "description": "Numbers, frameworks, step-by-step methods with prompts"},
      {"label": "Contrarian essay", "description": "Take a position, defend it, name the opposition"},
      {"label": "Case study teardown", "description": "One subject per issue, unpacked in depth"},
      {"label": "Curated digest", "description": "5 to 7 links with your commentary each week"},
      {"label": "Personal essay", "description": "Reflection on a theme, story-first"},
      {"label": "Interview or profile", "description": "One person per issue, Q and A or narrative"}
    ]
  }
]
```

After the user picks an archetype, load the matching defaults from `references/archetypes.md` inside this skill folder. Tune every field using voice.md and about-me.md before writing newsletter-voice.md. Flag inside the output file that archetype defaults were used and the file should be revisited after 5 published issues.

## Step 3. Write newsletter-voice.md

Create newsletter-voice.md in the project root. Single file, 800 to 1,200 words target. Use this structure:

```
# Newsletter Voice

## Source
[Sample-based: analysed X newsletter issues] OR [Archetype-based: [archetype name] tuned to voice.md. Revisit after 5 published issues.]

## Audience and purpose
[Who reads this newsletter and what they get from it. Written from about-me.md and voice.md. 2 to 3 sentences.]

## Voice principles
[3 to 5 core principles the writing always holds. Each one a short declarative sentence. Tuned to this user's voice.md.]

## Opening formula
[How issues start. Include 2 concrete templates with bracketed placeholders, e.g. "[Specific result with number]. [Credibility marker]. [Value promise for this issue]." Target word count for the opening section.]

## Section flow
[Standard structure of an issue, section by section, 5 to 8 sections max. Brief notes on what each section does and how long it runs.]

## Data and evidence
[How numbers and examples are used. Specific rules, e.g. "every claim needs a number", "sources linked inline", "example-to-abstraction ratio roughly 3:1".]

## Formatting rules
[Headers, lists, bold, italic, code blocks, visual markers. What to use, what to avoid. Drawn from samples or archetype defaults.]

## Closing and signoff
[How issues end. Forward-looking statement versus summary. Signoff phrase if a consistent one exists across samples (do not invent one).]

## What this newsletter never does
[1 short paragraph or 3 to 5 items. Drawn from absence patterns across samples or archetype defaults. Behaviours only, not a banned-words list.]

## Length
[Word count target for standard issues. Separate target for longer comprehensive guides if the user writes both formats.]
```

Fill every section from the samples (or tuned archetype defaults). No generic filler. If the samples do not cover something, say "no clear pattern across samples" rather than guessing.

## Step 4. Confirm and hand off

Tell the user:

> Your newsletter voice is built. newsletter-voice.md is in your project root alongside about-me.md and voice.md. When you want to draft an issue, say "write a newsletter" and I will use all three files together.
>
> [If archetype mode: Remember this file was built from archetype defaults. After 5 or so published issues, re-run this skill with your real samples for a sharper profile.]

## What this skill produces

One file in the project root:

- newsletter-voice.md: newsletter-specific writing instructions covering audience, voice principles, opening formula, section flow, data philosophy, formatting, closing, absence patterns, and length targets

## Rules

- Require voice.md and about-me.md in the project root before running. Stop and redirect to voice-builder if either is missing.
- Minimum 2 newsletter samples if the user chooses sample-based mode. Offer archetype mode if fewer.
- Keep newsletter-voice.md under 1,200 words. Tight beats exhaustive.
- Do not invent voice signals. Work only from samples or archetype defaults tuned to voice.md.
- Do not duplicate content from voice.md. Reference it where relevant. newsletter-voice.md adds newsletter-specific rules only.
- Do not bake in the user's specific names, URLs, or signoff phrases unless they appear consistently across 2 or more samples.
- Do not produce a separate voice or banned-words file. Absence patterns live inside newsletter-voice.md as a single section.
- British English throughout unless samples are clearly American.
- Never use em dashes in any output file or in any draft.


================================================================================

## 12. Expert Skill: post-formatter
> **Path within category:** `skills/post-formatter/SKILL.md`


# Post Formatter

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise. Start input gathering immediately.

## Step 1. Gather inputs

Call AskUserQuestion:

```json
[
  {
    "question": "What topic do you want to post about?",
    "header": "Topic",
    "multiSelect": false,
    "options": [
      {"label": "I will type the topic", "description": "Single sentence describing the subject"},
      {"label": "Paste a context dump", "description": "Notes, stats, transcripts to turn into a post"}
    ]
  },
  {
    "question": "Which framework?",
    "header": "Framework",
    "multiSelect": false,
    "options": [
      {"label": "PAS", "description": "Problem, Agitation, Solution"},
      {"label": "AIDA", "description": "Attention, Interest, Desire, Action"},
      {"label": "BAB", "description": "Before, After, Bridge"},
      {"label": "STAR", "description": "Situation, Task, Action, Result"},
      {"label": "SLAY", "description": "Story, Lesson, Actionable advice, You"},
      {"label": "Pick for me", "description": "Recommend the best framework based on the topic"}
    ]
  }
]
```

Ask one follow-up:

> Anything else I should know? Facts, stats, tone notes, or who this is for.

Wait for response.

## Step 2. Write the post

Apply these global rules to every output:

- Maximum 20 lines, 200 to 250 words total (~1,200 characters)
- Blank line after every line
- Most lines: one sentence, 55 characters or fewer
- Up to 4 lines may be mini-paragraphs (2 to 3 sentences, 110 characters or fewer)
- Grade 6 words. Zero adverbs, zero jargon, zero fluff
- No em dashes
- No questions unless the hook itself is a question
- No emojis except checkmarks for numbered lists (1. 2. 3.) and the recycle symbol in the CTA
- Rule of Three: use at most two trios per post
- Vary sentence starts. Do not over-use "I"

## Step 3. Structure

- **Line 1 (Hook)**: Bold. 50 characters or fewer.
- **Line 2 (Twist / Contrast)**: 50 characters or fewer. Opposes or surprises the hook.
- **Lines 3 to 18 (Core)**: The chosen framework, split across 3 to 5 lines per stage. Any list inside a stage must have exactly three items (1. 2. 3.). Use arrows to show flow where useful.

Framework maps:

- **PAS**: Problem -> Agitation -> Solution
- **AIDA**: Attention -> Interest -> Desire -> Action
- **BAB**: Before -> After -> Bridge
- **STAR**: Situation -> Task -> Action -> Result
- **SLAY**: Story -> Lesson -> Actionable advice -> You

- **Lines 19 to 20 (Wrap and CTA)**: 2 to 3 lines that lock the lesson. Close with one of these phrases followed by the recycle symbol: "Repost if", "Repost this", or "If this helped, repost".

## Step 4. Output

Output the finished post inside a code block. No preamble, no trailing notes.

## Step 5. Offer the next move

After the post, ask:

> Want a matching graphic (graphic-designer skill) or want me to score it against your post history (post-scorer skill)?

## Rules

- Return the finished post only. No meta-commentary.
- Enforce line length, word count, and lines count limits. Count them.
- Never use em dashes.
- British English unless voice.md specifies otherwise.
- If the user has voice.md in the project, tune tone and rhythm to match it.
- If a trio is used, it has exactly three items. Not two, not four.


================================================================================

## 13. Expert Skill: hook-generator
> **Path within category:** `skills/hook-generator/SKILL.md`


# Hook Generator

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise. Do not explain what makes a good hook.

## Step 1. Get the topic

If the user already pasted a topic in their message, use it and skip to Step 2.

Otherwise ask:

> What topic do you want hooks for?

Wait for response.

## Step 2. Write 6 hook variations

Every hook has the same structure:

- **Line 1 (Opening)**: 40 characters maximum. No questions. States something unexpected, specific, or punchy.
- **Line 2 (Contrast)**: 40 characters maximum. Contradicts, reframes, or undercuts the opening.

Every variation must:

- Include at least one "How I" or "I" statement across the two lines
- Include a digit or metric where possible
- Follow clickbait principles: tension, curiosity gap, stakes

Produce 6 variations covering different angles:

1. **Number-led**: Lead with a specific number or metric
2. **Contrarian**: State a belief then flip it
3. **Personal transformation**: Before vs after with a digit
4. **Authority steal**: Reference a name, tool, or brand
5. **Admission**: Confess a mistake or loss
6. **Future shock**: A prediction or "X is about to change"

## Step 3. Output format

```
HOOKS for [topic]

1. [Number-led]
[Line 1]
[Line 2]

2. [Contrarian]
[Line 1]
[Line 2]

3. [Personal transformation]
[Line 1]
[Line 2]

4. [Authority steal]
[Line 1]
[Line 2]

5. [Admission]
[Line 1]
[Line 2]

6. [Future shock]
[Line 1]
[Line 2]
```

## Step 4. Offer the next move

Ask:

> Want me to build one of these into a full post? Call the post-formatter skill with the hook number.

## Rules

- 40 characters maximum per line. Count them.
- No questions in the opening line.
- No em dashes.
- No filler words. Every word earns its place.
- Prefer digits over spelled numbers (3, not three).
- British English unless voice.md says otherwise.
- Never hedge. A weak hook is worse than no hook.


================================================================================

## 14. Expert Skill: content-matrix
> **Path within category:** `skills/content-matrix/SKILL.md`


# Content Matrix

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise. Start input gathering immediately.

## Step 1. Gather inputs

Check the project for about-me.md. If it exists, read it and pre-fill the description of who the user is. Skip that question and tell the user what you pulled.

If about-me.md is missing, ask:

> Give me at least two paragraphs describing who you are, what you do, and what you like to discuss. The more specific you are, the more relevant the ideas.

Wait for response.

Then call AskUserQuestion:

```json
[
  {
    "question": "What are your content pillars?",
    "header": "Pillars",
    "multiSelect": false,
    "options": [
      {"label": "I will type them", "description": "I have 3 to 4 content pillars to use"},
      {"label": "Pull from voice.md", "description": "Use the topics already defined in my voice files"},
      {"label": "Suggest them for me", "description": "Based on my about-me.md, recommend 4 pillars"}
    ]
  }
]
```

If the user types their own, accept 3 to 5 pillars. If fewer than 3, ask for more.

If the user picks "Suggest them for me", read about-me.md, propose 4 pillars covering their positioning, and ask them to confirm or edit before continuing.

## Step 2. Build the matrix

Generate a markdown table with:

- X axis (columns): 8 content formats, always in this order:
  1. Actionable
  2. Motivational
  3. Analytical
  4. Contrarian
  5. Observation
  6. X vs Y
  7. Present vs Future
  8. Listicle
- Y axis (rows): the user's 3 to 5 pillars

Every cell contains one specific, concrete post idea tailored to the pillar and format. Not generic. Not reusable across pillars.

Format definitions to apply when filling each cell:

- **Actionable**: Ultra-specific how-to. Teaches the reader to do one thing.
- **Motivational**: Inspirational story about someone who did something extraordinary in the niche.
- **Analytical**: Breakdown of why something works the way it does.
- **Contrarian**: Go against the common advice in the niche and back it up.
- **Observation**: A hidden, silent, or underdiscussed trend the user has noticed.
- **X vs Y**: Compare two entities (tools, styles, frameworks, companies).
- **Present vs Future**: Current state vs a specific prediction, with the why.
- **Listicle**: A list of resources, tips, mistakes, lessons, or steps.

Each cell's idea should be a specific headline, not a theme. Good: "The 3-line hook formula I stole from David Ogilvy". Bad: "Hooks".

## Step 3. Output (surface-aware)

Pick the output mode based on the surface you are running on. Do not output the table in a fenced markdown code block — that renders as monospace plain text and makes a 5×8 grid hard to scan.

- **Claude.ai or Claude Cowork (chat surfaces with interactive chart support):** render the matrix as an interactive chart / interactive table widget. Pillars as rows, formats as columns, each cell holding one specific headline. The user should be able to click a cell to see the full headline and any expansion notes. Do not also dump the table as markdown — the chart is the deliverable.
- **Claude Code (file-system surface, has Write/Edit tools):** save the matrix to `content-matrix-YYYY-MM-DD.md` in the current working directory and print the same table inline in the response as a plain markdown table (no triple-backtick wrap). Confirm the file path so the user can open it.
- **Fallback (no interactive chart, no file-system tools):** output a plain markdown table inline. Still no code-fence wrap.

Below the table or chart, add one sentence naming the single strongest idea across the matrix and why.

## Step 4. Offer the next move

Ask:

> Any cell here you want me to write as a full post? Reference the cell by pillar + format (for example "Hooks × Contrarian") and I will hand it to the post-writer or post-formatter skill.

On Claude Code, also offer to append the drafted post into the same `content-matrix-YYYY-MM-DD.md` file under the cell reference.

## Rules

- Minimum 3 pillars, maximum 5. More than 5 dilutes the matrix.
- Every cell idea must be specific to that pillar AND that format. Do not reuse the same idea across pillars.
- Tune the language to the user's voice if voice.md exists.
- British English unless voice.md specifies American.
- Never use em dashes.


================================================================================

## 15. Expert Skill: analytics-dashboard
> **Path within category:** `skills/analytics-dashboard/SKILL.md`


# Analytics Dashboard

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1.

## Step 1. Get the export file

Ask:

> Upload your LinkedIn Analytics export file (xlsx).
>
> Not sure how to get it? Go to LinkedIn Analytics, set your date range (30, 60, or 90 days works well), and click Export in the top right.

Wait for the file upload.

## Step 2. Parse the data

Read every sheet in the file. Expect these sheets:

- **DISCOVERY**: overall impressions and reach
- **ENGAGEMENT**: daily impressions and engagements over time
- **TOP POSTS**: top 50 posts, ranked by engagements and by impressions (two tables to merge)
- **FOLLOWERS**: daily new followers plus total count
- **DEMOGRAPHICS**: job titles, locations, industries, seniority, company size, top companies

Clean any messy headers. Merge the two TOP POSTS tables (by engagements and by impressions) into one unified dataset per post. De-duplicate.

## Step 3. Build the interactive dashboard

Create a single React artifact. Dark theme (background `#0f1117`), accent colours for charts. Use Recharts for all visualisations.

Include these panels in this order:

### Headline metrics (top row cards)
- Total impressions
- Total reach
- Total new followers
- Average daily impressions
- Average daily engagements
- Average engagement rate (engagements / impressions)
- Total posts tracked

### Engagement trend (line chart)
- Daily impressions (left y-axis) and engagements (right y-axis) over the full date range
- Highlight the top 3 spike days with markers

### Follower growth (area chart)
- Daily new followers
- 7-day moving average trendline overlaid
- Cumulative follower gain

### Post performance scatter
- X axis: impressions. Y axis: engagements
- Colour-code posts into four quadrants:
  - **Stars**: high reach + high engagement
  - **Viral but shallow**: high reach + low engagement
  - **Niche gold**: low reach + high engagement
  - **Underperformers**: low reach + low engagement
- Hoverable dots showing post URL and date

### Day-of-week heatmap
- Average impressions and engagements by day of week
- Highlight the strongest days

### Audience breakdown (bar charts)
- Job titles
- Industries
- Seniority
- Company size
- Top locations

### Formatting rules
- Format numbers: `67K` not `67000`, `1.2M` not `1200000`
- Total follower count prominent at the top
- Responsive layout (works on laptop and large display)
- Dark background, high contrast chart colours

## Step 4. Written strategic analysis

Below the dashboard, write a concise analysis with these sections:

### Performance Summary
- Trajectory: growing, plateauing, or declining (use trendlines)
- Current engagement rate and how it compares to LinkedIn benchmarks for accounts this size

### Top Post Patterns
- Analyse top 10 by impressions and top 10 by engagements
- Patterns: posting day, time of month, content themes
- High impressions + low engagement: what does that signal?
- Low impressions + high engagement: what does that signal?

### Audience-Content Fit
- Who the core audience is, based on demographics
- Which content topics and formats would resonate
- Segments to lean into or away from

### Growth Velocity
- Average daily follower growth
- 30, 60, 90 day projections at current pace
- Acceleration or deceleration trends

### Day and Timing Strategy
- Best days for impressions
- Best days for engagement
- Optimal posting schedule based on the data

### 5 Specific Content Recommendations
Each one includes:
- Content angle or topic
- Why the data supports it
- Which audience segment it targets
- Expected impact based on patterns in the data

## Step 5. Offer the next move

After the analysis:

> Want me to draft one of these 5 recommendations as a full post? Call the post-writer or post-formatter skill with the recommendation number.

## Rules

- Use numbers, not adjectives. "Engagement rate is 2.3%" beats "engagement is healthy".
- Keep the analysis direct. No fluff, no filler.
- Never invent metrics not present in the export.
- Flag data quality issues (missing columns, odd date ranges) instead of silently working around them.
- Never use em dashes.
- British English unless voice.md specifies otherwise.
- Recommend running this monthly. Patterns only surface over time.


================================================================================

## 16. Expert Skill: profile-optimizer
> **Path within category:** `skills/profile-optimizer/SKILL.md`


# Profile Optimizer

## CRITICAL: Auto-start on load

When this skill triggers, go straight to Step 1. Do not summarise. Do not explain what you will produce. Start input gathering immediately.

## Step 1. Gather inputs

Check the project for about-me.md. If it exists, pre-fill name, audience, topics, and POV from it. Skip those questions and tell the user what you pulled.

Call AskUserQuestion in two batches.

### Batch 1

```json
[
  {
    "question": "What is the primary goal of your LinkedIn presence?",
    "header": "Goal",
    "multiSelect": false,
    "options": [
      {"label": "Booked calls", "description": "Drive discovery calls or demos"},
      {"label": "Inbound leads", "description": "Attract prospects who reach out to you"},
      {"label": "Newsletter subscribers", "description": "Grow your email list from LinkedIn"},
      {"label": "Job opportunities", "description": "Get recruiters and hiring managers to reach out"}
    ]
  },
  {
    "question": "What is your main offer or service?",
    "header": "Offer",
    "multiSelect": false,
    "options": [
      {"label": "Coaching", "description": "1-on-1 or group coaching"},
      {"label": "Consulting", "description": "Advisory or strategy work"},
      {"label": "Agency services", "description": "Done-for-you services for clients"},
      {"label": "Freelance", "description": "Project-based or contract work"}
    ]
  },
  {
    "question": "Do you have brand colours (hex codes)?",
    "header": "Colours",
    "multiSelect": false,
    "options": [
      {"label": "No, suggest for me", "description": "Pick colours based on my positioning"},
      {"label": "Yes, I will paste them", "description": "I have specific hex codes to use"}
    ]
  },
  {
    "question": "Any social proof you want highlighted?",
    "header": "Proof",
    "multiSelect": false,
    "options": [
      {"label": "Years of experience", "description": "e.g. 10+ years in marketing"},
      {"label": "Client results", "description": "e.g. Helped 200+ clients"},
      {"label": "Media features", "description": "e.g. Featured in Forbes"},
      {"label": "I will type my own", "description": "Let me paste specific proof points"}
    ]
  }
]
```

### Batch 2

```json
[
  {
    "question": "What external links do you want in your Featured Section? (max 2)",
    "header": "Links",
    "multiSelect": false,
    "options": [
      {"label": "Booking page + newsletter", "description": "Primary link to book calls, secondary to subscribe"},
      {"label": "Portfolio + booking page", "description": "Show work first, then convert"},
      {"label": "I will paste URLs", "description": "I have specific links to use"}
    ]
  },
  {
    "question": "How should I get your current profile?",
    "header": "Current profile",
    "multiSelect": false,
    "options": [
      {"label": "I will paste it", "description": "I will copy-paste my headline, about, and experience"},
      {"label": "Start fresh", "description": "Ignore my current profile, build from scratch using my about-me.md"},
      {"label": "I will upload a screenshot", "description": "I will share a screenshot or PDF of my profile"}
    ]
  }
]
```

Wait for all inputs before proceeding.

## Step 2. The Headline

Write 3 headline options. Output in a code block.

Constraints:
- Maximum 50 characters each
- Sentence casing only (not Title Case)
- Lead with core value
- Include target audience where character count allows
- No job titles (no "Founder" / "CEO" / "Designer")
- No fluff words

Format: [Core value] + [for target audience]

```
Option 1 (Direct): [outcome + audience]
Option 2 (Pain-focused): [problem + audience]
Option 3 (Differentiator): [unique angle + audience]
```

Then call AskUserQuestion to let the user pick:

```json
[
  {
    "question": "Which headline do you want to go with?",
    "header": "Headline",
    "multiSelect": false,
    "options": [
      {"label": "Option 1", "description": "[The actual headline text from above]"},
      {"label": "Option 2", "description": "[The actual headline text from above]"},
      {"label": "Option 3", "description": "[The actual headline text from above]"}
    ]
  }
]
```

## Step 3. The About Section

Output in a code block. Formatting rules:
- Write in full sentences. Do not force line breaks mid-sentence.
- One line break between sentences or short phrases for readability.
- Double line break between sections (hook, story, authority, CTA).
- LinkedIn handles text wrapping on mobile and desktop. Do not manually wrap at 50 or 60 characters.
- Short punchy sentences are good. Chopping sentences in half is not.

Structure: Hook > Struggle/Empathy > Method/Philosophy > Authority > CTA

Tone: Punchy, direct, human. Not corporate.

Example of correct formatting:
```
I left my 9-to-5 in September 2024.
Two years later: 200k+ followers, multiple six-figure businesses, thousands of marketers trained.

Here is what I learned.
Most people do not need more content. They need a system that turns content into clients. That is what I build.

✦ Linked Agency: done-for-you LinkedIn content for founders and executives.
✦ Vislo: an AI design tool that creates publish-ready infographics in minutes.
✦ MarTech AI newsletter: 200k+ readers getting weekly AI marketing frameworks.
✦ The AI Creators Club: live breakdowns, proven systems, and a community that helps you grow in weeks, not months.

Brand partnerships and speaking: hello@influencermoso.com

Check out my Featured section below. Or DM me. I will point you in the right direction.
```

## Step 4. The Experience Section

Rewrite the top 2 roles. Output in a code block. Same formatting approach as the About section: full sentences, no forced mid-sentence line breaks, LinkedIn handles wrapping.

Structure per role: Context > Challenge > Action > Result

Storytelling format, not bullet points. 8 to 15 sentences per role maximum.

Example of correct formatting:
```
I walked into a team that had lost 3 managers in 2 years.
Morale was gone. Revenue was slipping.

I didn't start with strategy decks. I started with listening.

Within 6 months we rebuilt the culture.
Within 12 months revenue was up 40%.

That taught me everything about leading through chaos.
```

Example of incorrect formatting:
- Managed a team of 15 sales representatives
- Responsible for Q3 revenue targets
- Implemented new CRM system

## Step 5. Featured Section Strategy

2 items maximum. Both must be external links.

Item 1: Primary conversion goal
- Purpose: direct path to main offer (booking page, application form, sales page)
- Title: 3 to 5 words, benefit-focused

Item 2: Secondary value builder
- Purpose: build trust or capture leads (newsletter signup, free resource, portfolio, case study)
- Title: 3 to 5 words, benefit-focused

No subtitles. No internal LinkedIn posts. No "DM me" items.

## Step 6. Visual Design Brief

Output 4 separate image generation prompts, each in its own code block. Each prompt must be fully self-contained and work when pasted into Gemini as a standalone request.

State the brand colours at the top:
- Primary hex: [user-provided or suggested]
- Secondary hex: [user-provided or suggested]
- One line on why these fit the positioning

### Asset 1: LinkedIn Banner (1584 x 396 pixels)

The prompt must:
- State "Using the attached photo of me..."
- Create banner at exact dimensions
- Place the chosen headline text centre-right
- Place a 5 to 8 word tagline below the headline
- Include a CTA button element (3 to 4 words)
- Include social proof text
- Use brand colours
- Specify background style

### Asset 2: Profile Picture (400 x 400 pixels)

The prompt must:
- State "Using the attached headshot photo as the base..."
- Apply brand colour background (solid or gradient)
- Centre face at 60 to 70% of frame
- Work when cropped to a circle
- Add brand colour border if appropriate

### Asset 3: Featured Section Tile 1 (552 x 368 pixels)

- Title text from Featured Item 1 as focal point
- Brand colours matching the banner
- Simple clickable visual cue (arrow icon)
- Clean, minimal, no subtitle or body text
- No photo needed

### Asset 4: Featured Section Tile 2 (552 x 368 pixels)

- Title text from Featured Item 2 as focal point
- Visually distinct from Tile 1 (swap primary/secondary colour usage)
- No photo needed

After all 4 prompts, say:

> Copy each prompt into a new Gemini chat one at a time. For the banner and profile picture, attach your headshot alongside the prompt. The featured tiles do not need a photo.

## Rules

- Always read about-me.md if it exists and pre-fill inputs from it.
- All profile copy (headline, about, experience) must go in code blocks.
- Write full sentences. Do not force line breaks mid-sentence. LinkedIn handles wrapping.
- No job titles in headlines.
- No block paragraphs anywhere.
- Each image prompt must be fully self-contained.
- Never use em dashes.
- British English throughout.
- Do NOT offer to write a launch post or engagement strategy after the design brief. End at the design brief.


================================================================================

## 17. Expert Skill: post-writer
> **Path within category:** `skills/post-writer/SKILL.md`


# Post Writer

## CRITICAL: Auto-start on load

The moment this skill triggers, go straight to Step 1. Do not summarise the skill. Do not explain what it does. Do not list the files it references. Jump to input gathering immediately.

## Step 1. Gather inputs

Check the project for about-me.md and voice.md. Read both. If either is missing, tell the user to run the Voice Builder skill first ("say build my voice"), then stop.

If both files exist, call AskUserQuestion with this exact JSON:

```json
[
  {
    "question": "What topic do you want to post about?",
    "header": "Topic",
    "multiSelect": false,
    "options": [
      {"label": "Paste a context dump", "description": "I have notes, transcripts, or raw ideas to turn into a post"},
      {"label": "I have a topic in mind", "description": "I will type the topic after this"},
      {"label": "Suggest topics for me", "description": "Based on my voice system, suggest 5 topics I should post about"}
    ]
  },
  {
    "question": "Do you have any reference posts you want me to use as structural inspiration?",
    "header": "References",
    "multiSelect": false,
    "options": [
      {"label": "No references", "description": "Write from scratch using my voice files only"},
      {"label": "I will paste examples", "description": "I have posts from other creators I want you to study first"},
      {"label": "Use my training posts", "description": "Reference the posts I used in the Voice Builder"}
    ]
  }
]
```

Based on the answers:
- "Paste a context dump": wait for the user to paste, extract the core idea, then proceed to Step 2
- "I have a topic in mind": wait for the user to type it, then proceed to Step 2
- "Suggest topics for me": read about-me.md topic pillars and voice.md, suggest 5 specific topics with a one-line angle for each, then use AskUserQuestion to let them pick one
- "I will paste examples": wait for reference posts, note the structural patterns, then proceed
- "Use my training posts": reference whatever posts are already in the project

## Step 2. Research and plan

Before writing, research the topic. Look for:
- Data points or statistics that support the angle
- Contrarian takes or surprising facts
- Real examples or case studies
- Common misconceptions to challenge

Then present a post plan. Call AskUserQuestion:

```json
[
  {
    "question": "Which angle works best for this post?",
    "header": "Angle",
    "multiSelect": false,
    "options": [
      {"label": "[Angle 1 name]", "description": "[One sentence describing the angle and hook]"},
      {"label": "[Angle 2 name]", "description": "[One sentence describing the angle and hook]"},
      {"label": "[Angle 3 name]", "description": "[One sentence describing the angle and hook]"}
    ]
  },
  {
    "question": "Which framework do you want?",
    "header": "Framework",
    "multiSelect": false,
    "options": [
      {"label": "PAS", "description": "Problem, Agitate, Solution"},
      {"label": "How-to list", "description": "Numbered steps or tips"},
      {"label": "Story to lesson", "description": "Personal story with a takeaway"},
      {"label": "Contrarian take", "description": "Challenge a common belief"}
    ]
  }
]
```

Fill in the actual angle options based on the topic research. Do not use placeholder text for the angle descriptions.

## Step 3. Write the draft

Write the post following these rules:
- Read voice.md for tone, rhythm, hook style, CTA style, and the absence patterns section (what the voice never does)
- Read about-me.md for audience and topic context
- Match the sentence length and paragraph rhythm from voice.md
- Avoid every banned word, structure, and pattern listed in voice.md's absence section
- Use the hook pattern that fits the chosen angle
- End with the CTA style from voice.md

Output the post inside a plain code block:

```
[The full post goes here with all line breaks and formatting exactly as it should appear on LinkedIn]
```

After the code block, add 2 to 3 sentences on why you chose this hook and structure, referencing specific patterns from voice.md.

## Step 4. Iterate

Ask the user:

> How does this feel? Tell me what to change, or say "ship it" and I will save the final version.

If the user gives feedback, revise and output a new code block. Maximum 3 revision rounds.

If the user says "ship it" or equivalent, save the final post as a markdown file in the project.

Then say:

> Post saved. Say "design a graphic" to create a visual, or "score my post" to get feedback before publishing.

## Rules

- Always read about-me.md and voice.md before writing.
- Always output posts in a plain code block.
- Never use em dashes in any post.
- British English unless voice.md says otherwise.
- Do not add hashtags unless voice.md explicitly uses them.
- Do not add engagement bait CTAs unless they appear in voice.md.
- Keep posts between 150 and 300 words unless the user requests otherwise.
- Plan before writing. Never skip Step 2.


================================================================================
