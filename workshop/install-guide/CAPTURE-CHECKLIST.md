# Install Guide · Screenshot Capture Checklist

> **Purpose:** fill the 24 screenshot slots in `index.html` with real screenshots.
> **Estimated time:** 60 minutes for one person sitting at a Mac (+ 20 min for the Windows variants if we do both).
> **Output:** PNG files dropped into `workshop/install-guide/screenshots/`. Filenames match the list below.
> **Quality:** 1:1 Retina capture, crop tight to the relevant UI, no personal data visible (blur tokens, emails, names where noted).

---

## Capture rules

1. **Browser:** Chrome or Safari, incognito window, 1440×900 viewport, 100% zoom
2. **Theme:** light mode everywhere (never dark)
3. **Crop:** tight around the relevant UI, remove unrelated browser chrome/tabs
4. **Annotation:** use red circle (2px stroke) or red underline for buttons/fields to click
5. **Privacy:** blur any real tokens, email addresses, or names with a soft black rectangle
6. **Filename:** exactly as listed, lowercase, dashes, `.png` only
7. **Resolution:** keep under 400 KB each (use TinyPNG or squoosh.app if needed)

---

## The 24 screenshots (by step)

### Step 1 · Claude Pro + Claude Code (4 screenshots)

| # | Filename | Capture |
|---|---|---|
| 1 | `01a-claude-signup.png` | claude.ai homepage. Red-circle the "Sign up" button in top right. |
| 2 | `01b-claude-pro-upgrade.png` | claude.ai pricing page. Show the Pro tier card with "Upgrade" CTA highlighted. $20/mo must be visible. |
| 3 | `01c-claude-code-install-mac.png` | Mac Terminal after running the install script. Show 4–5 lines of progress ending in "Installation complete". |
| 4 | `01d-claude-code-install-win.png` | Windows PowerShell same install, white text on blue bg. |

### Step 2 · GitHub (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 5 | `02-github-signup.png` | github.com homepage. Red-circle the green "Sign up" button. |

### Step 3 · Install Git (2 screenshots)

| # | Filename | Capture |
|---|---|---|
| 6 | `03a-git-install-mac.png` | Mac Xcode Command Line Tools dialog. Red-circle "Install" button. |
| 7 | `03b-git-install-win.png` | Windows Git Setup wizard on "Select Components" screen. Highlight "Next >" button. All defaults ticked. |

### Step 4 · Clone repo (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 8 | `04-git-clone-output.png` | Terminal showing `git clone ...` + 4–5 lines of "Cloning into..." / "Receiving objects..." / "Resolving deltas..." ending in a prompt inside the new folder. |

### Step 5 · Install plugin (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 9 | `05-plugin-install-output.png` | Terminal showing `claude plugin install .` with success confirmation. |

### Step 6 · Verify 8 commands (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 10 | `06-slash-commands-menu.png` | Claude Code with `/` dropdown expanded. All 8 purely-personal commands visible. Red-circle the 8 commands as a group. |

### Step 7 · Gmail connector (2 screenshots)

| # | Filename | Capture |
|---|---|---|
| 11 | `07a-connectors-page.png` | claude.ai Settings → Connectors. Full list visible. Red-circle the "+ Add" button. |
| 12 | `07b-gmail-oauth-permissions.png` | Google OAuth consent screen for Gmail. All permission boxes ticked. Red-circle "Allow". |

### Step 8 · Notion (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 13 | `08-notion-connector.png` | Connectors page with Notion now in the "Connected" list, green checkmark. |

### Step 9 · Google Calendar (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 14 | `09-calendar-connector.png` | Connectors page with Google Calendar connected. |

### Step 10 · Google Drive (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 15 | `10-drive-connector.png` | Google OAuth consent screen for Drive. Highlight the "Create new files" permission specifically. |

### Step 11 · Stripe (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 16 | `11-stripe-connector.png` | Connectors page with Stripe connected. Caption area emphasizes "optional". |

