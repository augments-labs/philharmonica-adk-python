(references/api/graphs)=

# Graphs

State-machine orchestration: a directed graph of nodes executed in
supersteps, with checkpointing, interrupts, and streaming events.

## Core

- `philharmonica.adk.graphs.Graph`
- `philharmonica.adk.graphs.GraphBuilder`
- `philharmonica.adk.graphs.GraphConfig`

## Nodes and edges

- `philharmonica.adk.graphs.GraphNode`
- `philharmonica.adk.graphs.GraphEdge`
- `philharmonica.adk.graphs.EdgeCondition`
- `philharmonica.adk.graphs.NodeInputStrategy`
- `philharmonica.adk.graphs.NodeRetryPolicy`
- `philharmonica.adk.graphs.prepare_node_input`

## State and results

- `philharmonica.adk.graphs.GraphState`
- `philharmonica.adk.graphs.GraphRunResult`
- `philharmonica.adk.graphs.GraphRunResultStreaming`
- `philharmonica.adk.graphs.GraphRunStatus`
- `philharmonica.adk.graphs.StructuredInterrupts`

## Composition seam and adapters

- `philharmonica.adk.graphs.Executable`
- `philharmonica.adk.graphs.ExecutableInput`
- `philharmonica.adk.graphs.NodeResult`
- `philharmonica.adk.graphs.AgentExecutable`
- `philharmonica.adk.graphs.SwarmExecutable`
- `philharmonica.adk.graphs.CallableExecutable`
- `philharmonica.adk.graphs.CallableNodeFn`
- `philharmonica.adk.graphs.to_executable`

## Merge and join

- `philharmonica.adk.graphs.Merge`
- `philharmonica.adk.graphs.MergeFn`
- `philharmonica.adk.graphs.DEFAULT_MERGE`
- `philharmonica.adk.graphs.JoinBarrier`
- `philharmonica.adk.graphs.JoinSemantics`

## Checkpointers

- `philharmonica.adk.graphs.Checkpointer`
- `philharmonica.adk.graphs.GraphCheckpoint`
- `philharmonica.adk.graphs.InMemoryCheckpointer`
- `philharmonica.adk.graphs.SQLiteCheckpointer`
- `philharmonica.adk.graphs.TieredCheckpointer`

## Hooks

- `philharmonica.adk.graphs.GraphHooks`
- `philharmonica.adk.graphs.HookProvider`
- `philharmonica.adk.graphs.HookRegistry`

## Interrupts and resume

- `philharmonica.adk.graphs.Interrupt`
- `philharmonica.adk.graphs.InterruptException`
- `philharmonica.adk.graphs.GraphResume`
- `philharmonica.adk.graphs.GraphResumeError`
- `philharmonica.adk.graphs.NestedGraphInterrupt`
- `philharmonica.adk.graphs.NestedAgentInterrupt`
- `philharmonica.adk.graphs.NestedAgentApproval`
- `philharmonica.adk.graphs.NestedAgentRejection`
- `philharmonica.adk.graphs.NestedAgentReply`
- `philharmonica.adk.graphs.NestedAgentDecision`
- `philharmonica.adk.graphs.NestedAgentResumeError`
- `philharmonica.adk.graphs.NestedAgentSerializationError`
- `philharmonica.adk.graphs.request_human_input`
- `philharmonica.adk.graphs.NESTED_AGENT_TOOL_APPROVAL_KIND`
- `philharmonica.adk.graphs.NESTED_GRAPH_INTERRUPT_KIND`

## Events

- `philharmonica.adk.graphs.GraphStreamEvent`
- `philharmonica.adk.graphs.GraphEndEvent`
- `philharmonica.adk.graphs.NodeStartEvent`
- `philharmonica.adk.graphs.NodeEndEvent`
- `philharmonica.adk.graphs.NodeErrorEvent`
- `philharmonica.adk.graphs.NodeStreamEvent`
- `philharmonica.adk.graphs.SuperstepStartEvent`
- `philharmonica.adk.graphs.GRAPH_START`
- `philharmonica.adk.graphs.GRAPH_END`
- `philharmonica.adk.graphs.NODE_START`
- `philharmonica.adk.graphs.NODE_END`
- `philharmonica.adk.graphs.NODE_ERROR`
- `philharmonica.adk.graphs.NODE_INTERRUPT`
- `philharmonica.adk.graphs.NODE_STREAM`
- `philharmonica.adk.graphs.SUPERSTEP_START`
- `philharmonica.adk.graphs.SUPERSTEP_END`

Three further `GraphStreamEvent` subclasses, spelled out with the keys
each one carries:

- `GraphStartEvent` — emitted once at the top of a graph run, before
  the first superstep. Keys: `type` (always `GRAPH_START`),
  `graph_path`, `graph_id`, `description`, `entry_node`,
  `terminal_nodes`.
- `SuperstepEndEvent` — emitted after a superstep completes. Keys:
  `type` (always `SUPERSTEP_END`), `graph_path`, `superstep`,
  `fired_nodes`, `errored_nodes`.
- `NodeInterruptEvent` — a node raised `InterruptException` and the
  run is suspending; carries the pending `Interrupt` so consumers can
  prompt the human and resume via `GraphResume`. Keys: `type` (always
  `NODE_INTERRUPT`), `graph_path`, `node_id`, `interrupt`.

Graphs are executed via `Runner.arun_graph`. The end-to-end walkthrough
lives in the [Graphs guide](../../graphs/graphs.md).
