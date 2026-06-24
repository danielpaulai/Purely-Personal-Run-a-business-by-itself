# HTML Output Templates, AI CEO Brain
# Purely Personal · by Daniel Paul
# Complete HTML shells for Quick Advice, Monday Session, Deep Dive

---

## WHEN TO USE EACH TEMPLATE

| Mode | Template | File name |
|------|----------|-----------|
| Quick Advice (Mode 1) | Template A | `ceo-brain-[topic].html` |
| Monday Session (Mode 2) | Template B | `ceo-brain-monday-[YYYY-MM-DD].html` |
| Deep Dive (Mode 3) | Template C | `ceo-brain-deepdive-[topic].html` |

---

## TEMPLATE A, QUICK ADVICE

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[TOPIC] · AI CEO Brain · Purely Personal</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Rethink+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* PASTE FULL CSS FROM design-system.md HERE */
/* Include: reset, body, sec-label, card, card--accent, card--dark, card--action */
/* card__label, card__title, card__body, pillar-badge, action-list, action-item */
/* action-num, action-text, footer, animations */
</style>
</head>
<body>

<!-- COVER -->
<div style="text-align:center;padding:48px 0 40px;border-bottom:1px solid var(--border);margin-bottom:40px">
  <span class="pillar-badge">[PILLAR], [MODE]</span>
  <h1 style="font-family:var(--font-display);font-size:clamp(28px,4vw,44px);font-weight:900;letter-spacing:-.02em;line-height:1.1;margin-bottom:12px">[QUESTION OR TOPIC]</h1>
  <p style="font-family:var(--font-mono);font-size:12px;color:var(--text-3)">[DATE]</p>
</div>

