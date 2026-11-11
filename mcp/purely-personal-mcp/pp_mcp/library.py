"""Deterministic helpers: templates catalogue, daily angle, prospect query, revenue reports."""
from __future__ import annotations

import datetime as dt
import hashlib
import re
from collections import defaultdict

from .profile import Profile

# ----------------------------------------------------------------------------
# Template catalogue (mirrors the three post modes, five intents, carousel and cheatsheet formats)
# ----------------------------------------------------------------------------
POST_TEMPLATES = [
    {"id": "intent-driven", "name": "Intent-Driven (default)", "job": "Most posts. Hook, body and ask all serve one intent.",
     "best_for": ["Educating", "Nurturing", "Soft Selling", "Hard Selling", "Engagement"], "tool": "write_post(mode='intent-driven')"},
    {"id": "framework-heavy", "name": "Framework-Heavy (save-bait list)", "job": "Numbered, saveable frameworks that get reposted.",
     "best_for": ["Educating", "Engagement", "Soft Selling", "Hard Selling"], "tool": "write_post(mode='framework-heavy')"},
    {"id": "story-flow", "name": "Story-Flow (vulnerable narrative)", "job": "One moment with a time, place and person. Needs a real story from the Brain.",
     "best_for": ["Nurturing", "Soft Selling", "Engagement", "Educating"], "tool": "write_post(mode='story-flow')"},
    {"id": "opinion", "name": "The Opinion", "job": "A position some people in your industry would argue with. 1300-1600 chars, ends on a disagreement-inviting question.",
     "best_for": ["Engagement"], "tool": "write_post(mode='intent-driven', intent='Engagement')"},
    {"id": "proof", "name": "The Proof", "job": "Something you know your customer does not, as numbered steps or before/after. Teaches something usable alone.",
     "best_for": ["Educating", "Soft Selling"], "tool": "write_post(mode='framework-heavy', intent='Educating')"},
    {"id": "carousel-new", "name": "Carousel: New", "job": "Cover formula + flow pattern + one of 4 CTA types, chosen independently.", "best_for": ["Educating"], "tool": "write_carousel(mode='new')"},
    {"id": "carousel-intent", "name": "Carousel: Intent", "job": "Cover, flow and CTA all serve one intent.", "best_for": ["Soft Selling", "Hard Selling", "Engagement"], "tool": "write_carousel(mode='intent')"},
    {"id": "cheatsheet-listicles", "name": "Cheatsheet: Listicle", "job": "6 points x 4 takeaways, saveable.", "best_for": ["Educating"], "tool": "write_cheatsheet(format='listicles')"},
    {"id": "cheatsheet-comparison", "name": "Cheatsheet: Comparison", "job": "X vs Y, Bad vs Good, or Think vs Reality.", "best_for": ["Educating", "Engagement"], "tool": "write_cheatsheet(format='comparison')"},
    {"id": "cheatsheet-dos", "name": "Cheatsheet: Dos and Don'ts", "job": "Classic, Side-by-Side or Numbered Countdown.", "best_for": ["Educating"], "tool": "write_cheatsheet(format='dos-and-donts')"},
]

_ANGLES = [
    ("The position", "State the belief your customer's industry gets wrong and defend it with one real example.",
     "A position some of your peers would argue with about: {t}"),
    ("The objection, answered", "Take the reason they say no and answer it honestly with something you have seen.",
     "Answer this objection head on: \"{t}\""),
    ("Their words, your take", "Open on a line your customer says out loud, then give the reply nobody gives.",
     "Open on: \"{t}\" and say what you would tell them over coffee."),
    ("The mistake I watched", "A specific mistake you saw (or made), what it cost, what you do now.",
     "The costliest mistake in: {t}"),
    ("The number nobody shares", "One real figure from your work and what it means for the reader.",
     "Share the number that explains: {t}"),
    ("What I would do first", "If your customer started today, the first three moves and why that order.",
     "If someone started today with: {t}, what would you do first?"),
    ("The myth", "Pick a common belief, show where it breaks, replace it with what works.",
     "Break the myth around: {t}"),
    ("Behind the work", "Show a messy middle: the draft, the call, the decision, the thing that nearly went wrong.",
     "Show the unglamorous middle of: {t}"),
    ("The question I keep getting", "A question from your DMs and the answer in full.",
     "Answer the question you keep getting about: {t}"),
    ("Before and after", "Same person or situation, two states, the one change between them.",
     "Before/after story on: {t}"),
]


