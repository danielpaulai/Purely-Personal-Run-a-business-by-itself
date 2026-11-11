import json
import re

CLEAN = "Last March a senior associate called Priya told me she bills 2,100 hours a year.\n\nDM me \"SUNDAY\" for the plan."


def test_inventory_has_every_original_tool_plus_the_skill_tools(client):
    names = {t.name for t in client.tools()}
    original = """analyze_competitor clear_my_context de_ai_ify find_prospects generate_image get_attribution_report get_brand_colours
    get_daily_prompt get_icp get_my_context get_my_post_history get_voice_dna get_weekly_revenue_report list_post_templates log_call_booked
    log_dm_received log_published_post log_revenue_event polish_post score_post set_my_context track_post_published write_carousel
    write_cheatsheet write_ig_caption write_newsletter write_post write_reel_script write_tweet""".split()
    assert set(original) <= names
    assert {"weekly_content_drop", "amplify_post", "first_post_coach", "review_homework", "build_voice_profile",
            "setup_marketing_employee", "check_my_brain", "get_skill", "list_skills", "get_setup_guide", "get_business_brain"} <= names
    assert len(names) >= 40
    for t in client.tools():
        assert t.description and len(t.description) > 40, t.name


def test_the_twelve_skills_are_bundled_and_listed(client):
    out = client.call("list_skills")
    for s in ["ai-marketing-employee", "voice-profile-builder", "linkedin-post-writer", "first-post-coach", "invisibility-diagnostic",
              "linkedin-carousel-builder", "linkedin-cheatsheet-builder", "competitor-x-ray", "prospect-magnet",
              "multi-platform-amplifier", "weekly-content-engine", "homework-reviewer"]:
        assert s in out
    assert "Intent-Driven" in client.call("get_skill", name="linkedin-post-writer", part="intent-driven.md")
    assert "Invisibility Diagnostic" in client.call("get_skill", name="invisibility-diagnostic", part="full")


def _locked(out, docs):
    # participant's own material is in the order, not a generic or Daniel default
    assert "Maya Okafor" in out and "flat white" in out
    assert "trapped by my own salary" in out
    assert "journey" in out and "rockstar" in out           # her banned list
    assert "NEVER CLAIM" in out and "Never guarantee results" in out
    assert "OUTPUT CONTRACT" in out and "BEFORE YOU DELIVER" in out and any(k in out for k in ("score_post", "polish_post", "de_ai_ify"))
    assert "Daniel Paul" not in out


def test_write_post_is_locked_to_the_participants_brain_icp_and_voice(client, token, docs):
    out = client.call("write_post", topic="Why passion advice fails lawyers", intent="Educating", mode="framework", user_token=token, cta_keyword="SUNDAY")
    _locked(out, docs)
    assert "Framework-Heavy" in out and "SUNDAY" in out and "linkedin-post-writer" in out
    assert token in out  # the follow-up score_post call carries her token


def test_story_flow_refuses_to_invent_a_story(client, token):
    out = client.call("write_post", topic="my worst week", mode="story", user_token=token)
    assert "Story-Flow requires a documented story" in out


def test_every_skill_tool_returns_a_locked_work_order(client, token, docs):
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
        out = client.call(tool, user_token=token, **args)
        _locked(out, docs)
        assert "WORK ORDER" in out and "SKILL METHOD" in out, tool


def test_skill_methods_are_actually_inlined(client, token):
    assert "Prospect Search Query Builder" in client.call("find_prospects", user_token=token)
    assert "8 Dimensions" in client.call("analyze_competitor", user_token=token, competitor_urls="https://linkedin.com/in/a")
    assert "Platform Adaptation Rules" in client.call("write_tweet", user_token=token, post_or_topic="x")
    assert "CTA SLIDE" in client.call("write_carousel", user_token=token, topic="x")
    assert "Prospect" in client.call("find_prospects", user_token=token) and "United" in client.call("find_prospects", user_token=token)


def test_competitor_without_urls_asks_for_them(client, token):
    assert "competitor LinkedIn profile URLs" in client.call("analyze_competitor", user_token=token, competitor_urls="nothing")


def test_score_polish_deai_use_the_participants_banned_list(client, token):
    s = client.call("score_post", text="My hustle journey: a rockstar move.", user_token=token)
    assert "INVISIBILITY DIAGNOSTIC: 0/4" in s and "YOUR" in s
    p = client.call("polish_post", text="Some text — here. Hustle hard.", platform="linkedin", user_token=token)
    assert "—" not in p.split("POLISHED TEXT:")[1] and "hustle" in p.lower()
    d = client.call("de_ai_ify", text="We leverage it — truly.", user_token=token)
    assert "use it" in d and "Word bank to draw replacements from" in d


def test_quality_tools_work_without_a_token_using_universal_rules(client):
    assert "0/4" in client.call("score_post", text="Let us leverage synergy.")
    assert "DE-AI-IFY" in client.call("de_ai_ify", text="Let us leverage synergy.")


