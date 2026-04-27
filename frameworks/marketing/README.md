# Marketing Frameworks · Index

The framework library `/marketing-engine` reads from before drafting any
content. Each framework is canonical — pulled from operators who've
moved billions of dollars worth of marketing.

## When to use which

| Framework | When |
|---|---|
| [value-equation.md](value-equation.md) | Grade ANY offer, post, or pitch · 4 levers · math underneath every conversion |
| [hook-story-offer.md](hook-story-offer.md) | Default structure for ANY content · 3 parts in order |
| [storybrand-narrative.md](storybrand-narrative.md) | Brand spine · long-form pages · sales pages · "about" sections · 7-part hero structure |
| [linkedin-hooks.md](linkedin-hooks.md) | The 7 archetypes for the FIRST 210 characters · with templates and examples |
| [aida-pas-bab.md](aida-pas-bab.md) | The 3 classic copywriting frameworks · pick by audience awareness stage |
| [perfect-webinar.md](perfect-webinar.md) | Webinars · live launches · sales calls · 4-question close |
| [newsletter-structures.md](newsletter-structures.md) | 4 newsletter formats · 3-2-1 · curve · open loop · 5-bullet |
| [content-pillars.md](content-pillars.md) | 3-pillar authority system · weekly rhythm · audit |
| [hook-retain-reward.md](hook-retain-reward.md) | Algorithm-aware content principle · 6-minute rule |

## How `/marketing-engine` uses these

When generating a Monday Content Drop, the engine:

1. Reads the user's BUSINESS-BRAIN.md for voice, ICP, pillars
2. Reads the relevant framework files for the content type
3. Generates 3 LinkedIn variants (different archetypes from `linkedin-hooks.md`)
4. Each variant follows `hook-story-offer.md` structure
5. Applies `value-equation.md` as a final grading pass
6. Validates against `hook-retain-reward.md` 6-minute readiness

When generating a Wednesday Newsletter:

1. Reads `newsletter-structures.md` to pick format
2. Generates 3 subject lines (different patterns)
3. Writes the body in the picked structure
4. Closes with a reward line + ONE CTA

## Editing rules

- These files are LIVE · the engine reads them every run
- Edit any file to update the engine's behavior immediately
- Add new frameworks as new `.md` files · update this README
- Keep file names slug-style (kebab-case)
- Keep each file under ~500 lines · longer = ignored

## Adding your own frameworks

If you want to add a framework specific to YOUR business (e.g.,
"my-launch-checklist.md"), drop it in this directory and reference
it from `BUSINESS-BRAIN.md` § Voice section. The engine will pick it
up automatically on the next run.

## Source canon (no name credit · structures only)

These frameworks compress the working principles from:
- $100M Offers value-equation discipline
- DotCom/Expert Secrets hook-story-offer storytelling
- StoryBrand 7-part narrative structure
- The 7 LinkedIn hook archetypes from top operators
- AIDA / PAS / BAB · the 100-year copywriting canon
- Perfect Webinar 4-question close pattern
- The 3-2-1 / 5-Bullet newsletter forms used by major operators
- Algorithm-aware content principles from creator economy research
