#!/usr/bin/env node
// Check email files against the format and the house rules.
// Usage: node check-emails.mjs <file-or-folder> [more...] [--json]
// Exit code 1 if any ERROR is found. Node 18+, no dependencies.

import fs from 'node:fs';
import path from 'node:path';
import { readEmails, checkEmail, subjectLength, wordCount } from './email-lib.mjs';

const argv = process.argv.slice(2);
const asJson = argv.includes('--json');
const targets = argv.filter((a) => !a.startsWith('--'));
if (!targets.length) { console.error('Usage: node check-emails.mjs <file-or-folder> [--json]'); process.exit(2); }

const report = [];
for (const t of targets) {
  const p = path.resolve(t);
  if (!fs.existsSync(p)) { console.error(`Not found: ${p}`); process.exit(2); }
  for (const e of readEmails(p)) {
    report.push({
      file: e.file,
      type: e.type,
      subject: e.subject,
      subject_chars: subjectLength(e.subject),
      preview_chars: e.preview_text.length,
      words: wordCount(e.body),
      rating: e.rating_rounds.length ? e.rating_rounds.map((r) => r.overall).join(' > ') : 'not rated',
      checks: checkEmail(e),
    });
  }
}

const errors = report.reduce((n, r) => n + r.checks.filter((c) => c.level === 'error').length, 0);
if (asJson) {
  console.log(JSON.stringify({ errors, emails: report }, null, 2));
} else {
  if (!report.length) console.log('No email files found (an email file has frontmatter with a "type:" line).');
  for (const r of report) {
    console.log(`\n${path.basename(r.file)}  [${r.type}]  "${r.subject}" (${r.subject_chars} chars) · ${r.words} words · rating: ${r.rating}`);
    const shown = r.checks.filter((c) => c.level !== 'info');
    if (!shown.length) console.log('  OK');
    for (const c of r.checks) console.log(`  ${c.level.toUpperCase().padEnd(5)} ${c.msg}`);
  }
  console.log(`\n${report.length} email(s) checked, ${errors} error(s).`);
}
process.exit(errors ? 1 : 0);
