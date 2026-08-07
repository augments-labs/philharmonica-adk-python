"""Visualisation emitters for :class:`Flow` and :class:`Graph` topologies.

Pure-function emitters producing Mermaid or Graphviz DOT diagram strings
from the frozen topology of a :class:`~philharmonica.adk.flows.flow.Flow` or
:class:`~philharmonica.adk.graphs.graph.Graph`. No side effects, no I/O —
callers print, paste, save, or embed the returned string themselves.

Public functions:

- :func:`flow_to_mermaid` — Mermaid ``flowchart`` from a Flow.
- :func:`flow_to_dot` — Graphviz DOT from a Flow.
- :func:`graph_to_mermaid` — Mermaid ``flowchart`` from a Graph.
- :func:`graph_to_dot` — Graphviz DOT from a Graph.
- :func:`render_dot` / :func:`render_mermaid` — turn the emitter
  strings into image files on disk via the optional ``viz`` /
  ``mermaid`` extras (graceful fallback to raw source on missing
  CLI / network).

The ergonomic instance methods :meth:`Flow.to_mermaid` /
:meth:`Flow.to_dot` / :meth:`Graph.to_mermaid` / :meth:`Graph.to_dot`
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
