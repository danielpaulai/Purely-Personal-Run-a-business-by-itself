# HTML Output Templates, AI Employee Bootcamp
# Purely Personal · by Daniel Paul
# World-class, self-contained, branded HTML for every executive output.

This file is the single output standard for the executive skills. Every brief, post, prospect pack, and revenue dashboard is delivered as ONE self-contained `.html` file: all CSS inline, fonts and GSAP from CDN, nothing to paste from another file. Open it in any browser, it just works.

Live reference of the finished standard: https://ai-employee-visuals.vercel.app

---

## STEP 0, BRAND COLOR DETECTION (run before building any file)

Before writing a single line of HTML, set the brand color.

1. Look in the user's brain folder / foundation docs (positioning, voice-dna, brand, design notes) for a hex code (`#RRGGBB`).
2. **If a hex is found:** use it as `--primary` throughout the file. Derive `--primary-light` by mixing it ~35% toward white. If you cannot derive cleanly, reuse the same hex for both.
3. **If no hex is found:** default to Purely Personal red `--primary:#E8294C; --primary-light:#F5607A`.
4. Never hardcode a different accent. The whole document adapts to the one brand color, so every client's output looks like THEIR company.

### Theme choice (STANDARD or LIGHT)

Two themes ship in the CORE SHELL, switched by the `data-theme` attribute on `<body>`:

- **STANDARD** (`<body data-theme="standard">`, the default): bold, branded. A solid brand-color header band, white cards with a colored left accent, a dark closing note. High-impact, presentation-ready.
- **LIGHT** (`<body data-theme="light">`): airy, editorial. White background, no color band (the brand color drops to a small kicker and accents), hairline borders, a soft brand-tinted note. Calmer, lighter, closer to a Notion or Linear document.

Default to STANDARD. Use LIGHT when the user asks for a light, minimal, or airy version, when the output is a long read, or when the brand notes lean understated. Both use the exact same BODY templates, only the `data-theme` value changes.

---

## GUARDRAILS (non-negotiable for every file)

- **Self-contained.** One `.html` file. All CSS in a single `<style>` block. No external CSS file, no "paste from design-system" step. Fonts and GSAP via the CDN links in the CORE SHELL only.
- **Font is Rethink Sans.** Never Poppins, never anything else.
- **No em dashes.** Anywhere. Use a comma, a period, or "to" for ranges. This applies to every word of generated copy.
- **Human voice.** No AI tells ("dive in", "unlock", "elevate", "in today's fast-paced", "it's not just X, it's Y"). Read `references/ai-pattern-blacklist.md` and `references/human-writing-standards.md` before writing copy into the file.
- **Never auto-send.** These files are drafts and recommendations. Any drafted message (DM, email reply, post) is shown for approval, never sent. Say so in the file where relevant.
- **Numbers are real or clearly sample.** Never invent revenue or metrics. If a connector returned nothing, show an empty state ("No data yet, connect Gmail") instead of fabricating.
- **Graceful empty states.** Any section with no data renders a calm placeholder, not a broken layout.

---

## THE CORE SHELL (use for ALL four department layouts)