### Step 12 · Apify account + token (3 screenshots)

| # | Filename | Capture |
|---|---|---|
| 17 | `12a-apify-signup.png` | apify.com homepage. Red-circle "Sign up free" CTA. |
| 18 | `12b-apify-integrations-page.png` | console.apify.com → Settings → Integrations. Red-circle "+ Create new token" button. |
| 19 | `12c-apify-token-created.png` | "Token created" modal. Token string visible but BLURRED. Red-circle the Copy button. |

### Step 13 · Wire Apify MCP (2 screenshots)

| # | Filename | Capture |
|---|---|---|
| 20 | `13a-config-file-mac.png` | Mac TextEdit with the JSON config pasted. Blur the real token. Red-underline the `"APIFY_TOKEN"` line. |
| 21 | `13b-config-file-win.png` | Windows Notepad with identical config. Title bar shows `claude_desktop_config.json`. |

### Step 14 · Verify Apify (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 22 | `14-apify-test-output.png` | Claude Code conversation with test prompt + 3 real Google result cards. Tool call `apify:google-search-scraper` visible in the trace. |

### Step 15 · LinkedIn URL reply (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 23 | `15-linkedin-reply-example.png` | Gmail compose window, reply to confirmation email, body is just a LinkedIn URL. No other text. |

### Step 16 · Business folder + /plugins (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 24 | `16-claude-plugins-output.png` | Claude Code `/plugins` output with "purely-personal" in the loaded plugins list. |

### Step 17 · Empty BRAIN.md (1 screenshot)

| # | Filename | Capture |
|---|---|---|
| 25 | `17-empty-brain-file.png` | Finder (Mac) or Explorer (Windows) showing `my-business` folder containing empty `BUSINESS-BRAIN.md` (0 KB). |

---

## Ordering for fastest capture

If you're capturing on a single Mac:

**Round 1 · Browser (5 min)** · open apify.com, github.com, claude.ai, git-scm.com in tabs. Capture 01a, 02, 03b (Windows screenshot can come from VM), 12a.

**Round 2 · Mac Terminal (10 min)** · run through the install flow end-to-end in a fresh terminal. Capture 01c, 03a, 04, 05, 06, 16, 17.

**Round 3 · Claude.ai logged in (15 min)** · connect each connector for real. Capture 07a, 07b, 08, 09, 10, 11. (If you don't want to actually connect, capture the "+ Add → Service" modal for each.)

**Round 4 · Apify (10 min)** · sign up for a second test account, follow the flow end-to-end. Capture 12a, 12b, 12c, 14.

**Round 5 · Config file (5 min)** · TextEdit screenshot with the paste. Capture 13a (13b needs a Windows VM or someone else's machine).

**Round 6 · Gmail + misc (5 min)** · 15 (Gmail reply), 01b (pricing page).

**Round 7 · Post-process (10 min)** · crop all, blur tokens, compress with squoosh, rename to match the list.

Total: ~60 minutes solo on Mac.

---

## What to do when a screenshot is captured

1. Drop the file into `workshop/install-guide/screenshots/` with the exact filename
2. The HTML already references every filename · the placeholder flips to the real image automatically
3. No code changes needed

---

## What to do with Windows-specific shots

Two options:

**Option A · Shared VM:** spin up a free Windows 11 trial VM in UTM or Parallels. 30 min to set up, worth it for the Windows variants.

**Option B · Ask a Windows teammate:** send this checklist to one person on the team with Windows. They capture 01d, 03b, 13b in ~10 min.

If neither: ship with only Mac shots and note "Windows shots coming" in the guide header. Mac covers 85% of attendees.

---

## When done

Run this to verify every file exists:

```bash
cd workshop/install-guide/screenshots
ls *.png | wc -l   # should return 25
```

Then commit and push. The live guide updates on Vercel (or wherever it's hosted) within 20 seconds.