<!-- DIRECT ANSWER -->
<div class="sec-label">Danny's Take</div>
<div class="card card--accent fade-up fd-1">
  <div class="card__label">The Answer</div>
  <div class="card__body">[DIRECT ANSWER, Danny's voice, 1–2 sentences]</div>
</div>

<!-- THE THINKING -->
<div class="sec-label" style="margin-top:28px">The Thinking</div>
<div class="card card--dark fade-up fd-2">
  <div class="card__body">[WHY, Danny's voice, 2–4 short paragraphs, no more than 3 sentences each]</div>
</div>

<!-- ACTION BLOCK -->
<div class="sec-label" style="margin-top:28px">This Week</div>
<div class="card--action fade-up fd-3">
  <div class="card__label" style="color:var(--primary)">Your Next Step</div>
  <div class="card__title">[ONE SPECIFIC ACTION]</div>
  <ol class="action-list" style="margin-top:14px">
    <li class="action-item">
      <span class="action-num">1</span>
      <span class="action-text">[Step 1]</span>
    </li>
    <li class="action-item">
      <span class="action-num">2</span>
      <span class="action-text">[Step 2]</span>
    </li>
    <li class="action-item">
      <span class="action-num">3</span>
      <span class="action-text">[Step 3 if needed]</span>
    </li>
  </ol>
</div>

<!-- FOOTER -->
<footer>
  <div>
    <span class="footer__brand">Purely Personal</span>
    <span class="footer__by">by Daniel Paul</span>
  </div>
  <span class="footer__meta">AI CEO Brain · [DATE]</span>
</footer>

<script>
document.querySelectorAll('.fade-up').forEach((el,i) => {
  el.style.animationDelay = (i * 0.08) + 's';
});
</script>
</body>
</html>
```

---

## TEMPLATE B, MONDAY SESSION SUMMARY

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Monday CEO Session [DATE] · AI CEO Brain · Purely Personal</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Rethink+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* PASTE FULL CSS FROM design-system.md HERE */
/* Also include .step-card, .step-badge, .step-content, .step-label, .step-value */
</style>
</head>
<body>

<!-- COVER -->
<div style="text-align:center;padding:48px 0 40px;border-bottom:1px solid var(--border);margin-bottom:40px">
  <span class="pillar-badge">WEEKLY REVIEW</span>
  <h1 style="font-family:var(--font-display);font-size:clamp(28px,4vw,44px);font-weight:900;letter-spacing:-.02em;line-height:1.1;margin-bottom:12px">Monday CEO Session</h1>
  <p style="font-family:var(--font-mono);font-size:12px;color:var(--text-3)">[DATE]</p>
</div>

<!-- 5 STEPS -->
<div class="sec-label">Session Summary</div>

<!-- STEP 1 -->
<div class="step-card fade-up fd-1">
  <div class="step-badge">01</div>
  <div class="step-content">
    <div class="step-label">Last Week, Review</div>
    <div class="step-value">[SUMMARY OF WHAT HAPPENED, wins and gaps]</div>
  </div>
</div>

<!-- STEP 2 -->
<div class="step-card fade-up fd-2">
  <div class="step-badge">02</div>
  <div class="step-content">
    <div class="step-label">The Constraint</div>
    <div class="step-value">[THE ONE THING SLOWING THEM DOWN]</div>
  </div>
</div>

<!-- STEP 3 -->
<div class="step-card fade-up fd-3">
  <div class="step-badge">03</div>
  <div class="step-content">
    <div class="step-label">This Week, The One Thing</div>
    <div class="step-value">[SPECIFIC OUTCOME, what done looks like + by when]</div>
  </div>
</div>

<!-- STEP 4 -->
<div class="step-card fade-up fd-4">
  <div class="step-badge">04</div>
  <div class="step-content">
    <div class="step-label">Delegate</div>
    <div class="step-value">[WHAT GETS HANDED OFF + WHO GETS IT + BY WHEN]</div>
  </div>
</div>

<!-- STEP 5 -->
<div class="step-card fade-up fd-5">
  <div class="step-badge">05</div>
  <div class="step-content">
    <div class="step-label">Protected, Not Touching</div>
    <div class="step-value">[WHAT THEY'RE SAYING NO TO THIS WEEK]</div>
  </div>
</div>

<!-- COMMITMENT BLOCK -->
<div class="sec-label" style="margin-top:32px">Your Commitment</div>
<div class="card--action" style="margin-top:0">
  <div class="card__label" style="color:var(--primary)">The One Thing</div>
  <div class="card__title">[SPECIFIC OUTCOME FROM STEP 3]</div>
  <div class="card__body" style="margin-top:10px">Done looks like: [what done means]<br>By: [specific day]</div>
</div>

<!-- FOOTER -->
<footer>
  <div>
    <span class="footer__brand">Purely Personal</span>
    <span class="footer__by">by Daniel Paul</span>
  </div>
  <span class="footer__meta">AI CEO Brain · Monday Session · [DATE]</span>
</footer>

<script>
document.querySelectorAll('.fade-up').forEach((el,i) => {
  el.style.animationDelay = (i * 0.08) + 's';
});
</script>
</body>
</html>
```

---

## TEMPLATE C, DEEP DIVE

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[TOPIC] Deep Dive · AI CEO Brain · Purely Personal</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Rethink+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* PASTE FULL CSS FROM design-system.md HERE */
</style>
</head>
<body>

<!-- COVER -->
<div style="text-align:center;padding:48px 0 40px;border-bottom:1px solid var(--border);margin-bottom:40px">
  <span class="pillar-badge">[PILLAR], DEEP DIVE</span>
  <h1 style="font-family:var(--font-display);font-size:clamp(28px,4vw,44px);font-weight:900;letter-spacing:-.02em;line-height:1.1;margin-bottom:12px">[TOPIC]</h1>
  <p style="font-family:var(--font-mono);font-size:12px;color:var(--text-3)">[DATE]</p>
</div>

<!-- 1. WHAT IT IS -->
<div class="sec-label">What It Is</div>
<div class="card card--accent fade-up fd-1">
  <div class="card__body">[ONE PLAIN SENTENCE, what this concept is]</div>
</div>

<!-- 2. WHY PEOPLE GET IT WRONG -->
<div class="sec-label" style="margin-top:24px">Why Most People Get It Wrong</div>
<div class="card card--dark fade-up fd-2">
  <div class="card__body">[THE COMMON MISTAKE, Danny's voice]</div>
</div>

<!-- 3. HOW DANNY THINKS ABOUT IT -->
<div class="sec-label" style="margin-top:24px">How Danny Thinks About It</div>
<div class="card fade-up fd-3">
  <div class="card__body">[DANNY'S PERSPECTIVE, conversational, direct]</div>
</div>

<!-- 4. THE THINKING EXPLAINED -->
<div class="sec-label" style="margin-top:24px">The Breakdown</div>
<div class="card fade-up fd-4">
  <div class="card__title">[CONCEPT NAME IN DANNY'S WORDS]</div>
  <div class="card__body">[FULL EXPLANATION WITH REAL EXAMPLE, short paragraphs]</div>
</div>

<!-- 5. APPLY TO THEIR SITUATION -->
<div class="sec-label" style="margin-top:24px">Applied to Your Situation</div>
<div class="card card--accent fade-up fd-5">
  <div class="card__body">[SPECIFIC APPLICATION TO WHAT THEY SHARED]</div>
</div>

<!-- 6. ACTION THIS WEEK -->
<div class="sec-label" style="margin-top:24px">This Week</div>
<div class="card--action fade-up fd-5" style="margin-top:0">
  <div class="card__label" style="color:var(--primary)">One Thing to Do</div>
  <div class="card__title">[SPECIFIC ACTION]</div>
  <div class="card__body" style="margin-top:10px">[Why this is the right first move]</div>
</div>

<!-- FOOTER -->
<footer>
  <div>
    <span class="footer__brand">Purely Personal</span>
    <span class="footer__by">by Daniel Paul</span>
  </div>
  <span class="footer__meta">AI CEO Brain · Deep Dive · [DATE]</span>
</footer>

<script>
document.querySelectorAll('.fade-up').forEach((el,i) => {
  el.style.animationDelay = (i * 0.08) + 's';
});
</script>
</body>
</html>
```
