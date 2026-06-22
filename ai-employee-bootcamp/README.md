# AI Employee Bootcamp

Build your own AI employees, then run them on a schedule. This is the Bootcamp #3 system packaged so steps 2 through 6 of the workflow install in one move.

## What is inside

The toolkit has two halves: a build surface where you make employees, and a run surface where they work for you on a schedule.

**Build surface — make your employees**
- `matchmaker` — audits any skill against your foundation documents and produces a gap report plus a Tailor Briefing. Run it first.
- `tailor` — takes the briefing and rewrites a skill so it fits your voice, ICP, and offer. Ships an installable zip. Runs in Claude Code.
- `content-strategy`, `linkedin-caption-writer`, `dm-sequence-writer`, `newsletter-writer`, `sales-call-prep` — the 5 starter skills. Install them generic, then tailor them to you. This is the "customize what we gave you" path.
- `build-your-own-employee` — the skill that builds skills, for jobs nobody gave you a starter for. Interviews you about one job, writes a new employee in your voice using the same 8-section anatomy and 9-scrub standards as the tailored skills, pressure-tests it, hands you the installable file. This is the "build from scratch" path.

The two build paths feed each other. Build from scratch today, then run the Matchmaker and Tailor on it later to deepen it as your foundation documents sharpen.

**Run surface — put them to work on a schedule**
- `cmo-daily-post` — standing job. Every morning, drafts today's post in your voice from your content pillars, scores it, stages it. Never auto-publishes.
- `cro-weekly-prospects` — standing job. Every Monday, builds 10 ICP-matched prospects and drafts a first-touch DM for each. Drafts only.
- `coo-morning-brief` — standing job. Every morning, briefs you on calendar, inbox, and what is overdue. Drafts safe replies only.
- `cfo-weekly-revenue` — standing job. Every Friday, reports revenue versus last week and flags unpaid invoices. Read only, never moves money.

**Employee templates** (`employee-templates/`)
Four ready-to-personalize starters: coach (discovery call prep), consultant (proposal writer), trainer (session designer), agency (weekly client update). Fill in the brackets and install.

**Connectors** (`.mcp.json`)
Wires Canva (design), Stripe (invoices and revenue), and Apify (prospecting). Add the rest of your Starter 7 (Google Calendar, Gmail, Drive, and your social publisher) through Settings, Connectors. Your Voice DNA and revenue engine come from your own marketing-brain MCP, connect that too.

## Install

Drop this folder into your marketplace, then install like any plugin.

```
claude plugin marketplace add ./ai-employee-bootcamp
claude plugin install ai-employee-bootcamp@ai-employee-bootcamp-marketplace
```

Or add the plugin entry from `.claude-plugin/marketplace.json` to your existing `purely-personal-marketplace` and install it alongside your other plugins.

## How to make an employee run regularly

A skill does not run until you schedule it. Set a Claude Code routine at claude.ai/code/routines, connect your business brain repo, pick a time, and write the job. It runs in the cloud day and night, even with your laptop closed. That is the works-while-you-sleep version.

See the scheduling guide and the live demo script in the `bootcamp-3` folder.

## The rule the employees follow
They draft and recommend. They never send email, post, send invoices, or move money on their own. A human approves every outward action. This is the design, not a limitation.
