import re

from pp_mcp.profile import Profile


def test_parser_extracts_the_participants_own_voice_and_customer(docs):
    p = Profile.from_docs(**docs)
    v, c = p.voice, p.customer
    assert len(v["word_bank"]) >= 20 and "salary handcuffs" in v["word_bank"]
    assert "Test it before you torch it" in v["signature_phrases"]
    assert {"journey", "leverage", "hustle"} <= set(v["banned"])
    assert not any(b.lower().startswith(("no ", "rewrite")) for b in v["banned"])
    assert "flat white" in v["test_line"]
    assert any("trapped by my own salary" in w for w in c["their_words"])
    assert len(c["objections"]) == 5 and all(len(o) > 10 for o in c["objections"])
    assert p.colours["accent"] == "#1f6f5c" and p.colours["ink"] == "#14201c"
    assert p.name == "Maya Okafor"


def test_guard_rails_and_language_come_from_the_brain_itself(docs):
    p = Profile.from_docs(**docs)
    assert any("guarantee" in g.lower() for g in p.guard_rails) and any("name a client" in g.lower() for g in p.guard_rails)
    assert Profile.from_docs(brain="Name: Sam\nLanguage: Bahasa Indonesia\nI sell boats " * 20).language == "Bahasa Indonesia"
    assert Profile.from_docs(brain="x" * 400).language == "English"


def test_audit_flags_a_thin_brain():
    a = Profile.from_docs(brain="I coach people.").audit()
    assert not a["ready"] and a["score"] < 40
    assert any("Word bank" in c["check"] and not c["ok"] for c in a["checks"])


def test_check_my_brain_reads_the_documents_passed(client, docs):
    out = client.call("check_my_brain", **docs)
    assert "READY" in out and "salary handcuffs" in out and "trapped by my own salary" in out
    assert "NOT READY" in client.call("check_my_brain", brain="I coach people.")


def test_no_documents_means_a_request_for_them_not_someone_elses_voice(client):
    for tool, args in [("write_post", {"topic": "x"}), ("get_icp", {}), ("get_voice_dna", {}), ("write_carousel", {"topic": "x"}),
                       ("find_prospects", {}), ("analyze_competitor", {"competitor_urls": "https://linkedin.com/in/a"}),
                       ("weekly_content_drop", {}), ("setup_marketing_employee", {}), ("check_my_brain", {})]:
        out = client.call(tool, **args)
        assert "I need YOUR documents" in out, tool
        assert not re.search(r"daniel|danny|solo founders", out, re.I), tool


def test_each_call_uses_only_its_own_documents(client, docs):
    a = client.call("get_icp", **docs)
    b = client.call("get_icp", brain="# Brain: Sam Boats\n\n## THEIR WORDS\n- \"my hull is leaking\"\n- \"the marina wants more\"\n")
    assert "trapped by my own salary" in a and "hull" not in a
    assert "my hull is leaking" in b and "salary" not in b


def test_tools_have_no_token_or_override_parameters(client):
    for t in client.tools():
        blob = str(t.inputSchema).lower() + (t.description or "").lower()
        assert "token" not in blob and "override" not in blob, t.name
    names = {t.name for t in client.tools()}
    assert not ({"set_my_context", "get_my_context", "clear_my_context", "get_business_brain"} & names)


def test_local_install_reads_documents_from_a_folder(local):
    c, _ = local
    assert "flat white" in c.call("write_post", topic="Sunday dread")
    assert "trapped by my own salary" in c.call("get_icp")


def test_explicit_documents_beat_the_local_folder(local):
    c, _ = local
    out = c.call("get_icp", brain="# Other\n\n## THEIR WORDS\n- \"different person\"\n- \"another phrase\"\n- \"third\"\n")
    assert "different person" in out and "trapped by my own salary" not in out
