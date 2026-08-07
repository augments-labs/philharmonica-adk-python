# API Reference

The public surface of the framework's core modules, grouped by theme.
Each page lists the exported symbols; their signatures and docstrings
are authoritative in the source. Usage walkthroughs live under
[Guides](../../guides/index.md) and the per-topic sections linked from
each page.

## Core

- **[`Agent`](agent.md)** — Configuration-only object. Name, instructions, tools, handoffs, guardrails.
- **[`Runner`](runner.md)** — Execution entry-points: `arun`, `arun_streamed`, `arun_graph`, `arun_swarm`.
- **[`LLM`](llm.md)** — Framework-owned LLM abstract base class.
- **[`FunctionTool`](tool.md)** — The Tool ABC + decorator + types.

## Orchestration

- **[Swarms](swarms.md)** — Iterative multi-agent collaboration with explicit termination and pluggable routing.
- **[Graphs](graphs.md)** — State-machine orchestration with checkpointing, interrupts, and streaming events.
- **[Flows](flows.md)** — Decorator-driven multi-step orchestration over typed shared state.
- **[Tasks](tasks.md)** — Declarative units of work composed into pipelines and groups.

## State and persistence

- **[Memory](memory.md)** — Extracted, searchable knowledge carried across sessions.
- **[Session](session.md)** — Conversation persistence for agent runs.

## Safety and protocols

- **[Guardrails](guardrails.md)** — Built-in PII, prompt-injection, and wrong-language guardrails.
- **[MCP](mcp.md)** — Model Context Protocol servers, lifecycle, and tool filters.
- **[A2A](a2a.md)** — Agent-to-Agent protocol client and server surfaces.

## Foundations

- **[Exceptions](exceptions.md)** — The framework exception hierarchy rooted at `PhilharmonicaError`.
- **[Types](types.md)** — Provider-agnostic wire and history types.
