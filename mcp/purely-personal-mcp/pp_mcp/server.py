"""Purely Personal MCP v2.

The toolkit behind "Build Your 1st AI Employee". Every content tool runs one of the
program's 12 skills locked to the participant's own Business Brain, ICP and Voice DNA.
Nothing falls back to someone else's voice.

Run:
    python -m pp_mcp.server              # stdio (Claude Desktop / Claude Code)
    python -m pp_mcp.server --http 8000  # streamable HTTP at /mcp (remote connector)
"""
from __future__ import annotations

import datetime as dt
import functools
import json
import os
import re
import sys
import time

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

from . import library, scoring, skills, voice
from .profile import DEFAULT_BRAND, MAX_DOC, Profile
from .store import Store, default_store, new_token, valid_token

VERSION = "2.0.0"
DEMO_TOKENS = {"demo", "pp_demo"}

INSTRUCTIONS = """\
Purely Personal: the toolkit for Build Your 1st AI Employee.
Every writing, research and scoring tool is locked to the operator's OWN Business Brain, ICP and Voice DNA.
First time: call set_my_context with the three Day 1 documents to get a pp_ token, then pass it as
user_token on every call. Writing tools return a WORK ORDER: execute it, then run score_post,
polish_post and de_ai_ify on the draft before delivering. Never invent clients, results or numbers.
Call get_setup_guide for the full map of tools."""

_RO = ToolAnnotations(readOnlyHint=True, openWorldHint=False)
_WRITE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=False)
_DESTROY = ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=True, openWorldHint=False)


HOOK_ARCHETYPES = {
    "personal-pivot": "I stopped X. Because Y.",
    "warning": "If you're doing X, you're destroying Y.",
    "detection": "I can spot X. Because Y.",
    "contrarian-reframe": "X is the worst place for Y. Because Z.",
    "stat-lead-magnet": "I audited X. And Y% are losing because of Z.  (only with a real figure from the Brain)",
}


def _render_image(prompt: str, size: str) -> bytes:
    """OpenAI gpt-image-1. Isolated so tests can replace it."""
    import base64

    import httpx
    r = httpx.post("https://api.openai.com/v1/images/generations", timeout=120,
                   headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                   json={"model": "gpt-image-1", "prompt": prompt, "size": size, "n": 1})
    r.raise_for_status()
    return base64.b64decode(r.json()["data"][0]["b64_json"])


class SetupNeeded(Exception):
    pass


