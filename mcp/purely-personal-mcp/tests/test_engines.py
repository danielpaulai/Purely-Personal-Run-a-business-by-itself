from pp_mcp import scoring, voice
from pp_mcp.profile import Profile

STRONG = """Last March a senior associate called Priya told me she bills 2,100 hours a year and still feels trapped by her own salary.

Most career advice is wrong. Stop telling lawyers to follow their passion. It helps nobody.

Salary handcuffs are real. Test it before you torch it: one small experiment, low risk, 5 hours a week for 6 weeks.

DM me "SUNDAY" and I will send you the experiment plan."""

WEAK = """In today's fast-paced world, it's important to note that leveraging your journey can unlock your potential.

Moreover, a holistic approach is a game-changer. Hope this helps!"""


def test_strong_post_scores_higher_than_weak_and_explains_why(docs):
    p = Profile(token="pp_x", **docs)
    s, w = scoring.diagnose(STRONG, p), scoring.diagnose(WEAK, p)
    assert s["score"] == 4 and s["tier"] == "Magnetic"
    assert w["score"] <= 1 and w["tier"] == "Invisible" and w["fixes"] and w["ai_tells"]
    assert s["dimensions"]["Voice"]["point"] == 1 and "your own words" in s["dimensions"]["Voice"]["why"]


def test_asking_accepts_question_unless_strict():
    q = "I watched a client lose 12 weeks to a bad plan. Stop guessing. What is the one thing you would test first if money was no object today?"
    assert scoring.diagnose(q)["dimensions"]["Asking"]["point"] == 1
    assert scoring.diagnose(q, strict_asking=True)["dimensions"]["Asking"]["point"] == 0


def test_fix_lines_use_the_participants_signature_phrases(docs):
    p = Profile(token="pp_x", **docs)
    d = scoring.diagnose(WEAK, p)
    assert any("Test it before you torch it" in f or "Salary handcuffs" in f for f in d["fixes"])


def test_find_tells_catches_the_blacklist_with_line_numbers():
    t = voice.find_tells("Great start\nIt's not about the tool, it's about the system — really.\nLet's leverage this.\nThoughts?")
    kinds = {x.kind for x in t}
    assert {"em-dash", "contrast-frame", "banned-word", "banned-closing"} <= kinds
    assert all(x.line >= 1 for x in t)


def test_users_own_banned_list_is_enforced():
    t = voice.find_tells("My hustle journey was a rockstar move.", ["hustle", "rockstar", "unlock your potential"])
    assert {x.match.lower() for x in t if x.kind.startswith("your-")} >= {"hustle", "rockstar"}


def test_mechanical_clean_never_leaves_em_dashes_and_swaps_filler():
    out, changes = voice.mechanical_clean("We leverage AI — and it is seamless.\nMoreover, utilize it.\nHope this helps")
    assert "—" not in out and "leverage" not in out.lower() and "seamless" not in out and "Hope this helps" not in out
    assert not out.lower().startswith("moreover") and "Moreover" not in out
    assert changes


def test_polish_reports_length_hook_and_missing_ask():
    r = voice.polish("Short post about nothing in particular.\n\nIt ends with a statement.", "linkedin")
    assert r["chars"] < 1300 and any("under the linkedin target" in i for i in r["structure_issues"])
    assert any("No ask" in i for i in r["structure_issues"])
    x = voice.polish("Stop guessing #ai #marketing", "x")
    assert any("Hashtags on X" in i for i in x["structure_issues"])


def test_daily_prompt_is_rotating_personal_and_avoids_recent(docs):
    import datetime as dt

    from pp_mcp import library
    p = Profile(token="pp_x", **docs)
    a = library.daily_prompt(p, dt.date(2026, 11, 11))
    b = library.daily_prompt(p, dt.date(2026, 11, 12))
    assert a["today"]["prompt"] != b["today"]["prompt"]
    pool = [x.strip(" .\"'") for x in p.customer["their_words"] + p.customer["objections"] + p.customer["themes"]]
    assert a["today"]["seed"] in pool
    recent = library.daily_prompt(p, dt.date(2026, 11, 11), [a["today"]["seed"]])
    assert recent["today"]["seed"] != a["today"]["seed"]


def test_prospect_query_comes_from_the_icp(docs):
    from pp_mcp import library
    q = library.prospect_query(Profile(token="pp_x", **docs))
    assert "United Kingdom" in q["geography"] or "UK" in q["geography"] or "London" in q["geography"]
    assert q["confidence"] in ("medium", "high") and "harvestapi/linkedin-profile-search" in q["apify_actors"]
