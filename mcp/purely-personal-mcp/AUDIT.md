# Audit: Purely Personal MCP v1 (live) vs v2

Sources: the live connector at `purely-personal-mcp.vercel.app/mcp` (its 29 published tool definitions, plus calls to `get_icp` and `get_voice_dna` on 2026-11-11), the Command Page, the Day 1, 2 and 3 playbooks, the Day 1 ICP / Voice DNA / Business Brain pages, and the 12 skills in the shared Drive folder. The v1 server source is not in this repository, so v1 behaviour below is what its tool definitions and live responses show.

## What v1 has (29 tools)

| Group | Tools |
|---|---|
| Writing | `write_post` `write_carousel` `write_cheatsheet` `write_newsletter` `write_tweet` `write_ig_caption` `write_reel_script` |
| Research | `analyze_competitor` `find_prospects` `get_daily_prompt` `get_my_post_history` `list_post_templates` |
| Quality / design | `score_post` `polish_post` `de_ai_ify` `generate_image` `get_brand_colours` |
| Profile | `set_my_context` `get_my_context` `clear_my_context` `get_icp` `get_voice_dna` |
| Tracking | `log_published_post` `track_post_published` `log_dm_received` `log_call_booked` `log_revenue_event` `get_weekly_revenue_report` `get_attribution_report` |

## What was wrong

| # | Finding | Evidence | Why it matters |
|---|---|---|---|
| 1 | `get_icp` and `get_voice_dna` return **Daniel Paul's** ICP and voice for every caller | Live call: ICP "Solo founders… $5K-50K MRR", voice rules "'Yeah.' or 'So.' opener (~70%)", Daniel's banned list | Day 3 tells participants to "call get_icp and get_voice_dna and reconcile against your files". They reconcile against the wrong person. |
| 2 | `write_post` and `polish_post` default to Daniel unless overrides are pasted or a token is passed. `analyze_competitor` measures gaps "relative to Daniel's ICP" with no way to change that | Tool descriptions: "otherwise defaults to Daniel Paul", "content gaps relative to Daniel's ICP" | A participant who forgets the token gets a post in Daniel's voice, silently. Competitor analysis answers for the wrong business, always. |
| 3 | None of the 12 skills are used by the tools | Skill methods (templates, intents, cover formulas, CTA types, the 8 competitor dimensions, the 4-line DM structure) appear nowhere in the tool descriptions | The program teaches 12 skills; the connector ignores them. |
| 4 | Business Brain is not a first-class input | Only free-text `voice_override` / `icp_override`; no Brain, no never-claim guard rail | Day 1 produces `BUSINESS-BRAIN.md` and says it wins any disagreement. Nothing in v1 reads it. |
| 5 | No way to tell if a participant's brain is thin | No readiness check | "Output is generic" is the top support question (Day 3: "nine out of ten"), and the cause is a thin brain. |
| 6 | Scoring is not tied to the participant | v1 `score_post` takes only `post`; no token, so it cannot see their word bank or banned list | A post full of the participant's own banned words can still score. |
| 7 | Skills missing from the tool surface | No homework-reviewer, first-post-coach, voice-profile-builder, ai-marketing-employee, weekly-content-engine, multi-platform-amplifier as tools | Facilitator and Day 1 flows had to be run by hand. |
| 8 | Skill text carries the creator's identity | e.g. newsletter-writer: "use the bundled references (Daniel Paul's defaults)" | A direct path back into finding #1 if skills are ever loaded as-is. |

## What v2 does

