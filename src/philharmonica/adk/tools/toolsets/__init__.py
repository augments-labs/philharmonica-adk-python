"""Toolset composition module.

A ``Toolset`` is a live abstraction over a group of tools — it is
materialised each turn via ``await toolset.get_tools(ctx)``. The
abstraction lets agents organise large or multi-source tool
collections (MCP servers, sub-agent delegations, namespaced
domains) without name collisions or rigid construction-time
materialisation.

The full design rationale lives in
``src/philharmonica/adk/tools/toolsets/abstract.py``.

See ``docs/tools/toolsets.md`` for usage. See
``examples/tools/toolsets/`` for runnable examples.
"""

from typing import TYPE_CHECKING

from philharmonica.adk.tools.toolsets.abstract import Toolset, ToolsetFilter
from philharmonica.adk.tools.toolsets.combined import CombinedToolset
from philharmonica.adk.tools.toolsets.filtered import FilteredToolset
from philharmonica.adk.tools.toolsets.function_toolset import FunctionToolset
from philharmonica.adk.tools.toolsets.prefixed import PrefixedToolset
from philharmonica.adk.tools.toolsets.renamed import RenamedToolset
from philharmonica.adk.tools.toolsets.wrapper import WrapperToolset

if TYPE_CHECKING:
    from philharmonica.adk.tools.toolsets.mcp_toolset import MCPToolset
else:
    try:
        from philharmonica.adk.tools.toolsets.mcp_toolset import MCPToolset
    except ImportError as _exc:
        # Same gate as ``philharmonica.adk.mcp.__init__`` — degrade to ``None``
        # only when the mcp extra is missing, which shows up under either of
        # the two distributions it installs. Any other ImportError (typo,
        # transitive dep failure) surfaces.
        if getattr(_exc, "name", None) not in {"mcp", "httpx2"}:
            raise
        MCPToolset = None  # type: ignore[assignment,misc]


__all__ = [
    "CombinedToolset",
    "FilteredToolset",
    "FunctionToolset",
    "MCPToolset",
    "PrefixedToolset",
    "RenamedToolset",
    "Toolset",
    "ToolsetFilter",
    "WrapperToolset",
]
