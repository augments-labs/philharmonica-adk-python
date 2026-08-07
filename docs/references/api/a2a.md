# A2A

Agent-to-Agent protocol support: independent agents talking to each other
as peers, as protocol clients and as protocol servers.

The `a2a-sdk` package is an optional extra
(`pip install 'philharmonica-adk[a2a]'`). When it is not installed,
every name below is bound to `None` so downstream code can skip A2A
wiring gracefully.

## Client side

- `philharmonica.adk.a2a.A2AAgent`
- `philharmonica.adk.a2a.A2ARunner`
- `philharmonica.adk.a2a.A2AClient`
- `philharmonica.adk.a2a.A2ARunResult`
- `philharmonica.adk.a2a.A2AStreamEvent`

## Server side

- `philharmonica.adk.a2a.A2AServer`
- `philharmonica.adk.a2a.A2AExecutor`
- `philharmonica.adk.a2a.build_starlette_app`

## Long-running tasks

- `philharmonica.adk.a2a.A2AContinuationToken`
- `philharmonica.adk.a2a.A2ATaskStatus`
- `philharmonica.adk.a2a.A2ATaskStateLiteral`
- `philharmonica.adk.a2a.TaskStore`
- `philharmonica.adk.a2a.InMemoryTaskStore`
- `philharmonica.adk.a2a.SQLiteTaskStore`

## Composition

- `philharmonica.adk.a2a.A2AExecutableAdapter`

## Exceptions

- `philharmonica.adk.a2a.A2AError`
- `philharmonica.adk.a2a.A2AProtocolError`
- `philharmonica.adk.a2a.A2ATransportError`
- `philharmonica.adk.a2a.A2ATaskError`
- `philharmonica.adk.a2a.A2ATaskCancelledError`
- `philharmonica.adk.a2a.A2ATaskInterruptedError`

Usage lives in the [A2A guide](../../a2a/a2a.md).
