<!-- README — the hero asset. This is what sells the plugin on GitHub. -->

<div align="center">

# Purely Personal

### A Claude Code plugin that installs an AI C-Suite inside your business.

**One `BUSINESS-BRAIN.md` · Five AI executives · Zero SaaS subscriptions.**

[![Claude Code](https://img.shields.io/badge/Claude%20Code-1.0+-e90d41)](https://claude.com/claude-code)
[![License](https://img.shields.io/badge/license-MIT-1a1a1a)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/danielpaulai/Purely-Personal-Run-a-business-by-itself?style=social)](https://github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself)

[Install](#install-60-seconds) · [What you get](#what-you-get) · [Quick start](#quick-start) · [Workshop](#the-workshop)

![Business Brain screenshot](./examples/screenshot.png)

</div>

---

## The Promise

You know you should post consistently. Research your prospects. Write the newsletter. Pull the Stripe numbers. Plan next week.

But you're also closing deals, building product, and trying to sleep.

So the content team, the sales team, the ops team, the CFO — they all live as anxiety in your head instead of actual systems in your business.

**`purely-personal` installs those teams as skills inside Claude Code.** You fill in one document — your Business Brain. Every engine reads from it. And the output sounds like you, not ChatGPT.

- Content in your voice, not the voice of the 10,000 posts your model was trained on
- Outreach based on your actual ICP, not generic B2B playbooks
- Operations that follow your patterns, not Notion templates from 2022
- A morning brief that summarizes everything you didn't have time to look at

Zero SaaS. Zero subscriptions. Your Brain, your Claude, your voice.

---

## What You Get

### The Business Brain (`BUSINESS-BRAIN.md`)

One markdown file with nine sections. Every AI executive reads it before acting. It's your memory layer.

| # | Section | What's in it |
|---|---------|--------------|
| 1 | Operator | You. Name, tagline, headshot, LinkedIn. |
| 2 | Voice | Banned phrases, hook patterns, example posts — extracted from your real writing. |
| 3 | Business | Offer, positioning, pricing, 90-day goal, key metric. |
| 4 | Ideal Client | Named persona with pain, desire, objection. |
| 5 | Competitors | Top 3 with positioning gaps to own. |
| 6 | Brand Identity | Colors, fonts, visual voice — auto-extracted from your site. |
| 7 | AI Visibility | Score 0–100. Queries where you don't rank on ChatGPT / Perplexity / Claude. |
| 8 | Audience Pain | Real Reddit / forum verbatims from your niche. |
| 9 | Actions | Five slash commands. Always pinned. |

Build it in 40 minutes with `/build-my-brain`. Automated scrapes fill 80% of it from your LinkedIn, website, competitors, and Reddit.

### The Five Engines

Each engine is a slash command that reads the Brain and ships real work. No menus. No configuration. Just commands.

| Engine | Command | What it does |
|--------|---------|--------------|
| 🔵 Marketing | `/marketing-engine` | Drafts 3 LinkedIn posts, 1 X thread, 1 newsletter — in your voice |
| 🟢 Sales | `/sales-engine` | Researches 10 prospects + drafts outreach matched to your ICP |
| 🟣 Operations | `/operations-engine` | Triages inbox, writes SOPs from your patterns |
| 🟡 Cash | `/cash-engine` | Pulls Stripe, forecasts 90 days, flags anomalies |
| 🔴 Leadership | `/leadership-engine` | Summarizes the last 7 days across every engine |

### The Renderers

Two skills that turn your Brain and your outputs into screenshot-worthy visuals.

- **`business-brain-renderer`** — renders `BUSINESS-BRAIN.md` into a single-page HTML artifact with PDF export. Cinematic cover, dark proof band, hero stats, competitor matrix, pain quote, 5-engine actions panel. [Example →](./examples/BUSINESS-BRAIN.rendered.html)
- **`content-visual-builder`** — renders any content draft as a publish-ready card for LinkedIn, X, Instagram, or Newsletter. Same content, four platforms, four native looks.
- **`engine-output-builder`** — renders a single engine output (voice card, competitor matrix, ICP card) as a standalone shareable graphic.

---

## Install (60 seconds)

### Requirements
- [Claude Code](https://claude.com/claude-code) v1.0 or newer
- macOS, Linux, or Windows (WSL)
- A [Claude.ai](https://claude.ai) account

### Step 1 — Clone the plugin

```bash
git clone https://github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself.git
cd Purely-Personal-Run-a-business-by-itself
```

### Step 2 — Install the plugin

```bash
claude plugin install .
```

Or, if you prefer, symlink this directory into `~/.claude/plugins/purely-personal`.

### Step 3 — Verify

Open Claude Code in any project and run:

```
/build-my-brain --help
```

If you see the 4-act intake description, you're good.

### Optional — Install connectors

For the full `/build-my-brain` experience you need these [MCP connectors](https://modelcontextprotocol.io):

| Connector | Used by | Get it |
|-----------|---------|--------|
| Apify | LinkedIn + website + Reddit scrapes | [apify.com/mcp](https://apify.com/mcp) |
| Stripe | `/cash-engine` | [stripe.com/docs/mcp](https://stripe.com) |
| Gmail / Google | `/operations-engine` inbox triage | [Google MCP](https://github.com/modelcontextprotocol) |

The plugin works without them — you'll just be prompted to paste data manually instead.

---

## Quick Start

```bash
# 1. Build your Business Brain (40 min, mostly automated)
/build-my-brain

# 2. See it as a one-pager
/render-brain

# 3. Ship this week's content in your voice
/marketing-engine

# 4. Research 10 prospects + draft outreach
/sales-engine

# 5. Tomorrow morning — run this before coffee
/leadership-engine
```

---

## Example Output

Here's what `/render-brain` produces from a filled `BUSINESS-BRAIN.md`:

![Brain render example](./examples/BUSINESS-BRAIN.rendered.html)

[Open the full example HTML →](./examples/BUSINESS-BRAIN.rendered.html)

Screenshots of each section (for the impatient):

<details>
<summary>Cover Hero + Proof Stats Band</summary>

Cinematic hero with cream→white gradient, 128px headshot, 72px name, tilted `Ch. 01/09` stamp, 5 engine badges at 64px. Below: full-bleed dark band with three proof stats (`$0` / `2hr/wk` / `5 engines`).

</details>

<details>
<summary>Voice Card</summary>

Banned phrases as red pills. Hook patterns numbered. Example openings pulled from your real posts. A dark `// SIGNATURE` block with measured stats (avg sentence length, hook rate, short/long ratio).

</details>

<details>
<summary>Competitor 3×3 Matrix</summary>

Three competitors with full-bleed violet gradient "gap to own" blocks. Not subtle. This is the "I can see my positioning gaps" moment.

</details>

<details>
<summary>AI Visibility Scorecard</summary>

240px radial meter with your discoverability score. Breakdown row (Ranked / Missing / Tested). List of queries where ChatGPT/Perplexity/Claude don't find you.

</details>

<details>
<summary>Audience Pain (hero quote + 3 small)</summary>

One dark-charcoal hero card with the most emotionally resonant verbatim from your niche (28px italic display, giant red decorative quote mark). Three smaller theme cards below.

</details>

<details>
<summary>Actions Panel</summary>

Red-bordered card with five engine cards — one per AI executive. Each reads this Brain and acts in your voice. Click to copy the command.

</details>

---

## How the Skills Work Together

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  /build-my-brain  ──▶  BUSINESS-BRAIN.md  ◀── every engine │
│                                │                            │
│                                ▼                            │
│                     business-brain-renderer                 │
│                        (one-page HTML)                      │
│                                                             │
│  /marketing-engine  ──▶  content-visual-builder             │
│  /sales-engine      ──▶  outreach sequence + prospect cards │
│  /operations-engine ──▶  inbox triage + SOPs                │
│  /cash-engine       ──▶  forecast + anomaly flags           │
│  /leadership-engine ──▶  morning brief across all engines   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

One Brain. Every engine reads it. Outputs are tailored because the context is personal.

---

## The Workshop

This plugin is the deliverable from the **"Build a Business That Runs by Itself"** 2-day workshop. Attendees walk away with:

- Day 1 — A filled `BUSINESS-BRAIN.md` and one engine running live (Marketing)
- Day 2 — All five engines installed, one committed to running unattended for 7 days

Next workshop: TBA. [Join the waitlist →](https://purelypersonal.ai)

---

## Repo Structure

```
purely-personal/
├── .claude-plugin/
│   └── plugin.json                     # manifest
├── commands/                           # slash commands
│   ├── build-my-brain.md               # 4-act Brain intake
│   ├── marketing-engine.md
│   ├── sales-engine.md
│   ├── operations-engine.md
│   ├── cash-engine.md
│   └── leadership-engine.md
├── skills/                             # the brains behind the commands
│   ├── business-brain-renderer/        # renders BUSINESS-BRAIN.md as HTML
│   ├── content-visual-builder/         # 4-platform content cards
│   └── engine-output-builder/          # standalone engine visuals
├── scripts/
│   └── build_pdf.py                    # automated HTML→PDF export
├── examples/
│   ├── BUSINESS-BRAIN.sample.md        # reference Brain in the author's voice
│   └── BUSINESS-BRAIN.rendered.html    # example one-pager render
└── README.md                           # you are here
```

---

## Voice Rules (the plugin's north star)

Everything this plugin ships must:

- ✅ Sound like you, not like ChatGPT
- ✅ Use specifics (`$75K` not "significant revenue", `12 hours a month` not "many hours")
- ✅ Short sentences. One idea per line.
- ❌ Never use em-dashes, `unlock`, `delve`, `supercharge`, `game-changer`, `it's not just X, it's Y`, `elevate`, `seamless`, `leverage`

Every draft runs through a voice-rule check before it ships. If it smells like AI, it doesn't leave the terminal.

---

## FAQ

<details>
<summary><strong>Do I need to pay for Claude?</strong></summary>

You need a Claude.ai account (free or Pro). The plugin is free. The five engines run on your Claude quota.

</details>

<details>
<summary><strong>What about the Apify / Stripe / Gmail connectors?</strong></summary>

Optional. Without them, the plugin asks you to paste data manually instead of scraping. You can build a complete Business Brain with zero connectors — it just takes 20 minutes longer.

</details>

<details>
<summary><strong>Does this work without a GitHub account?</strong></summary>

Yes. The repo is just a distribution mechanism. Once you clone it locally, the plugin runs offline on your machine.

</details>

<details>
<summary><strong>Can I use this for multiple businesses?</strong></summary>

Yes. Create one `BUSINESS-BRAIN.md` per project. Each project gets its own voice, ICP, competitors, engines.

</details>

<details>
<summary><strong>How do I update the plugin?</strong></summary>

```bash
cd Purely-Personal-Run-a-business-by-itself
git pull
```

</details>

<details>
<summary><strong>Can I customize the voice rules?</strong></summary>

Yes. Edit the Voice section of your `BUSINESS-BRAIN.md`. Every skill reads from there.

</details>

---

## Roadmap

- [x] `business-brain-renderer` with V3 visual language
- [x] `content-visual-builder` with 4-platform card templates
- [x] `/build-my-brain` 4-act intake
- [x] `engine-output-builder` for standalone visuals
- [x] Five engine commands
- [x] Python PDF export script
- [ ] Demo GIF + video walkthrough
- [ ] Premium cohort-only skill pack (voice-extractor full, carousel-builder full, ICP-specific outreach)
- [ ] Cowork batch-run mode
- [ ] Morning brief email export
- [ ] Web UI for non-Claude-Code users

---

## Contributing

PRs welcome. The skill references are opinionated on purpose — if you'd like to push a change to the visual language or voice rules, please open an issue first so we can discuss.

- 📐 Visual changes → `skills/business-brain-renderer/references/design-system.md`
- ✍️ Voice changes → `skills/content-visual-builder/references/voice-application.md`
- 🧠 New engine → propose in an issue before PR

---

## Credits

Built by [Daniel Paul](https://purelypersonal.ai). Voice framework informed by the author's LinkedIn body of work and the `content-visual-builder` voice-application reference. Design language adapted from the author's `workshop-image-builder` skill.

---

## License

MIT. Use it, fork it, ship it. If this helps you build a business that actually runs without you, [let me know](https://linkedin.com/in/danielpaulai).

---

<div align="center">

### Ready?

```bash
claude plugin install ./purely-personal
```

**Your AI C-Suite is one command away.**

</div>
