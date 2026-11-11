-- Purely Personal MCP storage. Run once in the Supabase SQL editor.
-- The MCP server uses the SERVICE ROLE key, which bypasses RLS. RLS is enabled
-- with no policies so the anon/authenticated keys can never read these tables.

create table if not exists public.pp_profiles (
  token_hash text primary key,          -- sha256(token); the token itself is never stored
  data       jsonb not null,            -- brain, icp, voice_dna, settings
  updated    double precision not null default extract(epoch from now())
);

create table if not exists public.pp_events (
  id         bigserial primary key,
  token_hash text not null,
  kind       text not null,             -- post | dm | call | revenue
  data       jsonb not null,
  ts         double precision not null
);

create index if not exists pp_events_lookup on public.pp_events (token_hash, kind, ts desc);

alter table public.pp_profiles enable row level security;
alter table public.pp_events   enable row level security;
