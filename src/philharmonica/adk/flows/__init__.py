"""Flow primitive — decorator-driven multi-step orchestration over typed shared state.

A :class:`Flow` is a class-based, declarative orchestration that composes
:class:`~philharmonica.adk.agents.agent.Agent`, :class:`~philharmonica.adk.swarms.swarm.Swarm`,
:class:`~philharmonica.adk.graphs.graph.Graph`, and :class:`~philharmonica.adk.tasks.task.Task`
calls as ordered steps, with typed shared state, event-driven listeners,
and state-based routers. Fills the gap between the existing
:class:`~philharmonica.adk.graphs.graph.Graph` (DAG with message-threading) and
:class:`~philharmonica.adk.tasks.task_pipeline.TaskPipeline` (sequential with no
typed shared state).

Canonical minimal example — a two-step Flow over a Pydantic state::

    from pydantic import BaseModel

    from philharmonica.adk import Runner
    from philharmonica.adk.flows import Flow, flow_listen, flow_start


    class ResearchState(BaseModel):
        topic: str = ""
        summary: str = ""


    class ResearchFlow(Flow[ResearchState]):
        state_factory = ResearchState

        @flow_start
        async def kickoff(self) -> None:
            self.state.topic = "climate"

        @flow_listen(kickoff)
        async def summarize(self) -> None:
            self.state.summary = f"Summary of {self.state.topic}."


    flow = ResearchFlow()  # or ResearchFlow(initial_state=ResearchState(topic="ml"))
    result = await Runner.arun_flow(flow)

**Anti-hidden-behavior contract**: every wire is declared by an explicit
decorator on a method; step methods take only ``self``; ``self.state`` is
the developer's mutable typed object; persistence is explicit via
:class:`~philharmonica.adk.flows.checkpoint.FlowCheckpoint`. The framework
NEVER auto-injects arguments, auto-persists state, auto-routes on bare
string returns, or auto-instantiates state from the generic parameter.

**Combinators are operator-only**: use ``method_a | method_b`` /
``method_a & method_b``. There are no ``or_()`` / ``and_()`` helper
functions in this ADK — those CrewAI helpers are intentionally omitted
in favor of the fluent operator API.

The name ``Flow`` (rather than ``Workflow``) reserves the latter name
for the future Temporal-style durable execution layer, which composes
*over* this orchestration topology.

See ``docs/flows/flows.md`` for usage and ``examples/flows/`` for runnable
examples.
"""

from __future__ import annotations

from philharmonica.adk.flows.agent_bridge import arun_flow_agent
from philharmonica.adk.flows.approval_policy import FlowApprovalPolicy
from philharmonica.adk.flows.checkpoint import FlowCheckpoint
from philharmonica.adk.flows.combinators import And, Or
from philharmonica.adk.flows.config import FlowConfig, FlowErrorPolicy
from philharmonica.adk.flows.decorators import FlowTriggerSpec, flow_listen, flow_router, flow_start
from philharmonica.adk.flows.deferred import (
    FlowApprovalDecision,
    FlowApprovalStatus,
    FlowDeferralKind,
    FlowDeferredStep,
)
from philharmonica.adk.flows.definition import (
    FlowDefinition,
    GateInfo,
    StepInfo,
    build_flow_definition,
)
from philharmonica.adk.flows.events import (
    FlowEndEvent,
    FlowEvent,
    FlowRouteEvaluatedEvent,
    FlowStartEvent,
    FlowStepDeferredEvent,
    FlowStepEndEvent,
    FlowStepErrorEvent,
    FlowStepRejectedEvent,
    FlowStepSkippedEvent,
    FlowStepStartEvent,
)
from philharmonica.adk.flows.exceptions import (
    FlowAgentDeferred,
    FlowCheckpointNotFoundError,
    FlowDefinitionError,
    FlowMaxStepsExceeded,
    FlowStepError,
)
from philharmonica.adk.flows.executable import FlowExecutable
from philharmonica.adk.flows.flow import Flow, FlowMeta, collect_step_descriptions
from philharmonica.adk.flows.flow_wrappers import FlowRole, FlowStep
from philharmonica.adk.flows.registry import (
    FlowStepRegistry,
    FlowTransitionTable,
    GateSpec,
    TriggerSpec,
    build_transition_table,
)
from philharmonica.adk.flows.result import FlowRunResult, FlowRunResultStreaming, FlowRunStatus
from philharmonica.adk.flows.sqlite_worker_backend import SqliteFlowWorkerBackend
from philharmonica.adk.flows.step_cache_policy import FlowCacheKeyFn, FlowStepCachePolicy
from philharmonica.adk.flows.step_context import FlowStepContext, FlowStepGate
from philharmonica.adk.flows.step_guardrails import (
    FlowStepGuardrailFn,
    FlowStepGuardrails,
    FlowStepGuardrailVerdict,
)
from philharmonica.adk.flows.step_rate_limit import (
    FlowStepRateLimit,
    FlowStepRateLimitBehavior,
)
from philharmonica.adk.flows.triggers import FLOW_ERROR_TRIGGER, FlowTriggerEvent, FlowTriggerKind
from philharmonica.adk.flows.worker_backend import (
    FlowBatchClaim,
    FlowWorkerBackend,
    InMemoryFlowWorkerBackend,
)

__all__ = [
    # Alphabetically sorted (RUF022). Themes, for orientation:
    # core (Flow, FlowStep), decorators (flow_*), combinators (Or, And),
    # config & result, events, HITL & deferral, step governance,
    # triggers, distributed execution, exceptions, definition/registry.
    "FLOW_ERROR_TRIGGER",
    "And",
    "Flow",
    "FlowAgentDeferred",
    "FlowApprovalDecision",
    "FlowApprovalPolicy",
    "FlowApprovalStatus",
    "FlowBatchClaim",
    "FlowCacheKeyFn",
    "FlowCheckpoint",
    "FlowCheckpointNotFoundError",
    "FlowConfig",
    "FlowDeferralKind",
    "FlowDeferredStep",
    "FlowDefinition",
    "FlowDefinitionError",
    "FlowEndEvent",
    "FlowErrorPolicy",
    "FlowEvent",
    "FlowExecutable",
    "FlowMaxStepsExceeded",
    "FlowMeta",
    "FlowRole",
    "FlowRouteEvaluatedEvent",
    "FlowRunResult",
    "FlowRunResultStreaming",
    "FlowRunStatus",
    "FlowStartEvent",
    "FlowStep",
    "FlowStepCachePolicy",
    "FlowStepContext",
    "FlowStepDeferredEvent",
    "FlowStepEndEvent",
    "FlowStepError",
    "FlowStepErrorEvent",
    "FlowStepGate",
    "FlowStepGuardrailFn",
    "FlowStepGuardrailVerdict",
    "FlowStepGuardrails",
    "FlowStepRateLimit",
    "FlowStepRateLimitBehavior",
    "FlowStepRegistry",
    "FlowStepRejectedEvent",
    "FlowStepSkippedEvent",
    "FlowStepStartEvent",
    "FlowTransitionTable",
    "FlowTriggerEvent",
    "FlowTriggerKind",
    "FlowTriggerSpec",
    "FlowWorkerBackend",
    "GateInfo",
    "GateSpec",
    "InMemoryFlowWorkerBackend",
    "Or",
    "SqliteFlowWorkerBackend",
    "StepInfo",
    "TriggerSpec",
    "arun_flow_agent",
    "build_flow_definition",
    "build_transition_table",
    "collect_step_descriptions",
    "flow_listen",
    "flow_router",
    "flow_start",
]
