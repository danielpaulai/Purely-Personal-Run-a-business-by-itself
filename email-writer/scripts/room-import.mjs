#!/usr/bin/env node
// Import the Email Room downloads into the Email folder.
//   EMAIL-BRAIN.md   (room format: "# EMAIL BRAIN · Name" with "## Section" blocks)
//   my-emails-<date>.md  (all room emails in one file, each with its own frontmatter)
// Usage:
//   node room-import.mjs --email-dir <Email> [--brain <EMAIL-BRAIN.md>] [--emails <my-emails.md>] [--month YYYY-MM]
// Never overwrites a file. Node 18+, no dependencies. Prints a JSON summary.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { splitFrontmatter, parseYaml, roomSection } from './email-lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const REFS = path.join(here, '..', 'references');
const argv = process.argv.slice(2);
const opt = (k) => { const i = argv.indexOf('--' + k); return i === -1 ? '' : (argv[i + 1] || ''); };
const emailDir = path.resolve(opt('email-dir') || '.');
const summary = { created: [], kept: [], notes: [] };
const d = new Date();
const today = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

const LABEL_TO_TYPE = { 'client win': 'client_win', story: 'story', '9-word email': 'nine_word', 'how-to': 'how_to', 'event invite': 'event_invite', '8-minute email': 'eight_minute_edit' };
const TYPE_SLUG = { client_win: 'client-win', story: 'story', nine_word: 'nine-word', how_to: 'how-to', event_invite: 'event-invite', eight_minute_edit: 'eight-minute' };

function writeNew(file, text) {
  if (fs.existsSync(file)) { summary.kept.push(path.relative(emailDir, file)); return false; }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  summary.created.push(path.relative(emailDir, file));
  return true;
}

export function isRoomBrain(text) { return /^#\s*EMAIL BRAIN\b/m.test(text) && /^##\s+Name and sign-off/m.test(text); }

const cell = (s) => String(s).replace(/\|/g, '/').replace(/\n+/g, ' ').trim();
const lines = (s) => String(s).split('\n').map((l) => l.replace(/^[-*]\s+/, '').trim()).filter(Boolean);

export function convertRoomBrain(text) {
  const g = (h) => roomSection(text, h);
  const name = g('Name and sign-off');
  const sender = g('Sender name');
  const platformRaw = g('Where I send from');
  const perWeek = parseInt(g('Emails per week'), 10) || 1;
  const language = g('Language my clients read') || 'English';
  const proofRaw = g('Proof bank');
  const mayName = /May I name clients\?\s*Yes/i.test(proofRaw) ? 'yes' : 'ask';
  const wins = lines(proofRaw.replace(/May I name clients\?.*$/im, ''));
  const stories = lines(g('Story bank'));
  const q = (s) => JSON.stringify(String(s || ''));

  let t = fs.readFileSync(path.join(REFS, 'email-brain-template.md'), 'utf8');
  t = t.replace('name: ""', `name: ${q(name)}`)
    .replace('sender_name: ""', `sender_name: ${q(sender || name)}`)
    .replace('business: ""', `business: ${q(sender)}`)
    .replace('platform: ""', `platform: ${q(platformRaw)}`)
    .replace('emails_per_week: 1', `emails_per_week: ${perWeek}`)
    .replace('language: "English"', `language: ${q(language)}`)
    .replace('created: ""', `created: "${today}"`).replace('updated: ""', `updated: "${today}"`);
  // Replaces "- **Label:** hint", "1. **Label:** hint" or "- Label:" lines with the value.
  const setLine = (label, value) => {
    if (!value) return;
    const re = new RegExp('^(- |\\d\\. )(\\*\\*)?' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ':(\\*\\*)?.*$', 'm');
    const v = String(value).replace(/\n+/g, ' ');
    t = t.replace(re, (_, pre, b1, b2) => `${pre}${b1 || ''}${label}:${b2 || ''} ${v}`);
  };
  setLine('First name (sign-off)', name);
  setLine('Business name', sender);
  setLine('Who I help', g('Who I help'));
  setLine('The result I help them get', g('The result I get them'));
  setLine('Language my clients read', language);
  setLine('What I sell', g('My offer'));
  setLine('My call to action', g('My one call to action'));
  setLine('Emails a week for the next 30 days', String(perWeek));
  setLine('Events coming up', g('My event'));
  setLine('I send with', platformRaw);
  const ways = g('Three ways to work with me (PS)');
  if (ways) {
    const parts = ways.split(/\s*(?:^|\s)\d\.\s+/m).map((s) => s.trim()).filter(Boolean);
    if (parts.length === 3) { setLine('Smallest', parts[0]); setLine('Middle', parts[1]); setLine('Biggest', parts[2]); }
    else t = t.replace('1. **Smallest:**', `From the Email Room: ${ways.replace(/\$/g, '$$$$')}\n\n1. **Smallest:**`);
  }
  if (wins.length) {
    const rows = wins.map((w) => `| ${cell(w)} | | | | ${mayName} |`).join('\n');
    t = t.replace(/^\| \| \| \| \| yes \/ no \/ ask \|$/m, rows);
  }
  if (stories.length) {
    const rows = stories.map((s) => `| ${cell(s)} | | | |`).join('\n');
    t = t.replace(/^\| \| \| \| \|$/m, rows);
  }
  const sample = g('How I write (sample)');
  if (sample) setLine('Sample emails I wrote', 'voice-sample.md');
  const ideas = lines(g('Idea bank')).map((l) => {
    const m = l.match(/^(★\s*)?(.*?)\s*\(([^)]+)\)\s*$/);
    const title = m ? m[2] : l;
    const type = m ? (LABEL_TO_TYPE[m[3].toLowerCase()] || 'story') : 'story';
    return `- [ ] ${today} · ${type} · ${title.replace(/ · /g, ', ')} · from: room${m && m[1] ? ' · starred' : ''}`;
  });
  return { brain: t, sample, ideas };
}

