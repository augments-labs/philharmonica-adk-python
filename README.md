# Philharmonica Agent Development Kit (ADK)

**Where language becomes action.**

[![CI](https://github.com/augments-labs/philharmonica-adk-python/actions/workflows/ci.yml/badge.svg)](https://github.com/augments-labs/philharmonica-adk-python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/augments-labs/philharmonica-adk-python/branch/main/graph/badge.svg)](https://codecov.io/gh/augments-labs/philharmonica-adk-python)

A lightweight, provider-agnostic Python framework for orchestrating complex
systems of agents that perform real-world actions, across 100+ LLMs via litellm.

> [!NOTE]
> The JavaScript/TypeScript version of this ADK will be released soon. Stay tuned!

## The concept

An agent is a model that stopped talking and started doing: it calls tools,
changes state, and leaves side effects in the world. One agent is useful. A
set of specialists that cannot coordinate is a liability.

A philharmonic is not a crowd of capable musicians. It is a score, sections
that know their part, and a conductor holding the tempo. This ADK gives you
the same three things for agents:

- **The score** — explicit orchestration. Graphs for state machines, flows
  for pipelines, swarms for open-ended exploration, handoffs for delegation.
  You write the structure; nothing is inferred behind your back.
- **The sections** — agents scoped to one job, each carrying its own tools,
  guardrails, and budget. An `Agent` is configuration, never a hidden runtime.
- **The conductor** — the `Runner`. Every run travels one execution path,
  where turns, retries, token budgets, and interrupts are *enforced* rather
  than suggested.

The framework never injects a prompt, a tool, or a token you did not ask for,
and every cost-bearing default starts bounded. Decisions, tool I/O, and token
spend come back as structured traces, so what the ensemble actually did is
readable after the fact.

## Design tenets

1. **Explicit over magical.** If you can't step through it in a debugger, it
   doesn't belong in the orchestration path.
2. **One obvious way.** Fewer knobs, sharper edges — the ADK has opinions.
3. **Everything is inspectable.** Decisions, tool I/O, and token costs are
   structured traces, not anecdotes.
4. **Benchmarks or it didn't happen.** Claims ship with eval evidence or not
   at all — including this framework's own.

## Status

- **Today (v0.1.0 groundwork):** agents, `Runner` (sync/async/streaming),
  swarms, graphs, flows, task pipelines, tools, handoffs, guardrails, memory
  and sessions, MCP, A2A, sandboxed code execution, durable execution
  (Temporal/Restate), OpenTelemetry tracing, deploy targets, and a strict
  JSON/YAML config layer — all in this repository, MIT licensed.
- **Next:** `philharmonica-evals-python` (benchmarks vs. other frameworks) and
  `philharmonica-cookbook-python` (production-grade examples) — build with the ADK,
  prove it with the evals, learn it from the cookbook.

## Installation

### Use it in your own project

```bash
uv add philharmonica-adk          # or: pip install philharmonica-adk
```

The core install is deliberately lean — `litellm`, `pydantic`, `griffe`, `aiosqlite`, `typing-extensions` — and every optional provider / exporter / UI enhancement is gated behind its own extra:

```bash
pip install 'philharmonica-adk[anthropic]'   # native Anthropic SDK path
pip install 'philharmonica-adk[otel]'        # OpenTelemetry tracing bridge
pip install 'philharmonica-adk[mcp]'         # Model Context Protocol client
pip install 'philharmonica-adk[viz]'         # Agent graph visualization (graphviz)
pip install 'philharmonica-adk[verbose]'     # Rich-backed panel/line verbose renderer (ANSI fallback without it)
pip install 'philharmonica-adk[all]'         # all of the above
```

### Work on the ADK itself

Prerequisites: Python 3.12+ and [uv](https://docs.astral.sh/uv/) (uv installs the interpreter itself if you don't have it).

```bash
# 1. Clone the repository
git clone https://github.com/augments-labs/philharmonica-adk-python.git
cd philharmonica-adk-python

# 2. Build .venv from the committed lockfile — everything + test + lint + typecheck
uv sync --extra dev

# 3. Run anything inside it
uv run philharmonica --help
uv run pytest
```

`uv sync` resolves from `uv.lock`, so every contributor and every CI job installs byte-identical versions. Activate the environment directly (`source .venv/bin/activate`) if you would rather not prefix commands with `uv run`, and swap `--extra dev` for any other extra (`--extra anthropic`, `--extra all`, or none at all) to work against a leaner surface.

Conda works too, if you prefer it:

```bash
conda env create -f environment.yaml   # also runs `pip install -e '.[dev]'`
conda activate philharmonica-adk-python
```

Either way the install is editable: `philharmonica.adk` is importable from the `src/` layout defined in `pyproject.toml`, and source changes take effect immediately without reinstalling.

### API Keys

Set the API keys for the LLM providers you want to use:

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
```

### Verify Installation

```bash
python -c "from philharmonica.adk import Agent, Runner; print('OK')"
```

## Quick Start

```python
import asyncio
import logging

from philharmonica.adk import Agent, Runner

logger = logging.getLogger(__name__)

agent = Agent(
    name="Assistant",
    system_prompt="You are a helpful assistant.",
)

result = asyncio.run(Runner.arun(agent, "Hello!"))
logger.info(result.final_output)
```

## Command-Line Interface

The `philharmonica` console script drives agents from the terminal — scaffold a
project, validate its config without spending a token, then run or chat:

```bash
philharmonica new my_agent                       # scaffold config + tools + schema
philharmonica validate my_agent/agent.json       # strict schema check, no tokens
philharmonica run my_agent/agent.json "hello"    # one-shot run (config or --agent module:var)
philharmonica chat my_agent/agent.json           # interactive REPL, optional --session-db
philharmonica serve my_agent/agent.json                    # REST + health over HTTP ([serve] extra)
```

`run` auto-dispatches agents, swarms, graphs, and topologies; every
cost-affecting behavior (sessions, verbose rendering, tracing, env
files) stays off until you pass its flag. See `docs/cli/cli.md` for the
full command reference.

## Deployment

Serve an agent over HTTP, then ship the container to any cloud. The
framework imports no server runtime and no cloud SDK — every piece is
opt-in, and you keep control of the runtime.

```bash
pip install 'philharmonica-adk[serve]'

# Serve locally: REST (POST /run, POST /run_sse) + health (/healthz, /readyz).
philharmonica serve --agent my_agent.app:agent --host 0.0.0.0 --port 8000

# Generate the deployment artifacts you own (Dockerfile + manifests):
philharmonica deploy init --target k8s --agent my_agent.app:agent --image my-agent:latest

# Or build and ship to a target via your installed CLIs:
philharmonica deploy build      --agent my_agent.app:agent --image my-agent:latest --push
philharmonica deploy cloud-run  --agent my_agent.app:agent --image gcr.io/PROJECT/my-agent --project PROJECT --region REGION
philharmonica deploy gke        --agent my_agent.app:agent --image IMAGE --project P --region R --cluster C
philharmonica deploy ecs        --agent my_agent.app:agent --image ACCT.dkr.ecr.R.amazonaws.com/my-agent --region R --execution-role-arn ARN
```

`philharmonica deploy` targets `docker`, `k8s`, `gke`, `helm`, `cloudrun`,
`ecs`, `app-runner`, and `lambda`. The generated image satisfies the
universal container contract (binds `0.0.0.0:$PORT`, config from env,
non-root, `/healthz` + `/readyz` probes), so the same image runs
everywhere. Because the package is private, the generated
`requirements.txt` must make `philharmonica-adk` installable in your image
(private index, vendored wheel, or VCS URL).

A single replica works out of the box on the default per-pod SQLite
stores. For multi-replica (horizontally-scaled) deployments, back A2A
tasks and REST sessions with Postgres so state is shared across pods —
`philharmonica serve --task-dsn "$PG_DSN" --session-dsn "$PG_DSN"` (install
`philharmonica-adk[a2a-postgres,session-postgres]`). The AWS deploy commands
also accept `--push` to log in to ECR and build/push the image for you.
See [`docs/deploy/`](docs/deploy/) for the full guide.

## Running Examples

All examples are runnable from the project root:

```bash
python examples/agent_patterns/agents_as_tools.py
python examples/handoffs/llm_orchestrated.py
python examples/tools/tool_guardrails.py
```

## Core Concepts

- [**Agents**](docs/agents/) — Autonomous entities with tools, guardrails, and handoffs
- [**Tools**](docs/tools/) — Function wrappers with schema validation and guardrails
- [**Handoffs**](docs/handoffs/) — Agent-to-agent routing (LLM-orchestrated or code-orchestrated)
- [**Guardrails**](docs/guardrails/) — Pre/post execution validation at agent and tool level
- [**Memory**](docs/memory/) — Persistent knowledge across sessions
- [**Skills**](docs/skills/) — Reusable capability packages (instructions + tools + governance)
- [**Tracing**](docs/tracing/) — OpenTelemetry observability

## Project Structure

```
src/philharmonica/adk/       # Source code (namespace package)
tests/                 # Unit and integration tests
examples/              # Single-file runnable examples (one concept each)
docs/                  # Usage documentation
configs/               # Logging and other configs
```

## Key Dependencies

**Core**: `litellm` | `pydantic` | `griffe` | `aiosqlite` | `typing-extensions`
**Optional extras**: `anthropic` (`.[anthropic]`) | `mcp` (`.[mcp]`) | `opentelemetry-*` (`.[otel]`) | `graphviz` (`.[viz]`) | `rich` (`.[verbose]`)

## Acknowledgements

This ADK draws on prior art and ongoing work from across the
multi-agent ecosystem:

- [**LangGraph**](https://github.com/langchain-ai/langgraph) —
  state-machine multi-agent orchestration; influence on the
  `graphs/` subsystem.
- [**CrewAI**](https://github.com/crewAIInc/crewAI) — multi-agent
  collaboration patterns.
- [**OpenAI Swarm**](https://github.com/openai/swarm) — swarm cycle
  pattern (reference shape for `swarms/`).
- [**OpenAI Agents SDK**](https://github.com/openai/openai-agents-python) —
  Runner design and handoff mechanism reference.
- [**Anthropic Claude Agent SDK**](https://github.com/anthropics/anthropic-quickstarts) —
  Anthropic-native provider design.
- [**LiteLLM**](https://github.com/BerriAI/litellm) — provider-agnostic
  LLM abstraction over 100+ models.
- [**Model Context Protocol**](https://modelcontextprotocol.io/) —
  tool-integration substrate.
- [**Pydantic**](https://docs.pydantic.dev/) — typed validation.
- [**Temporal**](https://temporal.io/) — durable execution backbone.
- [**OpenTelemetry**](https://opentelemetry.io/) and
  [**OpenInference**](https://github.com/Arize-ai/openinference) —
  observability conventions.

Inclusion here records influence, not endorsement.
