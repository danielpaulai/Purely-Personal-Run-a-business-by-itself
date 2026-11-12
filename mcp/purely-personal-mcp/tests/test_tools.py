import json
import re

CLEAN = "Last March a senior associate called Priya told me she bills 2,100 hours a year.\n\nDM me \"SUNDAY\" for the plan."


def test_inventory_keeps_every_original_tool_except_the_three_token_tools(maya):
    names = {t.name for t in maya.tools()}
    original = """analyze_competitor de_ai_ify find_prospects generate_image get_attribution_report get_brand_colours
    get_daily_prompt get_icp get_my_post_history get_voice_dna get_weekly_revenue_report list_post_templates log_call_booked
    log_dm_received log_published_post log_revenue_event polish_post score_post track_post_published write_carousel
    write_cheatsheet write_ig_caption write_newsletter write_post write_reel_script write_tweet""".split()
    assert set(original) <= names
    assert {"weekly_content_drop", "amplify_post", "first_post_coach", "review_homework", "build_voice_profile",
            "setup_marketing_employee", "check_my_brain", "get_skill", "list_skills", "get_setup_guide"} <= names
    assert len(names) >= 35
    for t in maya.tools():
        assert t.description and len(t.description) > 40, t.name


def test_the_twelve_skills_are_bundled_and_listed(maya):
    out = maya.call("list_skills")
    for s in ["ai-marketing-employee", "voice-profile-builder", "linkedin-post-writer", "first-post-coach", "invisibility-diagnostic",
              "linkedin-carousel-builder", "linkedin-cheatsheet-builder", "competitor-x-ray", "prospect-magnet",
              "multi-platform-amplifier", "weekly-content-engine", "homework-reviewer"]:
        assert s in out
    assert "Intent-Driven" in maya.call("get_skill", name="linkedin-post-writer", part="intent-driven.md")
    assert "Invisibility Diagnostic" in maya.call("get_skill", name="invisibility-diagnostic", part="full")


def _locked(out, docs):
    # participant's own material is in the order, not a generic or Daniel default
    assert "Maya Okafor" in out and "flat white" in out
    assert "trapped by my own salary" in out
    assert "journey" in out and "rockstar" in out           # her banned list
    assert "NEVER CLAIM" in out and "guarantee a result" in out and "name a client" in out
    assert "OUTPUT CONTRACT" in out and "BEFORE YOU DELIVER" in out and any(k in out for k in ("score_post", "polish_post", "de_ai_ify"))
    assert "Daniel Paul" not in out


def test_write_post_is_locked_to_the_participants_brain_icp_and_voice(maya, docs):
    out = maya.call("write_post", topic="Why passion advice fails lawyers", intent="Educating", mode="framework", cta_keyword="SUNDAY")
    _locked(out, docs)
    assert "Framework-Heavy" in out and "SUNDAY" in out and "linkedin-post-writer" in out
    assert "same documents you passed" in out  # the follow-up score_post call reuses her documents


def test_story_flow_refuses_to_invent_a_story(maya):
    out = maya.call("write_post", topic="my worst week", mode="story")
    assert "Story-Flow requires a documented story" in out


def test_every_skill_tool_returns_a_locked_work_order(maya, docs):
    calls = [
        ("write_carousel", {"topic": "Test a career first", "mode": "intent", "intent": "Educating"}),
        ("write_cheatsheet", {"topic": "Career experiments", "format": "comparison"}),
        ("weekly_content_drop", {"idea": "Sunday dread"}),
        ("amplify_post", {"post": CLEAN, "platforms": "full"}),
        ("write_tweet", {"post_or_topic": CLEAN}),
        ("write_ig_caption", {"post_or_topic": CLEAN}),
        ("write_reel_script", {"post_or_topic": CLEAN}),
        ("write_newsletter", {"topic": "The Sunday scaries"}),
        ("analyze_competitor", {"competitor_urls": "https://linkedin.com/in/a\nhttps://linkedin.com/in/b\nhttps://linkedin.com/in/c"}),
        ("find_prospects", {"post": CLEAN, "limit": 12}),
        ("first_post_coach", {"draft": CLEAN}),
        ("setup_marketing_employee", {"mode": "validated"}),
        ("build_voice_profile", {"past_posts": "post one\n---\npost two"}),
    ]
    for tool, args in calls:
        out = maya.call(tool, **args)
        _locked(out, docs)
        assert "WORK ORDER" in out and "SKILL METHOD" in out, tool


