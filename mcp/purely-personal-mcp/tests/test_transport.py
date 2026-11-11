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
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
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
    assert h["name"] == "purely-personal-mcp" and h["tools"] >= 35 and h["mcp_endpoint"] == "/mcp" and h["stores_data"] is False
    assert httpx.get(http_server + "/nope").status_code == 404


def test_remote_connector_end_to_end_over_http(http_server):
    """What Claude does when you add https://.../mcp as a custom connector. Each connection is independent: no sessions, no storage."""
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    from conftest import read_docs
    docs = read_docs()

    async def run():
        async with streamablehttp_client(http_server + "/mcp") as (r, w, _):
            async with ClientSession(r, w) as s:
                await s.initialize()
                tools = {t.name for t in (await s.list_tools()).tools}
                assert len(tools) >= 35 and "write_post" in tools and "set_my_context" not in tools
                order = (await s.call_tool("write_post", {"topic": "Sunday dread", **docs})).content[0].text
                assert "WORK ORDER" in order and "flat white" in order and "Maya Okafor" in order
        async with streamablehttp_client(http_server + "/mcp") as (r, w, _):  # a brand-new connection, different person
            async with ClientSession(r, w) as s:
                await s.initialize()
                other = (await s.call_tool("get_icp", {"brain": "# B\n\n## THEIR WORDS\n- \"my hull is leaking\"\n- \"a\"\n- \"b\"\n"})).content[0].text
                assert "my hull is leaking" in other and "salary" not in other
                none = (await s.call_tool("write_post", {"topic": "x"})).content[0].text
                assert "I need YOUR documents" in none
                score = (await s.call_tool("score_post", {"text": "Stop leveraging synergy.", **docs})).content[0].text
                assert "INVISIBILITY DIAGNOSTIC" in score
                assert "monday_content_drop" in {p.name for p in (await s.list_prompts()).prompts}

    asyncio.run(run())


def test_stdio_transport():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run():
        params = StdioServerParameters(command=sys.executable, args=["-m", "pp_mcp"], cwd=str(ROOT),
                                       env={**os.environ, "PYTHONPATH": str(ROOT), "PP_HOME": os.environ.get("TMPDIR", "/tmp") + "/pp-stdio-test"})
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                assert len((await s.list_tools()).tools) >= 35
                out = (await s.call_tool("get_setup_guide", {})).content[0].text
                assert "12 skills" in out

    asyncio.run(run())


def test_smoke_script_passes_against_a_running_server(http_server):
    from pp_mcp.smoke import run
    assert asyncio.run(run(http_server)) == 0