Every executive file is the CORE SHELL below with one department BODY (Section further down) pasted into `<!-- BODY -->`, and `--primary` set per STEP 0. Do not change anything else.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[TITLE] · Purely Personal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --primary:#E8294C; --primary-light:#F5607A;            /* STEP 0 sets these */
    --black:#0A0A0A; --ink:#15151A; --white:#FFFFFF; --off-white:#F8F7F5;
    --gray:#E4E3E0; --gray-text:#5b5b62; --gray-light:#F2F1EE;
    --good:#16A34A; --warn:#D97706; --bad:#DC2626;
    --r-md:14px; --r-lg:22px; --pill:9999px;
    --sh:0 1px 2px rgba(0,0,0,.04),0 8px 28px rgba(0,0,0,.06);
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  html{scroll-behavior:smooth;}
  body{font-family:'Rethink Sans',sans-serif;background:var(--off-white);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased;}
  .doc{max-width:840px;margin:0 auto;padding:34px 22px 70px;}

  /* header band, takes the brand color */
  .ohead{border-radius:var(--r-md);padding:24px 26px;margin-bottom:22px;color:#fff;background:var(--primary);}
  .ohead .k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.82;font-weight:600;}
  .ohead h1{font-size:clamp(24px,4vw,32px);font-weight:800;letter-spacing:-.02em;margin:5px 0 3px;}
  .ohead .d{font-size:13px;opacity:.85;}

  /* building blocks */
  .sec{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--gray-text);font-weight:700;margin:24px 0 12px;}
  .card{background:#fff;border:1px solid var(--gray);border-radius:var(--r-md);box-shadow:var(--sh);padding:18px 20px;margin-bottom:14px;border-left:4px solid var(--primary);}
  .card h4{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--gray-text);margin-bottom:12px;}
  .lead{font-size:16px;}
  .row{display:flex;align-items:center;gap:10px;padding:8px 0;font-size:15px;border-bottom:1px solid var(--gray-light);}
  .row:last-child{border-bottom:none;}
  .row .when{color:var(--gray-text);font-size:13px;width:74px;flex-shrink:0;}
  .tagi{font-size:11px;font-weight:700;padding:2px 9px;border-radius:var(--pill);margin-left:auto;white-space:nowrap;}
  .t-red{background:#fdecec;color:var(--bad);} .t-amb{background:#fdf1de;color:var(--warn);}
  .t-grey{background:var(--gray-light);color:var(--gray-text);} .t-grn{background:#e7f6ee;color:var(--good);} .t-blue{background:#e6f0fc;color:#1E6FE0;}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
  .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  .stat{background:#fff;border:1px solid var(--gray);border-radius:var(--r-md);box-shadow:var(--sh);padding:18px 20px;}
  .stat .l{font-size:12px;color:var(--gray-text);} .stat .n{font-size:34px;font-weight:800;letter-spacing:-.02em;margin-top:4px;}
  .stat .delta{font-size:13px;font-weight:700;margin-top:2px;} .up{color:var(--good);} .down{color:var(--bad);}
  .bar{height:14px;border-radius:var(--pill);background:var(--gray-light);overflow:hidden;margin-top:10px;}
  .bar i{display:block;height:100%;width:0;border-radius:var(--pill);background:linear-gradient(90deg,var(--primary),var(--primary-light));}
  .note{background:var(--ink);color:#fff;border-radius:var(--r-md);padding:16px 20px;font-size:15px;margin-top:6px;}
  .note b{color:var(--primary-light);}
  .qbox{width:100%;border:1px dashed var(--gray);border-radius:10px;padding:12px;font-family:inherit;font-size:14px;color:var(--gray-text);background:#fff;margin-top:8px;}

  /* post mock (CMO) */
  .lipost{background:#fff;border:1px solid var(--gray);border-radius:var(--r-md);box-shadow:var(--sh);padding:20px;}
  .lihead{display:flex;align-items:center;gap:10px;margin-bottom:12px;}
  .av{width:46px;height:46px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;}
  .lihead .nm{font-weight:700;font-size:15px;} .lihead .mt{font-size:12px;color:var(--gray-text);}
  .lipost .post{font-size:15px;line-height:1.6;white-space:pre-line;}
  .chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;}
  .chip{font-size:12px;font-weight:600;background:var(--gray-light);color:var(--gray-text);padding:5px 11px;border-radius:var(--pill);}
  .score{display:inline-flex;align-items:center;gap:8px;background:#e7f6ee;color:var(--good);font-weight:700;font-size:13px;padding:6px 13px;border-radius:var(--pill);}

  /* prospect card (CRO) */
  .pcard{background:#fff;border:1px solid var(--gray);border-radius:var(--r-md);box-shadow:var(--sh);padding:16px 18px;}
  .pcard .ph{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
  .pcard .nm{font-weight:700;font-size:15px;} .pcard .rl{font-size:12px;color:var(--gray-text);}
  .pcard .dm{font-size:13px;background:var(--gray-light);border-radius:10px;padding:10px 12px;margin:10px 0;}

  footer{text-align:center;padding:30px 22px 10px;color:var(--gray-text);font-size:13px;}
  footer b{color:var(--ink);}

  /* LIGHT THEME, airy editorial variant. Activate by setting <body data-theme="light">. */
  body[data-theme=light]{background:#fff;}
  [data-theme=light] .ohead{background:#fff;color:var(--ink);border-bottom:1px solid var(--gray);border-radius:0;padding:4px 2px 18px;margin-bottom:24px;}
  [data-theme=light] .ohead .k{color:var(--primary);opacity:1;}
  [data-theme=light] .ohead h1{color:var(--ink);}
  [data-theme=light] .ohead .d{color:var(--gray-text);opacity:1;}
  [data-theme=light] .card,[data-theme=light] .stat,[data-theme=light] .pcard,[data-theme=light] .lipost{box-shadow:none;border:1px solid #ECEBE8;}
  [data-theme=light] .card{border-left:1px solid #ECEBE8;}
  [data-theme=light] .note{background:color-mix(in srgb,var(--primary) 7%,#fff);color:var(--ink);}
  [data-theme=light] .note b{color:var(--primary);}
  [data-theme=light] .qbox{background:#fff;}

  @media(max-width:640px){.grid2,.grid3{grid-template-columns:1fr;}}
</style>
</head>
<body data-theme="standard">
  <div class="doc">
    <!-- BODY -->
    <footer>The brain thinks. The team works. You approve. · <b>Built by Daniel Paul · Purely Personal</b></footer>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script>
    window.addEventListener('load',function(){
      if(!window.gsap)return; gsap.registerPlugin(ScrollTrigger);
      gsap.from('.ohead',{y:24,opacity:0,duration:.6,ease:'power3.out'});
      gsap.from('.card,.stat,.pcard,.lipost,.note,.bar',{y:18,opacity:0,duration:.5,stagger:.06,ease:'power2.out',scrollTrigger:{trigger:'.doc',start:'top 85%'}});
      gsap.utils.toArray('.count').forEach(function(el){
        var to=+el.dataset.to,o={v:0};
        gsap.to(o,{v:to,duration:1.4,ease:'power2.out',scrollTrigger:{trigger:el,start:'top 92%'},onUpdate:function(){el.textContent=Math.round(o.v).toLocaleString();}});
      });
      gsap.utils.toArray('.bar i').forEach(function(el){
        gsap.to(el,{width:el.dataset.pct||'75%',duration:1.4,ease:'power2.out',scrollTrigger:{trigger:el,start:'top 94%'}});
      });
    });
  </script>
</body>
</html>
```

Notes on the shell: animated metrics use `<span class="count" data-to="412">0</span>`. Progress bars use `<div class="bar"><i data-pct="75%"></i></div>`. Both animate on scroll automatically. Keep the `.count` class for the count-up animation.

---

## SECTION: DEPARTMENT BODIES

Paste ONE of these into `<!-- BODY -->`. Fill every `[PLACEHOLDER]`. Drop any block that has no data, or give it an empty state.

### BODY, COO morning brief
File name: `coo-brief-[YYYY-MM-DD].html`

```html
<div class="ohead"><div class="k">COO · Morning brief</div><h1>Good morning, [NAME]</h1><div class="d">[WEEKDAY, DD MONTH YYYY] · ran while you slept</div></div>

<div class="card"><h4>Today, in one line</h4><div class="lead">[THE SINGLE MOST IMPORTANT FRAMING FOR THE DAY]</div></div>

<div class="grid2">
  <div class="card"><h4>Calendar</h4>
    <div class="row"><span class="when">[TIME]</span> [EVENT]</div>
    <!-- repeat rows, or empty state: <div class="row">Nothing scheduled. Protect the day.</div> -->
  </div>
  <div class="card"><h4>Inbox · [N] need you</h4>
    <div class="row">[SENDER + ASK]<span class="tagi t-red">reply</span></div>
    <div class="row">[ITEM]<span class="tagi t-amb">decide</span></div>
    <div class="row">[ITEM]<span class="tagi t-grey">fyi</span></div>
  </div>
</div>

<div class="grid2">
  <div class="card"><h4>Overdue</h4><div class="row">[OVERDUE ITEM + HOW LATE]<span class="tagi t-red">act</span></div></div>
  <div class="stat"><div class="l">[KEY METRIC LABEL]</div><div class="n"><span class="count" data-to="[NUMBER]">0</span></div><div class="delta up">[CHANGE vs last week]</div></div>
</div>

<div class="note">One thing to move the needle today: <b>[THE SINGLE HIGHEST-LEVERAGE ACTION]</b>. [If a reply was drafted: "The draft is in your inbox, waiting for your yes." Never sent.]</div>
```

### BODY, CMO daily post
File name: `cmo-post-[YYYY-MM-DD].html`

```html
<div class="ohead"><div class="k">CMO · Daily post</div><h1>Today's post, in your voice</h1><div class="d">Pillar: [PILLAR] · scored and scrubbed</div></div>

<div class="lipost">
  <div class="lihead"><div class="av">[INITIALS]</div><div><div class="nm">[NAME] · 1st</div><div class="mt">[HEADLINE] · now</div></div></div>
  <div class="post">[FULL POST, in the participant's voice, line breaks preserved, no em dashes, ends on a question or specific ask]</div>
  <div class="chips"><span class="chip">[CHAR COUNT] chars</span><span class="chip">Hook: [TYPE]</span><span class="chip">No em dashes</span></div>
</div>

<div class="grid2">
  <div class="card"><h4>Hook options</h4>
    <div class="row">[CHOSEN HOOK]<span class="tagi t-grn">chosen</span></div>
    <div class="row">[ALT HOOK]</div>
    <div class="row">[ALT HOOK]</div>
  </div>
  <div class="card"><h4>Publish check</h4>
    <div class="row">Stops the scroll<span class="tagi t-grn">✓</span></div>
    <div class="row">Matches Voice DNA<span class="tagi t-grn">✓</span></div>
    <div class="row">Specific ask<span class="tagi t-grn">✓</span></div>
  </div>
</div>

<div class="sec">Pinned comment options</div>
<div class="card">
  <div class="row">[COMMENT OPTION 1]</div>
  <div class="row">[COMMENT OPTION 2]</div>
  <div class="row">[COMMENT OPTION 3]</div>
</div>

<div style="text-align:center;margin-top:8px"><span class="score">Invisibility Diagnostic: [SCORE] / 4</span></div>
```

### BODY, CRO weekly prospect pack
File name: `cro-prospects-[YYYY-MM-DD].html`

```html
<div class="ohead"><div class="k">CRO · Weekly prospect pack</div><h1>[N] matched. [H] hot.</h1><div class="d">Sourced from your ICP · DMs drafted, nothing sent</div></div>

<div class="grid3">
  <div class="stat"><div class="l">Prospects</div><div class="n"><span class="count" data-to="[N]">0</span></div></div>
  <div class="stat"><div class="l">Hot</div><div class="n" style="color:var(--good)"><span class="count" data-to="[H]">0</span></div></div>
  <div class="stat"><div class="l">DMs drafted</div><div class="n"><span class="count" data-to="[N]">0</span></div></div>
</div>

<div class="sec">The prospects</div>
<div class="grid2">
  <div class="pcard">
    <div class="ph"><div><div class="nm">[NAME]</div><div class="rl">[ROLE / COMPANY]</div></div><span class="tagi t-grn" style="margin-left:auto">hot</span></div>
    <div style="font-size:13px;color:var(--gray-text)">Signal: [WHY THEY MATCH / RECENT TRIGGER]</div>
    <div class="dm">[FIRST DM, personalised, one specific reference, soft open, no pitch]</div>
  </div>
  <!-- repeat one .pcard per prospect; tags: t-grn hot, t-amb warm, t-blue new -->
</div>

<div class="note">Open your highest-signal prospect first: <b>[NAME]</b>. [Reason]. Every DM here is a draft. You send, after you read it.</div>
```

### BODY, CFO weekly revenue
File name: `cfo-report-[YYYY-MM-DD].html`

```html
<div class="ohead"><div class="k">CFO · Weekly revenue</div><h1>This week: [$AMOUNT]</h1><div class="d">[WEEKDAY, DD MONTH YYYY] · read only, I never move money</div></div>

<div class="grid3">
  <div class="stat"><div class="l">This week</div><div class="n">$<span class="count" data-to="[NUM]">0</span></div><div class="delta up">[CHANGE vs last]</div></div>
  <div class="stat"><div class="l">This month</div><div class="n">$<span class="count" data-to="[NUM]">0</span></div><div class="delta up">[STATUS]</div></div>
  <div class="stat"><div class="l">Pipeline</div><div class="n">$<span class="count" data-to="[NUM]">0</span></div><div class="delta">[N] active deals</div></div>
</div>

<div class="card" style="padding:18px 20px"><div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:var(--gray-text)">Monthly goal · $[GOAL]</span><span style="font-weight:700">[PCT]%</span></div><div class="bar"><i data-pct="[PCT]%"></i></div></div>

<div class="card"><h4>Flags</h4>
  <div class="row">[INVOICE / ITEM + AGE]<span class="tagi t-amb">chase soon</span></div>
  <div class="row">[OVERDUE ITEM + AGE]<span class="tagi t-red">overdue</span></div>
  <!-- empty state: <div class="row">Nothing flagged. Clean week.</div> -->
</div>

<div class="note">One revenue action this week with the biggest impact?<textarea class="qbox" rows="2" placeholder="Type your answer, just for you..."></textarea></div>
```

---

## CEO BRAIN TEMPLATES (Quick Advice, Monday Session, Deep Dive)

The `ceo` skill uses the same CORE SHELL above. Build the file as CORE SHELL + the matching body below.

### BODY, CEO Quick Advice
File name: `ceo-brain-[topic].html`

```html
<div class="ohead"><div class="k">[PILLAR] · Quick advice</div><h1>[QUESTION OR TOPIC]</h1><div class="d">[DATE]</div></div>
<div class="sec">The answer</div>
<div class="card"><div class="lead">[DIRECT ANSWER, the participant's voice, 1 to 2 sentences]</div></div>
<div class="sec">The thinking</div>
<div class="card"><div>[WHY, 2 to 4 short paragraphs, 3 sentences max each]</div></div>
<div class="sec">This week</div>
<div class="note"><b>[ONE SPECIFIC ACTION]</b><br>1. [Step]<br>2. [Step]<br>3. [Step if needed]</div>
```

### BODY, CEO Monday Session
File name: `ceo-brain-monday-[YYYY-MM-DD].html`

```html
<div class="ohead"><div class="k">Weekly review</div><h1>Monday CEO session</h1><div class="d">[DATE]</div></div>
<div class="sec">Session summary</div>
<div class="card"><h4>01 · Last week, review</h4><div>[WINS AND GAPS]</div></div>
<div class="card"><h4>02 · The constraint</h4><div>[THE ONE THING SLOWING THINGS DOWN]</div></div>
<div class="card"><h4>03 · This week, the one thing</h4><div>[SPECIFIC OUTCOME + WHAT DONE LOOKS LIKE + BY WHEN]</div></div>
<div class="card"><h4>04 · Delegate</h4><div>[WHAT GETS HANDED OFF + TO WHOM + BY WHEN]</div></div>
<div class="card"><h4>05 · Protected, not touching</h4><div>[WHAT THEY ARE SAYING NO TO]</div></div>
<div class="note">The one thing: <b>[OUTCOME FROM 03]</b>. Done looks like: [definition]. By: [day].</div>
```

### BODY, CEO Deep Dive
File name: `ceo-brain-deepdive-[topic].html`

```html
<div class="ohead"><div class="k">[PILLAR] · Deep dive</div><h1>[TOPIC]</h1><div class="d">[DATE]</div></div>
<div class="sec">What it is</div><div class="card"><div class="lead">[ONE PLAIN SENTENCE]</div></div>
<div class="sec">Why most people get it wrong</div><div class="card"><div>[THE COMMON MISTAKE]</div></div>
<div class="sec">How to think about it</div><div class="card"><div>[THE PERSPECTIVE, conversational, direct]</div></div>
<div class="sec">The breakdown</div><div class="card"><h4>[CONCEPT NAME]</h4><div>[FULL EXPLANATION WITH A REAL EXAMPLE]</div></div>
<div class="sec">Applied to your situation</div><div class="card"><div>[SPECIFIC APPLICATION TO WHAT THEY SHARED]</div></div>
<div class="sec">This week</div><div class="note"><b>[SPECIFIC ACTION]</b><br>[Why this is the right first move]</div>
```

---

## FINAL CHECK before you hand over the file
- One `.html`, opens standalone, brand color applied from STEP 0.
- Rethink Sans, no Poppins. No em dashes anywhere.
- Every placeholder filled or its block removed. No `[BRACKETS]` left in the output.
- No invented numbers. Empty states where data is missing.
- Any drafted message is marked as a draft for approval, never sent.
- Tell the user the file name you saved and offer to open it.
