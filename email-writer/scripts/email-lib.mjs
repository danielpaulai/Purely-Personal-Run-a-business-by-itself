// Shared helpers for the email-writer plugin. Node 18+, no dependencies.
// Reads the email file format in references/email-file-format.md.

import fs from 'node:fs';
import path from 'node:path';

export const TYPES = ['client_win', 'story', 'nine_word', 'how_to', 'event_invite', 'eight_minute_edit'];
export const TYPE_LABELS = {
  client_win: 'Client win',
  story: 'Story',
  nine_word: '9-word',
  how_to: 'How-to',
  event_invite: 'Event invite',
  eight_minute_edit: '8-minute email',
};
export const STATUSES = ['draft', 'ready', 'scheduled', 'sent', 'spare'];
export const ANGLES = ['moment', 'label', 'problem'];
export const PARTS = ['subject', 'preview', 'opening', 'one_idea', 'voice', 'shape', 'ask', 'phone'];

// ---------- tiny YAML subset parser (what email-file-format.md allows) ----------

function splitTopLevel(s, sep = ',') {
  const out = [];
  let depth = 0, quote = null, cur = '';
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (quote) {
      cur += c;
      if (c === '\\' && quote === '"') { cur += s[++i] ?? ''; continue; }
      if (c === quote) quote = null;
      continue;
    }
    if (c === '"' || c === "'") { quote = c; cur += c; continue; }
    if (c === '[' || c === '{') depth++;
    if (c === ']' || c === '}') depth--;
    if (c === sep && depth === 0) { out.push(cur); cur = ''; continue; }
    cur += c;
  }
  if (cur.trim() !== '') out.push(cur);
  return out;
}

