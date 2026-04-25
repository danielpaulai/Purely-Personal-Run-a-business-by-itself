# Purely Personal Workshop MCP

An MCP server that wraps the workshop-scaffolder skill so it works in Claude Desktop, the Claude Agent SDK, and any other MCP client.

Use this when you want to spin up a new workshop launch package from a chat with Claude (not just inside Claude Code).

---

## What it exposes

### Tools

| Tool | What it does |
|------|--------------|
| `scaffold_workshop` | Generates a complete new workshop folder. Takes 14 parameters (name, slug, dates, topics, price, hook, cohort, etc.). Mechanical token substitutions happen here; voice-aware rewriting is delegated to Claude via a `REWRITE-NEEDED.md` file dropped in the new folder. |
| `validate_voice` | Checks any text for em-dashes, banned phrases, and AI-tells. Returns PASS or a line-numbered list of issues. |
| `list_workshops` | Lists existing workshops in your output directory (default `~/Desktop`). |

### Resources

| URI | Content |
|-----|---------|
| `brain://current` | Current `BUSINESS-BRAIN.md` from this repo |
| `voice://rules` | Full voice-rules document |
| `params://inventory` | Parameter inventory (which tokens live in which files) |

---

## Install (Claude Desktop)

### 1. Install the MCP Python SDK

```bash
pip3 install mcp
```

### 2. Find your Claude Desktop config

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

### 3. Add this server entry

```json
{
  "mcpServers": {
    "purely-personal-workshop": {
      "command": "python3",
      "args": [
        "/Users/danielpaul/Build a Business That runs by itself using claude code/purely-personal/mcp/workshop-mcp/server.py"
      ]
    }
  }
}
```

If the file already has `mcpServers` entries (e.g. Apify), just add `purely-personal-workshop` as another key inside the existing block. Watch the comma after the previous server's closing brace.

### 4. Fully quit Claude Desktop and reopen

The new server loads on startup. Confirm it's wired by typing in any conversation:

> "Use scaffold_workshop to spin up a new workshop called 'Test'."

If Claude calls the tool, you're done. If Claude says it doesn't have access to that tool, the server didn't load. Check:

- The path in `args[0]` is absolute and correct
- `python3 server.py` runs without errors when run manually
- The `mcp` package is installed in the same Python that `python3` resolves to

---

## Usage example (Claude Desktop chat)

```
You:  Spin up Workshop 02. Name it "Build Your Sales Machine in 30 Days".
      Dates June 14 + 15, 2026. Price $79. Seat count 60. Day 1 = prospect
      research engine, Day 2 = follow-up engine. Hook: "Stop chasing leads.
      Start running a system that researches and writes them for you."

Claude:  *calls scaffold_workshop with the inputs*
         
         Generated the folder at ~/Desktop/build-your-sales-machine-in-30-days/.
         Token substitutions done across landing page, install guide, emails,
         DM outreach, GHL spec.
         
         REWRITE-NEEDED.md says I should rewrite 5 files in your voice next:
           1. campaign/vsl-script.md (highest priority)
           2. campaign/email-campaign.md (subjects + first 3 bodies)
           3. campaign/dm-outreach.md (8 segment openers)
           4. campaign/video-scripts.md (3 short scripts)
           5. videos/.../narration-script.txt (4 phase voiceovers)
         
         Want me to start with the VSL?

You:  Yes, do the VSL.

Claude:  *reads brain://current resource for voice context*
         *reads voice://rules resource*
         *drafts a new VSL using the new hook in your voice*
         *calls validate_voice on the result*
         
         VSL draft v1 (PASS · 0 issues). Saved to:
         ~/Desktop/build-your-sales-machine-in-30-days/campaign/vsl-script.md
         
         [...full draft inline...]
```

---

## Usage from Claude Code (also works)

The MCP also runs from Claude Code if you add the same config to `claude_desktop_config.json` (it's shared). Same flow, same tools.

---

## How it differs from the slash command

The repo ships TWO ways to do the same thing:

| Method | Where it works | Pros | Cons |
|--------|---------------|------|------|
| `/new-workshop` slash command | Claude Code only (inside the plugin) | Conversational. LLM does both questions and rewriting. | Tied to one client (Claude Code). |
| `scaffold_workshop` MCP tool | Any MCP client (Claude Desktop, Code, IDEs, third-party) | Atomic. Programmatic. Shareable with team. | LLM still has to rewrite voice copy in a follow-up turn. |

Use the slash command if you live in Claude Code. Use the MCP if you want it from Claude Desktop chat or want to share it with team members who don't run Code.

---

## Run the server manually (debugging)

```bash
cd /Users/danielpaul/Build\ a\ Business\ That\ runs\ by\ itself\ using\ claude\ code/purely-personal/mcp/workshop-mcp
python3 server.py
```

The server runs on stdio. It hangs waiting for MCP protocol messages. That's normal · means the server started OK. Press Ctrl+C to stop.

To test a tool from the command line, use any MCP client. The official `mcp` CLI:

```bash
mcp dev server.py
```

Opens an interactive inspector at http://localhost:6274.

---

## Troubleshooting

### Claude Desktop says it doesn't have access to `scaffold_workshop`

- Confirm `claude_desktop_config.json` is valid JSON (paste into jsonlint.com)
- Confirm the path in `args[0]` is absolute, not `~/`
- Confirm `python3 server.py` runs without errors when run manually
- Fully quit Claude Desktop (Cmd+Q on Mac, right-click tray on Windows). Don't just close the window.

### Tool runs but writes nothing

- Check the source files exist at the paths assumed in the script (the server uses paths relative to its own location)
- Check write permission to `output_dir` (default `~/Desktop`)

### Validate_voice flags too aggressively

- The banned phrase list is in `UNIVERSAL_BANNED_PHRASES` in `server.py`. Edit the list to your taste.

---

## Files

```
mcp/workshop-mcp/
├── server.py            ← the MCP server
├── requirements.txt     ← just `mcp>=1.27.0`
└── README.md            ← you are here
```

---

## Credits

Built on top of the workshop-scaffolder skill (`purely-personal/skills/workshop-scaffolder/`) which lives in the same repo. The skill defines the parameter inventory + voice rules + question flow that this MCP server enforces in code.
