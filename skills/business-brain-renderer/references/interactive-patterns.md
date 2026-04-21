# Interactive Patterns — Business Brain Renderer

All JavaScript + CSS that turns a static Business Brain into an interactive artifact. Drop these into the `{{INTERACTIVE_SCRIPTS}}` slot in the base page wrapper when output mode = interactive.

**Rule:** every interactive pattern must also work cleanly in static mode — the page must degrade gracefully to a print-ready artifact with JS disabled.

---

## Master Script Bundle

Drop this entire block into the `{{INTERACTIVE_SCRIPTS}}` slot for full interactivity:

```html
<script>
(function(){
  'use strict';

  // ---------- CONFIG ----------
  const STORAGE_KEY = 'purely-personal-brain-draft';
  const SAVE_DEBOUNCE_MS = 600;

  // ---------- EDITABLE FIELDS ----------
  // Any element with data-editable="true" becomes contentEditable.
  // Hovering shows a subtle tint; focus shows strong tint.
  document.querySelectorAll('[data-editable="true"]').forEach(el => {
    el.setAttribute('contenteditable', 'true');
    el.setAttribute('spellcheck', 'true');
    el.addEventListener('input', scheduleSave);
    el.addEventListener('blur', save);
  });

  // ---------- AUTO-SAVE ----------
  let saveTimer = null;
  function scheduleSave() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, SAVE_DEBOUNCE_MS);
  }
  function save() {
    const draft = {};
    document.querySelectorAll('[data-editable="true"]').forEach(el => {
      const key = el.getAttribute('data-key');
      if (key) draft[key] = el.innerHTML;
    });
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(draft));
      flashIndicator('Saved');
    } catch(e) {
      console.warn('Save failed:', e);
    }
  }
  function load() {
    try {
      const draft = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      Object.entries(draft).forEach(([key, html]) => {
        const el = document.querySelector(`[data-key="${key}"]`);
        if (el) el.innerHTML = html;
      });
    } catch(e) {}
  }
  load();

  // ---------- SAVE INDICATOR ----------
  const indicator = document.getElementById('save-indicator');
  function flashIndicator(text) {
    if (!indicator) return;
    indicator.textContent = text;
    indicator.classList.add('visible');
    clearTimeout(indicator._t);
    indicator._t = setTimeout(() => indicator.classList.remove('visible'), 1400);
  }

  // ---------- COPY TO CLIPBOARD ----------
  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const text = btn.getAttribute('data-copy');
      try {
        await navigator.clipboard.writeText(text);
        const original = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(() => btn.textContent = original, 1200);
      } catch(err) {
        console.warn('Copy failed:', err);
      }
    });
  });

  // ---------- SLASH COMMAND RUNNER ----------
  // Clicking an action card copies the slash command and flashes confirmation.
  window.runCommand = function(cmd) {
    navigator.clipboard.writeText(cmd).catch(()=>{});
    flashIndicator(`Copied: ${cmd}`);
    return false; // prevent default anchor
  };

  // ---------- PDF EXPORT ----------
  const pdfBtn = document.getElementById('export-pdf');
  if (pdfBtn) {
    pdfBtn.addEventListener('click', async () => {
      // Method A (default): browser print dialog → Save as PDF
      window.print();
    });
  }

  // ---------- SHARE TO LINKEDIN ----------
  const shareBtn = document.getElementById('share-linkedin');
  if (shareBtn) {
    shareBtn.addEventListener('click', () => {
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(document.title);
      window.open(
        `https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}`,
        'linkedin-share',
        'width=600,height=600'
      );
    });
  }

  // ---------- EDIT TOGGLE ----------
  const editToggle = document.getElementById('edit-toggle');
  if (editToggle) {
    let editing = true; // default on in interactive mode
    editToggle.addEventListener('click', () => {
      editing = !editing;
      document.body.classList.toggle('editing', editing);
      editToggle.textContent = editing ? 'Done' : 'Edit';
      document.querySelectorAll('[data-editable="true"]').forEach(el => {
        el.setAttribute('contenteditable', editing ? 'true' : 'false');
      });
    });
    document.body.classList.add('editing');
  }

  // ---------- KEYBOARD SHORTCUTS ----------
  document.addEventListener('keydown', (e) => {
    // Cmd+P / Ctrl+P = already triggers browser print; let it through
    // Cmd+S / Ctrl+S = force save
    if ((e.metaKey || e.ctrlKey) && e.key === 's') {
      e.preventDefault();
      save();
    }
    // Escape = blur current editable
    if (e.key === 'Escape' && document.activeElement.getAttribute('contenteditable') === 'true') {
      document.activeElement.blur();
    }
  });

})();
</script>
```