// "Week 2 Tue" -> a date in the month: week 1 is the week of the first Monday.
function weekDayToDate(send, month) {
  const m = /Week\s+(\d)\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)/i.exec(send || '');
  if (!m || !month) return '';
  const [y, mo] = month.split('-').map(Number);
  const first = new Date(Date.UTC(y, mo - 1, 1));
  const toMon = (8 - first.getUTCDay()) % 7; // days until the first Monday (0 if the 1st is a Monday)
  const idx = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'].indexOf(m[2].toLowerCase());
  const d = new Date(Date.UTC(y, mo - 1, 1 + toMon + (Number(m[1]) - 1) * 7 + idx));
  return d.toISOString().slice(0, 10);
}

const ANGLES = ['moment', 'label', 'problem'];
function q(s) { return JSON.stringify(String(s ?? '')); }

export function splitRoomEmails(text) {
  const t = text.replace(/\r\n?/g, '\n');
  const starts = [];
  const re = /^---\ntype:/gm;
  let m;
  while ((m = re.exec(t))) starts.push(m.index);
  return starts.map((s, i) => t.slice(s, i + 1 < starts.length ? starts[i + 1] : t.length).replace(/\n-{3}\s*$/, '').trim());
}

export function convertRoomEmail(chunk, month) {
  const { data, body } = splitFrontmatter(chunk + '\n');
  let b = body.replace(/^#\s+[^\n]*\n+/, ''); // the "# subject" heading the room adds
  const fills = [];
  b = b.replace(/\n?>\s*Fill in:\s*([^\n]*)\n?/g, (_, list) => { fills.push(...list.split(' · ').map((x) => x.trim()).filter(Boolean)); return '\n'; }).trim();
  const found = b.match(/\[[^\]\n]{1,80}\]/g) || [];
  for (const f of found) if (!fills.includes(f)) fills.push(f);
  const opts = (Array.isArray(data.subject_options) ? data.subject_options : []).map((o) => (typeof o === 'object' ? o.text : String(o)));
  const date = weekDayToDate(data.send, month);
  const type = String(data.type);
  const step = Number(data.sequence_step || 0);
  const fm = [
    '---',
    `type: ${type}`,
    `sequence_step: ${step}`,
    `name: ${q('From the Email Room · ' + (/^\s*\{\{\s*first_name\s*\}\}\s*$/.test(String(data.subject || '')) ? b.split('\n')[0].slice(0, 50) : (data.subject || type)))}`,
    `date: ${date}`,
    `status: ${date ? 'draft' : 'spare'}`,
    `subject: ${q(data.subject || opts[0] || '')}`,
    'subject_options:',
    ...opts.map((o, i) => `  - text: ${q(o)}\n    angle: ${ANGLES[i] || 'label'}`),
    'recommended_reason: "Chosen in the Email Room."',
    `preview_text: ${q(data.preview_text || '')}`,
    `cta: ${q(data.cta || '')}`,
    'side_idea: ""',
    fills.length ? 'fill_in:\n' + fills.map((f) => `  - ${q(f)}`).join('\n') : 'fill_in: []',
    data.rating != null && data.rating !== '' ? `rating_rounds:\n  - round: 1\n    overall: ${Number(data.rating)}\n    honesty: pass\n    source: room\n    scores: {}` : 'rating_rounds: []',
    '---',
  ].join('\n');
  const slug = TYPE_SLUG[type] + (type === 'event_invite' ? '-' + (step || 1) : '');
  return { file: date ? `${date}-${slug}.md` : `spare-${slug}.md`, text: `${fm}\n${b}\n` };
}

