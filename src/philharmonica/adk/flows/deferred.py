"""FlowDeferredStep + FlowApprovalDecision — HITL deferral payloads.

When a step's ``FlowStep.requires_approval`` gate fires, the
executor captures the step into a ``FlowDeferredStep`` and halts
the run. The list of deferred steps lands on
``FlowCheckpoint.deferred_steps`` and
``FlowRunResult.deferred_steps``. Decisions live on the
checkpoint itself — recorded via ``FlowCheckpoint.approve`` /
``FlowCheckpoint.reject`` — and resumption goes through
``Runner.arun_flow_from_checkpoint(flow, checkpoint)``. Same
surface as the tool layer's
``RunState.approve`` / ``RunState.reject`` →
``Runner.arun(agent, state)``.

The deferral types support multiple use cases beyond bare
human approval:

- ``kind="approval"`` — single human-in-the-loop approval (default).
- ``kind="external_execution"`` — step is executed by an external
  service (webhook, batch job) and the result fed back via the
  resume path. The execution channel is identical; only the
  intent / driver differs.

Policy attachment (``FlowApprovalPolicy``) enables declarative
quorum / role / SLA semantics without bespoke callable code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

from philharmonica.adk.flows.approval_policy import FlowApprovalPolicy
from philharmonica.adk.flows.triggers import FlowTriggerEvent

FlowDeferralKind = Literal["approval", "external_execution"]
"""Why this step is deferred.

- ``"approval"`` — pending human approval (HITL). The default.
- ``"external_execution"`` — the step is being executed by an
  external system (webhook, batch job, external worker) and the run
  resumes once the external result is fed back on the checkpoint.
  Wire-compatible with the approval path; only the semantics differ.
"""


FlowApprovalStatus = Literal["pending", "approved", "rejected", "expired"]
"""Resolved status for one deferred step's approval lifecycle.

- ``"pending"`` — no decision yet.
- ``"approved"`` — at least one valid decision recorded with
  ``approved=True`` (and quorum met, when a
  ``FlowApprovalPolicy`` is attached).
- ``"rejected"`` — recorded decision with ``approved=False``, or
  quorum unmet within deadline.
- ``"expired"`` — deadline lapsed before sufficient decisions
  arrived; equivalent to a rejection with ``message="deadline_expired"``.
"""


@dataclass(frozen=True, kw_only=True)
class FlowDeferredStep:
    """One step paused awaiting an external decision.

    Frozen audit record: produced by the executor when a step's
    ``requires_approval`` gate fires (or when the developer wires an
    external-execution deferral), serialised into
    ``FlowCheckpoint``, surfaced on ``FlowRunResult``.
    Developers receive these to drive out-of-band approval / execution
    flows.

    Attributes:
        step_name: Method name of the deferred step.
        kind: Why the step is deferred — see ``FlowDeferralKind``.
            ``"approval"`` is the standard HITL case.
        triggers: Tuple of ``FlowTriggerEvent`` instances that
            scheduled the deferred step. Empty for ``@flow_start``;
            single-element for a direct listener or OR gate;
            multi-element for an AND gate. Same shape as
            ``FlowStepContext.triggers``.
        request_time: UTC timestamp at the moment the gate fired.
            Combined with ``FlowApprovalPolicy.deadline_seconds``
            to enforce SLAs.
        deadline: Optional explicit deadline. When set, supersedes any
            ``deadline_seconds`` derived from ``policy`` —
            ``None`` (default) means follow the policy's relative
            deadline, or no deadline if no policy attached.
        policy: Optional ``FlowApprovalPolicy`` declaring quorum
            / role / SLA semantics. ``None`` (default) is the bare
            single-approver case.
        metadata: Open-ended developer payload — never read by the
            framework. Useful for tagging the deferral with tenant
            IDs, ticket links, escalation hints, audit references.
        defer_key: Stable key for the inner agent invocation when an
            agent-level HITL deferral propagates up through a step body
            via ``arun_flow_agent``. ``None`` for plain step-level
            ``requires_approval`` gates that do not involve an agent run.
        agent_run_state: Serialised ``RunState`` JSON for
            agent-bridge deferrals. ``None`` for non-agent deferrals.
    """

    step_name: str
    """Method name of the deferred step."""

    kind: FlowDeferralKind = "approval"
    """Why this step is deferred (see ``FlowDeferralKind``)."""

    triggers: tuple[FlowTriggerEvent, ...] = ()
    """``FlowTriggerEvent``\\ s that scheduled the deferred step."""

    request_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    """UTC timestamp at the moment the gate fired."""

    deadline: datetime | None = None
    """Optional explicit deadline; overrides ``policy.deadline_seconds``."""

    policy: FlowApprovalPolicy | None = None
    """Optional declarative approval policy (quorum / roles / SLA)."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Open-ended developer payload — never read by the framework."""

    defer_key: str | None = None
    """Stable key for the inner agent invocation when ``kind="approval"`` rides on the agent bridge.

    Populated by ``arun_flow_agent`` when an agent-level HITL
    deferral propagates up through a step body. Empty (``None``) for
    plain step-level ``requires_approval`` gates that do not involve
    an agent run.
    """

    agent_run_state: str | None = None
    """Serialised ``RunState`` JSON for agent-bridge deferrals.

    Populated when an inner ``Runner.arun`` call inside a step
    body returns ``requires_action=True``. Carries the agent's full
    deferred-tool state so the resume path can hand it back to
    ``Runner.arun`` to continue the agent run after the human
    records decisions on the underlying ``RunState``.

    Round-trips through ``FlowCheckpoint`` JSON via
    ``_deferred_to_dict`` / ``_deferred_from_dict``. The
    encoding goes through ``RunState.to_dict`` ``+`` ``json.dumps``
    because the flow checkpoint owns its own serialisation envelope;
    the plain dict form contains exactly the fields needed and
    produces no extra wrapper keys.
    """


