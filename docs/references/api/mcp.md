(references/api/mcp)=

# MCP

Model Context Protocol integration: server transports, lifecycle
management, and tool filtering.

The `mcp` package is an optional extra. When it is not installed, every
name below is bound to `None` so callers can detect availability without
`ImportError` handling.

## Servers and transports

- `philharmonica.adk.mcp.MCPServerWithClientSession`
- `philharmonica.adk.mcp.MCPServerStdio`
- `philharmonica.adk.mcp.MCPServerStdioParams`
- `philharmonica.adk.mcp.MCPServerStreamableHttp`
- `philharmonica.adk.mcp.MCPServerStreamableHttpParams`
- `philharmonica.adk.mcp.MCPServerSse`
- `philharmonica.adk.mcp.MCPServerSseParams`
- `philharmonica.adk.mcp.MCPServerWebsocket`
- `philharmonica.adk.mcp.MCPServerWebsocketParams`

## Lifecycle

- `philharmonica.adk.mcp.MCPServerManager`

## Filters

- `philharmonica.adk.mcp.ToolFilter`
- `philharmonica.adk.mcp.ToolFilterContext`

## Auth and elicitation

- `philharmonica.adk.mcp.HeaderProvider`
- `philharmonica.adk.mcp.ElicitationHandler`

## Exceptions

- `philharmonica.adk.mcp.MCPError`
- `philharmonica.adk.mcp.MCPConnectionError`
- `philharmonica.adk.mcp.MCPToolCallError`
- `philharmonica.adk.mcp.MCPToolNotFoundError`
- `philharmonica.adk.mcp.MCPSchemaConversionError`
- `philharmonica.adk.mcp.UnsupportedTransportError`

The agent-facing adapter `MCPToolset` is a `Toolset` subclass and lives
under `philharmonica.adk.tools.toolsets.mcp_toolset`. Usage lives in the
[MCP guide](../../mcp/mcp.md).
