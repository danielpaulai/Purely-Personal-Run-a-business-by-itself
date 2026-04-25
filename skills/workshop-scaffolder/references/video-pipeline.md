# Video Pipeline

How the 4 phase walkthrough videos get regenerated for a new workshop.

---

## What changes per workshop

The video composition structure stays the same: title card → step badge → terminal/UI mockup → step badge → mockup → … → end card. The animation styles, brand colors, music, GSAP timeline patterns are all reused.

What changes:

1. **Voiceover script** · workshop-specific (mentions new dates, hook, deliverables)
2. **Composition ID** · `pp-install-phase-N` → `<slug>-phase-N`
3. **End card text** · references new workshop's deliverables (e.g., "Phase 1 complete · 6 of 17 done · Next: Connect your apps" stays generic; the celebration end card on Phase 4 needs new workshop name)
4. **Subtitles array** · derived from new voiceover transcript

---

## The pipeline (per phase)

For each phase 1, 2, 3, 4:

### Step 1 · Generate voiceover script
The skill writes `videos/pp-install-phase-N/assets/narration-script.txt` based on:
- The phase's universal install steps (these are the SAME across workshops)
- Workshop-specific hook references (sparingly · the voiceover is mostly install-focused)
- The user's voice from BUSINESS-BRAIN.md

Length targets:
- Phase 1 (Install software): ~330 words / 1:45 at 0.88 speed
- Phase 2 (Connect apps): ~290 words / 1:30
- Phase 3 (Wire scraper): ~340 words / 2:00
- Phase 4 (Final prep): ~280 words / 1:30

### Step 2 · Generate audio
The user runs (or the skill runs at handoff):
```bash
cd <new-workshop>/videos/pp-install-phase-N
npx hyperframes tts assets/narration-script.txt --voice am_adam --speed 0.88 --output assets/narration.wav
```

If Phase N's script exceeds Kokoro's stable context (~70s of audio), split into chunks first. See chunking pattern in `pp-install-phase-2` from Workshop 01 · that one needed splitting because the original generation looped.

### Step 3 · Transcribe for word-level timestamps
```bash
npx hyperframes transcribe assets/narration.wav --model small.en --json
```
Outputs `transcript.json`.

### Step 4 · Generate subtitles JSON
Run the helper:
```bash
python3 ../gen-subtitles.py .
```
(Helper lives at `videos/gen-subtitles.py`, copied from the existing Workshop 01 hyperframes workspace. It groups word-level timestamps into 5–8 word phrases.)

Outputs `subtitles.json`.

### Step 5 · Apply transcription fixes
Common Kokoro mishearings to fix in subtitles.json:
- `Epiphy` → `Apify`
- `Claud.ai` → `claude.ai`
- `a PI` → `API`
- `CMDQ` → `Cmd+Q`
- `claude code` → `Claude Code`

Use the same fix dictionary as Workshop 01's gen-subtitles step.

### Step 6 · Embed subtitles in composition HTML
Read `videos/pp-install-phase-N/index.html`. Find the `const SUBTITLES = ...` line. Replace with the contents of `subtitles.json` formatted as a JS array.

### Step 7 · Lint
```bash
npx hyperframes lint
```
Should be 0 errors. Warnings are OK.

### Step 8 · Render
```bash
npx hyperframes render --quality draft --output renders/phase-N-draft.mp4
```
For final/production:
```bash
npx hyperframes render --quality standard --output renders/phase-N.mp4
```

Standard quality is visually lossless at 1080p. Use draft for iteration, standard for shipping.

### Step 9 · Copy MP4 to install guide
```bash
cp renders/phase-N.mp4 ../../landing-page/install-guide/videos/phase-N.mp4
```

### Step 10 · Generate poster frame
```bash
ffmpeg -i ../../landing-page/install-guide/videos/phase-N.mp4 -ss 00:00:01.5 -vframes 1 -q:v 3 ../../landing-page/install-guide/videos/phase-N-poster.jpg
```

Done.

---

## RENDER.sh helper script

