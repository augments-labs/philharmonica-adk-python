# Philharmonica ADK

A provider-agnostic Python framework to orchestrate complex systems of agents
that perform real-world actions, across 100+ LLMs via
[LiteLLM](https://github.com/BerriAI/litellm).

- **[Foundations](foundations/index.md)** — The mathematical limits that shape every decision in this ADK.
- **[Architecture](architecture/index.md)** — Layer 1/2/3 types, Runner loop, LLM ABC, handoffs, swarms, graphs.
- **[Concepts](concepts/index.md)** — Every concept and how it differs from its neighbours.
- **[Guides](guides/index.md)** — Practical how-tos: agents, tools, memory, guardrails, tracing.
- **[Topics](topics/index.md)** — Deep per-module reference: graphs, swarms, tools, llms, sandbox, and more.
- **[CLI](cli/index.md)** — Run, chat, validate, scaffold, and serve agents from the terminal.
- **[Deployment](deploy/index.md)** — Package, containerise, and ship agents to Kubernetes, Cloud Run, and AWS.
- **[References](references/index.md)** — API reference, contributing, changelog, maintenance.

## Quickstart

```bash
uv add philharmonica-adk    # or: pip install philharmonica-adk

python -c "from philharmonica.adk import Agent, Runner; print('OK')"
```

Working on the ADK itself instead? Clone the repo and run `uv sync --extra dev`
(or `conda env create -f environment.yaml`) — see
[Contributing](contributing.md).

```python
import asyncio
import logging

from philharmonica.adk import Agent, Runner

logger = logging.getLogger(__name__)

agent = Agent(name="Assistant", system_prompt="You are a helpful assistant.")
result = asyncio.run(Runner.arun(agent, "Hello!"))
logger.info(result.final_output)
```

See [Guides → Agents](guides/agents.md) for the next step.
