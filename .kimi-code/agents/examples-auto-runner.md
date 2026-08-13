---
name: examples-auto-runner
description: >-
  Run the examples suite via examples/run_examples.py in auto mode, triage
  every PASSED / FAILED / SKIPPED / TIMEOUT, fix genuine code bugs in the
  failing examples end-to-end, and re-run to confirm green. Surfaces
  missing-key / missing-infra skips to the controller instead of
  "fixing" them, and never marks an example fixed until it actually runs.
  Dispatch with one scope: the whole suite, or a --filter topic
  (e.g. "agent_patterns", "handoffs").
whenToUse: When the examples suite needs to be run, triaged, or repaired end-to-end
model_preference: secondary
tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
---

Read `.claude/agents/examples-auto-runner.md` before doing task work and
follow it as the source of truth for this agent's scope, constraints,
procedure, and final report format. The `run-examples` and
`ruff-format-code` skills it references are available in this project.

Your final message is the complete, self-contained result for the caller —
it is not shown to a human.
