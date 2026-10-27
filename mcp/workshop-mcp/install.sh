#!/usr/bin/env bash
#
# One-line installer for purely-personal-workshop-mcp.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/danielpaulai/Purely-Personal-Run-a-business-by-itself/main/mcp/workshop-mcp/install.sh | bash
#
# Or, after cloning the repo:
#   bash mcp/workshop-mcp/install.sh

set -euo pipefail

REPO_URL="https://github.com/danielpaulai/Purely-Personal-Run-a-business-by-itself.git"
INSTALL_HOME="${PP_INSTALL_DIR:-$HOME/.purely-personal/Purely-Personal-Run-a-business-by-itself}"
SERVER_NAME="purely-personal-workshop"
MCP_SPEC="mcp>=1.27.0,<2"

# When piped (curl | bash) there is no script file, so BASH_SOURCE is empty.
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi

GREEN=$'\033[32m'; YELLOW=$'\033[33m'; BLUE=$'\033[34m'; RED=$'\033[31m'; DIM=$'\033[2m'; RESET=$'\033[0m'
step() { echo "${BLUE}> $1${RESET}"; }
ok()   { echo "${GREEN}OK · $1${RESET}"; }
warn() { echo "${YELLOW}WARN · $1${RESET}"; }
fail() { echo "${RED}FAIL · $1${RESET}"; exit 1; }

echo
echo "==========================================================="
echo "  Purely Personal Workshop MCP · installer"
echo "==========================================================="
echo

# Verify Python
step "Checking Python 3.10+"
command -v python3 >/dev/null 2>&1 || fail "python3 not found. Install Python 3.10+ first."
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    fail "Python 3.10+ required. Found: $PY_VER"
fi
ok "Python $PY_VER"

# Locate server.py. The server reads templates from the repo around it, so a
# piped install clones (or updates) the full repo instead of fetching one file.
step "Locating server.py"
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/server.py" ]; then
    :
else
    command -v git >/dev/null 2>&1 || fail "git not found. Install git, or clone the repo and run: bash mcp/workshop-mcp/install.sh"
    if [ -d "$INSTALL_HOME/.git" ]; then
        git -C "$INSTALL_HOME" pull --ff-only --quiet || warn "Could not update $INSTALL_HOME, using existing copy"
    else
        mkdir -p "$(dirname "$INSTALL_HOME")"
        git clone --depth 1 --quiet "$REPO_URL" "$INSTALL_HOME" || fail "git clone failed: $REPO_URL"
    fi
    SCRIPT_DIR="$INSTALL_HOME/mcp/workshop-mcp"
fi
SERVER_PATH="${SCRIPT_DIR}/server.py"
[ -f "$SERVER_PATH" ] || fail "server.py not found at $SERVER_PATH"
ok "server.py at $SERVER_PATH"

# Install MCP SDK (1.x: the 2.x SDK removed the FastMCP API this server uses)
step "Installing $MCP_SPEC"
if python3 -c "import mcp.server.fastmcp" 2>/dev/null; then
    ok "mcp 1.x already installed"
else
    pip3 install --user "$MCP_SPEC" >/dev/null 2>&1 \
        || pip3 install "$MCP_SPEC" >/dev/null 2>&1 \
        || python3 -m pip install --user "$MCP_SPEC" >/dev/null 2>&1 \
        || fail "pip install \"$MCP_SPEC\" failed"
    python3 -c "import mcp.server.fastmcp" 2>/dev/null || fail "mcp installed but FastMCP import fails. Run: pip3 install \"$MCP_SPEC\""
    ok "mcp installed"
fi

# Detect Claude Desktop config
step "Detecting Claude Desktop config location"
case "$(uname -s)" in
    Darwin*) CONFIG_DIR="$HOME/Library/Application Support/Claude" ;;
    Linux*)  CONFIG_DIR="$HOME/.config/Claude" ;;
    MINGW*|MSYS*|CYGWIN*) CONFIG_DIR="$APPDATA/Claude" ;;
    *) CONFIG_DIR="$HOME/.config/Claude"; warn "Unknown OS, using $CONFIG_DIR" ;;
esac
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
ok "Config: $CONFIG_FILE"

mkdir -p "$CONFIG_DIR"
[ -f "$CONFIG_FILE" ] || { echo '{"mcpServers": {}}' > "$CONFIG_FILE"; ok "Created empty config"; }

# Wire server into config (Python does the JSON merge)
step "Adding $SERVER_NAME to claude_desktop_config.json"
python3 - "$CONFIG_FILE" "$SERVER_NAME" "$SERVER_PATH" "${PP_BRAIN_PATH:-}" <<'PYEOF'
import json, sys
from pathlib import Path

config_file = Path(sys.argv[1])
server_name = sys.argv[2]
server_path = sys.argv[3]
brain_path = sys.argv[4]

with open(config_file) as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\033[31mFAIL · {config_file} is invalid JSON: {e}\033[0m")
        sys.exit(1)

config.setdefault("mcpServers", {})
entry = {"command": sys.executable, "args": [server_path]}
old_env = config["mcpServers"].get(server_name, {}).get("env", {})
if brain_path:
    old_env["PP_BRAIN_PATH"] = str(Path(brain_path).expanduser().resolve())
if old_env:
    entry["env"] = old_env
config["mcpServers"][server_name] = entry

with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

print(f"\033[32mOK · wrote {server_name} entry\033[0m")
PYEOF

# Verify server imports
step "Verifying server.py imports cleanly"
if VERIFY_OUT=$(python3 - "$SCRIPT_DIR" <<'PYEOF' 2>&1
import asyncio, sys
sys.path.insert(0, sys.argv[1])
import server
tools = asyncio.run(server.mcp.list_tools())
print(f"OK · {len(tools)} tools loaded")
PYEOF
); then
    echo "${GREEN}${VERIFY_OUT##*$'\n'}${RESET}"
else
    echo "$VERIFY_OUT" | tail -5
    fail "server.py does not import. Fix the error above, then re-run this installer."
fi

echo
echo "==========================================================="
echo "${GREEN}Install complete${RESET}"
echo "==========================================================="
echo
echo "NEXT:"
echo "  1. ${YELLOW}Fully quit Claude Desktop${RESET} (Cmd+Q on Mac, right-click tray on Windows)"
echo "  2. ${YELLOW}Reopen Claude Desktop${RESET}"
echo "  3. Test by asking: ${BLUE}\"Use score_post_against_brain on this draft\"${RESET}"
echo
echo "Tools now available in Claude Desktop chat:"
echo "  ${DIM}scaffold_workshop, validate_voice, score_post_against_brain,${RESET}"
echo "  ${DIM}prep_post_in_voice, prep_meeting_brief, prep_prospect_research,${RESET}"
echo "  ${DIM}prep_marketing_drop, prep_morning_brief, prep_pipeline_report, prep_routine,${RESET}"
echo "  ${DIM}list_workshops, quick_install_check, health_check,${RESET}"
echo "  ${DIM}render_install_video, deploy_landing_page${RESET}"
echo
echo "Use your own Brain: add \"env\": {\"PP_BRAIN_PATH\": \"/path/to/BUSINESS-BRAIN.md\"}"
echo "to the $SERVER_NAME entry, or re-run with PP_BRAIN_PATH=/path/to/BUSINESS-BRAIN.md"
echo
echo "Config: $CONFIG_FILE"
echo "Server: $SERVER_PATH"
echo
