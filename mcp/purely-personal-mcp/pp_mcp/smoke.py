"""Post-deploy check:  python -m pp_mcp.smoke https://your-deployment.vercel.app

Connects exactly like Claude does, saves a throwaway profile, checks that the work order is locked to
that profile (not anyone else's), then deletes it. Exit code 0 = healthy.
"""
from __future__ import annotations

import asyncio
import re
import sys

SAMPLE = {
    "brain": "# BUSINESS BRAIN: Smoke Test\n\n## 1. WHO I AM\nSmoke Tester. I sell lighthouse inspections to harbour authorities.\n\n## 6. NEVER DO THIS\n- journey\n- harbourwash\n",
    "icp": "# ICP\n\n## 4. THEIR WORDS\n- \"the beam keeps failing on Tuesdays\"\n- \"nobody has climbed it since 2019\"\n",
    "voice_dna": "# VOICE DNA\n\n### a) MY WORD BANK\n- lamp room\n- salt crust\n- proper climb\n",
}


async def run(base: str) -> int:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    url = base.rstrip("/")
    url = url if url.endswith("/mcp") else url + "/mcp"
    ok = True

    def check(name: str, cond: bool, detail: str = ""):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{('  ' + detail) if detail and not cond else ''}")

    print(f"Smoke testing {url}")
    async with streamablehttp_client(url) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name for t in (await s.list_tools()).tools}
            check("40+ tools listed", len(tools) >= 40, str(len(tools)))
            check("original 29 tool names kept", {"write_post", "score_post", "get_icp", "set_my_context", "find_prospects"} <= tools)
            blank = (await s.call_tool("write_post", {"topic": "x"})).content[0].text
            check("no token => setup message, never someone else's voice", "SETUP NEEDED" in blank and "Daniel" not in blank)
            saved = (await s.call_tool("set_my_context", SAMPLE)).content[0].text
            m = re.search(r"pp_\S+", saved)
            check("set_my_context returns a token", bool(m), saved[:120])
            if not m:
                return 1
            tok = m.group(0)
        async with streamablehttp_client(url) as (r, w, _):  # a fresh connection must still find it
            async with ClientSession(r, w) as s:
                await s.initialize()
                order = (await s.call_tool("write_post", {"topic": "Tuesday beam failures", "user_token": tok})).content[0].text
                check("new connection finds the saved profile (storage persists)", "lamp room" in order and "harbourwash" in order, order[:160])
                check("work order carries the skill method", "SKILL METHOD" in order and "OUTPUT CONTRACT" in order)
                icp = (await s.call_tool("get_icp", {"user_token": tok})).content[0].text
                check("get_icp returns THEIR icp", "the beam keeps failing" in icp and "solo founders" not in icp.lower())
                sc = (await s.call_tool("score_post", {"text": "We leverage a harbourwash.", "user_token": tok})).content[0].text
                check("score_post applies their banned list", "harbourwash" in sc and "0/4" in sc)
                gone = (await s.call_tool("clear_my_context", {"user_token": tok, "confirm": True})).content[0].text
                check("cleanup", "Cleared" in gone, gone)
    print("HEALTHY" if ok else "UNHEALTHY")
    return 0 if ok else 1


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python -m pp_mcp.smoke https://your-deployment.vercel.app")
    sys.exit(asyncio.run(run(sys.argv[1])))


if __name__ == "__main__":
    main()
