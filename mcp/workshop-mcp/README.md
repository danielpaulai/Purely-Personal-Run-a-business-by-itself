# Purely Personal Workshop MCP

An MCP server that brings the Purely Personal workshop's voice tools and engines into Claude Desktop (and any other MCP client).

Use it for:
- **Spinning up new workshops** without being in Claude Code
- **Validating any copy** for em-dashes, banned phrases, AI tells before you publish
- **Drafting LinkedIn posts** in your voice from Claude Desktop chat
- **Prep meeting briefs + prospect research** without rebuilding the engines each time

---

## What it exposes

### 15 tools

| Tool | What it does |
|------|--------------|
| `scaffold_workshop` | Generate a complete new workshop launch folder (16+ files) from 14 inputs. Every Workshop 01 date moves with your new dates, weekdays included. |
| `validate_voice` | Check any text for em-dashes + banned phrases + AI tells. Uses your Brain's banned list plus `extra_banned_phrases` (any language). Returns PASS or line-numbered issues. |
| `score_post_against_brain` | AI-slop score 0-100 for any draft. Includes voice violation list + ship/revise/rewrite verdict. Takes `extra_banned_phrases` too. |
| `prep_post_in_voice` | Returns voice context + hook pattern + platform spec for Claude to draft a post. |
| `prep_meeting_brief` | Returns research framework + format template for a 3-min meeting brief on any LinkedIn URL. |
| `prep_prospect_research` | Returns BANT scoring + 3-step outreach template for any prospect. |
| `prep_marketing_drop` | Returns the weekly content drop framework (3 LinkedIn posts + thread + newsletter). |
| `prep_morning_brief` | Returns the daily 60-second brief format across all 5 engines. |
| `prep_pipeline_report` | Returns the Sunday pipeline report template (Marketing + Sales + Cash). |
| `list_workshops` | Scans a directory and lists every workshop folder found. |
| `prep_routine` | One entry point for the 6 weekly routines (Mon content drop to Sun pipeline). |
| `quick_install_check` | Punch list of what's missing in a student's install (Claude Code, plugin, Desktop config, Brain). |
| `health_check` | Install check + git status + key files on one screen. |
| `render_install_video` | Render an install-guide phase video via Hyperframes. |
| `deploy_landing_page` | Deploy `landing-page/` to Vercel production. Does nothing unless called with `confirm=True`. |

### 3 resources

| URI | Content |
|-----|---------|
| `brain://current` | Your `BUSINESS-BRAIN.md` (same lookup as the tools, see below) |

---

## Make it yours (every student)

Every voice tool reads **your** `BUSINESS-BRAIN.md`, never someone else's. It looks in this order:

1. `brain_path="..."` passed to the tool
2. The `PP_BRAIN_PATH` environment variable in your MCP config (set it once, recommended)
3. `BUSINESS-BRAIN.md` in the plugin root
4. `BUSINESS-BRAIN.md` in the current folder

If none exists the tool says so and stops. It never falls back to the sample Brain, because that is Daniel's voice and ICP.

Set it once at install time:

```bash
PP_BRAIN_PATH="$HOME/Desktop/my-business/BUSINESS-BRAIN.md" bash mcp/workshop-mcp/install.sh
```

or add it by hand to the config entry:

```json
"purely-personal-workshop": {
  "command": "python3",
  "args": ["/absolute/path/to/mcp/workshop-mcp/server.py"],
  "env": { "PP_BRAIN_PATH": "/absolute/path/to/BUSINESS-BRAIN.md" }
}
```

**Your banned words.** Put them under a `## Banned phrases` (or `## Banned words`) heading in your Brain as a bullet list. Any language works:

```markdown
## Banned phrases
- modernste Technik
- Potenziale heben
```

