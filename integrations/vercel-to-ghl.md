# Vercel → GoHighLevel Connection Guide

> **Owner:** Karthik · **Deadline:** Apr 25 (so GHL has time to test before Apr 30 registration cliff)
> **Time required:** 5 minutes (simplest) to 30 minutes (full custom domain)

---

## TL;DR

**Don't embed the GHL form inside the Vercel page.** That path looks cleaner but creates 6 technical problems (CSP, pixel tracking, mobile iframes, etc.).

**Instead, redirect the CTAs.** Every "Reserve my seat" button on the landing page links to the GHL funnel URL. Visitor clicks → lands on GHL checkout → GHL owns the conversion. Vercel just drives traffic.

**This is how Apple, Stripe, and every major SaaS does it.** Landing site and checkout site are separate.

---

## The 3 Options (ranked by effort)

### Option 1 — Redirect CTAs (5 minutes) · RECOMMENDED

**What it looks like:**

- Visitor lands on `purely-personal-workshop.vercel.app`
- Clicks "Reserve my seat"
- Gets taken to `purelypersonal.gohighlevel.com/workshop-01-signup` (or custom GHL domain)
- GHL handles form + payment + automation

**Steps:**

1. Build the GHL funnel per [`ghl-build-spec.md`](./ghl-build-spec.md)
2. Copy the GHL funnel URL (example: `https://go.purelypersonal.ai/workshop-01`)
3. Open the landing page: `landing-page/index.html`
4. Find-replace these 3 patterns:

| Find | Replace with |
|------|--------------|
| `href="#reserve"` | `href="YOUR_GHL_URL?ref=landing-reserve"` |
| `href="#cta"` | `href="YOUR_GHL_URL?ref=landing-cta"` |
| `href="https://purelypersonal.ai/checkout"` | `href="YOUR_GHL_URL?ref=landing-final"` |

5. Commit + push:

```bash
git add landing-page/index.html
git commit -m "Wire CTA buttons to GHL funnel"
git push
```

6. Vercel auto-deploys in ~20 seconds
7. Test by clicking a CTA on the live site — should land on the GHL form

**Pros:**
- 5-minute setup
- Zero new infrastructure
- UTM params track attribution per-button in GHL analytics
- If GHL goes down, the landing page still works

**Cons:**
- Visitor leaves `purely-personal-workshop.vercel.app` to pay
- Two different domains (unless you custom-domain them, see Option 2)

---

### Option 2 — Custom Subdomain (30 minutes) · NEXT UPGRADE

**What it looks like:**

- Visitor lands on `workshop.purelypersonal.ai` (Vercel landing)
- Clicks CTA → goes to `signup.purelypersonal.ai` (GHL funnel) — same parent domain, feels like one site
- GHL handles checkout

**Steps:**

1. **In Vercel:**
   - Project Settings → Domains
   - Add `workshop.purelypersonal.ai`
   - Vercel gives you a CNAME target (e.g. `cname.vercel-dns.com`)

2. **In your DNS provider (Cloudflare / Namecheap / wherever `purelypersonal.ai` is hosted):**
   - Add CNAME record: `workshop` → `cname.vercel-dns.com`
   - TTL: 300 (5 minutes)

3. **In GHL:**
   - Settings → Domains → Add domain
   - Add `signup.purelypersonal.ai`
   - GHL gives you a CNAME or A record target

4. **In DNS:**
   - Add CNAME record: `signup` → GHL's target
   - TTL: 300

5. **Wait 5–15 minutes** for DNS to propagate

6. **Update landing page CTAs** (Option 1, step 4) but with `https://signup.purelypersonal.ai/workshop-01`

