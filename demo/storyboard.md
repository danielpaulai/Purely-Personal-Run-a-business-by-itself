# Demo GIF Storyboard
### `/build-my-brain` — 60 seconds

**Target:** a LinkedIn/Twitter-ready MP4 or GIF that shows the plugin going from zero to a filled Brain + rendered one-pager in under a minute.

**Audience:** SaaS founders, solopreneurs scrolling their feed. First 3 seconds must stop the scroll.

**Format:** 1200×800 @ 30fps. MP4 (primary) + optimized GIF (fallback, <10 MB).

**Tool:** [vhs by charmbracelet](https://github.com/charmbracelet/vhs) — records a scripted terminal session deterministically. Works cross-platform.

---

## Shot List (60 seconds total)

| # | Duration | What you see | Why it works |
|---|----------|--------------|--------------|
| 1 | 0:00–0:05 | **Cold open** — empty Claude Code terminal. Cursor blinks. Title card overlay: *"Build a business that runs by itself. In 40 minutes."* | The promise in one line. Stops the scroll. |
| 2 | 0:05–0:12 | Type `/build-my-brain` slowly. Hit enter. | The single command. No setup noise. |
| 3 | 0:12–0:22 | Paste LinkedIn URL → watch Apify scrape → voice rules appear one line at a time | The "wait, that's my voice" moment |
| 4 | 0:22–0:34 | Paste website URL → brand colors extract → 3 competitor URLs → positioning matrix renders | The "competitor intel" moment |
| 5 | 0:34–0:42 | AI visibility audit runs → score `42/100` drops + 7 gap queries appear | The "oh god, AI can't find me" moment |
| 6 | 0:42–0:48 | Type `/render-brain`. Hit enter. | The handoff. |
| 7 | 0:48–0:58 | Browser opens. V3 full Brain render scrolls top to bottom. Lingers on `$75K` hero stat. | The payoff. Shareable. |
| 8 | 0:58–1:00 | End card overlay: *"purelypersonal.ai"* | One word. One URL. |

**Total runtime:** ~60 seconds
**Visible wow moments:** 4

---

## Visual Rules

- **Font in terminal:** JetBrains Mono 16pt
- **Terminal background:** `#0f0f10` (matches plugin's dark surface color)
- **Terminal foreground:** `#ffffff` for input, `#e90d41` for accents, `#22C55E` for success
- **Cursor color:** `#e90d41`
- **Browser chrome:** hidden (use `--app=URL` mode on Chromium to open chrome-less)
- **Title cards:** Rethink Sans 800 display font, cream background `#faf8f4`, 500 ms fade in/out
- **Pace:** never faster than the human eye can follow. 3 second floor on any single shot.
- **Audio:** none. GIFs don't have audio. MP4 version stays silent — let the visual work.

---

## Backup Shot List (for when the full flow breaks)

If a live demo fails during workshop, have a 30-second pre-recorded backup that shows ONLY the render moment:

| # | Duration | Shot |
|---|----------|------|
| 1 | 0:00–0:05 | Empty terminal |
| 2 | 0:05–0:08 | Type `/render-brain` |
| 3 | 0:08–0:25 | V3 Brain renders in browser, scroll through |
| 4 | 0:25–0:30 | End card |

---

## Recording Approach

### Option A — vhs (recommended)

vhs reads a `.tape` file and produces an MP4 + GIF. Deterministic. No manual re-takes.

```bash
brew install vhs
vhs demo/build-my-brain.tape
```

See `build-my-brain.tape` in this folder for the recording script.

### Option B — Terminalizer

Similar. Older, less maintained. Only use if vhs doesn't work on the target OS.

```bash
npm install -g terminalizer
terminalizer record build-my-brain
terminalizer render build-my-brain
```

### Option C — Manual (macOS screen recording)

1. Set up Zoom or QuickTime screen recording
2. Record at 1200×800 region (focus on the terminal + browser)
3. Follow the shot list above manually
4. Edit in Final Cut / iMovie / DaVinci Resolve Free
5. Export MP4 + convert to GIF with `ffmpeg`:

```bash
# MP4 → optimized GIF
ffmpeg -i demo.mp4 -vf "fps=15,scale=800:-1:flags=lanczos" -c:v pam \
  -f image2pipe - | convert -delay 6 - -loop 0 -layers optimize demo.gif
```

Target: <10 MB GIF for LinkedIn DM / README embed.

---

## Shot-by-Shot Prompts (for manual re-recording)

If vhs fails and you're re-recording manually, use these exact prompts to get identical output every time:

### Shot 3 — Voice extraction
```
/build-my-brain
```

When asked for LinkedIn URL, paste:
```
https://linkedin.com/in/danielpaulai
```

Expected output (log this beforehand so you know what will appear):
- `✓ Pulled profile + 30 posts`
- `✓ Voice rules extracted: 8 banned phrases, 5 hook patterns`
- `✓ Profile score: 73/100`

### Shot 4 — Website + competitors
Paste: `https://purelypersonal.ai`

Then when asked: `https://taplio.com`, `https://lempire.com`, `https://justinwelsh.me`

### Shot 5 — Audience pain
Keyword: `AI content tools solopreneur`

### Shot 6 — Render
```
/render-brain
```

---

## Distribution

Once the GIF is rendered, deploy to:

1. **README.md** — embed as the first image after the hero (replace the placeholder `./examples/screenshot.png` reference)
2. **LinkedIn post** — announcing the workshop
3. **Twitter thread** — tweet 1 of the workshop launch thread
4. **Newsletter** — hero of the "Purely Personal is live" email
5. **purelypersonal.ai** homepage — above the fold

---

## Version 2 Ideas (for later)

- 2-minute narrated walkthrough on YouTube (voice-over)
- Silent 15-second shorts for Instagram Reels / TikTok
- Screen-capture of Cowork batch-mode running 30 posts at once (for the Cohort sales page)
- "Zero to Brain in 10 minutes" live-stream recording (raw, unedited)

---

## Success Metrics for the GIF

- **LinkedIn:** ≥100 likes within 24h of posting = the visual landed
- **Click-through to purelypersonal.ai:** ≥5% of impressions
- **"What's that tool?" DMs:** ≥3 within 48h
- **Workshop signups from the GIF:** track with UTM `?ref=demo-gif`