| Finding | Fix | Proof |
|---|---|---|
| 1, 2 | No documents means a request for them. `get_icp` / `get_voice_dna` read back only what the caller passed. There is no demo profile and no bundled copy of anyone's brain; a test calls every tool with another person's documents and fails on any trace of the creator. | `test_no_documents_means_a_request_for_them…`, `test_each_call_uses_only_its_own_documents`, `test_nothing_of_the_creator_appears_in_any_tool_output`, smoke script |
| 3 | Every content tool compiles one of the 12 skills (its real prompt files and process) into a work order. | `test_skill_methods_are_actually_inlined`, `test_every_skill_tool_returns_a_locked_work_order` |
| 4 | Every tool takes `brain`, `icp`, `voice_dna`. Name, publishing language, never-claim rules and brand colours are read from the Brain itself. The Brain wins ties. Never-claim is a hard rule in every order. | `_locked()` assertions in `tests/test_tools.py` |
| 5 | `check_my_brain`: readiness score with the exact fix per gap. | `test_audit_flags_a_thin_brain` |
| 6 | `score_post` checks Voice against the participant's word bank, signature phrases and customer phrases, and enforces their banned list. | `test_strong_post_scores_higher…`, `test_users_own_banned_list_is_enforced` |
| 7 | 10 new tools: `weekly_content_drop`, `amplify_post`, `first_post_coach`, `review_homework`, `build_voice_profile`, `setup_marketing_employee`, `check_my_brain`, `get_setup_guide`, `list_skills`, `get_skill`. | `test_inventory_has_every_original_tool…` |
| 8 | Every skill method passes through `depersonalize()`; author credit removed from the order header. | `_locked()` asserts "Daniel Paul" is absent from every order |

26 of the 29 original tool names are kept (the three token tools are gone), so the Day 2 and Day 3 prompts need no edits.

## Decisions worth knowing

