"""Temporal.io durable execution backend for Philharmonica ADK.

Wraps agent, graph, swarm, and flow runs as Temporal workflows with
crash-recovery, retry, and deterministic replay.

Install the ``temporal`` optional extra before importing this package::

    pip install "philharmonica-adk[temporal]"

Public surface exported here covers configuration types, the LLM shim,
tool wrapping helpers, the HITL workflow base class, streaming, MCP
routing, and worker wiring.
"""

from __future__ import annotations

from philharmonica.adk.workflows.engine import ModelActivityConfig, ToolActivityConfig
from philharmonica.adk.workflows.temporal.llm import TemporalLLM
from philharmonica.adk.workflows.temporal.mcp import TemporalMCPToolSet
from philharmonica.adk.workflows.temporal.plugin import PhilharmonicaTemporalPlugin
from philharmonica.adk.workflows.temporal.routing import (
    MappingTaskQueueRouter,
    TenantTaskQueueRouter,
    start_tenant_workflow,
)
from philharmonica.adk.workflows.temporal.streaming import TemporalStreamingLLM
from philharmonica.adk.workflows.temporal.tools import TemporalToolWrapper, activity_tool, to_durable_tool
from philharmonica.adk.workflows.temporal.tracing import (
    deterministic_timestamp,
    deterministic_uuid,
    should_emit_span,
)
from philharmonica.adk.workflows.temporal.workflow import HumanReply, PhilharmonicaWorkflow, ToolApprovalDecision

__all__ = [
    "HumanReply",
    "MappingTaskQueueRouter",
    "ModelActivityConfig",
    "PhilharmonicaTemporalPlugin",
    "PhilharmonicaWorkflow",
    "TemporalLLM",
    "TemporalMCPToolSet",
    "TemporalStreamingLLM",
    "TemporalToolWrapper",
    "TenantTaskQueueRouter",
    "ToolActivityConfig",
    "ToolApprovalDecision",
    "activity_tool",
    "deterministic_timestamp",
    "deterministic_uuid",
    "should_emit_span",
    "start_tenant_workflow",
    "to_durable_tool",
]
