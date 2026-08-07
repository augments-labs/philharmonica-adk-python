"""Restate durable execution backend for Philharmonica ADK.

Alternative to the Temporal backend using Restate's journaling-based
durable execution model.  LLM calls and tool calls are routed through
``ctx.run()`` so that results are journaled and replay-safe.

Install the ``restate`` optional extra before importing this package::

    pip install "philharmonica-adk[restate]"
"""

from __future__ import annotations

from philharmonica.adk.workflows.restate.llm import RestateLLM
from philharmonica.adk.workflows.restate.service import PhilharmonicaRestateService, RestateHumanReply
from philharmonica.adk.workflows.restate.tools import restate_tool

__all__ = [
    "PhilharmonicaRestateService",
    "RestateHumanReply",
    "RestateLLM",
    "restate_tool",
]
