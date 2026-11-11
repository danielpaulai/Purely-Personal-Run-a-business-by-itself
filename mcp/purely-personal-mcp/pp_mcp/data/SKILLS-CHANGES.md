# How the bundled skills differ from the Drive originals

The 12 program skills are copied from the shared Drive folder and then cleaned by `scripts/clean_skills.py`. Run that script again after replacing a skill; it is idempotent and exits non-zero if an upstream edit means a fix no longer applies.

1. Garbled banned-word lists restored to the program's real list.
2. One post length standard: 1300-1500 characters (about 200-250 words).
3. Invented proof points and unsupported claims removed; examples labelled "Illustrative only".
4. Sample copy rewritten to follow the style rules (no "Real talk", no negation pivots, short carousel slides).
5. Sections that depend on files, scripts or skills that are not part of the connector removed (renderer, `visual` HTML modes, CLI usage, bundled-files lists, Apify token setup, chained skills that do not exist). Each skill ends with the connector tool that runs it.
6. Cohort-specific material (times, session names, attendee counts, the author's name) removed or generalised. `homework-reviewer` is rewritten as a generic batch reviewer.
7. `competitor-x-ray` and `prospect-magnet` name the verified Apify actors (company pages vs profiles).

Tests: `tests/test_skill_bundle_quality.py`.
