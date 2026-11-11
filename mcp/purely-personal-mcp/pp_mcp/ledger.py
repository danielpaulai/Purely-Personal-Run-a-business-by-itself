"""Optional local ledger for posts, DMs, calls and revenue.

Only used by the local (stdio) install, where one person owns the machine. The hosted connector never
writes anything: it has no way to know who is calling, so it keeps no data. Hosted callers pass their own
records (from Notion, a sheet, LinkedIn) to the report tools instead.
"""
from __future__ import annotations

import json
import time
from pathlib import Path


class Ledger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, kind: str, data: dict) -> None:
        with self.path.open("a") as f:
            f.write(json.dumps({"kind": kind, "ts": time.time(), **data}) + "\n")

    def read(self, kind: str | None = None, since: float | None = None) -> list[dict]:
        if not self.path.exists():
            return []
        rows = []
        for line in self.path.read_text().splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if (not kind or r.get("kind") == kind) and (not since or r.get("ts", 0) >= since):
                rows.append(r)
        return sorted(rows, key=lambda r: -r.get("ts", 0))