7. **Test:**
   - `workshop.purelypersonal.ai` loads Vercel landing
   - Clicking CTA takes you to `signup.purelypersonal.ai/...`
   - Both show SSL lock icon (both have Let's Encrypt auto-issued)

**Pros:**
- Single parent domain looks professional
- SSL on both (automatic via Vercel + GHL)
- Perfect for sharing link in emails + DMs ("workshop.purelypersonal.ai")
- Email deliverability benefits (same domain as sending)

**Cons:**
- Requires DNS access
- 30 minutes instead of 5

---

### Option 3 — Embedded GHL Form (NOT recommended)

An iframe on the Vercel landing page that loads the GHL form inline.

**Why we're skipping this:**

1. **CSP headers block it.** Vercel and GHL both have Content Security Policies that fight over iframe embedding. Takes 2–3 hours of config to make work.
2. **Pixel tracking breaks.** GHL's tracking pixels fire in the iframe, not the parent page. Facebook / LinkedIn pixels don't see the conversion.
3. **Mobile UX is bad.** iframes on mobile don't scroll cleanly. Virtual keyboard resizes the parent page, not the form.
4. **Payment auth redirects fail.** Stripe 3DS challenges redirect away from the iframe, losing the session.
5. **GHL has heavy JS.** Slows Vercel landing load by 2–3 seconds.
6. **No UTM attribution.** Can't track which CTA button was clicked.

Net: Option 3 looks cleaner but breaks 3 critical features. Skip it.

---

## Recommendation

Start with **Option 1 (5 minutes)**. Launch Workshop 01 on Option 1. Upgrade to Option 2 sometime in May before Workshop 02. By Workshop 03 you'll want Option 2 for brand consistency.

---

## 3 URLs Karthik Needs from the GHL Specialist

As soon as the GHL funnel is built, the specialist hands Karthik:

| URL Label | What It Does | Used Where |
|-----------|--------------|------------|
| Funnel URL (Page 1) | Checkout form + payment | Every "Reserve my seat" CTA |
| Thank-you URL (Page 2) | Post-payment page with Zoom link | Shown after payment (automatic) |
| Webhook URL | Fires on purchase for attendee export | In Malik's Zapier/Sheet flow |

---

## Testing Checklist (before opening registration)

- [ ] Click every "Reserve" CTA on the live landing page → lands on GHL
- [ ] Submit form with test data (`test-{karthik}@purelypersonal.ai`)
- [ ] Payment via Stripe test mode completes
- [ ] Confirmation email arrives in test inbox within 60 seconds
- [ ] Webhook fires and appends to Zapier Sheet
- [ ] UTM params visible in GHL analytics per-button
- [ ] SSL lock icon present on both Vercel and GHL URLs
- [ ] Mobile test on iPhone + Android
- [ ] Refund test: issue refund, payment reverses in Stripe dashboard

If ANY of these fail, registration does NOT open. Fix, re-test, open.

---

## Who Does What

| Person | Action | Deadline |
|--------|--------|----------|
| GHL specialist | Build funnel per `ghl-build-spec.md`, deliver 3 URLs to Karthik | Apr 22 |
| Karthik | Update `landing-page/index.html` CTAs, push to GitHub | Apr 23 |
| Karthik + GHL specialist | Run full testing checklist together | Apr 24 |
| Danny | Final sign-off, run 1 real $49 payment end-to-end | Apr 25 |
| Everyone | Registration opens publicly | Apr 26 |

---

## Fallback Plan (if GHL isn't ready)

If the GHL funnel isn't ready by Apr 23, use **Stripe Payment Links** as a stopgap:

1. Create a Stripe Payment Link for $49
2. Send Vercel landing page CTAs to it
3. Manual onboarding via reply email until GHL catches up

This loses the automated email sequence + webhook integration but keeps registration open. Not ideal but functional.

---

## Related Files

- Full GHL build spec: [`integrations/ghl-build-spec.md`](./ghl-build-spec.md)
- Landing page source: [`landing-page/index.html`](../landing-page/index.html)
- Live landing page: [purely-personal-workshop.vercel.app](https://purely-personal-workshop.vercel.app)
