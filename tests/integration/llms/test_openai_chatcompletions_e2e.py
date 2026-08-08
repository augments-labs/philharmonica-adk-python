"""End-to-end live integration test for ``OpenAIChatCompletionsLLM``.

Skipped unless ``OPENAI_API_KEY`` holds a non-empty value. The test
executes exactly one real roundtrip against the OpenAI Chat
Completions API and asserts on non-empty output plus non-zero usage.

Run with::

    OPENAI_API_KEY=sk-... pytest tests/integration/llms/test_openai_chatcompletions_e2e.py -v
"""

from __future__ import annotations

import os

import pytest

from philharmonica.adk.agents.agent import Agent
from philharmonica.adk.llms.openai import OpenAIChatCompletionsLLM
from philharmonica.adk.run.runner import Runner

# Test truthiness, not `is None`. A workflow that forwards a secret with
# `OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}` defines the variable even
# when the secret does not exist — GitHub substitutes an empty string — so
# `is None` reports "key present" on exactly the runner that has no key, and
# the roundtrip fails on an empty credential instead of skipping.
pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="Set OPENAI_API_KEY to run this integration test.",
)


@pytest.mark.integration
async def test_openai_chatcompletions_basic_roundtrip() -> None:
    agent = Agent(
        name="Assistant",
        system_prompt="You are concise. Answer in one short sentence.",
        llm=OpenAIChatCompletionsLLM("gpt-4o-mini"),
    )

    result = await Runner.arun(agent, "In one sentence, what colour is the sky on a clear day?")

    assert result.final_output is not None
    assert len(str(result.final_output)) > 0
    assert result.context.usage.total_tokens > 0
