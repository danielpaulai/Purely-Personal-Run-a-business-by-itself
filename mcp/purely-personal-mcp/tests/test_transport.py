"""Real transports: streamable HTTP (uvicorn, lifespan off = serverless-like) and stdio."""
import asyncio
import json
import os
import re
import socket
import subprocess
import sys
import time

import httpx
import pytest

from conftest import FIX, ROOT


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


@pytest.fixture(scope="module")
def http_server(tmp_path_factory):
    port = _free_port()
    env = {**os.environ, "PP_DB_PATH": str(tmp_path_factory.mktemp("db") / "pp.db"), "PYTHONPATH": str(ROOT)}
    env.pop("SUPABASE_URL", None)
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "pp_mcp.server:app", "--port", str(port), "--lifespan", "off", "--log-level", "warning"],
                            cwd=ROOT, env=env)
    for _ in range(60):
        try:
            if httpx.get(f"http://127.0.0.1:{port}/health", timeout=1).status_code == 200:
                break
        except Exception:
            time.sleep(0.25)
    else:
        proc.kill()
        raise RuntimeError("server did not start")
    yield f"http://127.0.0.1:{port}"
    proc.terminate()
    proc.wait(5)


def test_health_and_404(http_server):
    h = httpx.get(http_server + "/health").json()
    assert h["name"] == "purely-personal-mcp" and h["tools"] >= 40 and h["mcp_endpoint"] == "/mcp"
    assert httpx.get(http_server + "/nope").status_code == 404


def test_remote_connector_end_to_end_over_http(http_server):
    """What Claude does when you add https://.../mcp as a custom connector."""
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    docs = {k: (FIX / f).read_text() for k, f in (("brain", "BUSINESS-BRAIN.md"), ("icp", "ICP.md"), ("voice_dna", "VOICE-DNA.md"))}

    async def run():
        async with streamablehttp_client(http_server + "/mcp") as (r, w, _):
            async with ClientSession(r, w) as s:
                await s.initialize()
                tools = {t.name for t in (await s.list_tools()).tools}
                assert len(tools) >= 40 and "write_post" in tools
                saved = (await s.call_tool("set_my_context", {"name": "Maya Okafor", **docs})).content[0].text
                tok = re.search(r"pp_\S+", saved).group(0)
                # a SECOND, independent request/session must still find the profile (serverless statelessness)
        async with streamablehttp_client(http_server + "/mcp") as (r, w, _):
            async with ClientSession(r, w) as s:
                await s.initialize()
                order = (await s.call_tool("write_post", {"topic": "Sunday dread", "user_token": tok})).content[0].text
                assert "WORK ORDER" in order and "flat white" in order and "Maya Okafor" in order
                score = (await s.call_tool("score_post", {"text": "Stop leveraging synergy.", "user_token": tok})).content[0].text
                assert "INVISIBILITY DIAGNOSTIC" in score
                prompts = {p.name for p in (await s.list_prompts()).prompts}
                assert "monday_content_drop" in prompts

    asyncio.run(run())


def test_stdio_transport():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run():
        params = StdioServerParameters(command=sys.executable, args=["-m", "pp_mcp"], cwd=str(ROOT),
                                       env={**os.environ, "PYTHONPATH": str(ROOT), "PP_DB_PATH": ":memory:"})
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                assert len((await s.list_tools()).tools) >= 40
                out = (await s.call_tool("get_setup_guide", {})).content[0].text
                assert "12 skills" in out

    asyncio.run(run())


def fake_postgrest():
    from pp_mcp.store import SupabaseStore

    tables = {"pp_profiles": {}, "pp_events": []}
    seen = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append((req.method, req.url.path, dict(req.url.params)))
        assert req.headers["apikey"] == "svc" and req.headers["authorization"] == "Bearer svc"
        t = req.url.path.rsplit("/", 1)[-1]
        q = dict(req.url.params)
        if t == "pp_profiles" and req.method == "POST":
            b = json.loads(req.content)
            tables["pp_profiles"][b["token_hash"]] = b["data"]
            return httpx.Response(201)
        if t == "pp_profiles" and req.method == "GET":
            h = q["token_hash"].removeprefix("eq.")
            return httpx.Response(200, json=[{"data": tables["pp_profiles"][h]}] if h in tables["pp_profiles"] else [])
        if t == "pp_profiles" and req.method == "DELETE":
            h = q["token_hash"].removeprefix("eq.")
            gone = tables["pp_profiles"].pop(h, None)
            return httpx.Response(200, json=[{"token_hash": h}] if gone is not None else [])
        if t == "pp_events" and req.method == "POST":
            tables["pp_events"].append(json.loads(req.content))
            return httpx.Response(201)
        if t == "pp_events" and req.method == "GET":
            h = q["token_hash"].removeprefix("eq.")
            rows = [e for e in tables["pp_events"] if e["token_hash"] == h and (not q.get("kind") or e["kind"] == q["kind"].removeprefix("eq."))]
            return httpx.Response(200, json=rows)
        if t == "pp_events" and req.method == "DELETE":
            h = q["token_hash"].removeprefix("eq.")
            tables["pp_events"] = [e for e in tables["pp_events"] if e["token_hash"] != h]
            return httpx.Response(204)
        return httpx.Response(400)

    return SupabaseStore("https://x.supabase.co", "svc", client=httpx.Client(transport=httpx.MockTransport(handler))), tables


def test_supabase_store_speaks_postgrest():
    """SupabaseStore against a fake PostgREST: proves queries, upsert, hashing and deletes."""
    from pp_mcp.store import new_token, token_hash

    st, tables = fake_postgrest()
    tok = new_token()
    assert st.get_profile(tok) is None
    st.put_profile(tok, {"name": "Maya"})
    assert st.get_profile(tok) == {"name": "Maya"}
    assert token_hash(tok) in tables["pp_profiles"] and tok not in json.dumps(tables)
    st.add_event(tok, "post", {"topic": "t"})
    assert st.events(tok, "post")[0]["topic"] == "t"
    assert st.delete_profile(tok) is True and st.get_profile(tok) is None and tables["pp_events"] == []
    assert st.delete_profile(tok) is False


def test_whole_server_runs_on_the_supabase_store():
    """Same product behaviour when the backing store is the remote one (how it runs on Vercel)."""
    from conftest import Client
    from pp_mcp.server import build_server

    st, tables = fake_postgrest()
    c = Client(build_server(st))
    docs = {k: (FIX / f).read_text() for k, f in (("brain", "BUSINESS-BRAIN.md"), ("icp", "ICP.md"), ("voice_dna", "VOICE-DNA.md"))}
    tok = re.search(r"pp_\S+", c.call("set_my_context", name="Maya Okafor", **docs)).group(0)
    assert "flat white" in c.call("write_post", topic="x", user_token=tok)
    c.call("log_published_post", user_token=tok, topic="Salary handcuffs", keyword="CUFFS")
    c.call("log_revenue_event", user_token=tok, amount=1500, post_ref="CUFFS")
    assert "1,500.00" in c.call("get_weekly_revenue_report", user_token=tok)
    assert "Salary handcuffs" in c.call("get_my_post_history", user_token=tok)
    assert tok not in json.dumps(tables)
    assert "Cleared" in c.call("clear_my_context", user_token=tok, confirm=True)
    assert not tables["pp_profiles"] and not tables["pp_events"]


def test_smoke_script_passes_against_a_running_server(http_server):
    from pp_mcp.smoke import run
    assert asyncio.run(run(http_server)) == 0
