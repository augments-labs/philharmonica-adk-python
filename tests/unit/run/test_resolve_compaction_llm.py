"""Tests for ``resolve_compaction_llm`` in ``run/llm_calls.py``."""

from __future__ import annotations

from collections.abc import AsyncIterator

from philharmonica.adk.agents import Agent
from philharmonica.adk.llms.llm import LLM
from philharmonica.adk.llms.llm_config import LLMConfig
from philharmonica.adk.run.config import RunConfig
from philharmonica.adk.run.llm_calls import resolve_compaction_llm, resolve_llm
from philharmonica.adk.schemas import AgentOutputSchemaBase
from philharmonica.adk.tools import Tool
from philharmonica.adk.types.input import LLMInputContentItem
from philharmonica.adk.types.responses.llm_response import (
    LLMResponse,
    LLMResponseText,
    LLMStreamEvent,
)


class _StubLLM(LLM):
    """Identifiable test stub — distinct instances for override testing."""

    def __init__(self, label: str) -> None:
        self.label = label

    # ``LLM.acomplete`` is ``@overload``-typed on ``stream`` — a concrete
    # stub cannot match both overloads simultaneously.
    async def acomplete(  # type: ignore[override]
        self,
        messages: str | list[LLMInputContentItem],
        llm_config: LLMConfig | None = None,
        tools: list[Tool] | None = None,
        output_schema: AgentOutputSchemaBase | None = None,
        stream: bool = False,
    ) -> LLMResponse | AsyncIterator[LLMStreamEvent]:
        return LLMResponse(
            response_id="stub",
            model=self.label,
            response=[LLMResponseText(text=self.label)],
        )


def test_compaction_llm_override_wins_over_agent_llm():
    """RunConfig.compaction_llm takes precedence over the agent's LLM."""
    agent_llm = _StubLLM(label="agent")
    override_llm = _StubLLM(label="override")
    agent = Agent(name="A", system_prompt="t", llm=agent_llm)
    config = RunConfig(compaction_llm=override_llm)

    resolved = resolve_compaction_llm(agent, config)

    assert resolved is override_llm
    assert resolve_llm(agent, config) is agent_llm  # Sanity: main turn unaffected


def test_compaction_llm_falls_back_to_agent_llm_when_none():
    """With no override, resolve_compaction_llm returns the agent's LLM."""
    agent_llm = _StubLLM(label="agent")
    agent = Agent(name="A", system_prompt="t", llm=agent_llm)
    config = RunConfig()  # compaction_llm defaults to None

    resolved = resolve_compaction_llm(agent, config)

    assert resolved is agent_llm


def test_compaction_llm_falls_back_to_default_when_agent_has_no_llm():
    """When agent has no LLM, resolve_compaction_llm falls back to the default."""
    agent = Agent(name="A", system_prompt="t")  # No llm set
    config = RunConfig(model="gpt-4o-mini")

    resolved = resolve_compaction_llm(agent, config)

    # Same instance as resolve_llm would return.
    assert resolved is resolve_llm(agent, config)
