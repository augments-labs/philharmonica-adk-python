"""Visualisation emitters for ``Flow`` and ``Graph`` topologies.

Pure-function emitters producing Mermaid or Graphviz DOT diagram strings
from the frozen topology of a ``Flow`` or
``Graph``. No side effects, no I/O —
callers print, paste, save, or embed the returned string themselves.

Public functions:

- ``flow_to_mermaid`` — Mermaid ``flowchart`` from a Flow.
- ``flow_to_dot`` — Graphviz DOT from a Flow.
- ``graph_to_mermaid`` — Mermaid ``flowchart`` from a Graph.
- ``graph_to_dot`` — Graphviz DOT from a Graph.
- ``render_dot`` / ``render_mermaid`` — turn the emitter
  strings into image files on disk via the optional ``viz`` /
  ``mermaid`` extras (graceful fallback to raw source on missing
  CLI / network).

The ergonomic instance methods ``Flow.to_mermaid`` /
``Flow.to_dot`` / ``Graph.to_mermaid`` / ``Graph.to_dot``
delegate to the emitter functions.
"""

from __future__ import annotations

from philharmonica.adk.visualization.dot import definition_to_dot, flow_to_dot, graph_to_dot
from philharmonica.adk.visualization.mermaid import definition_to_mermaid, flow_to_mermaid, graph_to_mermaid
from philharmonica.adk.visualization.render import RenderOutcome, render_dot, render_mermaid

__all__ = [
    "RenderOutcome",
    "definition_to_dot",
    "definition_to_mermaid",
    "flow_to_dot",
    "flow_to_mermaid",
    "graph_to_dot",
    "graph_to_mermaid",
    "render_dot",
    "render_mermaid",
]
