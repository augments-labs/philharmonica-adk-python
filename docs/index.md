(landing)=

# Philharmonica ADK

A lightweight, provider-agnostic Python framework for multi-agent workflows
with 100+ LLMs via [LiteLLM](https://github.com/BerriAI/litellm).

::::{grid} 1 2 3 3
:gutter: 3
:class-container: sd-text-center

:::{grid-item-card} Foundations
:link: foundations/index
:link-type: doc

The mathematical limits that shape every decision in this ADK.
:::

:::{grid-item-card} Architecture
:link: architecture/index
:link-type: doc

Layer 1/2/3 types, Runner loop, LLM ABC, handoffs, swarms, graphs.
:::

:::{grid-item-card} Concepts
:link: concepts/index
:link-type: doc

Every concept and how it differs from its neighbours.
:::

:::{grid-item-card} Guides
:link: guides/index
:link-type: doc

Practical how-tos: agents, tools, memory, guardrails, tracing.
:::

:::{grid-item-card} Topics
:link: topics/index
:link-type: doc

Deep per-module reference: graphs, swarms, tools, llms, sandbox, and more.
:::

:::{grid-item-card} CLI
:link: cli/index
:link-type: doc

Run, chat, validate, scaffold, and serve agents from the terminal.
:::

:::{grid-item-card} Deployment
:link: deploy/index
:link-type: doc

Package, containerise, and ship agents to Kubernetes, Cloud Run, and AWS.
:::

:::{grid-item-card} References
:link: references/index
:link-type: doc

API reference, contributing, changelog, maintenance.
:::

::::

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
