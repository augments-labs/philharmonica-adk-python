# Philharmonica Agents ADK

Lightweight, provider-agnostic Python framework for multi-agent workflows
with 100+ LLMs via litellm.

> Terminology: this codebase is an **ADK** (Agent Development Kit), not an
> SDK. Use "ADK" in commits, docstrings, comments. Reserve "SDK" for third
> parties (OpenAI Agents SDK, Anthropic SDK).

## Governance

Architectural invariants live in `.claude/rules/architecture.md` (always
loaded). Detailed style/module rules are path-scoped siblings in
`.claude/rules/` and load only when you edit matching files (`*.py`,
`tests/`, `examples/`, `llms/`, etc.). Read `architecture.md` for the
non-negotiables; trust the path-scoped rules to surface when relevant.

Codex compatibility: every `CLAUDE.md` is symlinked as `AGENTS.md`, so edits
to either filename affect both agents. Codex does not natively interpret
Claude's path-scoped rule front matter; when working as Codex, read
`.claude/rules/architecture.md` plus any `.claude/rules/*.md` whose `paths`
match the files you will edit. Do not copy these instruction rules into
`.codex/rules/`, which is for command permission policy.

## Architecture Overview

```
src/philharmonica/adk/
├── agents/      # Agent, guardrails, handoffs
├── prompts/     # SystemPrompt, tone, dynamic prompts
├── run/         # Runner, config, context, streaming
├── tools/       # Tool system + guardrails
├── types/       # Source of truth for framework types
├── llms/        # LLM abstraction (LLM ABC, LiteLLM, Anthropic, OpenAI, Gemini)
├── handoffs/    # Agent handoff mechanisms
├── swarms/      # Iterative multi-agent collaboration (cycles)
├── graphs/      # State-machine multi-agent orchestration
├── context/     # Compaction, editing, token counting
├── session/     # Persistence (SQLite)
├── memory/      # Memory tools
├── mcp/         # Model Context Protocol
├── a2a/         # Agent-to-Agent
├── tracing/     # OpenTelemetry
├── hooks/       # Lifecycle callbacks
├── schemas/     # AgentOutputSchema
├── config/      # Declarative JSON agent config (load_agent, strict schema)
└── exceptions/  # Exception hierarchy
```

`Input → Input guardrails → Agent loop (LLM → tools → handoffs) → Output
guardrails → Final result`

Each module under `src/philharmonica/adk/` (and `examples/`, `tests/`)
carries its own `CLAUDE.md` with module-specific decisions.

## .claude/ layout

- `rules/` — architectural invariants (`architecture.md`, always loaded)
  plus path-scoped style/module rules that load on matching edits.
- `skills/` — `code-hygiene-gate` and the `add-*` procedures
  (`add-llm-provider`, `add-hosted-tool`, `add-run-item`).
- `agents/` — project subagents. Run `/list-capabilities` for the current,
  authoritative roster (don't rely on names hardcoded in prose).
- `commands/` — slash commands (e.g. `/list-capabilities`).
- `settings.local.json` — machine-local env, plugins, and permissions
  (gitignored; there is no shared `settings.json`).

## Codex layout

- `AGENTS.md` — symlinks to matching `CLAUDE.md` files.
- `.agents/skills/` — symlinks to `.claude/skills/` plus Codex-native
  wrappers for command-style prompts.
- `.codex/agents/` — Codex custom-agent wrappers that delegate to
  `.claude/agents/*.md` as the source of truth.

## Cost Optimization

Default values affecting token cost MUST be cost-conservative (see
`architecture.md`). Levers: `max_result_tokens`, `max_retries`,
JSON-minified tool results, `prompt_caching`, `CacheStrategy.STABLE`,
context compaction + editing, `HandoffConfig.budget` / `collapse`.

## Quick Start

```bash
uv sync --extra dev          # builds .venv from uv.lock (Python 3.12+)
uv run pytest                # run anything inside it
```

`uv.lock` is the single source of truth for versions — CI installs from it
with `UV_FROZEN=1`, so never hand-edit it; run `uv lock` after changing
`pyproject.toml` and commit both. Conda (`environment.yaml`) still works for
anyone who prefers it; `make` targets take `RUN=` to skip the `uv run` prefix.

Deps: `litellm`, `pydantic`, `mcp`, `temporalio`.

Hygiene gate (must be clean before work is "done"): run the
`code-hygiene-gate` skill — `ruff check`, `ruff format --check`, `mypy`,
`pyright`, and IDE diagnostics. Fix at source, not via suppression.