def test_skill_methods_are_actually_inlined(maya):
    assert "Prospect Search Query Builder" in maya.call("find_prospects")
    assert "8 Dimensions" in maya.call("analyze_competitor", competitor_urls="https://linkedin.com/in/a")
    assert "Platform Adaptation Rules" in maya.call("write_tweet", post_or_topic="x")
    assert "CTA SLIDE" in maya.call("write_carousel", topic="x")
    assert "Prospect" in maya.call("find_prospects") and "United" in maya.call("find_prospects")


def test_competitor_without_urls_asks_for_them(maya):
    assert "Give me the competitors" in maya.call("analyze_competitor", competitor_urls="")


def test_score_polish_deai_use_the_participants_banned_list(maya):
    s = maya.call("score_post", text="My hustle journey: a rockstar move.")
    assert "INVISIBILITY DIAGNOSTIC: 0/4" in s and "YOUR" in s
    p = maya.call("polish_post", text="Some text — here. Hustle hard.", platform="linkedin")
    assert "—" not in p.split("POLISHED TEXT:")[1] and "hustle" in p.lower()
    d = maya.call("de_ai_ify", text="We leverage it — truly.")
    assert "use it" in d and "Word bank to draw replacements from" in d


def test_quality_tools_work_with_no_documents_using_universal_rules(client):
    assert "0/4" in client.call("score_post", text="Let us leverage synergy.")
    assert "DE-AI-IFY" in client.call("de_ai_ify", text="Let us leverage synergy.")


def test_brand_colours_and_image_brief_use_her_palette(maya):
    assert "#1f6f5c" in maya.call("get_brand_colours")
    img = maya.call("generate_image", prompt="Sunday night dread", aspect="4:5")
    assert "#1f6f5c" in img and "1024x1536" in img and "IMAGE BRIEF" in img
    assert "Say what the image is of" in maya.call("generate_image")


def test_generate_image_renders_when_a_key_is_set(maya, monkeypatch):
    import pp_mcp.server as srv
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(srv, "_render_image", lambda prompt, size: (b"\x89PNG\r\n\x1a\n" + prompt.encode()[:8]))
    import asyncio
    res = asyncio.run(maya.mcp.call_tool("generate_image", {"prompt": "cover", **maya.docs}))
    content = res[0] if isinstance(res, tuple) else res
    assert any(c.type == "image" for c in content) and any("#1f6f5c" in getattr(c, "text", "") for c in content)


def test_v1_parameter_names_still_work(maya):
    assert "INVISIBILITY DIAGNOSTIC" in maya.call("score_post", post="Stop leveraging synergy.")
    assert "POLISH" in maya.call("polish_post", post="Stop leveraging synergy.")
    assert "WORK ORDER" in maya.call("analyze_competitor", profile_url="https://linkedin.com/in/a", max_posts=20)
    fp = maya.call("find_prospects", keywords="wellness coach", location="EMEA")
    assert "wellness coach" in fp and "EMEA" in fp
    assert "#1f6f5c" in maya.call("get_brand_colours")


def test_daily_prompt_uses_her_icp(maya):
    out = maya.call("get_daily_prompt", date="2026-11-11")
    assert "DAILY PROMPT" in out and re.search(r"Sunday|pay cut|trapped|passion|librarian|senior|quitting|serious", out)


def test_local_ledger_feeds_history_daily_prompt_and_reports(local):
    c, home = local
    assert "No posts found" in c.call("get_my_post_history")
    for topic, kw in [("Why passion advice fails lawyers", "SUNDAY"), ("Salary handcuffs", "CUFFS")]:
        assert "Logged post" in c.call("log_published_post", topic=topic, keyword=kw, hook=topic)
    assert "Why passion advice" in c.call("get_my_post_history")
    c.call("log_dm_received", from_name="Priya", keyword="SUNDAY")
    c.call("log_dm_received", from_name="Tom", keyword="SUNDAY")
    c.call("log_call_booked", name="Priya", post_ref="SUNDAY")
    c.call("log_revenue_event", amount=2400, client="Priya", post_ref="SUNDAY", source="linkedin")
    rep = c.call("get_weekly_revenue_report")
    assert "2,400.00" in rep and "posts published 2 -> DMs received 2 -> calls booked 1 -> sales 1" in rep
    assert re.search(r"sunday\s+DMs\s+2 .* calls\s+1 .* sales\s+1 .* 2,400.00", c.call("get_attribution_report"))
    assert "Amount must be greater" in c.call("log_revenue_event", amount=0)
    assert (home / "ledger.jsonl").exists()