The skill emits a `videos/RENDER.sh` script in the new workshop folder that does all 4 phases sequentially:

```bash
#!/usr/bin/env bash
set -euo pipefail

WORKSHOP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VIDEOS_DIR="$WORKSHOP_DIR/videos"
INSTALL_GUIDE_VIDEOS="$WORKSHOP_DIR/landing-page/install-guide/videos"

mkdir -p "$INSTALL_GUIDE_VIDEOS"

for phase in 1 2 3 4; do
  echo "=== Phase $phase ==="
  cd "$VIDEOS_DIR/pp-install-phase-$phase"

  # Skip TTS if narration.wav already exists
  if [ ! -f assets/narration.wav ]; then
    echo "Generating audio for Phase $phase..."
    npx hyperframes tts assets/narration-script.txt --voice am_adam --speed 0.88 --output assets/narration.wav
  fi

  # Transcribe
  if [ ! -f transcript.json ]; then
    echo "Transcribing Phase $phase..."
    npx hyperframes transcribe assets/narration.wav --model small.en --json
  fi

  # Generate subtitles
  if [ ! -f subtitles.json ]; then
    echo "Generating subtitles for Phase $phase..."
    python3 "$VIDEOS_DIR/gen-subtitles.py" .
  fi

  # NOTE: subtitle injection into composition HTML is a manual step.
  # Open videos/pp-install-phase-$phase/index.html, find `const SUBTITLES = `,
  # paste the contents of subtitles.json. (Future improvement: automate this.)

  # Render
  echo "Rendering Phase $phase..."
  npx hyperframes lint
  npx hyperframes render --quality draft --output renders/phase-$phase-draft.mp4

  # Copy + poster
  cp renders/phase-$phase-draft.mp4 "$INSTALL_GUIDE_VIDEOS/phase-$phase.mp4"
  ffmpeg -y -i "$INSTALL_GUIDE_VIDEOS/phase-$phase.mp4" -ss 00:00:01.5 -vframes 1 -q:v 3 "$INSTALL_GUIDE_VIDEOS/phase-$phase-poster.jpg"
done

echo ""
echo "✓ All 4 phases rendered."
echo "  Videos: $INSTALL_GUIDE_VIDEOS/phase-{1,2,3,4}.mp4"
echo "  Posters: $INSTALL_GUIDE_VIDEOS/phase-{1,2,3,4}-poster.jpg"
echo ""
echo "Next: deploy the landing page (cd $WORKSHOP_DIR/landing-page && vercel --prod)"
```

The skill outputs this script. The user runs it once after generation. It takes ~20 min for all 4 videos at draft quality.

---

## When the skill writes the composition HTML

For each phase, the skill reads the existing Workshop 01 composition (`hyperframes-workspace/video-projects/pp-install-phase-N/index.html`) and:

1. Replaces `data-composition-id="pp-install-phase-N"` → `data-composition-id="<slug>-phase-N"` in 2 places (root div + `window.__timelines` key)
2. Replaces references to "Workshop 01" / "Purely Personal" if any
3. Replaces the SUBTITLES array (placeholder for now · gets filled at Step 6 above)
4. Updates the audio src path if needed (should still be `assets/narration.wav`)
5. Writes to `videos/pp-install-phase-N/index.html`

The composition's GSAP timeline structure stays identical. Only the IDs, the workshop-specific labels, and the subtitles change.

---

## Verification

After RENDER.sh finishes:
- `landing-page/install-guide/videos/phase-1.mp4` through `phase-4.mp4` exist
- 4 corresponding `*-poster.jpg` files exist
- Open install-guide/index.html in browser · all 4 inline videos play
- Voiceover audio matches the new workshop's hook + dates + topics
- Subtitles match audio
- End card on Phase 4 says "<NEW WORKSHOP NAME> · 17 of 17 · 100%"

If any of these fail, inspect the failing phase, fix the script or composition, re-run RENDER.sh · it's idempotent (skips steps that already produced output, except for the final render which always re-runs).
