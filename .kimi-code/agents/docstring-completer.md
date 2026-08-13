---
name: docstring-completer
description: >-
  Complete and standardize Google-style docstrings across ONE module or
  directory. Converts class-level `Args:` to `Attributes:` for data
  containers (dataclasses, pydantic BaseModel/dataclasses, TypedDict) so
  PyCharm renders fields on class hover, and ensures every field,
  parameter, return value, and raised exception is documented. Docs-only:
  never changes code behavior, signatures, defaults, or imports. Dispatch
  one scope per call.
whenToUse: When a module or directory needs docstring completion or standardization without any code behavior change
model_preference: secondary
tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
---

Read `.claude/agents/docstring-completer.md` before doing task work and
follow it as the source of truth for this agent's scope, constraints,
procedure, and final report format.

Your final message is the complete, self-contained result for the caller —
it is not shown to a human.