@dataclass(frozen=True, kw_only=True)
class FlowApprovalDecision:
    """One human decision for a deferred step.

    Recorded on ``FlowCheckpoint`` by
    ``FlowCheckpoint.approve`` / ``FlowCheckpoint.reject`` —
    same pattern as ``RunState.approve`` / ``RunState.reject``
    for tool-level HITL.

    Field semantics mirror the tool surface exactly:

    - ``message`` is the *routed* explanation — surfaced through
      ``FlowStepRejectedEvent`` and the
      ``FlowStepRejected`` internal exception that routes through
      ``FlowConfig.error_policy``. Analogue of the ``message``
      parameter on ``RunState.reject``.
    - ``reason`` is *audit-only* metadata — logged for compliance
      and never surfaced through events or error handlers. Analogue
      of the ``reason`` parameter on ``RunState.approve`` /
      ``RunState.reject``.

    Attributes:
        step_name: Method name of the deferred step the decision
            targets. MUST match one of the pending
            ``FlowDeferredStep.step_name`` values.
        approved: ``True`` to proceed with the step body, ``False``
            to reject. Rejected steps route through
            ``FlowConfig.error_policy``.
        message: Optional routed explanation. Surfaces through
            ``FlowStepRejectedEvent.message`` and
            ``FlowStepRejected``. ``None`` ⇒ no explanation
            forwarded.
        approver_id: Optional opaque identifier (audit only). Never
            surfaced through events or error handlers.
        approver_role: Optional role / group (audit only).
        reason: Optional free-form audit rationale. Logged alongside
            ``approver_id`` / ``approver_role``; never routed.
        decision_time: UTC timestamp at construction. Together with
            ``FlowDeferredStep.request_time`` yields the
            decision-latency for SLA tracking.
        expired: ``True`` when the rejection was auto-issued on SLA
            expiry (deadline lapsed before sufficient decisions arrived).
            Distinct from an explicit human rejection; surfaces through
            ``status`` as ``"expired"``.
        metadata: Open-ended audit / telemetry payload — never read by
            the framework.
    """

    step_name: str
    """Method name of the deferred step this decision targets."""

    approved: bool
    """Whether the step should proceed."""

    message: str | None = None
    """Routed rejection explanation — surfaces through events / error handlers."""

    approver_id: str | None = None
    """Audit-only opaque identifier of the approver."""

    approver_role: str | None = None
    """Audit-only role / group of the approver."""

    reason: str | None = None
    """Audit-only rationale; logged but never routed."""

    decision_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    """UTC timestamp at the moment the decision was constructed."""

    expired: bool = False
    """``True`` when the rejection was auto-issued by SLA expiry.

    Set by the driver (or the framework's future auto-reject path) when
    ``FlowApprovalPolicy.deadline_seconds`` /
    ``FlowDeferredStep.deadline`` lapses. Distinct from an
    explicit human rejection; surfaced through ``status`` as
    ``"expired"`` so downstream branching never relies on parsing
    ``message``.
    """

    metadata: dict[str, Any] = field(default_factory=dict)
    """Open-ended audit / telemetry payload — never read by the framework."""

    @property
    def status(self) -> FlowApprovalStatus:
        """Resolved ``FlowApprovalStatus`` for this decision.

        Derived structurally from ``approved`` and ``expired``
        — never from string parsing on ``message``. ``"expired"``
        is surfaced for SLA-driven auto-rejections so consumers can
        branch on cause without inspecting prose.
        """
        if self.approved:
            return "approved"
        if self.expired:
            return "expired"
        return "rejected"