def test_hosted_connector_stores_nothing_and_says_so(maya):
    for tool, args in [("log_published_post", {"topic": "x"}), ("log_dm_received", {"from_name": "x"}),
                       ("log_call_booked", {"name": "x"}), ("log_revenue_event", {"amount": 5})]:
        out = maya.call(tool, **args)
        assert "stores nothing" in out and "Notion" in out, tool


def test_hosted_reports_and_history_work_from_records_you_pass(maya):
    recs = json.dumps([
        {"kind": "post", "topic": "Salary handcuffs", "platform": "linkedin", "keyword": "CUFFS", "hook": "Salary handcuffs are real"},
        {"kind": "dm", "from_name": "Priya", "post_ref": "CUFFS"},
        {"kind": "revenue", "amount": 1500, "post_ref": "CUFFS", "currency": "GBP"},
    ])
    assert "Salary handcuffs" in maya.call("get_my_post_history", records=recs)
    assert "1,500.00 GBP" in maya.call("get_weekly_revenue_report", records=recs)
    assert "cuffs" in maya.call("get_attribution_report", records=recs).lower()
    d = maya.call("get_daily_prompt", records=recs, date="2026-11-11")
    assert "DAILY PROMPT" in d
    assert "records must be a JSON list" in maya.call("get_weekly_revenue_report", records="not json")


def test_nothing_of_the_creator_appears_in_any_tool_output(maya, client):
    """Every tool, called with another person's documents, must contain no trace of the program creator."""
    leak = re.compile(r"daniel|danny|danielpaul|purelypersonal\.ai|solo founders and small business", re.I)
    arg_sets = {
        "write_post": {"topic": "t"}, "write_carousel": {"topic": "t"}, "write_cheatsheet": {"topic": "t"}, "write_newsletter": {"topic": "t"},
        "weekly_content_drop": {}, "amplify_post": {"post": CLEAN}, "write_tweet": {"post_or_topic": CLEAN},
        "write_ig_caption": {"post_or_topic": CLEAN}, "write_reel_script": {"post_or_topic": CLEAN},
        "analyze_competitor": {"competitor_urls": "https://linkedin.com/in/a"}, "find_prospects": {}, "first_post_coach": {},
        "setup_marketing_employee": {}, "build_voice_profile": {}, "get_icp": {}, "get_voice_dna": {}, "check_my_brain": {},
        "get_daily_prompt": {}, "score_post": {"text": CLEAN}, "polish_post": {"text": CLEAN}, "de_ai_ify": {"text": CLEAN},
        "get_brand_colours": {}, "generate_image": {"prompt": "x"}, "get_setup_guide": {}, "list_post_templates": {},
        "get_my_post_history": {}, "get_weekly_revenue_report": {}, "get_attribution_report": {},
    }
    for tool, args in arg_sets.items():
        out = maya.call(tool, **args)
        assert not leak.search(out), f"{tool}: {leak.search(out).group(0)}"
    for tool in ("write_post", "get_icp", "get_voice_dna"):
        assert not leak.search(client.call(tool, topic="t") if tool == "write_post" else client.call(tool)), tool


def test_review_homework_ranks_and_flags_for_coaching(maya):
    posts = [
        {"name": "Sarah", "industry": "Coach", "post": "Last March a client called Priya paid me 4,000 after 6 calls. Stop discounting. Nobody tells you that. DM me \"PRICE\" for the sheet."},
        {"name": "Marcus", "industry": "Ecom", "post": "In today's fast-paced world, leverage your journey."},
    ]
    out = maya.call("review_homework", posts=json.dumps(posts))
    assert out.index("Sarah") < out.index("Marcus") and "COACH DM LIST" in out and "Marcus" in out.split("COACH DM LIST")[1]
    txt = maya.call("review_homework", posts="Name: A\nIndustry: X\nA post here.\n---\nName: B\nIndustry: Y\nAnother one.")
    assert "2 posts" in txt


def test_prompts_and_resources_registered(maya):
    import asyncio
    prompts = asyncio.run(maya.mcp.list_prompts())
    assert {p.name for p in prompts} >= {"monday_content_drop", "wednesday_market_scan", "friday_prospect_run"}
    assert asyncio.run(maya.mcp.list_resource_templates())


def test_errors_never_leak_stack_traces(maya):
    out = maya.call("get_skill", name="not-a-skill")
    assert "Error in get_skill" in out and "Traceback" not in out


def test_hook_archetype_formula_is_passed_through(maya):
    out = maya.call("write_post", topic="x", hook_archetype="warning")
    assert "If you're doing X, you're destroying Y." in out
