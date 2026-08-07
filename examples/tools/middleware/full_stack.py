"""All three middleware layers active in one run.

Demonstrates the canonical event ordering produced when
``Middleware(tools=..., agents=..., llms=...)`` is fully configured:

    AgentLoggingMiddleware enters
      LLMLoggingMiddleware enters (turn 1)
        — acomplete returns a tool_call —
      LLMLoggingMiddleware exits (turn 1)
      ToolLoggingMiddleware enters
        — tool runs —
      ToolLoggingMiddleware exits
      LLMLoggingMiddleware enters (turn 2)
        — acomplete returns final text —
      LLMLoggingMiddleware exits (turn 2)
    AgentLoggingMiddleware exits

The example uses a scripted stub LLM so the exact sequence is
deterministic and reproducible without any provider API key.

Usage:
    python examples/tools/middleware/full_stack.py
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
from collections.abc import AsyncIterator
from typing import Any

from philharmonica.adk.agents.agent import Agent
from philharmonica.adk.agents.middleware import Middleware
from philharmonica.adk.llms.llm import LLM
from philharmonica.adk.llms.llm_config import LLMConfig
from philharmonica.adk.llms.llm_middleware import LLMLoggingMiddleware
from philharmonica.adk.run.agent_middleware import AgentLoggingMiddleware
from philharmonica.adk.run.config import RunConfig
from philharmonica.adk.run.runner import Runner
from philharmonica.adk.schemas import AgentOutputSchemaBase
from philharmonica.adk.tools import Tool, ToolLoggingMiddleware, function_tool
from philharmonica.adk.types.input import LLMInputContentItem
from philharmonica.adk.types.responses.llm_response import (
    LLMResponse,
    LLMResponseFunctionToolCall,
    LLMResponseText,
    LLMStreamEvent,
)
from philharmonica.adk.verbose import VerboseConfig

logger = logging.getLogger(__name__)


@function_tool(name="echo", description="echo a string")
def echo(text: str) -> str:
    return f"echoed:{text}"


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
            raise NotImplementedError
        if self._index >= len(self._responses):
            return _text("[script exhausted]")
        response = self._responses[self._index]
        self._index += 1
        return response


async def main() -> None:
    agent = Agent(
        name="FullStack",
        system_prompt="Demo agent with all three middleware layers.",
        tools=[echo],
        llm=_ScriptedLLM(
            [
                _tool_call("echo", {"text": "hi"}, "c1"),
                _text("done"),
            ]
        ),
        middleware=Middleware(
            tools=[ToolLoggingMiddleware()],
            agents=[AgentLoggingMiddleware()],
            llms=[LLMLoggingMiddleware()],
        ),
    )

    logger.info("=== three-layer middleware demo ===")
    result = await Runner.arun(agent, "go", run_config=RunConfig(verbose=VerboseConfig()))
    logger.info("=== final_output: %r ===", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
