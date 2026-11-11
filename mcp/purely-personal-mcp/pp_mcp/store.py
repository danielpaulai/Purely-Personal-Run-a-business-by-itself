"""Persistence for profiles and event logs.

Two backends behind one interface:

* SQLiteStore   - default. Local/stdio use and any host with a persistent disk.
* SupabaseStore - for serverless hosting (Vercel), where disks are ephemeral.
                  Talks to PostgREST with the service-role key (server side only).

Tokens are never stored. Only sha256(token) is, so a database leak does not
hand out working tokens.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Protocol


def new_token() -> str:
    return "pp_" + secrets.token_urlsafe(18)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.strip().encode()).hexdigest()


def valid_token(token: str | None) -> bool:
    return bool(token) and token.strip().startswith("pp_") and 8 <= len(token.strip()) <= 80


class Store(Protocol):
    def get_profile(self, token: str) -> dict | None: ...
    def put_profile(self, token: str, data: dict) -> None: ...
    def delete_profile(self, token: str) -> bool: ...
    def add_event(self, token: str, kind: str, data: dict) -> None: ...
    def events(self, token: str, kind: str | None = None, since: float | None = None, limit: int = 500) -> list[dict]: ...


class SQLiteStore:
    def __init__(self, path: str | None = None):
        path = path or os.environ.get("PP_DB_PATH") or str(Path.home() / ".purely-personal" / "pp.db")
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock:
            self._db.executescript(
                """
                CREATE TABLE IF NOT EXISTS pp_profiles(
                    token_hash TEXT PRIMARY KEY, data TEXT NOT NULL, created REAL, updated REAL);
                CREATE TABLE IF NOT EXISTS pp_events(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, token_hash TEXT NOT NULL,
                    kind TEXT NOT NULL, data TEXT NOT NULL, ts REAL NOT NULL);
                CREATE INDEX IF NOT EXISTS pp_events_idx ON pp_events(token_hash, kind, ts);
                """
            )

    def get_profile(self, token: str) -> dict | None:
        with self._lock:
            r = self._db.execute("SELECT data FROM pp_profiles WHERE token_hash=?", (token_hash(token),)).fetchone()
        return json.loads(r[0]) if r else None

    def put_profile(self, token: str, data: dict) -> None:
        now = time.time()
        with self._lock:
            self._db.execute(
                "INSERT INTO pp_profiles(token_hash,data,created,updated) VALUES(?,?,?,?) "
                "ON CONFLICT(token_hash) DO UPDATE SET data=excluded.data, updated=excluded.updated",
                (token_hash(token), json.dumps(data), now, now),
            )
            self._db.commit()

    def delete_profile(self, token: str) -> bool:
        h = token_hash(token)
        with self._lock:
            n = self._db.execute("DELETE FROM pp_profiles WHERE token_hash=?", (h,)).rowcount
            self._db.execute("DELETE FROM pp_events WHERE token_hash=?", (h,))
            self._db.commit()
        return n > 0

    def add_event(self, token: str, kind: str, data: dict) -> None:
        with self._lock:
            self._db.execute(
                "INSERT INTO pp_events(token_hash,kind,data,ts) VALUES(?,?,?,?)",
                (token_hash(token), kind, json.dumps(data), time.time()),
            )
            self._db.commit()

    def events(self, token: str, kind: str | None = None, since: float | None = None, limit: int = 500) -> list[dict]:
        q, a = "SELECT kind,data,ts FROM pp_events WHERE token_hash=?", [token_hash(token)]
        if kind:
            q += " AND kind=?"; a.append(kind)
        if since:
            q += " AND ts>=?"; a.append(since)
        q += " ORDER BY ts DESC LIMIT ?"; a.append(limit)
        with self._lock:
            rows = self._db.execute(q, a).fetchall()
        return [{"kind": k, "ts": ts, **json.loads(d)} for k, d, ts in rows]


class SupabaseStore:
    """PostgREST client. Needs SUPABASE_URL and SUPABASE_SERVICE_KEY (see supabase/schema.sql)."""

    def __init__(self, url: str | None = None, key: str | None = None, client: Any = None):
        import httpx

        self.url = (url or os.environ["SUPABASE_URL"]).rstrip("/") + "/rest/v1"
        key = key or os.environ["SUPABASE_SERVICE_KEY"]
        self.h = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        self.c = client or httpx.Client(timeout=15)

    def _r(self, method: str, path: str, **kw):
        r = self.c.request(method, self.url + path, headers={**self.h, **kw.pop("headers", {})}, **kw)
        r.raise_for_status()
        return r

    def get_profile(self, token: str) -> dict | None:
        rows = self._r("GET", f"/pp_profiles?token_hash=eq.{token_hash(token)}&select=data").json()
        return rows[0]["data"] if rows else None

    def put_profile(self, token: str, data: dict) -> None:
        self._r("POST", "/pp_profiles?on_conflict=token_hash",
                headers={"Prefer": "resolution=merge-duplicates,return=minimal"},
                content=json.dumps({"token_hash": token_hash(token), "data": data, "updated": time.time()}))

    def delete_profile(self, token: str) -> bool:
        h = token_hash(token)
        self._r("DELETE", f"/pp_events?token_hash=eq.{h}")
        r = self._r("DELETE", f"/pp_profiles?token_hash=eq.{h}", headers={"Prefer": "return=representation"})
        return bool(r.json())

    def add_event(self, token: str, kind: str, data: dict) -> None:
        self._r("POST", "/pp_events", headers={"Prefer": "return=minimal"},
                content=json.dumps({"token_hash": token_hash(token), "kind": kind, "data": data, "ts": time.time()}))

    def events(self, token: str, kind: str | None = None, since: float | None = None, limit: int = 500) -> list[dict]:
        q = f"/pp_events?token_hash=eq.{token_hash(token)}&select=kind,data,ts&order=ts.desc&limit={limit}"
        if kind:
            q += f"&kind=eq.{kind}"
        if since:
            q += f"&ts=gte.{since}"
        return [{"kind": r["kind"], "ts": r["ts"], **r["data"]} for r in self._r("GET", q).json()]


def default_store() -> Store:
    if os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_KEY"):
        return SupabaseStore()
    return SQLiteStore()
