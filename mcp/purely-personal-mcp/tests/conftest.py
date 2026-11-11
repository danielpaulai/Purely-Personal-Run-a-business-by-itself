import asyncio
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
FIX = pathlib.Path(__file__).parent / "fixtures"

from pp_mcp.ledger import Ledger  # noqa: E402
from pp_mcp.server import build_server  # noqa: E402


def read_docs():
    return {k: (FIX / f).read_text() for k, f in (("brain", "BUSINESS-BRAIN.md"), ("icp", "ICP.md"), ("voice_dna", "VOICE-DNA.md"))}


class Client:
    """In-process caller that goes through FastMCP's real argument validation.
    With docs set it behaves like Claude does: it attaches the participant's documents to tools that take them."""

    def __init__(self, mcp, docs=None):
        self.mcp, self.docs = mcp, docs
        self._takes = {t.name: set(t.inputSchema.get("properties", {})) for t in asyncio.run(mcp.list_tools())}

    def call(self, _tool, /, **args):
        if self.docs and "brain" in self._takes.get(_tool, ()):
            args = {**self.docs, **args}
        res = asyncio.run(self.mcp.call_tool(_tool, args))
        content = res[0] if isinstance(res, tuple) else res
        return "".join(getattr(c, "text", "") for c in content)

    def tools(self):
        return asyncio.run(self.mcp.list_tools())


@pytest.fixture()
def docs():
    return read_docs()


@pytest.fixture()
def client():
    """Hosted shape: no documents attached, no ledger."""
    return Client(build_server())


@pytest.fixture()
def maya(tmp_path):
    """Hosted shape plus Maya's documents attached to every call."""
    return Client(build_server(), read_docs())


@pytest.fixture()
def local(tmp_path):
    """Local install shape: documents in a folder, private ledger."""
    home = tmp_path / "pp"
    home.mkdir()
    for f, n in (("BUSINESS-BRAIN.md", "BUSINESS-BRAIN.md"), ("ICP.md", "ICP.md"), ("VOICE-DNA.md", "VOICE-DNA.md")):
        (home / n).write_text((FIX / f).read_text())
    return Client(build_server(local_dir=home, ledger=Ledger(home / "ledger.jsonl"))), home
