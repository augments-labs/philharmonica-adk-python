(references/api/types)=

# Types

Provider-agnostic wire and history types shared across the framework.

## Run items

- `philharmonica.adk.types.RunItem`
- `philharmonica.adk.types.RunItemBase`
- `philharmonica.adk.types.UserItem`
- `philharmonica.adk.types.SystemItem`
- `philharmonica.adk.types.MessageOutputItem`
- `philharmonica.adk.types.ReasoningItem`
- `philharmonica.adk.types.ToolCallItem`
- `philharmonica.adk.types.ToolCallOutputItem`
- `philharmonica.adk.types.ToolApprovalItem`
- `philharmonica.adk.types.ToolSearchCallItem`
- `philharmonica.adk.types.ToolSearchOutputItem`
- `philharmonica.adk.types.HandoffCallItem`
- `philharmonica.adk.types.HandoffOutputItem`
- `philharmonica.adk.types.MCPListToolsItem`
- `philharmonica.adk.types.MCPApprovalRequestItem`
- `philharmonica.adk.types.MCPApprovalResponseItem`
- `philharmonica.adk.types.CompactionItem`
- `philharmonica.adk.types.ItemHelpers`

## Result

### `philharmonica.adk.types.RunResult`

Result of a completed (or interrupted) agent run. Contains the final
output (if the run completed), all items generated during execution,
and supports HITL interruptions via `deferred_requests`.

Fields:

- `final_output` — the final output from the agent, or `None` if
  interrupted for approval.
- `user_prompt` — the original user prompt passed to the run.
- `new_items` — Layer 3 `RunItem` values generated during this run
  (messages, tool calls, results).
- `context` — the run context with usage tracking.
- `last_agent` — the last agent that was active.
- `recovered` — `True` when an error handler produced `final_output`
  after the run raised; recovered runs skip session and memory
  persistence.
- `deferred_requests` — tools captured for approval or external
  execution; `None` if the run completed.
- `state` — serializable state for resuming interrupted runs.
- `guardrail_results` — per-phase agent-level guardrail audit trail
  (`input` and `output` slots).
- `guardrail_audit` — per-action guardrail audit records across every
  level (agent, tool, flow), captured as hashes, never raw payloads.
- `swarm_yield` — set only by the swarm driver when an agent turn
  yielded control; `None` on every plain `Runner.arun()` path.
- `sandbox_usage` — aggregate sandbox resource and cost usage, or
  `None` when no sandbox session ran.

Members:

- `requires_action` — property; `True` when human approval or external
  action is pending.
- `interruptions` — property; tool calls awaiting human approval, as a
  flat list.
- `last_response_id` — property; the `response_id` of the most recent
  LLM response in this run, or `None`.
- `release_agents(*, release_new_items=True)` — drop strong references
  to agents and, optionally, run items.
- `to_input_list()` — convert to a Layer 1 input list for a continued
  conversation.
- `final_output_as(output_type)` — cast the final output to the
  expected type.

Example:

```python
result = await Runner.arun(agent, "Delete user 123")
if result.requires_action:
    for req in list(result.deferred_requests.approvals):
        if await confirm(f"Approve {req.tool_name}?"):
            result.state.approve(req)
        else:
            result.state.reject(req, "Denied")
    result = await Runner.arun(agent, result.state)
```

## Built-in tool call and result types

- `philharmonica.adk.types.WebSearchToolCall`
- `philharmonica.adk.types.WebSearchToolCallResult`
- `philharmonica.adk.types.WebSearchResult`
- `philharmonica.adk.types.FileSearchToolCall`
- `philharmonica.adk.types.FileSearchToolCallResult`
- `philharmonica.adk.types.FileSearchResult`
- `philharmonica.adk.types.CodeInterpreterToolCall`
- `philharmonica.adk.types.CodeInterpreterToolCallResult`
- `philharmonica.adk.types.CodeInterpreterOutput`
- `philharmonica.adk.types.ComputerToolCall`
- `philharmonica.adk.types.ComputerToolCallResult`
- `philharmonica.adk.types.ComputerAction`
- `philharmonica.adk.types.ImageGenerationToolCall`
- `philharmonica.adk.types.ImageGenerationToolCallResult`
- `philharmonica.adk.types.ShellToolCall`
- `philharmonica.adk.types.ShellToolCallResult`
- `philharmonica.adk.types.ApplyPatchToolCall`
- `philharmonica.adk.types.ApplyPatchToolCallResult`
- `philharmonica.adk.types.ToolSearchToolCall`
- `philharmonica.adk.types.ToolSearchToolCallResult`
- `philharmonica.adk.types.ToolSearchResultEntry`
- `philharmonica.adk.types.MCPListTools`
- `philharmonica.adk.types.MCPListToolsTool`
- `philharmonica.adk.types.MCPCall`
- `philharmonica.adk.types.MCPCallResult`
- `philharmonica.adk.types.MCPApprovalRequest`
- `philharmonica.adk.types.MCPApprovalResponse`

## Tracing span data

- `philharmonica.adk.types.SpanData`
- `philharmonica.adk.types.AgentSpanData`
- `philharmonica.adk.types.FunctionSpanData`
- `philharmonica.adk.types.GenerationSpanData`
- `philharmonica.adk.types.GuardrailSpanData`
- `philharmonica.adk.types.HandoffSpanData`
- `philharmonica.adk.types.ResponseSpanData`
- `philharmonica.adk.types.CustomSpanData`
- `philharmonica.adk.types.AnySpanData`

How the type layers fit together is explained in the
[Types guide](../../types/types.md).
