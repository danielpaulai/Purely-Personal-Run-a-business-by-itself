# Purely Personal MCP v2

The connector behind **Build Your 1st AI Employee**. It turns the program's 12 skills into tools, and locks every one of them to the participant's **own** Business Brain, ICP and Voice DNA.

> v1 returned Daniel Paul's ICP and voice to everyone. v2 never does. No documents means a request for them, not someone else's voice. See [AUDIT.md](./AUDIT.md) for what changed and why.

## Add it to Claude (no sign-in)

**Connector address: `https://mcp-purelypersonal.vercel.app/mcp`**

Claude → Customize → Connectors → **Add custom connector** → paste the address → Add. There is no login, API key or OAuth step: the server advertises no authentication, so Claude connects straight away. Switch it on in the chat's connector menu and choose "Always allow".

Check it from a terminal any time: `curl https://mcp-purelypersonal.vercel.app/health`, or `python -m pp_mcp.smoke https://mcp-purelypersonal.vercel.app`.

## How it works

```
Claude Project knowledge                 every call
BUSINESS-BRAIN.md ─┐                     write_post(topic, brain=<full text>, icp=…, voice_dna=…)
ICP.md ────────────┼─ Claude reads them ─►          │
VOICE-DNA.md ──────┘  and passes them in            ▼
                                         WORK ORDER = skill method + YOUR voice lock + YOUR customer lock + hard rules
                                                       │  Claude writes it, then calls score_post / polish_post / de_ai_ify
```

**There are no tokens, accounts or stored profiles.** The participant's three Day 1 documents already live in their Claude Project, so Claude passes their full text in `brain` (and `icp`, `voice_dna` when it has them) on each call. The server reads them, answers, and keeps nothing. With no documents it asks for them; it has no default voice and no default customer.

A **work order** is the skill's method plus a parsed Voice Lock (word bank, signature phrases, banned list, writing rules, the test), a Customer Lock (the person, their words, objections, themes), the never-claim rules found in their own Brain, the output contract, and the exact quality calls to make before delivering. The calling Claude does the writing. The server never calls a language model, so it costs nothing to run.