For a one-off check, pass them straight in: `validate_voice(text, extra_banned_phrases="modernste Technik, Potenziale heben")`.
| `voice://rules` | Full voice rules document (banned phrases, hook patterns, etc.) |
| `params://inventory` | Parameter inventory (which tokens live where in Workshop 01) |

---

## Three install paths

### Path 1 · One-line installer (easiest, recommended for team + students)

After cloning the repo, run:

```bash
bash mcp/workshop-mcp/install.sh
```

Or directly from the web (works for fresh installs with no repo clone):

```bash
curl -fsSL https://raw.githubusercontent.com/danielpaulai/Purely-Personal-Run-a-business-by-itself/main/mcp/workshop-mcp/install.sh | bash
```

When piped from the web, the installer clones the repo to `~/.purely-personal/` first (the server needs the workshop templates around it), and updates that copy on later runs. Needs `git`.

The installer:
1. Verifies Python 3.10+
2. Installs the `mcp` package (pinned to 1.x: the 2.x SDK removed the API this server uses)
3. Auto-detects your Claude Desktop config location (Mac/Linux/Windows)
4. Adds the `purely-personal-workshop` entry to `claude_desktop_config.json`
5. Verifies the server imports cleanly (stops with the error if it doesn't)
6. Tells you to restart Claude Desktop

Then fully quit Claude Desktop (Cmd+Q on Mac, right-click tray on Windows) and reopen.

### Path 2 · pip install (medium · for developers)

```bash
pip install purely-personal-workshop-mcp
```

(Not supported yet · the server reads workshop templates from the repo around it, so a pip-installed copy can't scaffold. Use Path 1 or Path 3.)

Then add to `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or equivalent:

```json
{
  "mcpServers": {
    "purely-personal-workshop": {
      "command": "purely-personal-workshop-mcp"
    }
  }
}
```

### Path 3 · Manual config (for full control)

1. Install the SDK (1.x only):
   ```bash
   pip3 install "mcp>=1.27.0,<2"
   ```

2. Find your Claude Desktop config:

   | OS | Path |
   |----|------|
   | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
   | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
   | Linux | `~/.config/Claude/claude_desktop_config.json` |

3. Add this entry inside `mcpServers` (preserve any existing entries):

   ```json
   {
     "mcpServers": {
       "purely-personal-workshop": {
         "command": "python3",
         "args": [
           "/absolute/path/to/purely-personal/mcp/workshop-mcp/server.py"
         ]
       }
     }
   }
   ```

4. Fully quit Claude Desktop and reopen.

---

## Verify it's wired

Open any new conversation in Claude Desktop and type:

> "Use score_post_against_brain on this draft: Last year I was doing 5 full-time jobs by myself. Marketing. Sales. Operations."

If Claude calls the tool and returns a score, you're done. If Claude says it doesn't have access, the server didn't load. See [Troubleshooting](#troubleshooting).

---

## Usage examples

### Score a LinkedIn draft before publishing

```
You:  Score this post: "Imagine a world where AI handles your sales for you.
      I'll dive into how 3 founders unlocked their pipeline last year — it's
      game-changing."

Claude: *calls score_post_against_brain*

        AI-SLOP SCORE: 86/100  ·  FULL REWRITE
        
        Voice analysis:
          Em-dashes: 1
          Banned phrases: 2 (unlock, as "unlocked"; dive into)
          AI-tell patterns: 3 (Imagine a world, A world where, game-changing)
          ...
        
        Want me to rewrite it in your voice?
```

### Spin up Workshop 02 from chat

```
You:  Use scaffold_workshop. Name it "Build Your Sales Machine in 30 Days".
      Day 1 = June 14, Day 2 = June 15. Price $79. 60 seats. Hook: stop
      chasing leads, run a system that researches and writes them. No cohort.

Claude: *calls scaffold_workshop with all 14 inputs*

        Generated · Build Your Sales Machine in 30 Days
        Output: ~/Desktop/build-your-sales-machine-in-30-days/
        Files written: 16
        ...
        
        Want me to read REWRITE-NEEDED.md and start drafting the VSL?
```

### Daily morning brief

```
You:  Run prep_morning_brief. Then check my Gmail inbox + Notion CRM and fill
      it in.

Claude: *calls prep_morning_brief, gets the format*
        *calls Apify or Gmail MCP to read inbox*
        *fills in the template, validates voice, returns final brief*
        
        # Morning Brief · Friday April 25
        
        ## What needs you today
        - Reply to Sarah at TechFlow ($12k Q2 deal stuck 4 days)
        - Send invoice to Klein PA group (overdue 6 days)
        ...
```

---

## How it differs from the slash command

The repo ships TWO ways to use the same engines:

| Method | Where it works | Best for |
|--------|---------------|----------|
| `/new-workshop`, `/marketing-engine`, etc. (slash commands) | Claude Code only | Conversational, code-adjacent work |
| MCP tools (this server) | Any MCP client (Desktop, Code, IDEs, agent SDK) | Quick atomic actions, mobile/non-CLI use, sharing with team |

Use the slash command when you live in Claude Code. Use the MCP when you want it from Claude Desktop chat, want to share with team members who don't run Code, or want to call tools from automation.

---

## Troubleshooting

### Claude Desktop says it doesn't have access to the tool

- Confirm `claude_desktop_config.json` is valid JSON. Paste into [jsonlint.com](https://jsonlint.com).
- Confirm the path in `args[0]` is absolute, not `~/`.
- Confirm `python3 server.py` runs without errors when run manually:
  ```bash
  cd mcp/workshop-mcp
  python3 server.py
  # Should hang waiting for stdio input. That means it started OK. Ctrl+C to exit.
  ```
- Fully quit Claude Desktop (Cmd+Q on Mac, right-click tray on Windows). Don't just close the window.
- Re-run the installer · `bash install.sh` · it's idempotent.

### Tool runs but writes nothing

- Check the source files exist at the paths assumed by the script (server uses paths relative to its own location).
- Check write permission to `output_dir` (default `~/Desktop`).

### `score_post_against_brain` says BUSINESS-BRAIN.md not found

Every tool uses the same lookup: `brain_path`, then `PP_BRAIN_PATH`, then the plugin root, then the current folder. The error message lists each path it tried. Set `PP_BRAIN_PATH` once (see [Make it yours](#make-it-yours-every-student)) and every tool picks it up.

### `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`

You have the 2.x MCP SDK. Run `pip3 install "mcp>=1.27.0,<2"` (or re-run `install.sh`), then restart Claude Desktop.

### Validate flags too aggressively

The universal list is `UNIVERSAL_BANNED_PHRASES` in `server.py`. Your own additions belong in your Brain's `## Banned phrases` section, so they survive updates to this repo.

---

## Files

```
mcp/workshop-mcp/
├── server.py            ← the MCP server (15 tools, 3 resources)
├── pyproject.toml       ← pip-installable package metadata
├── install.sh           ← one-line installer (Path 1)
├── requirements.txt     ← just `mcp>=1.27.0,<2`
└── README.md            ← you are here
```

---

## What's in the box, summarized

This MCP gives you · and your team · and your workshop attendees · the ability to:

1. **Validate any copy** before publishing (one tool, one call)
2. **Spin up new workshops** in 5 minutes from any chat client
3. **Run the 5 engines** without being in Claude Code
4. **Distribute to non-technical teammates** with one bash command
5. **Call the tools from automation** (cron, GitHub Actions, scripts) over stdio

It's the same engine as the slash commands, exposed through a different protocol. Pick whichever distribution channel fits your workflow.

---

## Credits

Built on top of the workshop-scaffolder skill (`purely-personal/skills/workshop-scaffolder/`) and the 5 engine slash commands (`purely-personal/commands/`). The skill defines the parameter inventory + voice rules + question flow that this MCP server enforces in code.