---

## Interactive CSS Additions

Drop this into the `<style>` block of the base wrapper ONLY when interactive mode is on:

```css
/* Editable field hover + focus */
[data-editable="true"] {
  transition: background 120ms ease, outline 120ms ease;
  outline: 1px dashed transparent;
  outline-offset: 2px;
  border-radius: 2px;
}
body.editing [data-editable="true"]:hover {
  background: var(--pp-red-soft);
  outline-color: var(--pp-red);
}
body.editing [data-editable="true"]:focus {
  background: var(--pp-red-soft);
  outline-color: var(--pp-red);
  outline-style: solid;
}

/* Save indicator (top-right floating) */
#save-indicator {
  position: fixed;
  top: 16px;
  right: 16px;
  padding: 6px 12px;
  background: var(--text-primary);
  color: #fff;
  font-size: 12px;
  font-family: var(--mono);
  border-radius: 4px;
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 200ms ease, transform 200ms ease;
  pointer-events: none;
  z-index: 100;
}
#save-indicator.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Toolbar (PDF Export + Edit Toggle + Share) */
.brain-toolbar {
  position: fixed;
  top: 16px;
  right: 80px;
  display: flex;
  gap: 8px;
  z-index: 50;
}
.brain-toolbar button {
  padding: 8px 14px;
  background: var(--card-bg);
  border: 1px solid var(--divider-strong);
  border-radius: 4px;
  font-family: var(--body);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  cursor: pointer;
  transition: background 120ms ease, border-color 120ms ease;
}
.brain-toolbar button:hover {
  background: var(--sub-card-bg);
  border-color: var(--text-secondary);
}
.brain-toolbar button.primary {
  background: var(--pp-red);
  color: #fff;
  border-color: var(--pp-red);
  box-shadow: 0 2px 8px rgba(233,13,65,0.25);
}
.brain-toolbar button.primary:hover {
  background: var(--pp-red-deep);
  border-color: var(--pp-red-deep);
}

/* Action card hover (Actions Panel) */
body.editing .card a[onclick*="runCommand"] > div:hover,
.card a[onclick*="runCommand"] > div:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(20,14,8,0.08);
}

/* Print rules (hide all interactive chrome) */
@media print {
  .brain-toolbar,
  #save-indicator,
  [data-copy],
  #edit-toggle {
    display: none !important;
  }
  [data-editable="true"] {
    outline: none !important;
    background: transparent !important;
  }
}
```

---

## Toolbar HTML (drop above `<main>` in interactive mode)

```html
<!-- Save indicator (floats top-right, appears on save) -->
<div id="save-indicator" class="no-print">Saved</div>

<!-- Toolbar: Edit, Share, Export -->
<div class="brain-toolbar no-print">
  <button id="edit-toggle" type="button">Done</button>
  <button id="share-linkedin" type="button">Share</button>
  <button id="export-pdf" type="button" class="primary">Export PDF</button>
</div>
```

---

## Making Fields Editable — Wiring Rules

Each editable element needs:

```html
<p data-editable="true" data-key="voice.tone">{{VOICE_TONE}}</p>
```

- `data-editable="true"` → the script will wire it
- `data-key="voice.tone"` → the localStorage key (namespaced: `section.field`)

### Key Naming Convention

Use `section.field` or `section.field[index]`:

| Field | Key |
|-------|-----|
| Brain name | `cover.name` |
| Brain tagline | `cover.tagline` |
| Voice tone | `voice.tone` |
| Offer | `business.offer` |
| Positioning | `business.positioning` |
| 90-day goal | `business.goal` |
| ICP name | `icp.name` |
| ICP pain #1 | `icp.pain[0]` |
| ICP pain #2 | `icp.pain[1]` |
| Competitor 1 name | `comp[0].name` |
| Competitor 1 gap | `comp[0].gap` |

Bracket notation is a string inside the attribute (not parsed). Match the key exactly on load.

---

## PDF Export — Method A (default: browser print)

Method A uses `window.print()` + print CSS. Zero dependencies. Works offline. Produces a clean PDF via the OS print dialog.

**Pros:** Zero install, works everywhere, print CSS is already in the base template.
**Cons:** Requires user to click "Save as PDF" in the print dialog.