def daily_prompt(p: Profile, today: dt.date | None = None, recent_topics: list[str] | None = None) -> dict:
    today = today or dt.date.today()
    c = p.customer
    seeds = [("objection", x) for x in c["objections"]] + [("their words", x) for x in c["their_words"]] + \
            [("theme", x) for x in c["themes"]]
    if not seeds:
        seeds = [("brain", (p.name or "your work") + " and who it is for")]
    recent = " ".join(recent_topics or []).lower()
    picks = []
    base = int(hashlib.sha256(f"{today.isoformat()}|{p.name}".encode()).hexdigest(), 16)
    for i in range(len(seeds) * len(_ANGLES)):
        kind, seed = seeds[(base + i) % len(seeds)]
        name, how, tmpl = _ANGLES[(base // 7 + i) % len(_ANGLES)]
        seed_clean = re.sub(r"\s+", " ", seed).strip(" .\"'")[:140]
        key = seed_clean.lower()[:40]
        if key and key in recent:
            continue
        picks.append({"angle": name, "from": kind, "seed": seed_clean, "prompt": tmpl.format(t=seed_clean), "how": how})
        if len(picks) == 3:
            break
    if not picks:  # everything recently covered
        kind, seed = seeds[base % len(seeds)]
        name, how, tmpl = _ANGLES[base % len(_ANGLES)]
        picks.append({"angle": name, "from": kind, "seed": seed[:140], "prompt": tmpl.format(t=seed[:140]), "how": how})
    return {"date": today.isoformat(), "today": picks[0], "alternates": picks[1:],
            "note": "A starting point, not an order. Judge it against the week so far and your recent posts, then choose."}


# ----------------------------------------------------------------------------
# Prospect search (prospect-magnet Phase 2, from the ICP)
# ----------------------------------------------------------------------------
_ROLES = ["founder", "owner", "ceo", "coach", "consultant", "agency owner", "freelancer", "director",
          "head of", "manager", "partner", "lawyer", "solicitor", "accountant", "therapist", "designer",
          "developer", "engineer", "marketer", "recruiter", "trainer", "author", "creator", "solopreneur"]
_REGIONS = ["United States", "United Kingdom", "UK", "Ireland", "Canada", "Australia", "Germany", "France",
            "Spain", "Netherlands", "Singapore", "India", "Indonesia", "Vietnam", "UAE", "London", "New York",
            "Europe", "North America", "Asia", "Worldwide"]


def prospect_query(p: Profile, limit: int = 10) -> dict:
    text = " ".join([p.customer["persona"], p.icp[:2500], p.brain[:2500]]).lower()
    roles = [r for r in _ROLES if re.search(r"\b" + re.escape(r), text)]
    regions = [r for r in _REGIONS if re.search(r"\b" + re.escape(r.lower()) + r"\b", text)]
    kw_terms = roles[:4] or ["founder"]
    topic_terms = [re.sub(r"[^a-z0-9 ]", "", x.lower()).strip() for x in p.customer["themes"][:3]]
    topic_terms = [t for t in topic_terms if t][:3]
    keywords = " OR ".join(f'"{t}"' for t in kw_terms)
    if topic_terms:
        keywords = f"({keywords}) AND (" + " OR ".join(f'"{t}"' for t in topic_terms) + ")"
    return {
        "keywords": keywords, "roles_detected": roles[:8], "geography": regions[:5] or ["(not found in ICP: ask or leave global)"],
        "limit": limit,
        "apify_actors": ["harvestapi/linkedin-profile-search", "supreme_coder/linkedin-profile-scraper"],
        "confidence": "high" if roles and regions else "medium" if roles else "low",
        "note": "Starting query derived from your ICP. Refine with the Prospect Search Query Builder method in the work order.",
    }


# ----------------------------------------------------------------------------
# Revenue + attribution reports (from logged events)
# ----------------------------------------------------------------------------

def _d(ts: float) -> dt.datetime:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc)


def revenue_report(events: list[dict], now: float | None = None) -> str:
    now = now or dt.datetime.now(dt.timezone.utc).timestamp()
    wk, day = 7 * 86400, 86400
    rev = [e for e in events if e["kind"] == "revenue"]
    def tot(lo, hi):
        return sum(float(e.get("amount", 0)) for e in rev if now - hi <= e["ts"] < now - lo)
    this, prev, m30 = tot(0, wk), tot(wk, 2 * wk), tot(0, 30 * day)
    chg = f"{(this - prev) / prev * 100:+.0f}% vs prior week" if prev else ("first revenue week" if this else "no revenue logged")
    src = defaultdict(float)
    for e in rev:
        if now - e["ts"] <= wk:
            src[e.get("source") or "unattributed"] += float(e.get("amount", 0))
    cnt = lambda k: sum(1 for e in events if e["kind"] == k and now - e["ts"] <= wk)
    posts, dms, calls = cnt("post"), cnt("dm"), cnt("call")
    sales = sum(1 for e in rev if now - e["ts"] <= wk)
    cur = next((e.get("currency") for e in rev if e.get("currency")), "USD")
    lines = [f"WEEKLY REVENUE REPORT · week ending {_d(now).date()}", "",
             f"Revenue this week: {this:,.2f} {cur}  ({chg})", f"Last 30 days: {m30:,.2f} {cur}  (run-rate if held: {m30 / 30 * 365:,.0f} {cur}/yr)", "",
             "Funnel this week:", f"  posts published {posts} -> DMs received {dms} -> calls booked {calls} -> sales {sales}"]
    if dms:
        lines.append(f"  DM per post: {dms / max(posts, 1):.1f} · call rate: {calls / dms * 100:.0f}% · close rate: {sales / max(calls, 1) * 100:.0f}%")
    if src:
        lines += ["", "Revenue by source:"] + [f"  {k}: {v:,.2f} {cur}" for k, v in sorted(src.items(), key=lambda x: -x[1])]
    if not events:
        lines += ["", "Nothing logged yet. Use log_published_post, log_dm_received, log_call_booked and log_revenue_event."]
    return "\n".join(lines)


def attribution_report(events: list[dict], days: int = 90, now: float | None = None) -> str:
    now = now or dt.datetime.now(dt.timezone.utc).timestamp()
    ev = [e for e in events if now - e["ts"] <= days * 86400]
    by = defaultdict(lambda: {"dms": 0, "calls": 0, "sales": 0, "revenue": 0.0, "topic": ""})
    for e in ev:
        ref = (e.get("post_ref") or e.get("keyword") or "").strip().lower()
        if e["kind"] == "post":
            ref = (e.get("keyword") or e.get("url") or e.get("topic") or "").strip().lower() or ref
            by[ref]["topic"] = e.get("topic", "")
        if not ref:
            continue
        if e["kind"] == "dm":
            by[ref]["dms"] += 1
        elif e["kind"] == "call":
            by[ref]["calls"] += 1
        elif e["kind"] == "revenue":
            by[ref]["sales"] += 1
            by[ref]["revenue"] += float(e.get("amount", 0))
    if not by:
        return f"ATTRIBUTION · last {days} days\n\nNo posts or events carry a post_ref/keyword yet. Log them with the same keyword you use in the post's DM invitation."
    rows = sorted(by.items(), key=lambda kv: (-kv[1]["revenue"], -kv[1]["dms"]))
    out = [f"ATTRIBUTION · last {days} days · keyword/post -> DMs -> calls -> sales -> revenue", ""]
    for ref, v in rows:
        out.append(f"  {ref[:48]:<48} DMs {v['dms']:>2} · calls {v['calls']:>2} · sales {v['sales']:>2} · {v['revenue']:,.2f}  {('· ' + v['topic'][:40]) if v['topic'] else ''}")
    out += ["", "Read this as: the top row is the topic and keyword your market actually buys from. Write more like it."]
    return "\n".join(out)
