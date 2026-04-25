# Quickstart

The handoff message printed to the user after generation completes. Substitute the new workshop's values into this template.

---

## Print this exact format

```
✓ Generated · {WORKSHOP_NAME}
  Output: {OUTPUT_PATH}/{WORKSHOP_SLUG}/

  Contents:
   • landing-page/index.html
   • landing-page/install-guide/ (HTML + 4 video composition folders)
   • campaign/ (vsl-script, email-campaign, dm-outreach, video-scripts)
   • workshop/ (Workshop-Agenda.xlsx + 5 fillable worksheets)
   • integrations/ (ghl-build-spec, vercel-to-ghl)
   • notion-master-doc.md
   • README.md ← read this first

═══════════════════════════════════════════════════════════════════
THE 5 THINGS TO DO BEFORE YOU LAUNCH
═══════════════════════════════════════════════════════════════════

  1️⃣  CREATE A NEW GITHUB REPO
      Most install-guide references point to a {GITHUB_REPO_URL}
      placeholder. Create the repo on GitHub, push, then find-replace
      [NEW_REPO_URL] in install-guide/index.html with your new URL.
      
      cd {OUTPUT_PATH}/{WORKSHOP_SLUG}
      git init
      gh repo create {WORKSHOP_SLUG} --public --source=. --push

  2️⃣  REVIEW THE VSL DRAFT
      I wrote the VSL in your voice using your hook, but it's a draft.
      Read it once. Edit anything that doesn't sound like you.
      
      open {OUTPUT_PATH}/{WORKSHOP_SLUG}/campaign/vsl-script.md

  3️⃣  RENDER THE 4 PHASE WALKTHROUGH VIDEOS
      Each video is ~1:30–2:00 of animation + voiceover + subtitles.
      One render command per phase. Total ~30 min on an M-series Mac.
      
      bash {OUTPUT_PATH}/{WORKSHOP_SLUG}/videos/RENDER.sh
      
      (This calls hyperframes tts → transcribe → render for all 4
       phases sequentially. Outputs land in install-guide/videos/.)

  4️⃣  SET UP THE GHL FUNNEL
      Send integrations/ghl-build-spec.md to your GHL specialist.
      They build the funnel, give you the URL, you find-replace
      [CTA_PAYMENT_URL] in landing-page/index.html with that URL.

  5️⃣  DEPLOY THE LANDING PAGE
      Once the GitHub auto-deploy is connected (one-time Vercel setup),
      every git push redeploys automatically. For this NEW workshop:
      
      cd {OUTPUT_PATH}/{WORKSHOP_SLUG}/landing-page
      vercel link        ← creates a new Vercel project for this workshop
      vercel --prod      ← first deploy

      Or use a subdomain like {WORKSHOP_SLUG}.purelypersonal.ai for
      brand consistency across multiple workshops.

═══════════════════════════════════════════════════════════════════

📅  Timeline check
    Day 1: {DAY_1_DATE_HUMAN}
    Today: {TODAY}
    T-minus: {T_MINUS_DAYS} days

    The email campaign is timed for a 9-day pre-launch window.
    If you're tighter on time, compress emails A1–A6 into the
    days you have. The other emails (A7+ and B series) trigger
    on registration, not on calendar.

📂  Where things live
    Plugin (reused, no copy):    purely-personal/  (existing repo)
    New workshop assets:         {OUTPUT_PATH}/{WORKSHOP_SLUG}/
    Render workspace (videos):   ~/Build a Business.../hyperframes-workspace/

🔧  Common edits during launch
    • Adjust dates in emails:    sed -i '' 's/2026-06-14/.../g' campaign/email-campaign.md
    • Change Workshop number:    find-replace "Workshop {NN}" with "Workshop {NN+1}"
    • Add testimonials:          edit landing-page/index.html line 220 (testimonial section)

═══════════════════════════════════════════════════════════════════

Want me to:
  [O] Open the landing page now
  [V] Open the VSL draft
  [R] Read the README aloud
  [N] No, I'll take it from here

(Type O, V, R, or N)
```

---

## Branching

After the user picks O/V/R/N, the skill takes the appropriate action:

- **O** · `open <output>/landing-page/index.html`
- **V** · `open <output>/campaign/vsl-script.md` (or `cat` it in terminal)
- **R** · print the README contents in chat
- **N** · say "Good luck. See you when you're shipping the next one." and exit.

---

## Tone for the handoff

Keep it useful, terse, no fluff. The user just spent 5 minutes answering questions and watching a generation. Don't over-celebrate. Don't list 20 tips. Five concrete next steps. Done.
