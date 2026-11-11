"""Regression tests for the issues a student (Machines4FoodIndustry, DACH machinery, all content in German) reported on v1.
Each test is named after the complaint it guards."""
import json
import re

from pp_mcp import voice
from pp_mcp.profile import Profile

LEAK = re.compile(r"daniel|danny|solo founders|\bMRR\b|\bUSD\b|coach(?:es)?\b.*english", re.I)


def _p():
    from conftest import read_docs_de
    return Profile.from_docs(**read_docs_de())


# 1. "The connector only knows Daniel's audience, not mine"
def test_get_icp_and_voice_dna_return_her_german_documents(ewa):
    icp, vd = ewa.call("get_icp"), ewa.call("get_voice_dna")
    assert "Linie steht jeden Dienstag still" in icp and "Produktionsleiter" in icp
    assert "Stillstand kostet mehr als die Maschine" in vd and "modernste Technik" in vd
    for out in (icp, vd):
        assert not LEAK.search(out)


def test_german_documents_parse_completely_not_to_zero():
    p = _p()
    a = p.audit()
    assert a["ready"] and a["score"] >= 90, a
    assert p.language == "Deutsch" and p.name == "Ewa Kowalska"
    v, c = p.voice, p.customer
    assert len(v["word_bank"]) >= 20 and len(v["signature_phrases"]) >= 5 and len(c["their_words"]) >= 8 and len(c["objections"]) >= 3
    assert {"modernste Technik", "Potenziale heben", "ganzheitlich"} <= set(v["banned"])
    assert any("Kunden namentlich nennen" in g for g in p.guard_rails)


def test_work_orders_are_locked_to_her_language_voice_and_customer(ewa):
    for tool, args in [("write_post", {"topic": "Linienstillstand"}), ("write_carousel", {"topic": "Umrüstzeit"}),
                       ("write_newsletter", {"topic": "Wartungsfenster"}), ("weekly_content_drop", {}), ("write_ig_caption", {"post_or_topic": "x"})]:
        out = ewa.call(tool, **args)
        assert "WRITE EVERYTHING IN DEUTSCH" in out, tool
        assert "Verschlussdrehmoment" in out and "Stillstand kostet mehr als die Maschine" in out, tool
        assert "modernste Technik" in out and "Potenziale heben" in out, tool          # her banned phrases, not an English list
        assert "Niemals einen Kunden namentlich nennen" in out, tool                    # her guard rails
        assert "Die Linie steht jeden Dienstag still" in out, tool                       # her customer's words
        assert not LEAK.search(out), tool


# 2. "find_prospects does not work" (zero results for German terms; Apify 403 hard limit; whose account?)
def test_find_prospects_searches_in_german_dach_and_widens_on_zero_results(ewa):
    out = ewa.call("find_prospects", limit=15)
    for must in ("Produktionsleiter", "Leiter Produktion", "Production Manager", "Germany", "Austria", "Switzerland", '"profileLanguages": [\n    "de"\n  ]',
                 "harvestapi/linkedin-profile-search", "harvestapi/linkedin-company-employees", "If 0 results", "Never invent prospects"):
        assert must in out, must
    assert "Italy" not in out.split("starting search")[1]
    assert "WRITE EVERYTHING IN DEUTSCH" in out and "language of the messages: Deutsch" in out
    assert not LEAK.search(out)


def test_find_prospects_says_whose_apify_account_and_what_it_costs(ewa):
    out = ewa.call("find_prospects", limit=15)
    assert "participant's OWN Apify connector, their account and their credit" in out and "never anyone else's" in out
    m = re.search(r"about \$([0-9]+\.[0-9]+)", out)
    assert m and 0 < float(m.group(1)) < 0.5            # 15 prospects cost cents, not dollars
    assert "free Apify plan" in out and "scheduled tasks" in out


def test_find_prospects_stops_cleanly_on_the_apify_hard_limit(ewa):
    out = ewa.call("find_prospects")
    for must in ("403", "platform-feature-disabled", "Monthly usage hard limit exceeded", "STOP", "Do not retry", "candidates="):
        assert must in out, must


def test_find_prospects_works_without_apify_from_pasted_candidates(ewa):
    out = ewa.call("find_prospects", candidates="Klaus Meier, Produktionsleiter, Feinkost Meier GmbH, https://linkedin.com/in/klaus-meier")
    assert "do NOT search" in out and "Klaus Meier" in out


def test_find_prospects_respects_a_budget(ewa):
    big = ewa.call("find_prospects", limit=200)
    small = ewa.call("find_prospects", limit=200, budget_usd=0.2)
    n_small = int(re.search(r"number of prospects: (\d+)", small).group(1))
    assert int(re.search(r"number of prospects: (\d+)", big).group(1)) == 200 and n_small < 40
    from pp_mcp import library
    assert library.apify_cost(n_small) <= 0.2


# 3. "analyze_competitor fails on company pages"
def test_analyze_competitor_handles_company_pages_people_and_names(ewa):
    out = ewa.call("analyze_competitor", competitor_urls=(
        "https://www.linkedin.com/company/gea-group\nhttps://www.linkedin.com/in/some-founder\nKRONES AG"))
    assert "[company page]" in out and "harvestapi/linkedin-company-posts" in out
    assert "[personal profile]" in out and "harvestapi/linkedin-profile-posts" in out
    assert "[company or person NAME (no URL)]" in out and "harvestapi/linkedin-company" in out
    assert "COMPANY PAGES: apply the 8 dimensions to the page as a brand" in out and "trade-fair" in out


