# Purely Personal MCP v2

The connector behind **Build Your 1st AI Employee**. It turns the program's 12 skills into tools, and locks every one of them to the participant's **own** Business Brain, ICP and Voice DNA.

> v1 returned Daniel Paul's ICP and voice to everyone. v2 never does. No profile means a setup message, not someone else's voice. See [AUDIT.md](./AUDIT.md) for what changed and why.

## How it works

```
Day 1                       Day 2 / Day 3
ICP.md ─┐                   Claude ──► write_post(topic, user_token) ──► WORK ORDER
VOICE-DNA.md ─┼─► set_my_context ─► pp_ token              skill method + YOUR brain + YOUR voice lock
BUSINESS-BRAIN.md ┘                                         + YOUR customer lock + hard rules
                                    Claude executes it ──► score_post / polish_post / de_ai_ify (run in code)
```

A **work order** is the skill's method plus the participant's Brain, a parsed Voice Lock (word bank, signature phrases, banned list, writing rules, the test), a Customer Lock (the person, their words, objections, themes), their never-claim guard rail, the output contract, and the exact quality calls to make before delivering. The calling Claude does the writing. The server never calls a language model, so it costs nothing to run and nothing can drift between what a skill says and what the tool does.

The checks are real code, not prompts: scoring (Invisibility Diagnostic, personalised to the participant's own words), AI-tell detection, mechanical clean-up, platform polish, homework ranking, daily angle, prospect query, post history, revenue and attribution reports.

## The 40 tools

| Family | Tools |
|---|---|
| **Brain** | `set_my_context` · `get_my_context` · `check_my_brain` · `clear_my_context` · `get_icp` · `get_voice_dna` · `get_business_brain` · `get_setup_guide` |
| **12 skills** | `list_skills` · `get_skill` · `setup_marketing_employee` (ai-marketing-employee) · `build_voice_profile` (voice-profile-builder) · `write_post` (linkedin-post-writer) · `first_post_coach` · `write_carousel` (linkedin-carousel-builder) · `write_cheatsheet` (linkedin-cheatsheet-builder) · `weekly_content_drop` (weekly-content-engine) · `amplify_post` · `write_tweet` · `write_ig_caption` · `write_reel_script` (multi-platform-amplifier) · `analyze_competitor` (competitor-x-ray) · `find_prospects` (prospect-magnet) · `score_post` (invisibility-diagnostic) · `review_homework` (homework-reviewer) |
| **Also** | `write_newsletter` (newsletter-writer) |
| **Quality** (deterministic) | `score_post` · `polish_post` · `de_ai_ify` · `review_homework` |
| **Research** | `get_daily_prompt` · `list_post_templates` · `get_my_post_history` |
| **Design** | `get_brand_colours` · `generate_image` (renders with `OPENAI_API_KEY`, else returns a brief) |
| **Track** | `log_published_post` · `track_post_published` · `log_dm_received` · `log_call_booked` · `log_revenue_event` · `get_weekly_revenue_report` · `get_attribution_report` |

All 29 tool names from v1 are kept, so every Day 2 and Day 3 playbook prompt keeps working unchanged. Three prompts (slash commands) are added: `monday_content_drop`, `wednesday_market_scan`, `friday_prospect_run`. Each skill is also a resource at `pp://skills/{name}`.

## Participant flow (what to tell them)

1. After Day 1, in the project: *"Call set_my_context with my BUSINESS-BRAIN.md, ICP.md and VOICE-DNA.md. My name is …, I publish in …, never claim …"*
2. Claude returns a `pp_…` token and a **readiness score** with exactly what is thin (e.g. "Found 6 word-bank items, need 20+").
3. Save the token in the project instructions: *"Always pass user_token pp_… to the Purely Personal connector."*
4. `check_my_brain` any time output feels generic. A thin brain is the usual cause.

One-off use without saving anything: every writing tool also takes `brain_override`, `icp_override`, `voice_override`. `user_token="demo"` loads the sample brain read-only.

## Run locally

```bash
cd mcp/purely-personal-mcp
pip install -r requirements.txt
python -m pytest -q                 # 43 tests: parsing, every tool, HTTP, stdio, Supabase store
python -m pp_mcp                    # stdio, for Claude Desktop / Claude Code
python -m pp_mcp --http 8000        # http://localhost:8000/mcp
```

Claude Desktop (stdio), `claude_desktop_config.json`:

```json
{ "mcpServers": { "purely-personal": { "command": "python3", "args": ["-m", "pp_mcp"], "cwd": "/abs/path/to/mcp/purely-personal-mcp" } } }
```

Profiles are stored in SQLite at `~/.purely-personal/pp.db` (override with `PP_DB_PATH`).

## Deploy (Vercel + Supabase)

Serverless disks are ephemeral, so the hosted server stores profiles in Supabase. The handler is stateless (a fresh MCP session manager per request), so it needs no lifespan, no sticky sessions and no shared event loop.

1. **Supabase**: create a project, run [`supabase/schema.sql`](./supabase/schema.sql) in the SQL editor. Tables are RLS-enabled with no policies; only the service-role key (server side) can touch them. Only `sha256(token)` is stored.
2. **Vercel**: new project from this repo, **Root Directory = `mcp/purely-personal-mcp`**. Environment variables: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` (see `.env.example`). Deploy to a **preview** first.
3. **Verify** the preview exactly as Claude would use it:
   ```bash
   python -m pp_mcp.smoke https://YOUR-PREVIEW.vercel.app
   ```
   It saves a throwaway profile, checks a fresh connection finds it, checks the work order is locked to it and not to anyone else, then deletes it. `HEALTHY` and exit code 0 means go.
4. **Cut over**: attach the production domain (`purely-personal-mcp.vercel.app`) to the new deployment, or ship it under a new name and update the connector address on the Day 2 playbook and the Command Page.
5. Participants who already connected keep the same address. Anyone using the old `get_icp`/`get_voice_dna` now gets their own (or the setup message).

Health: `GET /health` returns tool count and storage backend.

## Security and privacy

- The `pp_` token (128-bit random) is the only credential. Treat it like a password; `clear_my_context` revokes it and deletes the profile and every event.
- The database holds `sha256(token)`, never the token. Profile text is stored as provided.
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
pp_mcp/store.py      SQLite and Supabase stores
pp_mcp/data/         the 12 skills (+ newsletter-writer), blacklist, demo brain
api/index.py         Vercel entry · vercel.json · supabase/schema.sql
tests/               43 tests, fixture participant (Maya Okafor)
```

## Updating a skill

The skills are copied from the Drive folder into `pp_mcp/data/skills/<name>/` (`SKILL.md` plus `prompts/`). To update one, replace those files and run the tests. The server picks them up on next start. Author names and the creator's own examples are stripped from every work order automatically (`depersonalize` in `skills.py`), so a participant's order never carries someone else's voice.
