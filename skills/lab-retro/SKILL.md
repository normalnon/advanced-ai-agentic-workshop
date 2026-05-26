---
name: lab-retro
description: "This skill walks a Claude Code Lab graduate through four sequential exercises that consolidate their learning, capture their best work, plan next s..."
---

# lab-retro

> **Path within category:** `lab-retro/SKILL.md`


# Claude Code Lab — Final Retrospective

This skill walks a Claude Code Lab graduate through four sequential exercises that consolidate their learning, capture their best work, plan next steps, and collect structured feedback for the organizer.

## How to run

Default flow: run all four parts in order. The user can also jump to a specific part with `/lab-retro 2` (or just say "part 3").

Between parts, briefly summarize what just happened and ask "ready for part N?" so the user controls the pace.

All artifacts are saved into a single folder `lab-retro-output/` in the current working directory:
- `01-progress.md`
- `02-best-prompt.md`
- `03-month-plan.md`
- `04-feedback.json` + `04-feedback-report.md`

Create the folder if missing.


## Part 2 — Best prompt

**Goal:** turn one prompt the participant is proud of into a reusable Skill.

Ask the participant: *"Скопируйте или опишите ваш самый полезный промт из лабы."*

Then `AskUserQuestion`:

1. **"Для какой задачи был промт?"** (singleSelect)
   - Автоматизация рутины
   - Создание контента/документации
   - Анализ данных/исследование
   - Прототипирование/разработка
   - Личный workflow / PKM

2. **"Что сделало его эффективным?"** (multiSelect)
   - Хороший контекст в CLAUDE.md
   - Чёткие критерии успеха
   - Разбиение на шаги
   - Использование Skills/MCP
   - Примеры в промте
   - Ограничения и анти-критерии

Reformat the prompt as a proper Skill (frontmatter + body), suggest an `description` line that would trigger it, and save to `lab-retro-output/02-best-prompt.md`. Suggest where to put it (`~/.claude/skills/<name>/SKILL.md`).


## Part 4 — Feedback for the organizer

**Goal:** structured feedback that goes back to the lab organizer.

`AskUserQuestion`:

1. **"Оцените лабу в целом (NPS)"** (singleSelect: 0–10)
2. **"Самая ценная встреча?"** (singleSelect: M01 / M03 / M05 / M07 / M09 / M11)
3. **"Самая ценная тема за все 6 недель?"** (multiSelect)
   - Основы Claude Code
   - Промтинг и контекст
   - Архитектура и субагенты
   - MCP / Skills / Hooks
   - Agent SDK и деплой
   - Evals и качество
   - AI-гигиена
4. **"Что улучшить?"** (free text)
5. **"Главное препятствие, с которым вы столкнулись?"** (free text)
6. **"Согласны ли поделиться отзывом публично?"** (singleSelect: да / да-анонимно / нет)

Save TWO files:
- `lab-retro-output/04-feedback.json` — structured for the organizer
- `lab-retro-output/04-feedback-report.md` — human-readable summary for the participant

**Then submit to the public proxy** (no secrets needed):

```bash
curl -sS -X POST https://lab-feedback-proxy.vercel.app/api/feedback \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg name "<participant name>" --slurpfile notes lab-retro-output/04-feedback.json '{name:$name, notes:($notes[0]|tostring)}')"
```

The proxy forwards to Baserow table 746002 with a server-side token. Response is `{"ok":true,"row_id":<N>}`. Confirm row ID with the participant.

If the request fails, fall back to local files only and tell the participant: "submit failed — your feedback is saved locally in `lab-retro-output/04-feedback.json`, send it to the organizer manually."
