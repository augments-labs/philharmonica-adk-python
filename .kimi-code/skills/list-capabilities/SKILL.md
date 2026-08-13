---
name: list-capabilities
description: List the current runtime subagents and MCP servers so delegation and live-tool choices use what Kimi Code actually exposes now.
whenToUse: When the user runs /list-capabilities or asks what subagents or MCP servers are available
---

# List Capabilities

Goal: produce the current set of things available for delegation or direct
tool use in this session, drawn from the live runtime rather than
machine-specific install paths.

Do not read `~/.kimi-code/plugins/` install records or any plugin cache
directory. Those paths and layouts differ by machine and version. Runtime
tool metadata is the portable source.

## Subagents

List every subagent type the **Agent** tool exposes in your current system
prompt — that live list is exactly what you can dispatch. Present a compact
table (name · one-line purpose · origin), grouped by origin:

- **Built-in** — the three agents shipped with Kimi Code CLI: `coder`
  (general software engineering), `explore` (read-only codebase
  exploration), and `plan` (read-only implementation planning).
- **Project** — defined in this repo. Identify these precisely with a
  repo-relative listing (portable — no `$HOME`):

  ```bash
  ls .kimi-code/agents/*.md .agents/agents/*.md 2>/dev/null
  ```

- **User / extra / plugin** — any other custom agents the current session
  exposes (from `$KIMI_CODE_HOME/agents/`, `~/.agents/agents/`,
  `extra_agent_dirs`, or enabled plugins).

Use the current runtime tools and project files to identify what is actually
available. Do not invent agents from prose.

## MCP Servers

Separately, list every MCP server exposed this session. MCP tools are named
`mcp__<server>__<tool>` and are direct tools against live systems, not
agents to dispatch. The `/mcp` command shows connection status.

Group by server name and summarize the available tool purpose in one line,
folding in any MCP server instructions in your context.

## Selection Rule

For audit, review, security, testing, quality, documentation, or codebase
search, prefer the matching specialist subagent when one is available;
reserve the built-in `explore`/`coder` for generic lookups and
implementation. Use MCP when the task needs a live external system such as
docs, databases, browser, payments, or workspace data.

Report only what your runtime exposes now. Do not invent agents or servers,
and do not enumerate plugin directories from disk.
