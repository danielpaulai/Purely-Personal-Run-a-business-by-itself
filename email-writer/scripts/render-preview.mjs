#!/usr/bin/env node
// Render one email file, or a folder of them, into a self-contained inbox preview.
// Usage:
//   node render-preview.mjs <file-or-folder> [--out preview.html] [--open]
//        [--from "Maya"] [--email maya@example.com] [--platform gohighlevel|mailchimp|activecampaign|other]
//        [--title "November 2026"] [--no-fonts]
// Node 18+, no dependencies.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import {
  readEmails, findEmailRoot, readBrain, checkEmail, subjectLength, TYPE_LABELS, slugify,
} from './email-lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATE = path.join(here, '..', 'templates', 'preview-template.html');

function args(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) out[k] = true; else { out[k] = next; i++; }
    } else out._.push(a);
  }
  return out;
}

function platformKey(s) {
  const t = String(s || '').toLowerCase().replace(/[^a-z]/g, '');
  if (t.includes('highlevel') || t === 'ghl') return 'gohighlevel';
  if (t.includes('mailchimp')) return 'mailchimp';
  if (t.includes('activecampaign')) return 'activecampaign';
  return t ? 'other' : '';
}

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

function main() {
  const a = args(process.argv.slice(2));
  const input = a._[0];
  if (!input) {
    console.error('Usage: node render-preview.mjs <email.md | folder> [--out file.html] [--open]');
    process.exit(2);
  }
  const target = path.resolve(input);
  if (!fs.existsSync(target)) { console.error(`Not found: ${target}`); process.exit(2); }
  const isDir = fs.statSync(target).isDirectory();

  const emails = readEmails(target);
  if (!emails.length) {
    console.error('No email files found. An email file starts with frontmatter that has a "type:" line (see references/email-file-format.md).');
    process.exit(1);
  }

  const root = findEmailRoot(target);
  const brain = readBrain(root);
  const fromName = String(a.from || brain.sender_name || brain.name || 'You');
  const fromEmail = String(a.email || brain.sender_email || '');
  const platform = platformKey(a.platform || brain.platform);

  let title = a.title;
  const folderName = path.basename(isDir ? target : path.dirname(target));
  if (!title) {
    const m = folderName.match(/^(\d{4})-(\d{2})$/);
    if (isDir && m) title = `${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
    else if (!isDir) title = emails[0].name || emails[0].subject;
    else title = folderName === 'Email' ? 'All emails' : folderName;
  }

  const data = {
    title,
    generated: new Date().toISOString(),
    sender: { name: fromName, email: fromEmail, initial: (fromName.trim()[0] || 'Y').toUpperCase() },
    platform,
    emails: emails.map((e, i) => ({
      id: i,
      file: path.relative(isDir ? target : path.dirname(target), e.file),
      type: e.type,
      typeLabel: TYPE_LABELS[e.type] || e.type,
      sequence_step: e.sequence_step,
      name: e.name,
      date: e.date,
      time: e.time,
      status: e.status,
      subject: e.subject,
      subjectChars: subjectLength(e.subject),
      subject_options: e.subject_options.map((o) => ({ ...o, chars: subjectLength(o.text), chosen: o.text === e.subject })),
      recommended_reason: e.recommended_reason,
      preview_text: e.preview_text,
      cta: e.cta,
      side_idea: e.side_idea,
      fill_in: e.fill_in,
      best_line: e.best_line,
      rating_rounds: e.rating_rounds.map((r) => ({ round: Number(r.round), overall: Number(r.overall), honesty: String(r.honesty || ''), scores: r.scores || {} })),
      body: e.body,
      checks: checkEmail(e),
    })),
  };

  let html = fs.readFileSync(TEMPLATE, 'utf8');
  const json = JSON.stringify(data).replace(/</g, '\\u003c').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
  html = html.split('__EMAIL_DATA__').join(json);
  html = html.split('__PAGE_TITLE__').join(escapeHtml(`${title} · Email preview`));
  if (a['no-fonts']) html = html.replace(/<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>\s*/g, '');

  let out = a.out ? path.resolve(String(a.out)) : null;
  if (!out) {
    if (isDir) out = path.join(target, 'preview.html');
    else {
      const base = root ? path.join(root, 'previews') : path.dirname(target);
      out = path.join(base, slugify(path.basename(target, '.md')) + '.html');
    }
  }
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, html);

  const errors = data.emails.reduce((n, e) => n + e.checks.filter((c) => c.level === 'error').length, 0);
  const fills = data.emails.reduce((n, e) => n + e.fill_in.length, 0);
  console.log(`Preview: ${out}`);
  console.log(`${data.emails.length} email(s) · ${fills} thing(s) to fill in · ${errors} error(s) from the checker`);

  if (a.open) {
    const cmd = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'cmd' : 'xdg-open';
    const cargs = process.platform === 'win32' ? ['/c', 'start', '', out] : [out];
    try { spawn(cmd, cargs, { stdio: 'ignore', detached: true }).unref(); } catch { console.log('Could not open it automatically. Double-click the file to open it.'); }
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

main();
