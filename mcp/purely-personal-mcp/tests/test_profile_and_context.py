import re

from pp_mcp.profile import Profile


def test_parser_extracts_the_participants_own_voice_and_customer(docs):
    p = Profile(token="pp_x", **docs)
    v, c = p.voice, p.customer
    assert len(v["word_bank"]) >= 20 and "salary handcuffs" in v["word_bank"]
    assert "Test it before you torch it" in v["signature_phrases"]
    assert {"journey", "leverage", "hustle"} <= set(v["banned"])
    assert not any(b.lower().startswith(("no ", "rewrite")) for b in v["banned"])
    assert "flat white" in v["test_line"]
    assert any("trapped by my own salary" in w for w in c["their_words"])
    assert len(c["objections"]) == 5 and all(len(o) > 10 for o in c["objections"])
    assert p.colours["accent"] == "#1f6f5c" and p.colours["ink"] == "#14201c"


def test_audit_flags_a_thin_brain():
    p = Profile(token="pp_x", brain="I coach people.")
    a = p.audit()
    assert not a["ready"] and a["score"] < 40
    assert any("Word bank" in c["check"] and not c["ok"] for c in a["checks"])


def test_set_get_check_clear_roundtrip(client, docs):
    out = client.call("set_my_context", name="Maya Okafor", **docs)
    tok = re.search(r"pp_\S+", out).group(0)
    assert "READY" in out and "Maya Okafor" in out
    ctx = client.call("get_my_context", user_token=tok, include_documents=True)
    assert "flat white" in ctx and "Fraunces" in ctx
    assert "BRAIN CHECK" in client.call("check_my_brain", user_token=tok)
    assert "confirm=true" in client.call("clear_my_context", user_token=tok)
    assert "Cleared" in client.call("clear_my_context", user_token=tok, confirm=True)
    assert "No profile found" in client.call("get_my_context", user_token=tok)


def test_update_keeps_other_fields(client, token):
    client.call("set_my_context", user_token=token, language="Bahasa Indonesia")
    ctx = client.call("get_my_context", user_token=token, include_documents=True)
    assert "Bahasa Indonesia" in ctx and "flat white" in ctx


def test_token_is_not_stored_in_clear(store, client, token):
    rows = store._db.execute("select token_hash, data from pp_profiles").fetchall()
    assert token not in rows[0][0] and token not in rows[0][1]


def test_each_participant_is_isolated(client, docs):
    a = re.search(r"pp_\S+", client.call("set_my_context", **docs)).group(0)
    b = re.search(r"pp_\S+", client.call("set_my_context", brain="# Brain: Someone Else\n\nI sell boats.", name="Sam")).group(0)
    assert a != b
    assert "boats" not in client.call("get_business_brain", user_token=a)
    assert "flat white" not in client.call("get_business_brain", user_token=b)


def test_no_token_means_setup_not_someone_elses_voice(client):
    for tool, args in [("write_post", {"topic": "x"}), ("get_icp", {}), ("get_voice_dna", {}), ("write_carousel", {"topic": "x"}),
                       ("find_prospects", {}), ("analyze_competitor", {"competitor_urls": "https://linkedin.com/in/a"})]:
        out = client.call(tool, **args)
        assert "SETUP NEEDED" in out and "set_my_context" in out, tool
        assert "Daniel" not in out


def test_bad_and_unknown_tokens_are_handled(client):
    assert "not valid" in client.call("get_icp", user_token="hello")
    assert "No profile found" in client.call("get_icp", user_token="pp_doesnotexist12345")


def test_demo_profile_works_but_cannot_store(client):
    assert "Daniel" in client.call("get_business_brain", user_token="demo")
    assert "needs a saved profile" in client.call("log_published_post", user_token="demo", topic="x")
    assert "read-only" in client.call("set_my_context", user_token="demo", brain="x")


def test_one_off_overrides_work_without_saving(client, docs):
    out = client.call("write_post", topic="Sunday dread", brain_override=docs["brain"], voice_override=docs["voice_dna"])
    assert "flat white" in out and "SETUP NEEDED" not in out