- **Tools return work orders, not finished copy.** The server has no model key and makes no network calls. The calling Claude (already running in the participant's project, with Apify attached) does the writing. This keeps the skills the single source of truth and costs nothing to run.
- **Asking dimension accepts a closing question by default.** The skill's strict test is a keyword DM invitation, but the Day 2 and Day 3 prompts require posts to "end on a question that invites disagreement" and to reach 4/4. Counting only keywords would make those two instructions contradict. `strict_asking=true` restores the skill's strict reading.
- **`generate_image` still renders, if you give it a key.** v1 rendered with OpenAI gpt-image-1 and defaulted to Purely Personal's red palette. v2 does the same when `OPENAI_API_KEY` is set on the server, but uses the participant's own palette. With no key it returns a brief for Aura / Canva instead of failing.
- **Research tools hand the scraping to the participant's Apify connector.** v1 ran Apify itself (`harvestapi/linkedin-profile-search`, `linkedin-profile-posts`). Day 2 already has every participant connect Apify and says "use the Apify connector and the Purely Personal connector", so v2 returns the skill's method, the derived search and the scoring rubric, and Claude runs the actors. Upside: no shared Apify bill and no Apify token on the server. Downside: it needs the Apify connector switched on in that chat; if it is off the order says so rather than guessing.
- **`polish_post` reports and fixes mechanically; the rewrite is Claude's job.** v1 rewrote inside the tool. v2 applies the safe fixes (dashes, filler words, whitespace) and lists what remains, and the work order tells Claude to rewrite those lines in the participant's words.
- **v1 parameter names still work** where they still make sense: `post` for `score_post` / `polish_post` / `de_ai_ify`, `profile_url` / `max_posts`, `keywords` / `location`, `days_back` / `platform_filter`.
- **Scores are heuristic.** The tool says so on every result. A script cannot hear that a sentence is not yours.
- **No tokens, no storage (your call).** The hosted server cannot know who is calling, so instead of an identifier it receives the participant's own documents on every call and keeps nothing. Consequences: (1) Claude must pass the Brain each call (the project instructions say so once); (2) post history and revenue/attribution come from rows Claude reads out of Notion and passes as `records=`; (3) the `log_*` tools only work in the local install, which keeps a private ledger. Old `pp_` tokens simply stop mattering.

## Not done here

- **Not deployed.** The live address serves participants; replacing it is a release decision. `README.md` has the steps and `python -m pp_mcp.smoke <url>` verifies a deployment before cutover. Vercel's Python runtime could not be exercised from this sandbox; the HTTP transport was tested with uvicorn in serverless mode (no lifespan, new connection per request).
- The Day 2 / Day 3 pages still say "thirty tools" (v2 has 36), and the Day 1 Business Brain page says "you turn this document into a token" (Day 3 wording). Both need a wording pass when this ships: there is no token now.

## Student report (Machines4FoodIndustry, DACH, all content in German)

A participant tested v1 on a real B2B business and reported five failures. Each was reproduced against v2 before fixing, and each now has a regression test in `tests/test_german_student_feedback.py`.

| Her report (v1) | What was really wrong | v2 |
|---|---|---|
| `get_icp` / `get_voice_dna` return Daniel's English ICP and voice. `analyze_competitor` measures gaps "relative to Daniel's ICP" | Hard-wired defaults (finding 1 above) | Read back only the documents passed in. Gaps are measured against the caller's own ICP. |
| `find_prospects`: zero results for German terms; then `Apify run failed (403): platform-feature-disabled, Monthly usage hard limit exceeded` | v1 ran Apify on the server with English search terms, so German-language profiles never matched; the 403 came from whichever Apify account that server-side key belonged to (v1 source is not available here, so which one cannot be confirmed) | v2 never runs Apify itself: it uses the participant's **own** Apify connector, so there is no shared credit to exhaust. The search is derived from the ICP in its own language (German and English titles, Germany/Austria/Switzerland, German profile language) and walks a four-step ladder on zero results (titles+locations, drop filters, company-first via company search and company-employees, report and stop). It shows the estimated cost first (about $0.16 for 15 prospects at the verified Apify free-tier prices), accepts `budget_usd`, and on a 403/hard-limit it stops, says so plainly, and offers the no-Apify route (`candidates=`). |
| `analyze_competitor` errors on LinkedIn company pages | v1 used a profile-posts scraper only | URLs are classified: `/company/` pages use `harvestapi/linkedin-company-posts` plus `linkedin-company`, `/in/` profiles use `linkedin-profile-posts`, plain names are resolved first. The 8 dimensions are adapted for company pages (tagline, followers, employee-led vs logo posts, trade-fair and installation posts). Shows cost, accepts `budget_usd`, and works with no Apify at all from `pasted_posts=`. |
| `de_ai_ify` replaced German "innovative" with English "new", left " , " after a dash, and ignored her banned phrases | English-only word lists and swaps applied to German text; naive dash replacement; banned phrases only matched as exact substrings | Language is detected (or set with `language=`). German text gets German rules and German swaps only (`innovative Lösung` becomes `neue Lösung`); English lists never fire on German prose. Dashes become correct punctuation (`..., mit ...`). Her banned phrases match inflected forms, filler words and reversed order (`modernste Technik`, `modernster Technik`, `Potenziale heben`, `hebt Potenziale`). German transitions are flagged, not deleted, because deleting them breaks German verb-second word order. |
| (not reported, found while reproducing) | **v2's own parser was English-only**: her German Brain, ICP and Voice DNA parsed to *zero* word-bank items, zero banned phrases, language "English" | Section titles, banned-list markers, never-claim rules, language and name are read in German and English. Her documents now score 100/100 readiness. |
| "Where do I get my pp_ token?" | Tokens were v1's identity mechanism | There is no token in v2. Claude passes her documents with each call. |

Known limits: irregular German participles are not matched (`Potenziale gehoben` is not caught by `Potenziale heben`); only German and English have language-specific rules (other languages get the universal checks and the participant's own banned list).

## Skill bundle review (seven defects in the bundled skills and tools)

A reviewer read the bundled skills and the scorer against each other. All seven points were reproduced in the files before any fix; the fixes are in `scripts/clean_skills.py` (re-runnable) and `pp_mcp/scoring.py`, and each has a test (`tests/test_skill_bundle_quality.py`, `tests/test_engines.py`).

| # | Defect | Where | Fix |
|---|---|---|---|
| 1 | Banned-word lists garbled by a find-and-replace: "use, open up, big, help, path, go deep, handle, improve, solid, whole, fit, brainstorm, model, use, unleash" (leverage, unlock, game-changing, empower, journey, dive deep, navigate ... became their plain substitutes, and "use" appeared twice). `de_ai_ify` then swapped "unlock" for "open up", which the same lists called a tell | 13 places in 9 skill files, **in the source skills**, not only in the bundle | Restored to the program's real list (Day 1 default + AI Pattern Blacklist). `de_ai_ify` now only makes context-free swaps (leverage to use, seamless to smooth ...); verbs whose replacement depends on the sentence (unlock, empower, elevate, navigate, harness, delve ...) are flagged for a rewrite, and a test fails if any swap target is itself a banned or garbled word |
| 2 | Contradicting length targets: 1300-1500 characters (`linkedin-post-writer`, `polish_post`) vs "150 words" (`first-post-coach`, `ai-marketing-employee`, `voice-profile-builder`, `multi-platform-amplifier`) vs "under 220 words" (`invisibility-diagnostic`) | 12 places | One standard everywhere: **1300-1500 characters (about 200-250 words)**. `polish_post` takes `min_chars` / `max_chars` for tasks with their own range (the Day 3 story post is 1100-1400) |
| 3 | Scorer looser than the skill. Specificity accepted a generic role ("a client", "a founder") as if it were a name; POV missed "Volume is not the problem, voice is" because it only matched a fixed word list | `scoring.py` | Specificity needs a **real name** (cued by "called/named/client X", a title, a company with a legal form, or a mid-sentence capitalised name that is not a day, month or tool) **and** a real number (list markers and dates do not count). POV now recognises positions by pattern ("X is not the problem", "I told her to stop", "costs more than", "the mistake most people make") as well as stance words. A post with no name can no longer reach 4/4 |
| 4 | Breaks its own anti-invention rule: `first-post-coach` told users to add "a real (or real-feeling) client name"; unsupported claims and invented proof ("47 likes, 8 DMs", "2,000+ scored posts", "5+ Calls Booked in 1 Week", "4 billion AI posts published daily", a named client's "1.9M impressions", "proven in her last cohort") | 12 places | Advice rewritten to "use the client's first name from your own notes, never invent one". Claims and invented proof removed. Every Examples section now opens with an "Illustrative only, never reuse" banner. A test scans every bundled file and every work order for these strings |
| 5 | Sample copy broke the style rules: "Real talk:" filler markers, "it's not X. It's Y" frames, an em dash, and carousel slides of 2-3 sentences at 10-15 words each | post-writer sample and prompts, amplifier sample, carousel prompts | Sample post rewritten (and checked by `find_tells`: no contrast frame, filler or em dash); "Real talk" removed everywhere; carousel slides are now a 6-word title and 1-2 short sentences, 20 words maximum |
| 6 | Pointed at things that do not exist here: `render.py`, `scripts/template.html`, `~/.claude/skills/...`, `APIFY_TOKEN`, "ICP Builder", `workbook`, `cold-outreach-sequence`, `content-multiplier`, the `visual` HTML modes, `supreme_coder` actors | all 12 skills | Dangling sections and rows removed, ICP references point to the operator's ICP.md or Business Brain, Apify steps point to the participant's own connector, and each skill ends with "Use in the Purely Personal connector" naming the tool that runs it. `competitor-x-ray` now names the right scrapers (profile posts vs company posts) instead of using a profile scraper for posts |
| 7 | Built for one cohort: CET times, "Day 2 stage", "312 attendees", Game 1, lesson numbers, the author's name | `first-post-coach`, `homework-reviewer`, `weekly-content-engine`, intros of six more | `homework-reviewer` rewritten as a generic batch reviewer that describes what `review_homework` actually does; the others generalised or trimmed |

**What this does not change:** the skills installed in participants' Claude from the Drive folder still contain these defects. The connector serves the cleaned versions, and `pp_mcp/data/SKILLS-CHANGES.md` lists what differs, but the Drive originals need the same fixes if participants use the skills directly. `scripts/clean_skills.py` is the repeatable way to produce them.

