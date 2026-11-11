import asyncio
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
FIX = pathlib.Path(__file__).parent / "fixtures"

from pp_mcp.server import build_server  # noqa: E402
from pp_mcp.store import SQLiteStore  # noqa: E402


class Client:
    """In-process caller that goes through FastMCP's real argument validation."""

    def __init__(self, mcp):
        self.mcp = mcp

    def call(self, _tool, /, **args):
        res = asyncio.run(self.mcp.call_tool(_tool, args))
        content = res[0] if isinstance(res, tuple) else res
        return "".join(getattr(c, "text", "") for c in content)

    def tools(self):
        return asyncio.run(self.mcp.list_tools())


@pytest.fixture()
def store():
    return SQLiteStore(":memory:")


@pytest.fixture()
def client(store):
    return Client(build_server(store))


@pytest.fixture()
def docs():
    return {k: (FIX / f).read_text() for k, f in (("brain", "BUSINESS-BRAIN.md"), ("icp", "ICP.md"), ("voice_dna", "VOICE-DNA.md"))}


@pytest.fixture()
def token(client, docs):
    out = client.call("set_my_context", name="Maya Okafor", never_claim="Never guarantee results. Never name a client.", **docs)
    import re
    return re.search(r"pp_[A-Za-z0-9_\-]+", out).group(0)
