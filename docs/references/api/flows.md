(references/api/flows)=

# Flows

Decorator-driven multi-step orchestration over typed shared state, with
event-driven listeners and state-based routers.

## Core

- `philharmonica.adk.flows.Flow`
- `philharmonica.adk.flows.FlowMeta`
- `philharmonica.adk.flows.FlowStep`
- `philharmonica.adk.flows.FlowRole`

## Decorators

- `philharmonica.adk.flows.flow_start`
- `philharmonica.adk.flows.flow_listen`
- `philharmonica.adk.flows.flow_router`
- `philharmonica.adk.flows.FlowTriggerSpec`

## Combinators

- `philharmonica.adk.flows.Or`
- `philharmonica.adk.flows.And`

## Config and results

- `philharmonica.adk.flows.FlowConfig`
- `philharmonica.adk.flows.FlowErrorPolicy`
- `philharmonica.adk.flows.FlowRunResult`
- `philharmonica.adk.flows.FlowRunResultStreaming`
- `philharmonica.adk.flows.FlowRunStatus`

## Triggers

- `philharmonica.adk.flows.FlowTriggerEvent`
- `philharmonica.adk.flows.FlowTriggerKind`
- `philharmonica.adk.flows.FLOW_ERROR_TRIGGER`

## Events

- `philharmonica.adk.flows.FlowStartEvent`
- `philharmonica.adk.flows.FlowEndEvent`
- `philharmonica.adk.flows.FlowStepStartEvent`
- `philharmonica.adk.flows.FlowStepEndEvent`
- `philharmonica.adk.flows.FlowStepErrorEvent`
- `philharmonica.adk.flows.FlowStepSkippedEvent`
- `philharmonica.adk.flows.FlowStepDeferredEvent`
- `philharmonica.adk.flows.FlowStepRejectedEvent`
- `philharmonica.adk.flows.FlowRouteEvaluatedEvent`
- `philharmonica.adk.flows.FlowEvent`

## Approvals and deferral

- `philharmonica.adk.flows.FlowApprovalPolicy`
- `philharmonica.adk.flows.FlowApprovalDecision`
- `philharmonica.adk.flows.FlowApprovalStatus`
- `philharmonica.adk.flows.FlowDeferralKind`
- `philharmonica.adk.flows.FlowDeferredStep`
- `philharmonica.adk.flows.FlowAgentDeferred`

## Step governance

- `philharmonica.adk.flows.FlowStepContext`
- `philharmonica.adk.flows.FlowStepGate`
- `philharmonica.adk.flows.FlowStepGuardrails`
- `philharmonica.adk.flows.FlowStepGuardrailFn`
- `philharmonica.adk.flows.FlowStepGuardrailVerdict`
- `philharmonica.adk.flows.FlowStepCachePolicy`
- `philharmonica.adk.flows.FlowCacheKeyFn`
- `philharmonica.adk.flows.FlowStepRateLimit`
- `philharmonica.adk.flows.FlowStepRateLimitBehavior`

## Persistence and distributed execution

- `philharmonica.adk.flows.FlowCheckpoint`
- `philharmonica.adk.flows.FlowWorkerBackend`
- `philharmonica.adk.flows.FlowBatchClaim`
- `philharmonica.adk.flows.InMemoryFlowWorkerBackend`
- `philharmonica.adk.flows.SqliteFlowWorkerBackend`

## Definition and registry

- `philharmonica.adk.flows.FlowDefinition`
- `philharmonica.adk.flows.StepInfo`
- `philharmonica.adk.flows.GateInfo`
- `philharmonica.adk.flows.FlowStepRegistry`
- `philharmonica.adk.flows.FlowTransitionTable`
- `philharmonica.adk.flows.GateSpec`
- `philharmonica.adk.flows.TriggerSpec`
- `philharmonica.adk.flows.build_flow_definition`
- `philharmonica.adk.flows.build_transition_table`
- `philharmonica.adk.flows.collect_step_descriptions`

## Agent bridge

- `philharmonica.adk.flows.FlowExecutable`
- `philharmonica.adk.flows.arun_flow_agent`

## Exceptions

- `philharmonica.adk.flows.FlowDefinitionError`
- `philharmonica.adk.flows.FlowStepError`
- `philharmonica.adk.flows.FlowMaxStepsExceeded`
- `philharmonica.adk.flows.FlowCheckpointNotFoundError`

Flows are executed via `Runner.arun_flow`. The end-to-end walkthrough
lives in the [Flows guide](../../flows/flows.md).
