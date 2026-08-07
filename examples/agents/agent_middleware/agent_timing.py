"""Agent middleware — per-agent observability with a custom timing chain.

Demonstrates:

1. ``AgentLoggingMiddleware`` — the shipped baseline that logs the
   start and end of every per-agent block.
2. A custom ``TimingMiddleware`` that records cumulative wall-clock
   time per agent (per-block resets every handoff transition).
3. Multi-agent handoff — middleware re-fires per agent, so a
   3-agent flow shows the chain firing three times. ``RunHooks``
   would only frame the run once; middleware fills the per-agent gap.

The example uses a scripted stub LLM so it runs without any
provider API key.

Usage:
    python examples/agents/agent_middleware/agent_timing.py
"""

from __future__ import annotations

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import asyncio
import json
import logging
import time
from collections.abc import AsyncIterator
from typing import Any

from philharmonica.adk.agents.agent import Agent
from philharmonica.adk.agents.middleware import Middleware
from philharmonica.adk.llms.llm import LLM
from philharmonica.adk.llms.llm_config import LLMConfig
from philharmonica.adk.run.agent_middleware import (
    AgentBlockOutcome,
    AgentLoggingMiddleware,
    AgentMiddlewareNext,
)
from philharmonica.adk.run.config import RunConfig
from philharmonica.adk.run.context import RunContext
from philharmonica.adk.run.runner import Runner
from philharmonica.adk.schemas import AgentOutputSchemaBase
from philharmonica.adk.tools import Tool
from philharmonica.adk.types.input import LLMInputContentItem
from philharmonica.adk.types.responses.llm_response import (
    LLMResponse,
    LLMResponseFunctionToolCall,
    LLMResponseText,
    LLMStreamEvent,
)
from philharmonica.adk.verbose import VerboseConfig

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom middleware: cumulative per-agent wall-clock
# ---------------------------------------------------------------------------


class TimingMiddleware:
    """Record cumulative wall-clock time per agent name."""

    def __init__(self) -> None:
        self.totals: dict[str, float] = {}
        self.counts: dict[str, int] = {}

    async def __call__(
        self,
        agent: Agent,
        messages: list[LLMInputContentItem],
        context: RunContext[Any],
        next: AgentMiddlewareNext,
    ) -> AgentBlockOutcome:
        start = time.monotonic()
        outcome = await next(agent, messages)
        elapsed = time.monotonic() - start
        self.totals[agent.name] = self.totals.get(agent.name, 0.0) + elapsed
        self.counts[agent.name] = self.counts.get(agent.name, 0) + 1
        return outcome

    def report(self) -> None:
        logger.info("=== TimingMiddleware report ===")
        for name in sorted(self.totals.keys()):
            total = self.totals[name]
            count = self.counts[name]
            logger.info(
                "  %s — %d block(s), total %.4fs, avg %.4fs",
                name,
                count,
                total,
                total / count,
            )


# ---------------------------------------------------------------------------
# Stub LLM so the example runs without a real provider
# ---------------------------------------------------------------------------


def _tool_call(name: str, args: dict[str, Any], call_id: str) -> LLMResponse:
    return LLMResponse(
        response_id=f"r-{call_id}",
        model="stub",
        response=[
            LLMResponseFunctionToolCall(
                call_id=call_id,
                name=name,
                arguments=json.dumps(args),
            )
        ],
    )


def _text(text: str) -> LLMResponse:
    return LLMResponse(
        response_id="r-final",
        model="stub",
        response=[LLMResponseText(text=text)],
    )


class _ScriptedLLM(LLM):
    """Returns scripted ``LLMResponse`` values in order."""

    def __init__(self, responses: list[LLMResponse]) -> None:
        self._responses = list(responses)
        self._index = 0

    # Stub narrows the overloaded ``acomplete`` to one fixed return
    # union; mypy cannot see the overload chain resolves the same way.
    async def acomplete(  # type: ignore[override]
        self,
        messages: str | list[LLMInputContentItem],
        llm_config: LLMConfig | None = None,
        tools: list[Tool] | None = None,
        output_schema: AgentOutputSchemaBase | None = None,
        stream: bool = False,
    ) -> LLMResponse | AsyncIterator[LLMStreamEvent]:
        if stream:
            raise NotImplementedError("stub does not stream")
        if self._index >= len(self._responses):
            return _text("[stub script exhausted]")
        response = self._responses[self._index]
        self._index += 1
        return response


# ---------------------------------------------------------------------------
# Compose and run
# ---------------------------------------------------------------------------


async def main() -> None:
    timing = TimingMiddleware()

    # Beta agent — final output only.
    beta = Agent(
        name="Beta",
        system_prompt="You are Beta.",
        middleware=Middleware(agents=[AgentLoggingMiddleware(), timing]),
    )
    beta.llm = _ScriptedLLM([_text("Beta says hello")])

    # Alpha agent — hands off to Beta on its first turn.
    alpha = Agent(
        name="Alpha",
        system_prompt="You are Alpha. Hand off to Beta.",
        handoffs=[beta],
        middleware=Middleware(agents=[AgentLoggingMiddleware(), timing]),
    )
    alpha.llm = _ScriptedLLM([_tool_call("transfer_to_beta", {}, "h1")])

    result = await Runner.arun(alpha, "begin", run_config=RunConfig(verbose=VerboseConfig()))
    logger.info("final_output: %r", result.final_output)
    logger.info("last_agent:   %s", result.last_agent.name)
    timing.report()


if __name__ == "__main__":
    asyncio.run(main())
