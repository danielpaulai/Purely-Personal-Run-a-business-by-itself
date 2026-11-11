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

