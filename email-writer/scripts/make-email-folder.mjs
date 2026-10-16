#!/usr/bin/env node
// Create the Email/ folder inside a Second Brain. Safe to run twice: it never overwrites a file.
// Usage: node make-email-folder.mjs <second-brain-folder> [--import path/to/EMAIL-BRAIN.md] [--refresh-kit]
// Node 18+, no dependencies. Prints a JSON summary.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { isRoomBrain, convertRoomBrain } from './room-import.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const REFS = path.join(here, '..', 'references');

const argv = process.argv.slice(2);
const flag = (k) => { const i = argv.indexOf(k); return i === -1 ? null : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const brainDir = argv.find((a, i) => !a.startsWith('--') && argv[i - 1] !== '--import');
if (!brainDir) { console.error('Usage: node make-email-folder.mjs <second-brain-folder> [--import EMAIL-BRAIN.md] [--refresh-kit]'); process.exit(2); }

const root = path.resolve(brainDir, path.basename(path.resolve(brainDir)) === 'Email' ? '.' : 'Email');
const summary = { email_folder: root, created: [], kept: [], notes: [] };
const today = new Date().toISOString().slice(0, 10);

function write(rel, content) {
  const f = path.join(root, rel);
  if (fs.existsSync(f)) { summary.kept.push(rel); return false; }
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, content);
  summary.created.push(rel);
  return true;
}

for (const d of ['drafts', 'months', 'sent', 'previews', 'kit']) {
  const p = path.join(root, d);
  if (!fs.existsSync(p)) { fs.mkdirSync(p, { recursive: true }); summary.created.push(d + '/'); }
}

// EMAIL-BRAIN.md: import theirs, or start from the template
const imp = flag('--import');
const brainPath = path.join(root, 'EMAIL-BRAIN.md');
if (imp && imp !== true) {
  const src = path.resolve(imp);
  if (!fs.existsSync(src)) summary.notes.push(`import file not found: ${src}`);
  else {
    const raw = fs.readFileSync(src, 'utf8');
    let text = raw;
    if (isRoomBrain(raw)) {
      const c = convertRoomBrain(raw);
      text = c.brain;
      if (c.sample) write('voice-sample.md', `# How I write (sample from the Email Room)\n\n${c.sample}\n`);
      if (c.ideas.length) write('ideas.md', `# Email ideas\n\nSay "add an idea: ..." to add one. Say "find me ideas" for ten more. Ticked ideas have been used.\n\nFormat: - [ ] date · type · the idea · where it came from\n\n${c.ideas.join('\n')}\n`);
      summary.notes.push('Converted the Email Room download into the plugin format.');
    }
    if (!fs.existsSync(brainPath)) { fs.writeFileSync(brainPath, text); summary.created.push('EMAIL-BRAIN.md (imported)'); }
    else { write('EMAIL-BRAIN.imported.md', text); summary.notes.push('EMAIL-BRAIN.md already existed. The download was saved as EMAIL-BRAIN.imported.md to merge.'); }
  }
}
const template = fs.readFileSync(path.join(REFS, 'email-brain-template.md'), 'utf8')
  .replace('created: ""', `created: "${today}"`).replace('updated: ""', `updated: "${today}"`);
write('EMAIL-BRAIN.md', template);

write('ideas.md', `# Email ideas

Say "add an idea: ..." to add one. Say "find me ideas" for ten more. Ticked ideas have been used.

Format: - [ ] date · type · the idea · where it came from

`);

write('scoreboard.md', `# Friday scoreboard

Four numbers every Friday. Missed a week? Just send the next one.

| Week of | Emails sent | Replies | New subscribers | Calls booked | Next week's one upgrade |
|---|---|---|---|---|---|
`);

write('README.md', `# My Email folder

- **EMAIL-BRAIN.md**: who I help, my offer, my proof and stories. Keep it true and up to date.
- **ideas.md**: every email idea. Say "add an idea: ..." to Claude.
- **drafts/**: single emails. **months/**: a month of emails with a calendar and a preview.
- **sent/**: emails that went out. **kit/**: the recipes, subject lines, scripts and rules.

Things to say to Claude: "write next month's emails", "write a client win", "fix my email",
"give me subject lines for this", "show me my emails", "help me load this into GoHighLevel", "Friday scoreboard".

Nothing is ever sent for me. I read it out loud, I paste it, I schedule it.
`);

// The kit: the member-facing parts, copied so they can read and edit them.
const KIT = { 'recipes.md': 'recipes.md', 'subject-lines.md': 'subject-lines.md', 'nine-word-scripts.md': 'nine-word-scripts.md', 'rules.md': 'rules.md', 'cadence.md': 'cadence.md', 'glossary.md': 'glossary.md', 'ideas.md': 'finding-ideas.md' };
const refresh = Boolean(flag('--refresh-kit'));
for (const [src, dest] of Object.entries(KIT)) {
  const s = path.join(REFS, src);
  if (!fs.existsSync(s)) { summary.notes.push(`kit file missing from the plugin: ${src} (run scripts/sync-kit.sh)`); continue; }
  const d = path.join(root, 'kit', dest);
  if (fs.existsSync(d) && !refresh) { summary.kept.push('kit/' + dest); continue; }
  fs.copyFileSync(s, d);
  summary.created.push('kit/' + dest + (refresh ? ' (refreshed)' : ''));
}

console.log(JSON.stringify(summary, null, 2));
