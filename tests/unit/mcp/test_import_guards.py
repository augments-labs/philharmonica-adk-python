"""Subprocess regression tests for the optional-dependency import guards in
``philharmonica.adk.mcp.__init__`` and ``philharmonica.adk.tools.toolsets``.

The ``mcp`` extra pulls two distributions, not one: the ``mcp`` client itself
and ``httpx2``, which the streamable HTTP transport imports directly to build
the client it hands to the transport. A guard that swallows only
``ModuleNotFoundError(name="mcp")`` therefore re-raises when ``httpx2`` is the
missing piece, and ``import philharmonica.adk.mcp`` crashes instead of
degrading to the documented ``None`` bindings.

Each case runs in a fresh subprocess so a meta-path blocker installed before
import sees an interpreter with no cached ``philharmonica`` modules.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap


def _run_blocked_import(block_name: str, body: str) -> subprocess.CompletedProcess[str]:
    """Run ``body`` with ``block_name`` masked as an uninstalled distribution."""
    script = textwrap.dedent(
        f"""
        import importlib.abc
        import sys

        BLOCK = {block_name!r}

        class _Blocker(importlib.abc.MetaPathFinder):
            def find_spec(self, name, path=None, target=None):
                if name == BLOCK or name.startswith(BLOCK + "."):
                    raise ModuleNotFoundError("No module named " + repr(name), name=BLOCK)
                return None

        sys.meta_path.insert(0, _Blocker())
        for cached in list(sys.modules):
            if cached == BLOCK or cached.startswith(BLOCK + "."):
                del sys.modules[cached]

        {textwrap.indent(textwrap.dedent(body), " " * 8).lstrip()}
        print("IMPORT_OK")
        """
    )
    return subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)


_MCP_BODY = """
from philharmonica.adk.mcp import (
    MCPServerSse,
    MCPServerStdio,
    MCPServerStreamableHttp,
    MCPServerStreamableHttpParams,
)

assert MCPServerStreamableHttp is None, "MCPServerStreamableHttp must degrade to None"
assert MCPServerStreamableHttpParams is None, "MCPServerStreamableHttpParams must degrade to None"
assert MCPServerStdio is None, "MCPServerStdio must degrade to None"
assert MCPServerSse is None, "MCPServerSse must degrade to None"
"""

# ``mcp_toolset`` defers its client imports, so ``MCPToolset`` stays importable
# with either distribution absent and the toolsets guard never fires. These
# cases pin that: the package must import cleanly rather than degrade.
_TOOLSETS_BODY = """
from philharmonica.adk.tools.toolsets import FunctionToolset, MCPToolset

assert FunctionToolset is not None, "the non-optional toolsets must remain importable"
assert MCPToolset is not None, "MCPToolset defers its client imports and stays importable"
"""


def test_mcp_import_survives_missing_httpx2() -> None:
    # THE regression: the mcp client is installed but httpx2 is not, so the
    # first failure carries name="httpx2" rather than name="mcp".
    result = _run_blocked_import("httpx2", _MCP_BODY)
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert "IMPORT_OK" in result.stdout


def test_mcp_import_survives_missing_mcp() -> None:
    # The originally covered case: name == "mcp" stays swallowed.
    result = _run_blocked_import("mcp", _MCP_BODY)
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert "IMPORT_OK" in result.stdout


def test_toolsets_import_survives_missing_httpx2() -> None:
    # The toolsets guard reaches philharmonica.adk.mcp through mcp_toolset, so if
    # that ever stops deferring its imports it inherits this same failure.
    result = _run_blocked_import("httpx2", _TOOLSETS_BODY)
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert "IMPORT_OK" in result.stdout


def test_toolsets_import_survives_missing_mcp() -> None:
    result = _run_blocked_import("mcp", _TOOLSETS_BODY)
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert "IMPORT_OK" in result.stdout
