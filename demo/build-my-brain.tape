# vhs tape — /build-my-brain 60-second demo
# Run: vhs demo/build-my-brain.tape
# Outputs: demo/build-my-brain.mp4 + demo/build-my-brain.gif

Output demo/build-my-brain.mp4
Output demo/build-my-brain.gif

# Visual setup — matches the plugin's dark surface color
Set FontSize 16
Set FontFamily "JetBrains Mono"
Set Width 1200
Set Height 800
Set Padding 24
Set Theme { "name": "purely-personal", "background": "#0f0f10", "foreground": "#ffffff", "cursor": "#e90d41", "black": "#1a1a1d", "red": "#e90d41", "green": "#22C55E", "yellow": "#EAB308", "blue": "#3B82F6", "magenta": "#8B5CF6", "cyan": "#ffffff", "white": "#ffffff", "brightBlack": "#6b6b6b", "brightRed": "#e90d41", "brightGreen": "#22C55E", "brightYellow": "#EAB308", "brightBlue": "#3B82F6", "brightMagenta": "#8B5CF6", "brightCyan": "#ffffff", "brightWhite": "#ffffff" }
Set WindowBar Colorful
Set CursorBlink true

# ==========================================
# SHOT 1 — Cold open (0:00–0:05)
# ==========================================
Sleep 800ms
Type "# Build a business that runs by itself."
Sleep 1200ms
Enter
Type "# In 40 minutes."
Sleep 1500ms
Enter
Sleep 1200ms
Ctrl+L

# ==========================================
# SHOT 2 — The one command (0:05–0:12)
# ==========================================
Sleep 500ms
Type@100ms "/build-my-brain"
Sleep 800ms
Enter
Sleep 400ms

# ==========================================
# SHOT 3 — Voice extraction (0:12–0:22)
# ==========================================
# (script will prompt for LinkedIn URL)
Type@80ms "https://linkedin.com/in/danielpaulai"
Enter
Sleep 2000ms

# Expected output prints:
# ✓ Pulled profile + 30 posts
# ✓ Voice rules extracted
# ✓ Profile score: 73/100
Sleep 3000ms

# ==========================================
# SHOT 4 — Website + competitors (0:22–0:34)
# ==========================================
Type@80ms "https://purelypersonal.ai"
Enter
Sleep 1800ms

# Competitor URLs — one per line
Type@60ms "https://taplio.com"
Enter
Type@60ms "https://lempire.com"
Enter
Type@60ms "https://justinwelsh.me"
Enter
Sleep 4000ms

# ==========================================
# SHOT 5 — AI visibility audit (0:34–0:42)
# ==========================================
Type@80ms "AI content tools solopreneur"
Enter
Sleep 4000ms

# Expected:
# ✓ Reddit pain themes: 4
# ✓ AI visibility score: 42/100

# ==========================================
# SHOT 6 — Render (0:42–0:48)
# ==========================================
Sleep 1000ms
Ctrl+L
Type@100ms "/render-brain"
Sleep 600ms
Enter

# ==========================================
# SHOT 7 — The payoff (0:48–0:58)
# ==========================================
# The render command will open the HTML in the browser
# vhs can't capture the browser window, but the terminal will show:
# "✓ Rendered BUSINESS-BRAIN.md → examples/BUSINESS-BRAIN.rendered.html (opened in browser)"
Sleep 2000ms
Type "# Your Brain is live."
Sleep 1000ms
Enter
Type "# 5 engines ready to run."
Sleep 1500ms
Enter

# ==========================================
# SHOT 8 — End card (0:58–1:00)
# ==========================================
Type "# purelypersonal.ai"
Sleep 2500ms
Enter
Sleep 1500ms