def build_server(store: Store | None = None) -> FastMCP:
    store = store or default_store()
    mcp = FastMCP(
        "purely-personal", instructions=INSTRUCTIONS, stateless_http=True, json_response=True,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )

    # ------------------------------------------------------------------ helpers
    def load(user_token: str = "", brain_override: str = "", icp_override: str = "", voice_override: str = "",
             need: bool = True) -> Profile | None:
        tok = (user_token or "").strip()
        p: Profile | None = None
        if tok.lower() in DEMO_TOKENS:
            demo = (skills.DATA / "demo-brain.md").read_text()
            p = Profile(token="demo", name="Daniel Paul (demo)", brain=demo, demo=True)
        elif tok:
            if not valid_token(tok):
                raise SetupNeeded("That token is not valid. Tokens start with pp_. Call set_my_context to create one.")
            d = store.get_profile(tok)
            if d is None:
                raise SetupNeeded("No profile found for that token (it may have been cleared). Call set_my_context again.")
            p = Profile.from_dict(tok, d)
        if brain_override or icp_override or voice_override:
            p = p or Profile(token="")
            p.brain = brain_override or p.brain
            p.icp = icp_override or p.icp
            p.voice_dna = voice_override or p.voice_dna
        if p is None and need:
            raise SetupNeeded(skills.NEEDS_SETUP)
        return p

    def need_real(p: Profile, what: str) -> None:
        if p.demo or not p.token:
            raise SetupNeeded(f"{what} needs a saved profile. Call set_my_context first and pass your pp_ token (the demo and one-off overrides cannot store data).")

    def safe(fn):
        @functools.wraps(fn)
        def inner(*a, **kw):
            try:
                return fn(*a, **kw)
            except SetupNeeded as e:
                return str(e)
            except Exception as e:  # never leak a stack trace to the client
                return f"Error in {fn.__name__}: {type(e).__name__}: {e}"
        return inner

    def tool(annotations: ToolAnnotations = _RO):
        def deco(fn):
            return mcp.tool(annotations=annotations)(safe(fn))
        return deco

    def banned_for(p: Profile | None) -> list[str]:
        return p.voice["banned"] if p else []

    def events(p: Profile, kind: str | None = None, days: int | None = None) -> list[dict]:
        if p.demo or not p.token:
            return []
        since = time.time() - days * 86400 if days else None
        return store.events(p.token, kind, since)

    def norm_platform(x: str, default: str = "linkedin") -> str:
        x = (x or default).lower().strip().replace("twitter", "x").replace("ig", "instagram").replace("fb", "facebook")
        return x if x in voice.PLATFORMS else default

    def pick(value: str, options: dict[str, str], default: str) -> str:
        v = (value or "").lower().strip().replace("_", "-").replace(" ", "-")
        for k, canon in options.items():
            if v == k or v.startswith(k):
                return canon
        return default

    def tok_of(p: Profile) -> str:
        return p.token if p.token and not p.demo else ""

    # ====================================================================
    # 1. CONTEXT: your Business Brain, ICP and Voice DNA
    # ====================================================================
    @tool(_WRITE)
    def set_my_context(brain: str = "", icp: str = "", voice_dna: str = "", name: str = "", language: str = "",
                       never_claim: str = "", platform: str = "", handle: str = "", brand_colours: str = "",
                       user_token: str = "", existing_token: str = "", brand_colors: str = "", brand_guide: str = "",
                       email: str = "", language_preference: str = "", linkedin_url: str = "") -> str:
        """Save your Business Brain, ICP and Voice DNA (the three Day 1 documents) and get a pp_ token.
        Paste each document in full; do not shorten them. Pass an existing user_token to update only the
        fields you provide. Optional: name, language you publish in, never_claim (what your employee must
        never claim), platform (linkedin/instagram/facebook), handle, brand_colours ('accent=#e90d41, ink=#0d0d0f').
        Also accepts v1 parameter names: existing_token, brand_colors, brand_guide, language_preference, linkedin_url.
        Returns the token plus a readiness audit showing exactly what was parsed and what is thin."""
        user_token = user_token or existing_token
        brand_colours = brand_colours or brand_colors
        language = language or ({"en": "English", "vi": "Vietnamese", "zh": "Chinese", "es": "Spanish", "fr": "French",
                                 "de": "German", "pt": "Portuguese", "id": "Indonesian"}.get(language_preference, language_preference))
        handle = handle or linkedin_url
        if brand_guide.strip():
            brain = (brain + "\n\n## BRAND GUIDE\n" + brand_guide.strip()).strip() if brain else ""
            if not brain:
                voice_dna = (voice_dna + "\n\n## BRAND GUIDE\n" + brand_guide.strip()).strip()
        existing = None
        if user_token.strip():
            if user_token.strip().lower() in DEMO_TOKENS:
                raise SetupNeeded("The demo profile is read-only. Omit user_token to create your own.")
            if not valid_token(user_token):
                raise SetupNeeded("That token is not valid. Tokens start with pp_.")
            existing = store.get_profile(user_token)
            if existing is None:
                raise SetupNeeded("Unknown token. Omit user_token to create a new profile.")
        if not existing and not (brain.strip() or icp.strip() or voice_dna.strip()):
            raise SetupNeeded("Provide at least one of brain, icp or voice_dna (ideally all three, in full).")
        p = Profile.from_dict(user_token.strip() if existing else "", existing or {})
        for f, v in (("brain", brain), ("icp", icp), ("voice_dna", voice_dna), ("name", name), ("language", language),
                     ("never_claim", never_claim), ("platform", platform), ("handle", handle)):
            if v.strip():
                setattr(p, f, v.strip())
        if brand_colours.strip():
            for k, v in re.findall(r"([a-z]+)\s*[=:]\s*(#[0-9a-fA-F]{6})", brand_colours):
                p.brand[k.lower()] = v.lower()
        p.clipped()
        if not p.name:
            from .profile import extract_name
            p.name = extract_name(p.brain, p.icp, p.voice_dna)
        p.platform = norm_platform(p.platform)
        now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        p.created = p.created or now
        p.updated = now
        token = p.token or new_token()
        store.put_profile(token, p.to_dict())
        p.token = token
        a = p.audit()
        miss = [c for c in a["checks"] if not c["ok"]]
        lines = [f"SAVED. Your token: {token}",
                 "Keep it private: it is the key to your profile. Pass it as user_token on every tool.", "",
                 f"Readiness {a['score']}/100 · " + ("READY" if a["ready"] else "NOT READY: fix the items below, then call set_my_context again with your user_token."),
                 f"Parsed: {a['counts']['word_bank']} word-bank items · {a['counts']['signature_phrases']} signature phrases · "
                 f"{a['counts']['banned']} banned items · {a['counts']['customer_phrases']} customer phrases · "
                 f"{a['counts']['objections']} objections · {a['counts']['themes']} themes"]
        if miss:
            lines += ["", "TO FIX:"] + [f"  - {c['check']}: {c['fix']}" for c in miss]
        lines += ["", f"Operator: {p.name or '(not detected: pass name=)'} · language {p.language} · platform {p.platform}"]
        return "\n".join(lines)

    @tool()
    def get_my_context(user_token: str, include_documents: bool = False) -> str:
        """Retrieve what is saved under your token: settings, readiness and (optionally) the three full documents,
        so you can verify it or copy it to another machine."""
        p = load(user_token)
        a = p.audit()
        out = {"name": p.name, "language": p.language, "platform": p.platform, "handle": p.handle,
               "never_claim": p.never_claim, "brand": p.colours, "updated": p.updated,
               "readiness": a["score"], "counts": a["counts"],
               "document_chars": {"brain": len(p.brain), "icp": len(p.icp), "voice_dna": len(p.voice_dna)}}
        if include_documents:
            out.update({"brain": p.brain, "icp": p.icp, "voice_dna": p.voice_dna})
        return json.dumps(out, indent=2)

    @tool()
    def check_my_brain(user_token: str) -> str:
        """Audit your Business Brain, ICP and Voice DNA: what is present, what is thin, and exactly how to fix each gap.
        Run this after set_my_context, and any time your output feels generic (a thin brain is the usual cause)."""
        p = load(user_token)
        a = p.audit()
        v, c = p.voice, p.customer
        lines = [f"BRAIN CHECK · {a['score']}/100 · {'READY' if a['ready'] else 'NOT READY'}", ""]
        lines += [f"  {'✓' if x['ok'] else '✗'} {x['check']}" + ("" if x["ok"] else f"  ->  {x['fix']}") for x in a["checks"]]
        lines += ["", "What the tools will lock to:",
                  f"  Word bank: {', '.join(v['word_bank'][:8]) or '(none)'}",
                  f"  Signature phrases: {' | '.join(v['signature_phrases'][:4]) or '(none)'}",
                  f"  Your banned list: {', '.join(v['banned'][:8]) or '(none; universal blacklist only)'}",
                  f"  Customer phrases: {' | '.join(c['their_words'][:3]) or '(none)'}"]
        if p.brain and (p.icp or p.voice_dna):
            lines += ["", "Reconcile: the Brain wins on any disagreement with the ICP or Voice DNA files."]
        return "\n".join(lines)

    @tool(_DESTROY)
    def clear_my_context(user_token: str, confirm: bool = False) -> str:
        """Permanently delete your saved profile and all logged events (posts, DMs, calls, revenue). Requires confirm=true."""
        p = load(user_token)
        if p.demo:
            return "The demo profile is read-only; there is nothing to clear."
        if not confirm:
            return "This permanently deletes your Business Brain, ICP, Voice DNA and every logged event. Call again with confirm=true to proceed."
        return "Cleared. Your token no longer works." if store.delete_profile(user_token) else "Nothing found for that token."

    @tool()
    def get_icp(user_token: str = "", view: str = "full") -> str:
        """Return YOUR ICP (not anyone else's): the person you write for, their words, objections and themes.
        view='full' returns the saved document plus parsed fields; view='parsed' returns the parsed fields only."""
        p = load(user_token)
        c = p.customer
        parsed = "PARSED ICP\n" + json.dumps(c, indent=2)
        if view == "parsed":
            return parsed
        return (p.icp or "(no separate ICP saved; the Business Brain carries the customer section)\n\n" + p.brain[:6000]) + "\n\n---\n" + parsed

    @tool()
    def get_voice_dna(user_token: str = "", view: str = "full") -> str:
        """Return YOUR Voice DNA: word bank, signature phrases, writing rules, banned list and the test every piece must pass.
        view='full' returns the saved document plus parsed fields; view='parsed' returns the parsed fields only."""
        p = load(user_token)
        parsed = "PARSED VOICE DNA\n" + json.dumps(p.voice, indent=2)
        if view == "parsed":
            return parsed
        return (p.voice_dna or "(no separate Voice DNA saved; the Business Brain carries the voice section)\n\n" + p.brain[:6000]) + "\n\n---\n" + parsed

    @tool()
    def get_business_brain(user_token: str = "") -> str:
        """Return YOUR Business Brain document exactly as saved (the source of truth every tool reads first)."""
        p = load(user_token)
        return p.brain or "(no combined Business Brain saved; the tools use your ICP and Voice DNA directly)"

    @tool()
    def get_setup_guide() -> str:
        """The map: how the program fits together and which tool to use for what. Call this if you are unsure where to start."""
        rows = "\n".join(f"  {r['name']:<28} v{r['version']}" for r in skills.catalogue())
        return f"""\
PURELY PERSONAL MCP v{VERSION}: how it fits together

THE BRAIN (Day 1)  ICP.md + VOICE-DNA.md -> BUSINESS-BRAIN.md
  set_my_context -> returns your pp_ token. check_my_brain -> readiness. Every other tool takes user_token.

THE HANDS (12 skills, each one a tool family)
{rows}

WRITE     write_post · write_carousel · write_cheatsheet · weekly_content_drop · write_newsletter
          amplify_post · write_tweet · write_ig_caption · write_reel_script · first_post_coach
RESEARCH  analyze_competitor · find_prospects · get_daily_prompt · get_my_post_history · list_post_templates
QUALITY   score_post · polish_post · de_ai_ify · review_homework        (deterministic, run in code)
DESIGN    get_brand_colours · generate_image
TRACK     log_published_post · log_dm_received · log_call_booked · log_revenue_event
          get_weekly_revenue_report · get_attribution_report
SETUP     setup_marketing_employee · build_voice_profile · check_my_brain · list_skills · get_skill

HOW A WRITING TOOL WORKS: it returns a work order = the skill's method + your Brain/ICP/Voice lock + hard rules.
You execute it, then run score_post (aim 4/4), polish_post and de_ai_ify before delivering.
If the Brain, ICP and Voice DNA disagree, the Brain wins."""

    # ====================================================================
    # 2. SKILLS: the 12 program skills
    # ====================================================================
    @tool()
    def list_skills() -> str:
        """List the 12 program skills bundled in this server, with versions and what each one does."""
        return "\n\n".join(f"{r['name']} (v{r['version']})\n  {r['description'][:300]}" + (f"\n  prompts: {', '.join(r['prompts'])}" if r["prompts"] else "")
                           for r in skills.catalogue())

    @tool()
    def get_skill(name: str, part: str = "method") -> str:
        """Return a bundled skill. part='method' (process + output + checklist), 'full' (whole SKILL.md),
        or a prompt filename such as 'intent-driven.md' for skills that ship prompts."""
        if part == "full":
            return skills.skill_md(name)
        if part.endswith(".md"):
            t = skills.prompt_file(name, part)
            return t or f"No prompt '{part}' in {name}. Available: {', '.join(skills.prompt_files(name)) or 'none'}"
        return skills.skill_sections(name, "Process", "Output", "Quality", "Self-Critique", "Mode", "Required") or skills.skill_md(name)

    @tool()
    def setup_marketing_employee(mode: str = "full", user_token: str = "") -> str:
        """Run the ai-marketing-employee skill: generate the personalised Project Instructions, the 3-step install guide
        and a validation post for your Claude Project, from your saved profile. mode: quick | full | validated | refresh."""
        p = load(user_token)
        m = pick(mode, {"quick": "quick", "full": "full", "valid": "validated", "refresh": "refresh"}, "full")
        return skills.work_order(
            title="Install my AI Marketing Employee", skill="ai-marketing-employee", p=p,
            method=skills.skill_sections("ai-marketing-employee", "Why This", "Required Inputs", "Mode", "Process", "The Project Instructions Template", "Output Structure", "Self-Critique"),
            inputs={"mode": m, "voice_profile": "the VOICE LOCK above + Voice DNA", "industry_context": "the Business Brain above"},
            task="Generate my personalised Project Instructions from my saved profile, then the 3-step install guide. "
                 + ("Run the validation post and score it with score_post." if m == "validated" else "Skip validation."),
            contract="1) Project Instructions in one fenced block ready to paste. 2) The 3-step install guide (create project, add the one Business Brain file to knowledge, paste instructions). 3) A 30-second test prompt.",
            checks=["Confirm the instructions name my customer, my banned list and my never-claim rule.", "Confirm no em dashes and no invented facts."])

    @tool()
    def build_voice_profile(past_posts: str = "", voice_notes: str = "", dm_replies: str = "", faq: str = "",
                            mode: str = "standard", user_token: str = "") -> str:
        """Run the voice-profile-builder skill on the 4 inputs (past posts, voice-note transcripts, DM/email replies, FAQ answers)
        and produce a hardened, paste-ready Voice Profile. With no inputs it hardens the Voice DNA already saved."""
        p = load(user_token)
        have = {k: bool(v.strip()) for k, v in {"past_posts": past_posts, "voice_notes": voice_notes, "dm_replies": dm_replies, "faq": faq}.items()}
        return skills.work_order(
            title="Build / harden my Voice Profile", skill="voice-profile-builder", p=p,
            method=skills.skill_sections("voice-profile-builder", "The 4 Inputs", "Mode", "Context Loading", "Process", "Output Structure", "Self-Critique"),
            inputs={"mode": mode, "inputs_provided": ", ".join(k for k, v in have.items() if v) or "none (harden the saved Voice DNA)",
                    "PAST POSTS": past_posts, "VOICE NOTES": voice_notes, "DM / EMAIL REPLIES": dm_replies, "FAQ": faq},
            task="Extract vocabulary, beliefs, rhythm and format from the inputs. Flag thin inputs honestly (THINNESS FLAGS). Never improve my words.",
            contract="The Voice Profile exactly as the Output Structure specifies, paste-ready for Project Knowledge, with thinness flags.",
            checks=["Check every example uses words from the extracted word bank.", "No em dashes."])

    # ====================================================================
    # 3. WRITE
    # ====================================================================
    def _post_args(p: Profile, topic, intent, brain_dump, cta_keyword, language, real_result):
        return {"topic": topic, "content_intent": intent or "(infer from topic; state which you chose)",
                "reference_material / brain dump": brain_dump, "real result to anchor": real_result,
                "DM keyword for the ask": cta_keyword or "(choose one derived from my offer and use it in the last 2 lines)",
                "publishing language": language or p.language}

    @tool()
    def write_post(topic: str, intent: str = "", mode: str = "intent-driven", brain_dump: str = "", real_result: str = "",
                   cta_keyword: str = "", hook_archetype: str = "auto", language: str = "", user_token: str = "",
                   voice_override: str = "", icp_override: str = "", brain_override: str = "") -> str:
        """Write a LinkedIn text post in YOUR voice with the linkedin-post-writer skill. mode: intent-driven (default) |
        framework-heavy (save-bait list) | story-flow (needs a real story). intent: Educating | Nurturing | Soft Selling |
        Hard Selling | Engagement. brain_dump = raw facts/story the post may use (the only allowed source of names and numbers).
        hook_archetype: personal-pivot | warning | detection | contrarian-reframe | stat-lead-magnet | auto.
        Returns a work order; execute it, then score_post/polish_post/de_ai_ify. Needs user_token (or *_override for one-off use)."""
        p = load(user_token, brain_override, icp_override, voice_override)
        m = pick(mode, {"intent": "intent-driven", "framework": "framework-heavy", "story": "story-flow"}, "intent-driven")
        method = skills.prompt_file("linkedin-post-writer", f"{m}.md") + "\n\n" + skills.skill_sections("linkedin-post-writer", "Process", "Quality Checklist")
        inp = _post_args(p, topic, intent, brain_dump, cta_keyword, language, real_result)
        inp["hook archetype"] = (f"{hook_archetype}: {HOOK_ARCHETYPES[hook_archetype]} (fill X/Y/Z from MY customer's world, in MY words)"
                                 if hook_archetype in HOOK_ARCHETYPES else "auto: choose the strongest for this topic and intent")
        inp["template"] = m
        note = ""
        if m == "story-flow" and not (brain_dump.strip() or real_result.strip()):
            note = " Story-Flow requires a documented story: use one from my Business Brain; if there is none that fits, say so and ask me for one instead of inventing it."
        return skills.work_order(
            title=f"LinkedIn post · {m}", skill="linkedin-post-writer", p=p, method=method, inputs=inp,
            task=f"Write one LinkedIn post about the topic, 1300-1500 characters, in my voice, for my customer.{note}",
            contract="Just the post, no preamble. Last line of your reply, separate from the post: [chars · intent · template · self-scored N/4].")

    @tool()
    def first_post_coach(draft: str = "", minutes: int = 10, mode: str = "live", user_token: str = "") -> str:
        """Run the first-post-coach skill: take someone from blank page to a published 4/4 post in ~10 minutes with
        real-time scoring, one-line edits and a ship-it gate. Pass draft to coach an existing draft (audit mode)."""
        p = load(user_token)
        return skills.work_order(
            title="First post coach", skill="first-post-coach", p=p,
            method=skills.skill_sections("first-post-coach", "Required Inputs", "Mode", "The 3 Phases", "Common Failure", "Coaching Rules", "Output Structure"),
            inputs={"mode": "audit" if draft.strip() else mode, "time box (minutes)": minutes, "draft": draft},
            task="Coach me through finishing, not perfecting. Use score_post after each draft cycle and give one-line edits. Ship at 4/4 or when the time box ends.",
            contract="The coaching output for the current phase exactly as the skill's Output Structure defines it.",
            checks=["Score each draft with score_post before coaching it.", "Never write the post for me without my story; ask the one question that unlocks it."])

    @tool()
    def write_carousel(topic: str, mode: str = "new", intent: str = "", cta_type: str = "", slides: int = 10,
                       brain_dump: str = "", cta_keyword: str = "", user_token: str = "",
                       voice_override: str = "", icp_override: str = "", brain_override: str = "") -> str:
        """Write LinkedIn carousel copy with the linkedin-carousel-builder skill. mode: new (cover formula + flow + CTA chosen
        independently) | intent (cover, flow and CTA serve one intent: Educating/Nurturing/Soft Selling/Hard Selling/Engagement).
        cta_type (new mode): educational-follow | lead-gen-comment | niche-follow | proof. Default 10 slides. Returns a work order."""
        p = load(user_token, brain_override, icp_override, voice_override)
        m = pick(mode, {"new": "new", "intent": "intent"}, "new")
        f = "new-carousel.md" if m == "new" else "intent-carousel.md"
        method = skills.prompt_file("linkedin-carousel-builder", f) + "\n\n" + skills.skill_sections("linkedin-carousel-builder", "Process", "Output Structure (text", "Quality Checklist")
        return skills.work_order(
            title=f"LinkedIn carousel · {m}", skill="linkedin-carousel-builder", p=p, method=method,
            inputs={"topic": topic, "mode": m, "number of slides": slides, "intent (intent mode)": intent, "CTA type (new mode)": cta_type or "Educational Follow",
                    "reference context / brain dump": brain_dump, "keyword for CTA": cta_keyword},
            task=f"Write a {slides}-slide carousel on the topic: cover, body slides, CTA slide. Preserve technical terms exactly.",
            contract="Slide-by-slide copy in the skill's strict slide format (headline, body line, one line of designer direction per slide), then a Canva AI handoff prompt.")

    @tool()
    def write_cheatsheet(topic: str, format: str = "listicles", sub_variant: str = "", brain_dump: str = "", user_token: str = "",
                         voice_override: str = "", icp_override: str = "", brain_override: str = "") -> str:
        """Write a saveable LinkedIn cheatsheet with the linkedin-cheatsheet-builder skill. format: listicles (6 points x 4 takeaways) |
        comparison (X vs Y / Bad vs Good / Think vs Reality) | dos-and-donts (Classic / Side-by-Side / Numbered Countdown).
        Leave format blank and the skill's decision tree picks. Returns a work order."""
        p = load(user_token, brain_override, icp_override, voice_override)
        m = pick(format, {"list": "listicles", "comp": "comparison", "do": "dos-and-donts"}, "listicles")
        f = {"listicles": "listicles.md", "comparison": "comparison.md", "dos-and-donts": "dos-and-donts.md"}[m]
        method = skills.prompt_file("linkedin-cheatsheet-builder", f) + "\n\n" + skills.skill_sections("linkedin-cheatsheet-builder", "Format Selection", "Process", "Output Structures", "Quality Checklist")
        return skills.work_order(
            title=f"Cheatsheet · {m}", skill="linkedin-cheatsheet-builder", p=p, method=method,
            inputs={"topic": topic, "format": m, "sub-variant": sub_variant or "(apply the decision tree)", "reference context": brain_dump},
            task="Build the cheatsheet. It must work as a standalone image with no post around it.",
            contract="The cheatsheet content in the skill's output structure, designer-ready, then the Canva AI handoff prompt.")

    @tool()
    def weekly_content_drop(idea: str = "", platform: str = "linkedin", user_token: str = "") -> str:
        """Run the weekly-content-engine skill: one short idea in, a long-form post + a 5-7 slide carousel + a save-worthy
        cheatsheet out, each with a Canva AI handoff prompt. Leave idea blank to have the engine pick the week's angle
        from your Brain and your post history."""
        p = load(user_token)
        hist = [e.get("topic", "") for e in events(p, "post", 60)]
        daily = library.daily_prompt(p, recent_topics=hist)
        method = skills.skill_sections("weekly-content-engine", "Why this exists", "Required inputs", "Modes", "The 3 outputs", "Process", "Output structure (`standard`") + \
            "\n\n" + skills.prompt_file("weekly-content-engine", "canva-carousel.md") + "\n\n" + skills.prompt_file("weekly-content-engine", "canva-cheatsheet.md")
        return skills.work_order(
            title="Weekly content drop", skill="weekly-content-engine", p=p, method=method,
            inputs={"idea": idea or f"(none given) suggested starting angle: {daily['today']['prompt']}", "platform": norm_platform(platform),
                    "do not repeat (last 60 days)": "; ".join(t for t in hist if t) or "nothing logged yet"},
            task="Produce the three outputs for the week: Monday long-form post, Wednesday carousel, Friday cheatsheet. Voice from my Voice Lock, customer from my Customer Lock.",
            contract="Three outputs in the skill's standard output structure, each ready to publish, each with its Canva AI prompt, each self-scored 4/4.")

    @tool()
    def amplify_post(post: str, platforms: str = "core", keyword: str = "", handle: str = "", user_token: str = "") -> str:
        """Run the multi-platform-amplifier skill: turn one LinkedIn post into platform-native X thread, Instagram caption and
        Reels script (platforms='core'), plus Threads ('full'), or a video-first storyboard ('video-first'). Returns a work order."""
        p = load(user_token)
        m = pick(platforms, {"core": "core", "full": "full", "video": "video-first"}, "core")
        return skills.work_order(
            title=f"Amplify one post · {m}", skill="multi-platform-amplifier", p=p,
            method=skills.skill_sections("multi-platform-amplifier", "Required Inputs", "Mode", "Platform Adaptation Rules", "Process", "Output Structure (`core`", "Self-Critique"),
            inputs={"mode": m, "source LinkedIn post": post, "DM keyword": keyword or "(detect from the post; ask if none)", "handle": handle or p.handle},
            task="Keep the core idea, voice and ICP anchor. Change hook, format, length and CTA to each platform's rules.",
            contract="Each platform version in the skill's Output Structure, labelled, with character counts.",
            checks=["Score the X hook and Instagram hook with score_post (Specificity and POV count).", "No hashtags on X. Instagram hashtag mix per the rules."])

    @tool()
    def write_tweet(post_or_topic: str, thread: bool = True, keyword: str = "", user_token: str = "") -> str:
        """Write an X (Twitter) thread, or a single tweet with thread=false, in YOUR voice from a LinkedIn post or a topic.
        Uses the multi-platform-amplifier X rules (hook under 240 chars, 1 idea per tweet, no hashtags). Returns a work order."""
        p = load(user_token)
        return skills.work_order(
            title="X thread" if thread else "Single tweet", skill="multi-platform-amplifier", p=p,
            method=skills.skill_sections("multi-platform-amplifier", "Platform Adaptation Rules", "Self-Critique"),
            inputs={"source": post_or_topic, "format": "5-7 tweet thread" if thread else "one tweet, max 280 chars", "DM keyword": keyword},
            task="Write only the X version, using the X / Twitter rules.", contract="Numbered tweets with char counts. No preamble.",
            checks=["Every tweet <= 280 chars.", "Run de_ai_ify on the thread."])

    @tool()
    def write_ig_caption(post_or_topic: str, keyword: str = "", user_token: str = "") -> str:
        """Write an Instagram caption (1,500-2,200 chars, hook in the first 125) in YOUR voice from a LinkedIn post or a topic,
        with the 9-12 hashtag mix. Uses the multi-platform-amplifier Instagram rules. Returns a work order."""
        p = load(user_token)
        return skills.work_order(
            title="Instagram caption", skill="multi-platform-amplifier", p=p,
            method=skills.skill_sections("multi-platform-amplifier", "Platform Adaptation Rules", "Self-Critique"),
            inputs={"source": post_or_topic, "DM keyword": keyword},
            task="Write only the Instagram caption using the Instagram Caption rules (hook before the 'more' cut, white space, DM CTA plus question CTA, hashtags after a separator).",
            contract="The caption, then the hashtag block, then the character count.",
            checks=[f"polish_post(platform='instagram', user_token=\"{tok_of(p) or '<token>'}\")", "de_ai_ify the caption."])

    @tool()
    def write_reel_script(post_or_topic: str, seconds: int = 75, keyword: str = "", user_token: str = "") -> str:
        """Write a 60-90 second Reels/TikTok script in YOUR voice: hook 0-3s, setup, 3-5 beats with visual cues, spoken DM-keyword CTA,
        end screen, captions on. Uses the multi-platform-amplifier Reels rules and (if you have one) the danny-video-voice style. Returns a work order."""
        p = load(user_token)
        return skills.work_order(
            title="Reels / TikTok script", skill="multi-platform-amplifier", p=p,
            method=skills.skill_sections("multi-platform-amplifier", "Platform Adaptation Rules", "Self-Critique"),
            inputs={"source": post_or_topic, "length (seconds)": seconds, "DM keyword": keyword},
            task="Write only the Reels/TikTok script using the Reels rules. Spoken lines must sound like me talking, not writing.",
            contract="A timed script table: time · spoken line · on-screen text · visual cue. Then captions text and the end screen.")

    @tool()
    def write_newsletter(topic: str, brain_dump: str = "", cta_keyword: str = "", length_words: int = 600, user_token: str = "",
                         voice_override: str = "", icp_override: str = "", brain_override: str = "") -> str:
        """Write a newsletter issue in YOUR voice with the newsletter-writer skill: subject line options, story-led opening,
        one clear idea, one ask. Returns a work order."""
        p = load(user_token, brain_override, icp_override, voice_override)
        return skills.work_order(
            title="Newsletter issue", skill="newsletter-writer", p=p,
            method=skills.skill_md("newsletter-writer")[:14000],
            inputs={"topic": topic, "reference / brain dump": brain_dump, "ask / keyword": cta_keyword, "target length (words)": length_words},
            task="Write the issue. Give 5 subject line options first, then the body.",
            contract="Subject options (with the one you recommend), preview text, body, sign-off, P.S.",
            checks=[f"polish_post(platform='newsletter', user_token=\"{tok_of(p) or '<token>'}\")", "de_ai_ify the body."])

    # ====================================================================
    # 4. RESEARCH
    # ====================================================================
    @tool()
    def analyze_competitor(competitor_urls: str = "", mode: str = "standard", user_token: str = "", profile_url: str = "", max_posts: int = 30) -> str:
        """Run the competitor-x-ray skill: given 3 competitor LinkedIn URLs (one per line) and YOUR ICP, scrape each profile and
        their recent posts with the Apify connector, compare them on 8 dimensions, find content gaps and give you a strategic content
        direction. mode: quick | standard | deep. Needs the Apify connector on. Returns a work order."""
        p = load(user_token)
        urls = [u.strip() for u in re.split(r"[\n,\s]+", competitor_urls + " " + profile_url) if u.strip().startswith("http")]
        if not urls:
            return "Give me the competitor LinkedIn profile URLs (up to 3, one per line)."
        m = pick(mode, {"quick": "quick", "deep": "deep", "standard": "standard"}, "standard")
        return skills.work_order(
            title=f"Competitor X-Ray · {m}", skill="competitor-x-ray", p=p,
            method=skills.skill_sections("competitor-x-ray", "Mode", "The 8 Dimensions", "Process", "Output Structure (`standard`"),
            inputs={"mode": m, "competitor URLs": " | ".join(urls[:3]), "posts to read per competitor": max_posts, "data source": "Use the Apify connector (search the store for a LinkedIn profile and post scraper). If Apify is unavailable, say so; never guess their posts."},
            task="Scrape, analyse each competitor on the 8 dimensions, synthesise, then write the Strategic Content Direction for ME using my Customer Lock and Voice Lock.",
            contract="The skill's standard output: per-competitor cards, side-by-side matrix, 3-5 content gaps vs my ICP, and the Strategic Content Direction.",
            checks=["Every claim about a competitor must cite a scraped post or profile field.", "No em dashes."])

    @tool()
    def find_prospects(post: str = "", limit: int = 10, mode: str = "standard", user_token: str = "", keywords: str = "", location: str = "") -> str:
        """Run the prospect-magnet skill: turn YOUR ICP into a LinkedIn search (derived for you here), find real matching people with
        the Apify connector, score each 0-10 against your ICP and write a personalised first message per person in YOUR voice,
        referencing the post you pass. Needs the Apify connector on. Returns a work order."""
        p = load(user_token)
        q = library.prospect_query(p, limit)
        if keywords.strip():
            q["keywords"], q["confidence"] = keywords.strip(), "operator-specified"
        if location.strip():
            q["geography"] = [location.strip()]
        return skills.work_order(
            title="Prospect Magnet", skill="prospect-magnet", p=p,
            method=skills.prompt_file("prospect-magnet", "prospect-search.md") + "\n\n" + skills.prompt_file("prospect-magnet", "personalized-dm.md") + "\n\n" +
                   skills.skill_sections("prospect-magnet", "Mode", "Process", "Output Structure (`standard`", "Self-Critique"),
            inputs={"mode": mode, "number of prospects": limit, "post to reference": post or "(none given: reference a theme from my Brain instead)",
                    "starting search query (derived from my ICP, confidence " + q["confidence"] + ")": json.dumps(q, indent=2)},
            task="Refine the starting query, run the search and enrichment through the Apify connector, score ICP fit 0-10, then draft one message per prospect.",
            contract="A ranked table (name, headline, fit score, why) then one first message per prospect, 4-line structure, in my voice. No placeholders.",
            checks=["Never invent a detail about a person; use only scraped fields.", "Run de_ai_ify on every message."])

    @tool()
    def get_daily_prompt(user_token: str = "", date: str = "") -> str:
        """Today's content angle, built from YOUR ICP (their words, objections, themes) and rotated by date, skipping what you
        already posted. Returns one angle plus two alternates. A starting point to judge, not an order."""
        p = load(user_token)
        today = dt.date.fromisoformat(date) if date else dt.date.today()
        d = library.daily_prompt(p, today, [e.get("topic", "") for e in events(p, "post", 60)])
        alt = "\n".join(f"  - {a['angle']}: {a['prompt']}" for a in d["alternates"])
        t = d["today"]
        return f"DAILY PROMPT · {d['date']}\n\nAngle: {t['angle']} (from your ICP {t['from']})\nPrompt: {t['prompt']}\nHow: {t['how']}\n\nAlternates:\n{alt}\n\n{d['note']}"

    @tool()
    def list_post_templates() -> str:
        """Every post, carousel and cheatsheet structure available, what each is for, and the tool call that uses it."""
        return "\n".join(f"{t['id']}: {t['name']}\n   {t['job']}\n   best for: {', '.join(t['best_for'])} · use: {t['tool']}" for t in library.POST_TEMPLATES)

    @tool()
    def get_my_post_history(user_token: str, days: int = 60, days_back: int = 0, limit: int = 30, platform_filter: str = "all") -> str:
        """Everything you logged as published in the last N days (topic, platform, hook, keyword), so nothing repeats."""
        p = load(user_token)
        need_real(p, "Post history")
        days = days_back or days
        ev = [e for e in events(p, "post", days) if platform_filter in ("all", "", e.get("platform"))][:limit]
        if not ev:
            return f"No posts logged in the last {days} days. Log them with log_published_post after publishing."
        return f"POST HISTORY · last {days} days · {len(ev)} posts\n" + "\n".join(
            f"  {dt.datetime.fromtimestamp(e['ts'], dt.timezone.utc).date()} · {e.get('platform', '')} · {e.get('topic', '')[:70]} · hook: {e.get('hook', '')[:60]} · kw: {e.get('keyword', '')}" for e in ev)

    # ====================================================================
    # 5. QUALITY (deterministic)
    # ====================================================================
    @tool()
    def score_post(text: str = "", mode: str = "score-with-fix", strict_asking: bool = False, user_token: str = "", post: str = "") -> str:
        """Score a post 0-4 on the Invisibility Diagnostic: Voice (uses YOUR words), POV, Specificity (real name + number in the first half),
        Asking (keyword DM invitation or direct closing question in the last 2 lines). Returns a one-line fix per missing dimension and the
        AI tells found. mode: score-only | score-with-fix. strict_asking=true accepts only a keyword invitation. Aim for 4/4."""
        text = text or post
        if not text.strip():
            return "Pass the post text (text= or post=)."
        p = load(user_token, need=False)
        return scoring.render(scoring.diagnose(text, p, strict_asking), mode)

    @tool()
    def polish_post(text: str = "", platform: str = "linkedin", user_token: str = "", post: str = "") -> str:
        """Platform polish: applies mechanical fixes (whitespace, em dashes, plain-word swaps) and reports length vs target, hook length vs the
        fold, paragraph density, hashtags, missing ask and remaining AI tells. platform: linkedin | instagram | x | threads | facebook | newsletter."""
        text = text or post
        if not text.strip():
            return "Pass the post text (text= or post=)."
        p = load(user_token, need=False)
        r = voice.polish(text, platform, banned_for(p))
        out = [f"POLISH · {r['platform']} · {r['chars']} chars (target {r['target']})", ""]
        out += ["MECHANICAL FIXES APPLIED: " + (", ".join(sorted(set(r["mechanical_changes"]))) or "none")]
        out += ["", "STRUCTURE ISSUES:"] + ([f"  - {x}" for x in r["structure_issues"]] or ["  none"])
        out += ["", "REMAINING AI TELLS (rewrite these yourself):"] + ([f"  - {x}" for x in r["remaining_tells"][:20]] or ["  none"])
        out += ["", "POLISHED TEXT:", "-----", r["polished"], "-----"]
        return "\n".join(out)

    @tool()
    def de_ai_ify(text: str = "", user_token: str = "", post: str = "") -> str:
        """Strip AI tells from a draft. Mechanically fixes em dashes, corporate filler words and filler transitions, then lists every
        remaining tell (contrast frames, banned openers/closers, question openers, staccato runs, YOUR banned words) with line numbers
        for you to rewrite in your own words. Never invents content."""
        text = text or post
        if not text.strip():
            return "Pass the text (text= or post=)."
        p = load(user_token, need=False)
        cleaned, changes = voice.mechanical_clean(text, banned_for(p))
        left = voice.find_tells(cleaned, banned_for(p))
        lines = [f"DE-AI-IFY · {len(changes)} mechanical fixes · {len(left)} tells left for you to rewrite", ""]
        if changes:
            lines += ["FIXED: " + ", ".join(sorted(set(changes))), ""]
        if left:
            lines += ["REWRITE THESE (in the operator's own words, using their word bank):"] + [f"  - {t.render()}" for t in left[:30]] + [""]
        lines += ["CLEANED TEXT:", "-----", cleaned, "-----"]
        if p and p.voice["word_bank"]:
            lines += ["", "Word bank to draw replacements from: " + ", ".join(p.voice["word_bank"][:15])]
        return "\n".join(lines)

    @tool()
    def review_homework(posts: str, top_n: int = 10, user_token: str = "") -> str:
        """Run the homework-reviewer skill on a batch of posts: score every post with the Invisibility Diagnostic, rank them, build the
        top-N shortlist with industry coverage, a chat shout-out list and a private coach-DM list. posts = JSON list of
        {"name","industry","post"} OR plain text with posts separated by a line containing only ---. Facilitator tool; works without a token."""
        rows: list[dict] = []
        txt = posts.strip()
        try:
            data = json.loads(txt)
            data = data if isinstance(data, list) else data.get("posts", [])
            rows = [{"name": d.get("name", f"Post {i + 1}"), "industry": d.get("industry", "unknown"), "post": d.get("post") or d.get("text", "")} for i, d in enumerate(data)]
        except Exception:
            for i, chunk in enumerate(re.split(r"\n\s*---+\s*\n", txt)):
                if chunk.strip():
                    m = re.match(r"^\s*(?:Name|By)\s*:\s*(.+)\n(?:Industry\s*:\s*(.+)\n)?(.*)$", chunk, re.S | re.I)
                    rows.append({"name": m.group(1).strip() if m else f"Post {i + 1}", "industry": (m.group(2) or "unknown").strip() if m else "unknown",
                                 "post": (m.group(3) if m else chunk).strip()})
        if not rows:
            return "No posts found. Pass a JSON list of {name, industry, post} or plain text separated by lines of ---."
        p = load(user_token, need=False)
        scored = []
        for r in rows:
            d = scoring.diagnose(r["post"], p)
            scored.append({**r, "score": d["score"], "tier": d["tier"], "fixes": d["fixes"], "chars": d["chars"],
                           "specific": d["dimensions"]["Specificity"]["point"] if d["dimensions"] else 0})
        scored.sort(key=lambda r: (-r["score"], -r["specific"], -r["chars"]))
        dist = {s: sum(1 for r in scored if r["score"] == s) for s in (4, 3, 2, 1, 0)}
        out = [f"HOMEWORK REVIEW · {len(scored)} posts · 4/4: {dist[4]} · 3/4: {dist[3]} · 2/4: {dist[2]} · 0-1/4: {dist[1] + dist[0]}", "",
               f"STAGE TOP {min(top_n, len(scored))} (read aloud in this order; diversity-aware):"]
        picked, seen = [], {}
        for r in scored:
            if len(picked) >= top_n:
                break
            if seen.get(r["industry"], 0) >= 2 and len(scored) > top_n * 1.5:
                continue
            seen[r["industry"]] = seen.get(r["industry"], 0) + 1
            picked.append(r)
        for i, r in enumerate(picked, 1):
            hook = next((l for l in r["post"].split("\n") if l.strip()), "")[:110]
            out.append(f"  {i}. {r['name']} · {r['industry']} · {r['score']}/4 · \"{hook}\"")
        out += ["", "INDUSTRY COVERAGE: " + ", ".join(f"{k} ({v})" for k, v in sorted(seen.items(), key=lambda x: -x[1]))]
        out += ["", "CHAT SHOUT-OUTS (next 15):"] + [f"  - {r['name']} · {r['score']}/4" for r in scored if r not in picked][:15]
        coach = [r for r in scored if r["score"] <= 1]
        out += ["", "COACH DM LIST (0-1/4, private check-in):"] + ([f"  - {r['name']}: {r['fixes'][0] if r['fixes'] else ''}" for r in coach] or ["  none"])
        out += ["", "Scores are heuristic. Read the top 10 yourself before going on stage."]
        return "\n".join(out)

    # ====================================================================
    # 6. DESIGN
    # ====================================================================
    @tool()
    def get_brand_colours(user_token: str = "") -> str:
        """Your brand colours: pulled from your Business Brain / brand settings when present, else the Purely Personal defaults.
        Pass these to generate_image, Canva and any HTML output so visuals match."""
        p = load(user_token, need=False)
        col = p.colours if p else dict(DEFAULT_BRAND)
        src = "your profile" if p and (p.brand or any(k in col for k in ("primary", "palette"))) else "Purely Personal defaults (none found in your Brain)"
        return json.dumps({"source": src, **col}, indent=2)

    @tool()
    def generate_image(prompt: str = "", subject: str = "", purpose: str = "post cover", aspect: str = "", size: str = "",
                       style: str = "auto", use_brand: bool = True, user_token: str = ""):
        """Make an image for a post, carousel cover or cheatsheet, in YOUR brand colours (from your Business Brain / brand settings;
        Purely Personal defaults if none). With OPENAI_API_KEY set on the server it renders the image (gpt-image-1) and returns it;
        otherwise it returns a ready-to-run image brief for Aura / Canva. size: 1024x1024 | 1536x1024 | 1024x1536 (or aspect 1:1 | 4:5 | 16:9 | 9:16).
        style: photo | illustration | infographic | minimal | auto. use_brand=false skips the palette."""
        subject = prompt or subject
        if not subject.strip():
            return "Say what the image is of (prompt=)."
        p = load(user_token, need=False)
        col = p.colours if p else dict(DEFAULT_BRAND)
        asp = {"1:1": "1024x1024", "4:5": "1024x1536", "9:16": "1024x1536", "16:9": "1536x1024"}
        size = size if size in ("1024x1024", "1536x1024", "1024x1536") else asp.get(aspect, "1024x1024")
        text = f"{purpose}: {subject}. Editorial composition, one strong focal point, generous negative space."
        if style and style != "auto":
            text += f" Style: {style}."
        if use_brand:
            text += f" Palette: accent {col.get('accent')}, ink {col.get('ink')}, background {col.get('paper')}."
        text += " No stock-photo handshakes, no glowing brains or robots, no watermarks, no tiny unreadable text; any words 8 or fewer."
        if os.environ.get("OPENAI_API_KEY"):
            from mcp.server.fastmcp.utilities.types import Image
            png = _render_image(text, size)
            return [Image(data=png, format="png"), f"Rendered {size}. Prompt used:\n{text}"]
        brief = {"prompt": text, "size": size, "colours": col if use_brand else {}}
        return ("IMAGE BRIEF (this server has no image key set, so paste this into Aura / Canva / your image tool):\n"
                + json.dumps(brief, indent=2))

    # ====================================================================
    # 7. TRACK (events)
    # ====================================================================
    def _log(user_token: str, kind: str, data: dict, label: str) -> str:
        p = load(user_token)
        need_real(p, "Logging")
        store.add_event(p.token, kind, {k: v for k, v in data.items() if v not in (None, "")})
        return f"Logged {label}."

    @tool(_WRITE)
    def log_published_post(user_token: str, topic: str, platform: str = "linkedin", hook: str = "", keyword: str = "", url: str = "", template: str = "") -> str:
        """Record that you published a post (topic, platform, hook line, the DM keyword used, URL, template). Feeds post history,
        the daily prompt (no repeats) and attribution."""
        return _log(user_token, "post", {"topic": topic, "platform": norm_platform(platform), "hook": hook, "keyword": keyword, "url": url, "template": template}, f"post '{topic[:50]}'")

    @tool(_WRITE)
    def track_post_published(user_token: str, topic: str, platform: str = "linkedin", hook: str = "", keyword: str = "", url: str = "", template: str = "") -> str:
        """Alias of log_published_post (kept for older workflows)."""
        return _log(user_token, "post", {"topic": topic, "platform": norm_platform(platform), "hook": hook, "keyword": keyword, "url": url, "template": template}, f"post '{topic[:50]}'")

    @tool(_WRITE)
    def log_dm_received(user_token: str, from_name: str, keyword: str = "", post_ref: str = "", note: str = "") -> str:
        """Record a DM from a prospect. Use the same keyword/post_ref as the post that triggered it so attribution works."""
        return _log(user_token, "dm", {"from_name": from_name, "keyword": keyword, "post_ref": post_ref or keyword, "note": note}, f"DM from {from_name}")

    @tool(_WRITE)
    def log_call_booked(user_token: str, name: str, source: str = "", post_ref: str = "", date: str = "", note: str = "") -> str:
        """Record a booked call (who, where it came from, the post_ref/keyword that started it, date)."""
        return _log(user_token, "call", {"name": name, "source": source, "post_ref": post_ref or source, "date": date, "note": note}, f"call with {name}")

    @tool(_WRITE)
    def log_revenue_event(user_token: str, amount: float, client: str = "", source: str = "", post_ref: str = "", currency: str = "USD", note: str = "") -> str:
        """Record a payment (amount, client, source, the post_ref/keyword it traces to, currency). Feeds the weekly revenue and attribution reports."""
        if amount <= 0:
            return "Amount must be greater than zero."
        return _log(user_token, "revenue", {"amount": float(amount), "client": client, "source": source, "post_ref": post_ref or source, "currency": currency.upper(), "note": note}, f"{amount:,.2f} {currency.upper()}")

    @tool()
    def get_weekly_revenue_report(user_token: str) -> str:
        """The CFO view from what you logged: revenue this week vs last, 30-day run-rate, the posts -> DMs -> calls -> sales funnel and revenue by source."""
        p = load(user_token)
        need_real(p, "The revenue report")
        return library.revenue_report(store.events(p.token, None, time.time() - 60 * 86400, 5000))

    @tool()
    def get_attribution_report(user_token: str, days: int = 90) -> str:
        """Which posts and keywords actually produced DMs, calls and revenue (matched on post_ref/keyword). Tells you what to write more of."""
        p = load(user_token)
        need_real(p, "The attribution report")
        return library.attribution_report(store.events(p.token, None, time.time() - days * 86400, 5000), days)

    # ====================================================================
    # Prompts (slash commands) and resources
    # ====================================================================
    @mcp.prompt(name="monday_content_drop", description="Day 3 task: write this week's three posts from your brain, score and polish them.")
    def monday_content_drop(user_token: str) -> str:
        return (f"Use the Purely Personal connector with user_token=\"{user_token}\". Call get_my_post_history(60) and get_daily_prompt, "
                "then write_post three times (opinion, story, proof) with different templates from list_post_templates. "
                "Score every post with score_post (fix anything under 4/4), then polish_post and de_ai_ify. "
                "Deliver three publish-ready posts and name the one to publish first.")

    @mcp.prompt(name="wednesday_market_scan", description="Day 3 task: analyze 3 competitors and say what to write about.")
    def wednesday_market_scan(user_token: str, competitor_urls: str) -> str:
        return (f"Use analyze_competitor with user_token=\"{user_token}\" on these URLs:\n{competitor_urls}\n"
                "Then get_daily_prompt and tell me the one angle that fills the biggest gap.")

    @mcp.prompt(name="friday_prospect_run", description="Day 3 task: find 15-20 prospects and write the first message for each.")
    def friday_prospect_run(user_token: str) -> str:
        return (f"Use find_prospects with user_token=\"{user_token}\" and limit=15. Return the ranked table and a first message per person, "
                "then log nothing until I tell you who replied.")

    @mcp.resource("pp://skills/{name}", description="Full text of a bundled program skill")
    def skill_resource(name: str) -> str:
        return skills.skill_md(name)

    return mcp