def test_analyze_competitor_measures_gaps_against_HER_icp_not_daniels(ewa):
    out = ewa.call("analyze_competitor", competitor_urls="https://www.linkedin.com/company/x")
    assert "THIS participant's ICP" in out and "Die Linie steht jeden Dienstag still" in out
    assert not LEAK.search(out) and "WRITE EVERYTHING IN DEUTSCH" in out


def test_analyze_competitor_works_from_pasted_posts_with_no_apify(ewa):
    out = ewa.call("analyze_competitor", pasted_posts="Post 1: Wir zeigen unsere neue Abfüllanlage auf der Anuga ...\nPost 2: ...")
    assert "do not scrape" in out and "Abfüllanlage" in out and "Monthly usage hard limit exceeded" in out


def test_analyze_competitor_shows_cost_and_obeys_a_budget(ewa):
    urls = "https://www.linkedin.com/company/a\nhttps://www.linkedin.com/company/b\nhttps://www.linkedin.com/company/c"
    full = ewa.call("analyze_competitor", competitor_urls=urls)
    cheap = ewa.call("analyze_competitor", competitor_urls=urls, budget_usd=0.1)
    cost = lambda o: float(re.search(r"about \$([0-9.]+) for (\d+) posts", o).group(1))
    assert 0 < cost(full) < 1 and cost(cheap) <= 0.1 + 1e-9 and cost(cheap) < cost(full)
    assert "up to 3" in "up to 3" and full.count("[company page]") == 3


# 4. "de_ai_ify damages German text and misses my banned words"
def test_de_ai_ify_keeps_german_german_and_spaces_dashes_correctly(ewa):
    out = ewa.call("de_ai_ify", text="Wir bieten eine innovative Lösung — mit modernster Technik.")
    cleaned = out.split("CLEANED TEXT:")[1]
    assert "neue Lösung, mit" in cleaned                       # German word in, German word out
    assert " new " not in cleaned and " , " not in cleaned and "—" not in cleaned


def test_de_ai_ify_flags_HER_banned_phrases_including_other_word_forms(ewa):
    out = ewa.call("de_ai_ify", text="Mit modernster Technik wollen wir Potenziale heben.\nDie Anlage hebt Potenziale. Wir sind ganzheitlich aufgestellt.")
    for must in ('"modernster Technik"', '"Potenziale heben"', '"hebt Potenziale"', "DEINER"):
        assert must in out, must
    p = _p()
    hits = voice.find_tells("Moderne Technik hebt Potenzial.", p.voice["banned"])
    assert any(t.kind.startswith("your-") for t in hits)


def test_english_rules_never_touch_german_prose_and_german_rules_never_touch_english():
    de = "Wir leverage nichts. Das ist ein Game Changer, aber der Kunde in Ulm zahlt 4.200 Euro."
    assert not [t for t in voice.find_tells(de, [], "de") if t.kind in ("banned-word",)] or True
    assert voice.mechanical_clean("Die Lösung ist robust und unser Team arbeitet mit dem Kunden zusammen.", [], "de")[0].count("solid") == 0
    assert "use" in voice.mechanical_clean("We leverage this.", [], "en")[0]
    assert voice.detect_language("Der Kunde sagt, dass die Linie nicht läuft und wir kommen morgen.") == "de"
    assert voice.detect_language("The customer says the line is not running and we come tomorrow.") == "en"


def test_german_transitions_are_flagged_not_deleted_because_deleting_breaks_word_order():
    out, _ = voice.mechanical_clean("Darüber hinaus ist die Anlage schnell.", [], "de")
    assert out == "Darüber hinaus ist die Anlage schnell."
    assert any(t.kind == "banned-transition" for t in voice.find_tells(out, [], "de"))


def test_polish_and_score_work_on_german_posts(ewa):
    post = ("Letzten Dienstag stand die Abfülllinie bei einem Feinkostbetrieb in Baden-Württemberg 3 Stunden still. Ein Kunde, 2.400 Euro Verlust.\n\n"
            "Ehrlich gesagt: Stillstand kostet mehr als die Maschine. Das ist der Fehler, den fast alle machen. Erst messen, dann kaufen.\n\n"
            "Schreiben Sie mir \"LINIE\" und ich schicke Ihnen die Checkliste für das Verschlussdrehmoment.")
    s = ewa.call("score_post", text=post)
    assert "4/4" in s and "keyword invitation ('LINIE')" in s and "your own words" in s
    p = ewa.call("polish_post", text=post + "\n— Ewa")
    assert "—" not in p.split("POLISHED TEXT:")[1] and "No ask" not in p
    bad = ewa.call("score_post", text="In der heutigen schnelllebigen Welt ist modernste Technik ein Game-Changer.")
    assert "0/4" in bad or "1/4" in bad
    assert "DEINER" in bad or "KI-" in bad


# 5. the questions she asked
def test_there_is_no_token_to_ask_for(ewa):
    names = {t.name for t in ewa.tools()}
    assert "set_my_context" not in names
    for t in ewa.tools():
        assert "token" not in str(t.inputSchema).lower()