export function parseScalar(raw) {
  const s = String(raw ?? '').trim();
  if (s === '') return '';
  if (s.startsWith('"')) {
    const end = s.lastIndexOf('"');
    const inner = end > 0 ? s.slice(0, end + 1) : s + '"';
    try { return JSON.parse(inner); } catch { return inner.slice(1, -1).replace(/\\"/g, '"'); }
  }
  if (s.startsWith("'")) {
    const end = s.lastIndexOf("'");
    return (end > 0 ? s.slice(1, end) : s.slice(1)).replace(/''/g, "'");
  }
  if (s.startsWith('[') && s.endsWith(']')) {
    const inner = s.slice(1, -1).trim();
    return inner === '' ? [] : splitTopLevel(inner).map(parseScalar);
  }
  if (s.startsWith('{') && s.endsWith('}')) {
    const obj = {};
    const inner = s.slice(1, -1).trim();
    if (inner === '') return obj;
    for (const part of splitTopLevel(inner)) {
      const m = part.match(/^\s*["']?([^"':]+)["']?\s*:\s*(.*)$/);
      if (m) obj[m[1].trim()] = parseScalar(m[2]);
    }
    return obj;
  }
  if (s === 'true') return true;
  if (s === 'false') return false;
  if (s === 'null' || s === '~') return null;
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
  return s;
}

const KEY_RE = /^([A-Za-z_][\w-]*)\s*:(?:\s+(.*)|\s*)$/;
const indentOf = (l) => l.match(/^ */)[0].length;
const isBlank = (l) => l.trim() === '' || l.trim().startsWith('#');

function nextContent(lines, i) {
  while (i < lines.length && isBlank(lines[i])) i++;
  return i;
}

function parseBlock(lines, i, indent) {
  i = nextContent(lines, i);
  if (i >= lines.length) return [null, i];
  if (lines[i].trim().startsWith('- ') || lines[i].trim() === '-') return parseSeq(lines, i, indent);
  return parseMap(lines, i, indent);
}

function parseMap(lines, i, indent) {
  const obj = {};
  while (true) {
    i = nextContent(lines, i);
    if (i >= lines.length) break;
    const ind = indentOf(lines[i]);
    if (ind < indent) break;
    if (ind > indent) { i++; continue; }
    const t = lines[i].trim();
    if (t.startsWith('- ')) break;
    const m = t.match(KEY_RE);
    if (!m) { i++; continue; }
    const key = m[1];
    const rest = m[2] ?? '';
    if (rest.trim() !== '') { obj[key] = parseScalar(rest); i++; continue; }
    const j = nextContent(lines, i + 1);
    if (j < lines.length) {
      const jind = indentOf(lines[j]);
      const jt = lines[j].trim();
      if (jind > indent || (jind === indent && (jt.startsWith('- ') || jt === '-'))) {
        const [val, ni] = parseBlock(lines, j, jind);
        obj[key] = val; i = ni; continue;
      }
    }
    obj[key] = ''; i++;
  }
  return [obj, i];
}

function parseSeq(lines, i, indent) {
  const arr = [];
  while (true) {
    i = nextContent(lines, i);
    if (i >= lines.length) break;
    const ind = indentOf(lines[i]);
    const t = lines[i].trim();
    if (ind !== indent || !(t.startsWith('- ') || t === '-')) break;
    const content = t === '-' ? '' : t.slice(2);
    if (content.trim() === '') {
      const [val, ni] = parseBlock(lines, i + 1, indent + 2);
      arr.push(val); i = ni; continue;
    }
    if (KEY_RE.test(content) && !/^["'[{]/.test(content)) {
      lines[i] = ' '.repeat(indent + 2) + content;
      const [val, ni] = parseMap(lines, i, indent + 2);
      arr.push(val); i = ni; continue;
    }
    arr.push(parseScalar(content)); i++;
  }
  return [arr, i];
}

export function parseYaml(text) {
  const lines = text.replace(/\t/g, '  ').split('\n');
  const [val] = parseMap(lines, 0, 0);
  return val || {};
}

export function splitFrontmatter(raw) {
  const text = raw.replace(/^﻿/, '').replace(/\r\n?/g, '\n');
  if (!text.startsWith('---\n')) return { data: {}, body: text.trim(), hasFrontmatter: false };
  const end = text.indexOf('\n---', 4);
  if (end === -1) return { data: {}, body: text.trim(), hasFrontmatter: false };
  const fm = text.slice(4, end);
  let rest = text.slice(end + 4);
  rest = rest.replace(/^[^\n]*\n?/, ''); // drop the rest of the closing --- line
  return { data: parseYaml(fm), body: rest.replace(/^\s*\n/, '').replace(/\s+$/, ''), hasFrontmatter: true };
}

// ---------- reading emails ----------

const SKIP_DIRS = new Set(['kit', 'previews', 'node_modules', '.git', '.obsidian', '.trash']);

export function listMarkdown(p, depth = 3) {
  const st = fs.statSync(p);
  if (st.isFile()) return [p];
  const out = [];
  for (const name of fs.readdirSync(p).sort()) {
    if (name.startsWith('.')) continue;
    const full = path.join(p, name);
    const s = fs.statSync(full);
    if (s.isDirectory()) { if (depth > 0 && !SKIP_DIRS.has(name)) out.push(...listMarkdown(full, depth - 1)); }
    else if (name.endsWith('.md') && !name.endsWith('.original.md')) out.push(full);
  }
  return out;
}

export function normaliseOptions(opts) {
  if (!Array.isArray(opts)) return [];
  return opts.map((o) => (typeof o === 'object' && o !== null)
    ? { text: String(o.text ?? ''), angle: String(o.angle ?? '') }
    : { text: String(o), angle: '' }).filter((o) => o.text);
}

export function readEmail(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const { data, body, hasFrontmatter } = splitFrontmatter(raw);
  if (!hasFrontmatter || !data.type) return null;
  const toList = (v) => (Array.isArray(v) ? v.map(String).filter(Boolean) : (v ? [String(v)] : []));
  return {
    file,
    type: String(data.type),
    sequence_step: Number(data.sequence_step || 0),
    name: String(data.name ?? ''),
    date: data.date ? String(data.date) : '',
    time: data.time ? String(data.time) : '',
    status: String(data.status || 'draft'),
    subject: String(data.subject ?? ''),
    subject_options: normaliseOptions(data.subject_options),
    recommended_reason: String(data.recommended_reason ?? ''),
    preview_text: String(data.preview_text ?? ''),
    cta: String(data.cta ?? ''),
    side_idea: String(data.side_idea ?? ''),
    fill_in: toList(data.fill_in),
    best_line: String(data.best_line ?? ''),
    rating_rounds: Array.isArray(data.rating_rounds) ? data.rating_rounds.filter((r) => r && typeof r === 'object') : [],
    idea: String(data.idea ?? ''),
    body,
  };
}

export function readEmails(p) {
  return listMarkdown(p).map(readEmail).filter(Boolean).sort((a, b) => {
    const sa = a.status === 'spare' || !a.date, sb = b.status === 'spare' || !b.date;
    if (sa !== sb) return sa ? 1 : -1;
    return (a.date + (a.time || '') + a.sequence_step).localeCompare(b.date + (b.time || '') + b.sequence_step);
  });
}

// ---------- the Email folder and EMAIL-BRAIN.md ----------

export function findEmailRoot(p) {
  let dir = fs.statSync(p).isDirectory() ? p : path.dirname(p);
  for (let k = 0; k < 6; k++) {
    if (fs.existsSync(path.join(dir, 'EMAIL-BRAIN.md'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

export function readBrain(root) {
  if (!root) return {};
  const f = path.join(root, 'EMAIL-BRAIN.md');
  if (!fs.existsSync(f)) return {};
  const raw = fs.readFileSync(f, 'utf8');
  const { data, body } = splitFrontmatter(raw);
  const grab = (label) => {
    const m = body.match(new RegExp('\\*\\*' + label + '[^*]*:\\*\\*[ \\t]*([^\\n]*)', 'i'));
    if (m && m[1].trim()) return m[1].trim();
    const sec = roomSection(body, label);
    return sec;
  };
  return {
    name: String(data.name || grab('First name') || grab('Name and sign-off') || ''),
    sender_name: String(data.sender_name || grab('Sender name') || data.name || ''),
    business: String(data.business || grab('Business name') || grab('Sender name') || ''),
    sender_email: String(data.sender_email || ''),
    platform: String(data.platform || grab('I send with') || grab('Where I send from') || ''),
    emails_per_week: data.emails_per_week || '',
    language: String(data.language || ''),
  };
}

// The Email Room's download uses "## Heading" sections with "(not filled in yet)" for empty ones.
export function roomSection(body, heading) {
  const re = new RegExp('^##\\s+' + heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[^\\n]*\\n([\\s\\S]*?)(?=^##\\s|(?![\\s\\S]))', 'mi');
  const m = String(body).match(re);
  if (!m) return '';
  const v = m[1].trim();
  return /^\(not filled in yet\)$/i.test(v) ? '' : v;
}

// ---------- merge fields ----------

export const MERGE_RE = /\{\{\s*first_name\s*\}\}/g;
export const MERGE_FIELDS = {
  gohighlevel: '{{contact.first_name}}',
  mailchimp: '*|FNAME|*',
  activecampaign: '%FIRSTNAME%',
  plain: '{{first_name}}',
};
export function convertMerge(text, platform) {
  const field = MERGE_FIELDS[platform] ?? MERGE_FIELDS.plain;
  return String(text).replace(MERGE_RE, () => field);
}

// Count characters the way a reader sees them: a first name is about 6 letters.
export function subjectLength(s) {
  return String(s).replace(MERGE_RE, 'xxxxxx').length;
}

// Measured on real phones (EmailToolTester, Aug 2026): Gmail Android shows 33, Gmail iPhone 37, Apple Mail iPhone 48.
// green: fits every phone. amber: cut off in the Gmail app. red: cut off on most phones.
export function subjectFit(n) {
  return n <= 33 ? 'green' : n <= 48 ? 'amber' : 'red';
}

// ---------- checks ----------

const BANNED = [
  'delve', 'game-changer', 'game changer', 'unlock', 'supercharge', 'leverage', 'seamless', 'seamlessly',
  'elevate', "in today's fast-paced world", "here's the thing", 'let that sink in', 'i hope this finds you well',
  "in today's email", 'i wanted to share',
];
const GURUS = ['taki', 'hormozi', 'dean jackson', 'blackbelt', 'black belt', 'lakajev'];
const PLACEHOLDER_RE = /\[[^\]\n]{1,80}\]/g;

const RANGES = {
  client_win: [120, 200], story: [200, 350], how_to: [280, 380], nine_word: [0, 25],
  'event_invite:1': [0, 40], 'event_invite:2': [150, 250], 'event_invite:3': [0, 30],
};

export function paragraphs(body) {
  return String(body).split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}
const isPS = (p) => /^P\.?\s?S\.?\b/i.test(p);
export function wordCount(body, { withPS = false } = {}) {
  const ps = paragraphs(body).filter((p) => withPS || !isPS(p));
  return ps.join(' ').replace(MERGE_RE, 'name').split(/\s+/).filter(Boolean).length;
}

export function ratingCheck(r) {
  const s = r.scores && typeof r.scores === 'object' ? r.scores : {};
  if (r.source === 'room' || !Object.keys(s).length) return { ok: true };
  const vals = PARTS.map((k) => Number(s[k])).filter((n) => !Number.isNaN(n));
  if (vals.length !== PARTS.length) return { ok: false, msg: `round ${r.round}: scores must have all eight parts (${PARTS.join(', ')})` };
  const min = Math.min(...vals);
  const others = [...vals]; others.splice(vals.indexOf(min), 1);
  let max = others.every((n) => n >= 9) ? Math.min(10, min + 1) : min;
  const h = String(r.honesty);
  if (h === 'fail' || h === 'fail-detail') max = Math.min(max, 4);
  if (h === 'fail-proof') max = Math.min(max, 2);
  const lo = Math.min(min, max);
  const o = Number(r.overall);
  if (o < lo || o > max) return { ok: false, msg: `round ${r.round}: overall ${o} does not match the rubric (should be ${lo === max ? lo : lo + ' or ' + max})` };
  return { ok: true };
}

export function checkEmail(e) {
  const out = [];
  const add = (level, msg) => out.push({ level, msg });
  if (!TYPES.includes(e.type)) add('error', `type "${e.type}" is not one of ${TYPES.join(', ')}`);
  if (!STATUSES.includes(e.status)) add('warn', `status "${e.status}" should be one of ${STATUSES.join(', ')}`);
  if (e.type === 'event_invite' && ![1, 2, 3].includes(e.sequence_step)) add('error', 'event_invite needs sequence_step 1, 2 or 3');
  if (!e.date && e.status !== 'spare') add('warn', 'no date: add the planned send day (YYYY-MM-DD)');
  if (e.date && !/^\d{4}-\d{2}-\d{2}$/.test(e.date)) add('error', `date "${e.date}" must be YYYY-MM-DD`);
  if (!e.subject) add('error', 'no subject');
  if (!e.preview_text) add('warn', 'no preview_text');
  if (!e.cta && e.type !== 'eight_minute_edit') add('warn', 'no cta: every email asks for one small thing');
  if (!e.body) add('error', 'the body is empty');

  const all = [e.subject, e.preview_text, e.body, ...e.subject_options.map((o) => o.text)].join('\n');
  if (/[\u2014\u2013]/.test(all)) add('error', 'em dash or en dash found: use a comma or a full stop');
  if (/\s-\s/.test(e.body)) add('warn', 'a " - " used as a dash: use a comma or a full stop');
  const low = all.toLowerCase();
  for (const w of BANNED) if (new RegExp('\\b' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(all)) add('error', `"${w}" is on the never-use list`);
  if (/\bjourney\b/i.test(all)) add('warn', '"journey" only if it is real travel');
  for (const g of GURUS) if (new RegExp('\\b' + g + '\\b', 'i').test(all)) add('error', `names a guru ("${g}"): remove it`);
  if (/!!/.test(all)) add('warn', 'double exclamation marks');

  // subjects
  const sl = subjectLength(e.subject);
  const fit = subjectFit(sl);
  if (fit === 'red') add('warn', `subject is ${sl} characters: cut off on most phones (over 48)`);
  else if (fit === 'amber') add('info', `subject is ${sl} characters: cut off in the Gmail app, so the first 33 characters must make sense alone`);
  if (/^(re|fwd?):/i.test(e.subject)) add('error', 'no fake "Re:" or "Fwd:"');
  const words = e.subject.replace(MERGE_RE, '').split(/\s+/).filter((w) => /^[A-Za-z]{4,}/.test(w));
  if (words.length >= 3 && words.every((w) => /^[A-Z]/.test(w))) add('warn', 'subject looks like Title Case: write it like a person, in sentence case');
  if (/\b[A-Z]{5,}\b/.test(e.subject.replace(MERGE_RE, ''))) add('warn', 'subject has a word in ALL CAPS');
  if (e.subject_options.length !== 3) add('warn', `${e.subject_options.length} subject options: write 3 (moment, label, problem)`);
  const angles = new Set(e.subject_options.map((o) => o.angle));
  if (e.subject_options.length === 3 && !ANGLES.every((a) => angles.has(a))) add('warn', 'subject options should cover the three angles: moment, label, problem');
  if (e.subject && e.subject_options.length && !e.subject_options.some((o) => o.text === e.subject)) add('warn', 'subject is not one of the subject_options');
  for (const o of e.subject_options) { const n = subjectLength(o.text); if (n > 48 && o.text !== e.subject) add('info', `option "${o.text}" is ${n} characters (over 48)`); }

  // preview text
  const pl = e.preview_text.length;
  if (e.preview_text && (pl < 40 || pl > 90)) add('warn', `preview_text is ${pl} characters: aim for 40 to 90`);
  if (e.preview_text && e.subject && e.preview_text.toLowerCase().startsWith(e.subject.toLowerCase())) add('warn', 'preview_text repeats the subject: continue the thought instead');

  // body shape
  const paras = paragraphs(e.body);
  const hasPS = paras.some(isPS);
  const key = e.type === 'event_invite' ? `event_invite:${e.sequence_step}` : e.type;
  const range = RANGES[key];
  const wc = wordCount(e.body, { withPS: e.type === 'nine_word' });
  if (range) {
    if (wc > range[1]) add('warn', `${wc} words: the recipe says ${range[0] ? range[0] + ' to ' : 'at most '}${range[1]}`);
    else if (wc < range[0]) add('warn', `${wc} words: the recipe says ${range[0]} to ${range[1]}`);
  }
  if (e.type === 'nine_word') {
    if (hasPS) add('error', 'the 9-word email has no PS');
    if (/https?:\/\//.test(e.body)) add('error', 'the 9-word email has no link: the reply is the ask');
  }
  if (['client_win', 'story', 'how_to'].includes(e.type) && !hasPS) add('info', 'no PS: add the Three Ways PS if EMAIL-BRAIN.md has your three offers');
  // A tip label line like "1. One Folder." is not a sentence.
  const sentences = (p) => (p.replace(/^\d+\.\s+[^\n]{1,50}\n/, '').replace(/\b\d+\.(?=\s)/g, '').match(/[.!?](\s|$)/g) || []).length;
  const long = paras.filter((p) => !isPS(p) && sentences(p) > 3);
  if (long.length) add('warn', `${long.length} paragraph(s) with more than 3 sentences: break them up for phones`);
  if (/(^|\n)#{1,6}\s|\*\*[^*]+\*\*/.test(e.body)) add('warn', 'markdown headings or bold in the body: emails are plain text');
  if (!/\{\{\s*first_name\s*\}\}/.test(e.body) && !['nine_word', 'eight_minute_edit'].includes(e.type) && !(e.type === 'event_invite' && e.sequence_step !== 2)) add('info', 'no {{first_name}} greeting');
  if (/\{\{(?!\s*first_name\s*\}\})[^}]*\}\}|\*\|[A-Z]+\|\*|%[A-Z]+%/.test(all)) add('error', 'use only {{first_name}} as the merge field; the preview converts it per platform');

  // placeholders vs fill_in
  const found = [...new Set((all.match(PLACEHOLDER_RE) || []))];
  const listed = e.fill_in.join(' | ');
  const missing = found.filter((p) => !listed.includes(p));
  if (missing.length) add('warn', `placeholders not in fill_in: ${missing.join(', ')}`);
  if (found.length) add('info', `${found.length} thing(s) to fill in before sending`);

  // rating rounds
  for (const r of e.rating_rounds) { const c = ratingCheck(r); if (!c.ok) add('warn', c.msg); }
  return out;
}

export function slugify(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'email';
}