function main() {
  const brainFile = opt('brain');
  const emailsFile = opt('emails');
  let month = opt('month');
  if (!month) { const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + 1); month = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`; }
  fs.mkdirSync(emailDir, { recursive: true });

  if (brainFile) {
    const raw = fs.readFileSync(path.resolve(brainFile), 'utf8');
    const target = path.join(emailDir, 'EMAIL-BRAIN.md');
    let brainText = raw, sample = '', ideas = [];
    if (isRoomBrain(raw)) ({ brain: brainText, sample, ideas } = convertRoomBrain(raw));
    else summary.notes.push('The brain file is not in the Email Room format. Copied as it is.');
    const existing = fs.existsSync(target) ? fs.readFileSync(target, 'utf8') : '';
    const untouched = existing && /^name: ""$/m.test(existing) && !/\| [^|\s][^|]* \| .* \| (yes|no|ask) \|/.test(existing);
    if (!existing || untouched) { fs.writeFileSync(target, brainText); summary.created.push('EMAIL-BRAIN.md (from the Email Room)'); }
    else { writeNew(path.join(emailDir, 'EMAIL-BRAIN.imported.md'), brainText); summary.notes.push('EMAIL-BRAIN.md was already filled in. The room version is in EMAIL-BRAIN.imported.md: merge the two.'); }
    if (sample) writeNew(path.join(emailDir, 'voice-sample.md'), `# How I write (sample from the Email Room)\n\n${sample}\n`);
    if (ideas.length) {
      const f = path.join(emailDir, 'ideas.md');
      const cur = fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : '# Email ideas\n\n';
      const add = ideas.filter((l) => !cur.includes(l.split(' · ')[2]));
      if (add.length) { fs.writeFileSync(f, cur.replace(/\s*$/, '\n') + add.join('\n') + '\n'); summary.created.push(`ideas.md (+${add.length} ideas)`); }
    }
  }

  if (emailsFile) {
    const raw = fs.readFileSync(path.resolve(emailsFile), 'utf8');
    const chunks = splitRoomEmails(raw);
    const dir = path.join(emailDir, 'months', month);
    for (const c of chunks) {
      const { file, text } = convertRoomEmail(c, month);
      let f = path.join(dir, file);
      for (let n = 2; fs.existsSync(f); n++) f = path.join(dir, file.replace(/\.md$/, `-${n}.md`));
      writeNew(f, text);
    }
    summary.notes.push(`${chunks.length} email(s) from the room placed in months/${month}/. Check the dates against your calendar.`);
  }
  console.log(JSON.stringify(summary, null, 2));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
