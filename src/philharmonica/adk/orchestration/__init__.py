"""Orchestration primitives — cross-module composition seams.

This package hosts the abstractions that let different multi-agent
primitives compose with one another without any of them knowing about
the others. Concretely:

- ``Executable`` is the ABC that ``Agent``,
  ``Swarm``, and
  ``Graph`` all plug into via thin
  adapters. A ``Graph`` node can therefore host an ``Agent``, another
  ``Graph``, a ``Swarm``, or a plain ``Callable`` uniformly.

- ``NodeResult`` is the uniform return envelope every
  ``Executable`` produces. It carries the terminal output, the
  Layer 3 items generated, per-run usage, and arbitrary metadata.

The package deliberately holds no runtime loop logic. Drivers
(``run/swarm_loop.py``, ``run/graph_loop.py``) import these types and
orchestrate them; the primitives themselves import nothing from the
drivers.
"""

from __future__ import annotations

from philharmonica.adk.orchestration.executable import (
    Executable,
    ExecutableInput,
    NodeResult,
)

__all__ = [
    "Executable",
    "ExecutableInput",
    "NodeResult",
]