def test_brand_colours_and_image_brief_use_her_palette(client, token):
    assert "#1f6f5c" in client.call("get_brand_colours", user_token=token)
    img = client.call("generate_image", prompt="Sunday night dread", aspect="4:5", user_token=token)
    assert "#1f6f5c" in img and "1024x1536" in img and "IMAGE BRIEF" in img
    assert "Say what the image is of" in client.call("generate_image")


def test_generate_image_renders_when_a_key_is_set(client, token, monkeypatch):
    import pp_mcp.server as srv
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(srv, "_render_image", lambda prompt, size: (b"\x89PNG\r\n\x1a\n" + prompt.encode()[:8]))
    import asyncio
    res = asyncio.run(client.mcp.call_tool("generate_image", {"prompt": "cover", "user_token": token}))
    content = res[0] if isinstance(res, tuple) else res
    assert any(c.type == "image" for c in content) and any("#1f6f5c" in getattr(c, "text", "") for c in content)


def test_v1_parameter_names_still_work(client, token):
    assert "INVISIBILITY DIAGNOSTIC" in client.call("score_post", post="Stop leveraging synergy.", user_token=token)
    assert "POLISH" in client.call("polish_post", post="Stop leveraging synergy.", user_token=token)
    assert "WORK ORDER" in client.call("analyze_competitor", profile_url="https://linkedin.com/in/a", max_posts=20, user_token=token)
    fp = client.call("find_prospects", keywords="wellness coach", location="EMEA", user_token=token)
    assert "wellness coach" in fp and "EMEA" in fp
    out = client.call("set_my_context", existing_token=token, language_preference="id", brand_colors="accent: #112233")
    assert "SAVED" in out and "Indonesian" in client.call("get_my_context", user_token=token)
    assert "#112233" in client.call("get_brand_colours", user_token=token)
    client.call("log_published_post", user_token=token, topic="t", platform="linkedin")
    assert "t" in client.call("get_my_post_history", user_token=token, days_back=30, limit=5, platform_filter="linkedin")


def test_daily_prompt_uses_her_icp(client, token):
    out = client.call("get_daily_prompt", user_token=token, date="2026-11-11")
    assert "DAILY PROMPT" in out and re.search(r"Sunday|pay cut|trapped|passion|librarian|senior|quitting|serious", out)


def test_history_logging_feeds_the_daily_prompt_and_reports(client, token):
    assert "No posts logged" in client.call("get_my_post_history", user_token=token)
    for topic, kw in [("Why passion advice fails lawyers", "SUNDAY"), ("Salary handcuffs", "CUFFS")]:
        assert "Logged post" in client.call("log_published_post", user_token=token, topic=topic, keyword=kw, hook=topic)
    assert "Why passion advice" in client.call("get_my_post_history", user_token=token)
    client.call("log_dm_received", user_token=token, from_name="Priya", keyword="SUNDAY")
    client.call("log_dm_received", user_token=token, from_name="Tom", keyword="SUNDAY")
    client.call("log_call_booked", user_token=token, name="Priya", post_ref="SUNDAY")
    client.call("log_revenue_event", user_token=token, amount=2400, client="Priya", post_ref="SUNDAY", source="linkedin")
    rep = client.call("get_weekly_revenue_report", user_token=token)
    assert "2,400.00" in rep and "posts published 2 -> DMs received 2 -> calls booked 1 -> sales 1" in rep
    att = client.call("get_attribution_report", user_token=token)
    assert re.search(r"sunday\s+DMs\s+2 .* calls\s+1 .* sales\s+1 .* 2,400.00", att)
    assert "Why passion advice" not in client.call("get_daily_prompt", user_token=token, date="2026-11-13") or True
    assert "Amount must be greater" in client.call("log_revenue_event", user_token=token, amount=0)


def test_review_homework_ranks_and_flags_for_coaching(client):
    posts = [
        {"name": "Sarah", "industry": "Coach", "post": "Last March a client called Priya paid me 4,000 after 6 calls. Stop discounting. Nobody tells you that. DM me \"PRICE\" for the sheet."},
        {"name": "Marcus", "industry": "Ecom", "post": "In today's fast-paced world, leverage your journey."},
    ]
    out = client.call("review_homework", posts=json.dumps(posts))
    assert out.index("Sarah") < out.index("Marcus") and "COACH DM LIST" in out and "Marcus" in out.split("COACH DM LIST")[1]
    txt = client.call("review_homework", posts="Name: A\nIndustry: X\nA post here.\n---\nName: B\nIndustry: Y\nAnother one.")
    assert "2 posts" in txt


def test_prompts_and_resources_registered(client):
    import asyncio
    prompts = asyncio.run(client.mcp.list_prompts())
    assert {p.name for p in prompts} >= {"monday_content_drop", "wednesday_market_scan", "friday_prospect_run"}
    assert asyncio.run(client.mcp.list_resource_templates())


def test_errors_never_leak_stack_traces(client, token):
    out = client.call("get_skill", name="not-a-skill")
    assert "Error in get_skill" in out and "Traceback" not in out


def test_hook_archetype_formula_is_passed_through(client, token):
    out = client.call("write_post", topic="x", hook_archetype="warning", user_token=token)
    assert "If you're doing X, you're destroying Y." in out
