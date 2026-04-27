# Operations Frameworks · Index

The framework library `/operations-engine` reads from before
generating any operational output. Each framework comes from
operating-team systems that have shipped at scale.

## When to use which

| Framework | When |
|---|---|
| [four-disciplines-execution.md](four-disciplines-execution.md) | Weekly operating cadence · WIGs · lead vs lag measures · scoreboards |
| [atomic-habits-4-laws.md](atomic-habits-4-laws.md) | Designing routines that stick · the 4 laws of behavior change |
| [eos-level-10-meeting.md](eos-level-10-meeting.md) | The 90-min weekly L10 meeting · IDS · solo version included |
| [para-second-brain.md](para-second-brain.md) | 4-folder knowledge architecture · everywhere · forever |
| [eisenhower-matrix.md](eisenhower-matrix.md) | The 2-question prioritization · Q1/Q2/Q3/Q4 with the 80% Q2 rule |
| [sop-template.md](sop-template.md) | 5-section SOP structure · trigger/inputs/steps/outputs/QC |
| [automation-hierarchy.md](automation-hierarchy.md) | Eliminate → Automate → Delegate · in that order · always |

## How `/operations-engine` uses these

When generating Friday Weekly Wrap:

1. Reads BUSINESS-BRAIN.md for current Rocks + WIGs
2. Pulls metrics from Stripe, Notion, Gmail
3. Renders 4DX-style scoreboard (lead + lag measures)
4. Auto-generates L10 meeting agenda for Monday
5. Surfaces issues (off metrics + missed todos) for IDS
6. Suggests Q2 work for next week (Eisenhower)

When triaging inbox (Monday + ad-hoc):

1. Sorts emails into 3 buckets (respond / draft-and-send / archive)
2. Drafts replies for the middle bucket using the user's voice
3. Detects repeat questions → auto-generates SOP
4. Files SOPs in Resources (PARA structure)

When generating new SOPs:

1. Uses the 5-section template
2. Files by area in `purely-personal/sops/`
3. Indexes in BUSINESS-BRAIN.md § Operations

## The 7-day operating rhythm (combine all 7)

```
MON 09:00  ·  L10 meeting (or solo L10) · 4DX scoreboard review
MON 7am    ·  /marketing-engine fires · Q2 content block
TUE 8am    ·  /sales-engine fires · pipeline build
WED 8am    ·  /marketing-engine newsletter · Q2 content
THU 7am    ·  /sales-engine meeting prep · Q1 fires (real meetings)
FRI 17:00  ·  /operations-engine wrap · audit Q1/Q2/Q3/Q4 split
SUN 18:00  ·  /sales-engine pipeline report · prep next L10
```

Every routine produces Q2 leverage. The system trades Q3 noise
(reactive work) for Q2 compounding (the actual moat).

## Editing rules

- Files are LIVE · the engine reads them every run
- Edit any file to update behavior immediately
- Add new frameworks as new `.md` files · update this README
- Keep file names slug-style (kebab-case)

## Source canon (no name credit · structures only)

These frameworks compress the working principles from:
- 4 Disciplines of Execution · operating cadence
- Atomic Habits · 4 laws of behavior change · identity-based habits
- EOS · Level 10 meeting · IDS · quarterly Rocks
- Building a Second Brain / PARA · knowledge architecture
- Eisenhower Matrix · the urgent/important framing
- The 5-section SOP template · standard operating procedures
- Automation hierarchy · eliminate-automate-delegate · in that order
