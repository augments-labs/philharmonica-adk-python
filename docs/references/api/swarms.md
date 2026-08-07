# Swarms

Multi-agent iterative collaboration: a roster of agents taking turns on a
shared problem until an explicit termination signal fires.

## Core

- `philharmonica.adk.swarms.Swarm`
- `philharmonica.adk.swarms.SwarmBuilder`
- `philharmonica.adk.swarms.SwarmConfig`

## Policies

- `philharmonica.adk.swarms.SwarmPolicy`
- `philharmonica.adk.swarms.LLMHandoffPolicy`
- `philharmonica.adk.swarms.RoundRobinPolicy`
- `philharmonica.adk.swarms.StructuredRoutingPolicy`
- `philharmonica.adk.swarms.CustomPolicy`
- `philharmonica.adk.swarms.SwarmSelector`
- `philharmonica.adk.swarms.SwarmExtraToolsFn`

## Termination

- `philharmonica.adk.swarms.TerminationCondition`
- `philharmonica.adk.swarms.ExplicitDoneTermination`
- `philharmonica.adk.swarms.MaxTurnsTermination`
- `philharmonica.adk.swarms.TokenBudgetTermination`
- `philharmonica.adk.swarms.TextMentionTermination`
- `philharmonica.adk.swarms.HandoffToTermination`
- `philharmonica.adk.swarms.AndTermination`
- `philharmonica.adk.swarms.OrTermination`

## State and results

- `philharmonica.adk.swarms.SwarmState`
- `philharmonica.adk.swarms.SwarmStateDict`
- `philharmonica.adk.swarms.SwarmRunResult`
- `philharmonica.adk.swarms.SwarmRunResultStreaming`
- `philharmonica.adk.swarms.StopReason`

## Events

- `philharmonica.adk.swarms.SwarmStartEvent`
- `philharmonica.adk.swarms.SwarmTurnStartEvent`
- `philharmonica.adk.swarms.SwarmTurnEndEvent`
- `philharmonica.adk.swarms.SwarmTurnInterruptEvent`
- `philharmonica.adk.swarms.SwarmHandoffEvent`
- `philharmonica.adk.swarms.SwarmDoneEvent`
- `philharmonica.adk.swarms.SwarmEvent`

## Yield signals

- `philharmonica.adk.swarms.SwarmDone`
- `philharmonica.adk.swarms.SwarmHandoff`
- `philharmonica.adk.swarms.SwarmYieldSignal`

## Hooks and checkpoints

- `philharmonica.adk.swarms.SwarmHooks`
- `philharmonica.adk.swarms.HookRegistry`
- `philharmonica.adk.swarms.SwarmHookRegistry`
- `philharmonica.adk.swarms.SwarmCheckpoint`
- `philharmonica.adk.swarms.SwarmCheckpointer`

## Interrupt and resume

- `philharmonica.adk.swarms.SwarmResume`
- `philharmonica.adk.swarms.request_human_input_in_swarm`

## Shared context

- `philharmonica.adk.swarms.SharedContextConfig`
- `philharmonica.adk.swarms.SharedContextStrategy`
- `philharmonica.adk.swarms.prepare_turn_input`
- `philharmonica.adk.swarms.prompt_with_swarm_instructions`

## Constants

- `philharmonica.adk.swarms.DEFAULT_MAX_TURNS`
- `philharmonica.adk.swarms.DEFAULT_TERMINATION`
- `philharmonica.adk.swarms.RECOMMENDED_SWARM_PROMPT_PREFIX`
- `philharmonica.adk.swarms.SWARM_DONE_TOOL_NAME`

Swarms are executed via `Runner.arun_swarm`. The end-to-end walkthrough
lives in the [Swarms guide](../../swarms/swarms.md).