# ----------------------------------------------------------------------------
# Entrypoints
# ----------------------------------------------------------------------------
_server: FastMCP | None = None


def get_server() -> FastMCP:
    global _server
    if _server is None:
        _server = build_server()
    return _server


async def app(scope, receive, send):
    """ASGI app. Stateless: a fresh session manager per request, so it works on serverless
    hosts (no lifespan, no shared event loop, no sticky sessions)."""
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

    if scope["type"] == "lifespan":
        while True:
            msg = await receive()
            if msg["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif msg["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
    if scope["type"] != "http":
        return
    path = scope.get("path", "/").rstrip("/") or "/"

    async def reply(status: int, body: dict | str, ctype: str = "application/json"):
        raw = (json.dumps(body) if isinstance(body, dict) else body).encode()
        await send({"type": "http.response.start", "status": status, "headers": [(b"content-type", ctype.encode()), (b"cache-control", b"no-store")]})
        await send({"type": "http.response.body", "body": raw})

    if path in ("/", "/health", "/api/health"):
        srv = get_server()
        n = len(await srv.list_tools())
        return await reply(200, {"name": "purely-personal-mcp", "version": VERSION, "tools": n, "mcp_endpoint": "/mcp",
                                 "storage": "supabase" if os.environ.get("SUPABASE_URL") else "sqlite"})
    if path not in ("/mcp", "/api/mcp", "/api/index"):
        return await reply(404, {"error": "not found", "mcp_endpoint": "/mcp"})
    mgr = StreamableHTTPSessionManager(app=get_server()._mcp_server, json_response=True, stateless=True,
                                       security_settings=TransportSecuritySettings(enable_dns_rebinding_protection=False))
    scope = dict(scope, path="/mcp")
    async with mgr.run():
        await mgr.handle_request(scope, receive, send)


def main() -> None:
    args = sys.argv[1:]
    if "--http" in args:
        import uvicorn
        port = int(args[args.index("--http") + 1]) if len(args) > args.index("--http") + 1 else 8000
        uvicorn.run("pp_mcp.server:app", host="0.0.0.0", port=port, lifespan="on")
    else:
        get_server().run(transport="stdio")


if __name__ == "__main__":
    main()
