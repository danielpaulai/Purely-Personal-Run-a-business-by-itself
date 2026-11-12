"""Post-deploy check:  python -m pp_mcp.smoke https://your-deployment.vercel.app

Connects exactly like Claude does, passes a made-up participant's documents, and checks every answer is built
from THAT participant and nothing else. Stores nothing on the server, so there is nothing to clean up.
Exit code 0 = healthy.
"""
from __future__ import annotations

import asyncio
import re
import sys

DOCS = {
    "brain": "# BUSINESS BRAIN: Smoke Test\n\n## 1. WHO I AM\nSmoke Tester. I sell lighthouse inspections to harbour authorities.\n\n## 6. NEVER DO THIS\n- journey\n- harbourwash\n- Never claim I guarantee a result.\n",
    "icp": "# ICP\n\n## 4. THEIR WORDS\n- \"the beam keeps failing on Tuesdays\"\n- \"nobody has climbed it since 2019\"\n",
    "voice_dna": "# VOICE DNA\n\n### a) MY WORD BANK\n- lamp room\n- salt crust\n- proper climb\n",
}
LEAK = re.compile(r"daniel|danny|danielpaul|solo founders|purelypersonal\.ai", re.I)


async def run(base: str) -> int:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    url = base.rstrip("/")
    url = url if url.endswith("/mcp") else url + "/mcp"
    ok = True

    def check(name: str, cond: bool, detail: str = ""):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{('  ' + detail[:160]) if detail and not cond else ''}")

    async def call(s, tool, args):
        return (await s.call_tool(tool, args)).content[0].text

    print(f"Smoke testing {url}")
    async with streamablehttp_client(url) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name for t in (await s.list_tools()).tools}
            check("35+ tools listed", len(tools) >= 35, str(len(tools)))
            check("original tool names kept", {"write_post", "score_post", "get_icp", "find_prospects", "polish_post"} <= tools)
            check("no token / storage tools exist", not ({"set_my_context", "get_my_context", "clear_my_context"} & tools))
            blank = await call(s, "write_post", {"topic": "x"})
            check("no documents => asks for them, no default voice", "I need YOUR documents" in blank and not LEAK.search(blank), blank)
            order = await call(s, "write_post", {"topic": "Tuesday beam failures", **DOCS})
            check("work order is built from this participant", "lamp room" in order and "harbourwash" in order and "the beam keeps failing" in order, order)
            check("work order carries the skill method", "SKILL METHOD" in order and "OUTPUT CONTRACT" in order)
            check("nothing of anyone else leaks into the order", not LEAK.search(order), LEAK.search(order).group(0) if LEAK.search(order) else "")
            icp = await call(s, "get_icp", DOCS)
            check("get_icp reads back THEIR icp", "the beam keeps failing" in icp and not LEAK.search(icp), icp)
            sc = await call(s, "score_post", {"text": "We leverage a harbourwash.", **DOCS})
            check("score_post applies their banned list", "harbourwash" in sc and "0/4" in sc, sc)
            hist = await call(s, "get_my_post_history", {})
            check("hosted connector stores nothing (says so)", "Nothing is stored" in hist, hist)
    print("HEALTHY" if ok else "UNHEALTHY")
    return 0 if ok else 1


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python -m pp_mcp.smoke https://your-deployment.vercel.app")
    sys.exit(asyncio.run(run(sys.argv[1])))


if __name__ == "__main__":
    main()
