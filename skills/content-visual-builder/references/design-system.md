# Design System — Content Visual Builder

**This skill uses the shared Purely Personal design system.** All tokens, typography, and rules live in the master design-system file of the Business Brain Renderer skill.

👉 **Read:** [`../../business-brain-renderer/references/design-system.md`](../../business-brain-renderer/references/design-system.md)

---

## Scope of This File

This file only documents the **platform-specific additions** that Content Visual Builder layers on top of the master system. Everything else — colors, typography scale, spacing, print rules — is inherited as-is.

---

## Additional Tokens (platform variants)

On top of the master tokens, add these for the 4 content platforms:

```css
:root {
  /* Inherit all master tokens from business-brain-renderer/references/design-system.md */

  /* Platform accents (additions) */
  --platform-linkedin:    #0A66C2;
  --platform-x:           #0F1419;
  --platform-x-blue:      #1D9BF0;
  --platform-instagram-gradient: linear-gradient(135deg, #833AB4, #FD1D1D, #FCB045);
  --platform-newsletter:  #E8D9C5;
}
```

---

## Card-Native Surface Colors

Each platform card uses a different background treatment to match the real platform:

| Platform | Card bg | Outer page bg | Border |
|----------|---------|---------------|--------|
| LinkedIn | `#ffffff` | `#F3F2EF` (LinkedIn grey) | `#e8e2d8` |
| X | `#ffffff` light mode OR `#000000` dark | `transparent` | `#e8e2d8` light / `#2f3336` dark |
| Instagram | `#ffffff` | `#fafafa` | — (gradient top accent) |
| Newsletter | `var(--platform-newsletter)` cream | `#ffffff` | `#0a0a0a` 4px top |

---

## Typography Per Platform

Typography scale is the **same as the master system**, with platform-specific adjustments:

| Platform | Display adjustment | Body adjustment |
|----------|-------------------|-----------------|
| LinkedIn | None — use master scale | 14px body (slightly tighter) |
| X | None | 15px body (X's native size) |
| Instagram | None | 14px body |
| Newsletter | 32px subject line | 15px body, 1.7 line-height (reading density) |

---

## Rule: Voice > Design

A content card's visual quality is secondary to its voice quality. A perfectly-designed card with AI-smelling copy is worse than a plain card with a banger line. Always run voice validation from `voice-application.md` before worrying about visual polish.

---

## Brand Mark Rules

Every card includes ONE of:

1. **User's handle** in header (for single-platform post cards)
2. **`pp` brand dot** in corner (for Quote, Stat, Cheatsheet cards)
3. **Newsletter name** in header strip (for Newsletter card)

Never omit brand attribution. The card is either the user's voice or an orphaned asset.

---

## Anti-patterns (specific to this skill, in addition to master list)

- ❌ Never hardcode platform colors. Use CSS custom properties.
- ❌ Never mix platform styles in one card (e.g. LinkedIn layout with X dark mode).
- ❌ Never render Instagram card without the gradient element somewhere.
- ❌ Never exceed the master font weight rule (400 + 700/800 only).
- ❌ Never add a second custom font beyond Rethink Sans + Inter + JetBrains Mono.