The checks are real code, not prompts: scoring (Invisibility Diagnostic, personalised to the participant's own words), AI-tell detection, mechanical clean-up, platform polish, homework ranking, daily angle, prospect query, revenue and attribution reports.

## The 36 tools

| Family | Tools |
|---|---|
| **Your documents** | `check_my_brain` (readiness + exactly what is thin) · `get_icp` · `get_voice_dna` (read back what was understood, to reconcile with ICP.md / VOICE-DNA.md) · `get_setup_guide` |
| **12 skills** | `list_skills` · `get_skill` · `setup_marketing_employee` (ai-marketing-employee) · `build_voice_profile` (voice-profile-builder) · `write_post` (linkedin-post-writer) · `first_post_coach` · `write_carousel` (linkedin-carousel-builder) · `write_cheatsheet` (linkedin-cheatsheet-builder) · `weekly_content_drop` (weekly-content-engine) · `amplify_post` · `write_tweet` · `write_ig_caption` · `write_reel_script` (multi-platform-amplifier) · `analyze_competitor` (competitor-x-ray) · `find_prospects` (prospect-magnet) · `score_post` (invisibility-diagnostic) · `review_homework` (homework-reviewer) |
| **Also** | `write_newsletter` (newsletter-writer) |
| **Quality** (deterministic) | `score_post` · `polish_post` · `de_ai_ify` · `review_homework` |
| **Research** | `get_daily_prompt` · `list_post_templates` · `get_my_post_history` |
| **Design** | `get_brand_colours` · `generate_image` (renders with `OPENAI_API_KEY`, else returns a brief) |
| **Track** | `get_my_post_history` · `get_weekly_revenue_report` · `get_attribution_report` take `records=` (JSON rows from Notion / your CRM). `log_published_post` · `track_post_published` · `log_dm_received` · `log_call_booked` · `log_revenue_event` write to a private ledger on the **local install only** |

26 of the 29 v1 tool names are kept, so the Day 2 and Day 3 playbook prompts keep working. The three removed are the token tools (`set_my_context`, `get_my_context`, `clear_my_context`). Three prompts (slash commands) are added: `monday_content_drop`, `wednesday_market_scan`, `friday_prospect_run`. Each skill is also a resource at `pp://skills/{name}`.

## Languages

Works in English and German. Documents written in German parse completely (German section titles, German banned-list markers, `Niemals …` rules, `Sprache: Deutsch`). The writing tools write in the language in the Business Brain; `de_ai_ify`, `polish_post` and `score_post` detect German automatically (or take `language="de"`), apply German rules only, and match the participant's own banned phrases in inflected form. Other languages get the universal checks plus the participant's own banned list.

## Apify (prospecting and competitor analysis)

`find_prospects` and `analyze_competitor` use the **participant's own Apify connector** (their account, their credit). Each shows an estimated cost first (free-tier prices checked 2026-11-11: about $0.16 for 15 prospects, about $0.06 per competitor for 30 posts), accepts `budget_usd`, runs a 3-item test first, and stops cleanly on an Apify limit instead of retrying. With no Apify at all, paste the material instead: `candidates=` for prospects, `pasted_posts=` for competitors. Company pages (`linkedin.com/company/...`) use the company scrapers.

## Participant flow (what to tell them)

Nothing to set up beyond Day 1. In the project, the instructions say once:

> When you use the Purely Personal connector, read BUSINESS-BRAIN.md (and ICP.md, VOICE-DNA.md) from project knowledge and pass their full text in `brain`, `icp` and `voice_dna`. Never shorten them.

Then `check_my_brain` any time output feels generic. A thin brain is the usual cause. Put your never-claim rules, name, publishing language (`Language: …`) and brand colours (`Accent #xxxxxx`) in the Brain itself; the server reads them from there.

Post history and revenue reports live in the participant's own Notion / CRM (Day 3 already files every post there). Claude reads the rows and passes them as `records=`. The hosted connector cannot log anything because it cannot know who is calling.

## Run locally

```bash
cd mcp/purely-personal-mcp
pip install -r requirements.txt
python -m pytest -q                 # 100 tests: parsing, every tool, isolation, HTTP, stdio
python -m pp_mcp                    # stdio, for Claude Desktop / Claude Code
python -m pp_mcp --http 8000        # http://localhost:8000/mcp
```

Claude Desktop (stdio), `claude_desktop_config.json`:

```json
{ "mcpServers": { "purely-personal": { "command": "python3", "args": ["-m", "pp_mcp"], "cwd": "/abs/path/to/mcp/purely-personal-mcp" } } }
```

The local install is single-user, so it can keep your documents in a folder instead of being handed them each call: put `BUSINESS-BRAIN.md`, `ICP.md` and `VOICE-DNA.md` in `~/.purely-personal/` (or `PP_HOME`). It also keeps a private ledger there (`ledger.jsonl`) for the `log_*` tools. Documents passed on a call always win over the folder.

## Deploy (Vercel)

There is no database and no secret to configure. The handler is stateless (a fresh MCP session manager per request), so it needs no lifespan, no sticky sessions and no shared event loop.

1. **Vercel**: new project from this repo, **Root Directory = `mcp/purely-personal-mcp`**. Deploy to a **preview** first.
2. **Verify** the preview exactly as Claude would use it:
   ```bash
   python -m pp_mcp.smoke https://YOUR-PREVIEW.vercel.app
   ```
   It passes a made-up participant's documents and checks every answer is built from that participant and contains no trace of anyone else. `HEALTHY` and exit code 0 means go.
3. **Cut over**: attach the production domain (`purely-personal-mcp.vercel.app`) to the new deployment. The connector address participants already added does not change.
4. Optional: set `OPENAI_API_KEY` so `generate_image` renders pictures (otherwise it returns an image brief).

Health: `GET /health` returns the tool count and `"stores_data": false`.

## Security and privacy

- Hosted, the server stores nothing: no profiles, no logs of documents, no accounts. A participant's Brain exists only for the length of the request.
- There is no credential to leak because there is no credential. Anyone can call the connector, and each call is answered only from the documents in that call.
- Only `generate_image` touches the network, and only when you set `OPENAI_API_KEY`. No tool calls a language model. Errors return a one-line message, never a stack trace.
- Inputs are capped at 200k characters per document.

## Layout

```
pp_mcp/server.py     tools, prompts, resources, ASGI app (stateless HTTP) and stdio entry
pp_mcp/profile.py    parses Brain / ICP / Voice DNA; readiness audit
pp_mcp/skills.py     bundled skills, work-order compiler, depersonalise pass
pp_mcp/voice.py      AI Pattern Blacklist, tell detection, clean-up, platform polish
pp_mcp/scoring.py    Invisibility Diagnostic
pp_mcp/library.py    templates, daily angle, prospect query, revenue + attribution
pp_mcp/ledger.py     optional local ledger (stdio install only)
pp_mcp/data/         the 12 skills (+ newsletter-writer), blacklist
api/index.py         Vercel entry · vercel.json
tests/               100 tests, fixture participant (Maya Okafor)
```

## Updating a skill

The skills are copied from the Drive folder into `pp_mcp/data/skills/<name>/` (`SKILL.md` plus `prompts/`) and then cleaned. To update one:

```bash
# replace pp_mcp/data/skills/<name>/ with the new files, then
python scripts/clean_skills.py     # re-applies every fix (idempotent; non-zero exit if an upstream change breaks one)
python -m pytest -q                # tests/test_skill_bundle_quality.py lints the bundle
```

What the cleaner fixes, and why, is in [`AUDIT.md`](./AUDIT.md) ("Skill bundle review") and [`pp_mcp/data/SKILLS-CHANGES.md`](./pp_mcp/data/SKILLS-CHANGES.md). The creator's name and examples are also stripped from every work order at serve time (`depersonalize` in `skills.py`).
