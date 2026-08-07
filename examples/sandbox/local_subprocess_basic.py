"""Minimal local sandbox example.

Constructs a SandboxAgent with a Shell capability + LocalSubprocess
backend, then runs a tiny command through the agent loop.
"""

from __future__ import annotations

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import asyncio
import logging

logger = logging.getLogger(__name__)


async def main() -> None:
    from philharmonica.adk.run.config import RunConfig
    from philharmonica.adk.run.runner import Runner
    from philharmonica.adk.sandbox.agent import SandboxAgent
    from philharmonica.adk.sandbox.capabilities.shell import ShellCapability
    from philharmonica.adk.sandbox.clients.local import LocalSubprocessSandboxClient
    from philharmonica.adk.sandbox.config import SandboxRunConfig
    from philharmonica.adk.verbose import VerboseConfig

    agent = SandboxAgent(
        name="coder",
        system_prompt="You can run shell commands in a sandboxed workspace.",
        capabilities=[ShellCapability()],
    )

    client = LocalSubprocessSandboxClient()
    run_config = RunConfig(sandbox=SandboxRunConfig(client=client), verbose=VerboseConfig())

    # The full agent loop integration of capability tools lands in a
    # follow-up phase; until then, this example demonstrates that the
    # sandbox bracket opens correctly around Runner.arun.
    result = await Runner.arun(
        agent,
        "Hello, sandboxed coder. Reply briefly.",
        run_config=run_config,
    )
    logger.info("Agent final output: %s", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