### Enhancement — Single-file Download Hint

On first PDF export, flash a tooltip:

```js
// Inside pdfBtn listener, before window.print():
if (!localStorage.getItem('pdf-hint-shown')) {
  alert('In the print dialog, choose "Save as PDF" as the destination.');
  localStorage.setItem('pdf-hint-shown', '1');
}
```

---

## PDF Export — Method B (advanced: html2pdf.js)

If the user wants programmatic one-click PDF download, load `html2pdf.js` and replace the export handler:

```html
<!-- Load library -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

<script>
document.getElementById('export-pdf').addEventListener('click', () => {
  const element = document.querySelector('main');
  const opt = {
    margin: 0,
    filename: `${document.title.replace(/[^a-z0-9]/gi,'_')}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true, backgroundColor: '#faf8f4' },
    jsPDF: { unit: 'pt', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['css', 'legacy'] }
  };
  html2pdf().set(opt).from(element).save();
});
</script>
```

**Pros:** Single-click download, filename auto-set.
**Cons:** Adds 400KB library, requires CORS-enabled headshot URL, needs stable internet for CDN.

**Recommendation:** Use Method A by default. Offer Method B as an upgrade when user explicitly asks for "one-click PDF" or the skill is being bundled with other html2pdf-dependent skills.

---

## PDF Export — Method C (python script, for automated exports)

When the user runs `/export-brain-pdf`, invoke a Python script that uses Playwright to render the HTML → PDF. Belongs in `scripts/build_pdf.py` at the plugin root:

```python
#!/usr/bin/env python3
"""Render BUSINESS-BRAIN.md → single-page HTML → PDF."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def render_to_pdf(html_path: str, pdf_path: str):
    html_url = Path(html_path).absolute().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_url, wait_until='networkidle')
        page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: build_pdf.py <html_in> <pdf_out>')
        sys.exit(1)
    render_to_pdf(sys.argv[1], sys.argv[2])
```

Invoke:

```bash
python3 scripts/build_pdf.py brain.html brain.pdf
```

Dependencies: `pip install playwright && playwright install chromium` (one-time).

---

## Traffic-light Rating (future: per-section completeness indicator)

For sections that are partially filled, show a small traffic light indicator next to the label. Reserved for future use — not yet wired.

Color logic:

| State | Color | Meaning |
|-------|-------|---------|
| Complete (all fields filled) | `--engine-sales` green | Good |
| Partial (≥1 missing) | `--engine-cash` gold | Needs attention |
| Empty | `--engine-leadership` red | Not started |

```html
<span class="traffic-light" data-state="partial"></span>
```

```css
.traffic-light {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  margin-left: 6px;
  vertical-align: middle;
}
.traffic-light[data-state="complete"] { background: var(--engine-sales); }
.traffic-light[data-state="partial"]  { background: var(--engine-cash); }
.traffic-light[data-state="empty"]    { background: var(--engine-leadership); }
```

---

## Accessibility Rules

- All interactive controls have visible focus states (outlines use `--pp-red`, never removed)
- All buttons have `type="button"` to prevent form-submit behavior
- Editable fields use `contenteditable` + `spellcheck="true"`
- Color is never the only signal (traffic lights pair with text labels in final implementation)
- Minimum touch target: 40×40px on all buttons
- Keyboard: Cmd+S saves, Escape blurs, Tab traverses in DOM order

---

## Degradation (JS disabled)

If JavaScript is disabled, the page still renders cleanly:

- Editable fields show their values as normal text (no contentEditable)
- Toolbar buttons render as non-functional but visually intact (native print via Cmd+P still works)
- Action cards in the Actions Panel still display commands — user can copy manually
- No error messages. The page degrades silently to print-ready static.

This is required behavior — the artifact must remain valuable as a PDF/screenshot even when stripped of interactivity.

---

## Anti-patterns

- ❌ Don't wire `onsubmit` or `onchange` handlers. Use `input` (contenteditable) and `click`.
- ❌ Don't animate field saves. A brief indicator flash is enough — no pulsing borders.
- ❌ Don't load jQuery, lodash, or any heavy library. Everything above is vanilla JS < 2KB.
- ❌ Don't use `alert()` except for the one-time PDF-hint. Use the save indicator pattern for all other confirmations.
- ❌ Don't remove focus outlines ever. `outline: none` is banned for keyboard users.
- ❌ Don't make the toolbar sticky at the top of the *scroll*. Fixed position is fine; sticky interferes with print.
