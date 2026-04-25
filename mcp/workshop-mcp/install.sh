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

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="${SCRIPT_DIR}/server.py"
SERVER_NAME="purely-personal-workshop"

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

# Verify server.py
step "Locating server.py"
[ -f "$SERVER_PATH" ] || fail "server.py not found at $SERVER_PATH"
ok "server.py at $SERVER_PATH"

# Install MCP SDK
step "Installing mcp package"
if python3 -c "import mcp" 2>/dev/null; then
    ok "mcp already installed"
else
    pip3 install --user mcp >/dev/null 2>&1 || pip3 install mcp >/dev/null 2>&1 || fail "pip install mcp failed"
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
python3 - "$CONFIG_FILE" "$SERVER_NAME" "$SERVER_PATH" <<'PYEOF'
import json, sys
from pathlib import Path

config_file = Path(sys.argv[1])
server_name = sys.argv[2]
server_path = sys.argv[3]

with open(config_file) as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\033[31mFAIL · {config_file} is invalid JSON: {e}\033[0m")
        sys.exit(1)

config.setdefault("mcpServers", {})
config["mcpServers"][server_name] = {"command": "python3", "args": [server_path]}

with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

print(f"\033[32mOK · wrote {server_name} entry\033[0m")
PYEOF

# Verify server imports
step "Verifying server.py imports cleanly"
if python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); import server; n=len(list(server.mcp._tool_manager.list_tools())); print(f'OK · {n} tools loaded')" 2>&1 | tail -1; then
    :
else
    warn "Server import issues. Run python3 server.py manually to debug."
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
echo "  ${DIM}prep_marketing_drop, prep_morning_brief, prep_pipeline_report, list_workshops${RESET}"
echo
echo "Config: $CONFIG_FILE"
echo "Server: $SERVER_PATH"
echo
