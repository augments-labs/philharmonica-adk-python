# Changelog

<!--include-from-here-->

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-08-08

### Fixed

- `import philharmonica.adk.mcp` raised `ModuleNotFoundError: No module named
  'httpx2'` instead of degrading to `None` bindings when the `mcp` extra was
  not installed. That extra installs two distributions — the `mcp` client and
  `httpx2` — but the guard swallowed only `ImportError(name="mcp")`, and
  `httpx2` is the name actually seen first, since the streamable HTTP
  transport imports it at module level. Both names are now recognised as "the
  extra is absent". The equivalent guard in `philharmonica.adk.tools.toolsets`
  gained the same set; it was unreachable in practice only because
  `MCPToolset` defers its client imports.

## [0.2.0] - 2026-08-08

### Security

- The data-URL pattern behind the multimodal `File` / `Image` types matched in
  exponential time. A `File` argument of the form `data:a/b` followed by a run
  of semicolons and no comma forced the engine through every partition of that
  run: 0.53s at 24 semicolons, and at 40 it does not finish. Since these types
  parse LLM-supplied tool arguments, a single argument could hang the process.
  The pattern is now unambiguous and matches in linear time, accepting exactly
  the same URLs.
- RAG loader routing selected the YouTube and GitHub loaders by testing whether
  the URL's `netloc` *contained* their domain. A netloc carries userinfo, so
  `https://youtube.com@evil.com/watch` routed to the YouTube loader while the
  origin fetched was `evil.com`; `evil-youtube.com.attacker.net` matched on
  suffix alone. Routing now compares the parsed hostname against a domain set
  by equality or subdomain.

### Removed

- **`MCPServerWebsocket` and `MCPServerWebsocketParams`.** The MCP client
  library dropped its WebSocket client, so there is no transport left to wrap.
  Use `MCPServerStreamableHttp`, which carries server-pushed messages over the
  same connection.
- **`UnsupportedTransportError`.** The WebSocket transport was its only
  raiser; nothing in the framework raises it now.

### Changed

- **The `mcp` extra now requires `mcp>=2.0.0`.** The transports are built
  against `streamable_http_client` and the `httpx2` client types, neither of
  which the 1.x line provides.
- **`MCPServerStreamableHttpParams.httpx_client` and `.httpx_client_factory`
  now take `httpx2` objects** (`httpx2.AsyncClient`, `httpx2.Timeout`,
  `httpx2.Auth`) rather than `httpx` ones. `httpx2` is a separate
  distribution that installs alongside `httpx`; the two sets of types are not
  interchangeable. A client you supply yourself stays yours to close; one built
  by the factory is closed with the transport.
- **`MCPServer.read_resource(uri)` forwards the URI string unchanged** instead
  of parsing it into a `pydantic.AnyUrl` first. The protocol types this field
  as an opaque string and leaves scheme interpretation to the server, so URIs
  a strict URL parser rejects now reach the server.

## [0.1.1] - 2026-08-08

### Fixed

- `examples/skills/skills_agent_with_skills.py`: the tool input guardrail read
  `data.agent_output`, which `ToolInputGuardrailData` does not define, so the
  example raised `AttributeError` on its first tool call. It now reads
  `data.context.tool_arguments`.
- `examples/tools/deferred_tools_hitl.py`: the conditional-approval callback
  dereferenced `ctx.context` in a scenario that runs without one, raising
  `AttributeError` on `None`. It now falls back to the non-production branch.
- `examples/config/run_config_agent.py` and
  `examples/tools/tool_advanced_features.py`: reading `.name` off a tool
  collection that can also hold hosted tools and toolsets, neither of which
  defines it.
- `examples/skills/skills_customer_support.py`: the demo account store was
  typed loosely enough that arithmetic on a balance was unsound.
- Assorted typing repairs across the examples suite (`run_examples.py`,
  `toolsets_basic.py`, `llm_orchestrated.py`, `human_in_the_loop.py`,
  `middleware_basic.py`, `agent_guardrails.py`, `message_filters.py`,
  `run_topology.py`).

### Added

- The examples suite is type-checked on every pull request. It was previously
  excluded from the type checker, so a broken attribute access in a shipped
  example could not fail any gate.

### Changed

- The README header logo renders at 256px wide.

## [0.1.0] - 2026-08-07

### Added

- Initial public release of Philharmonica ADK as `philharmonica-adk`: the
  `philharmonica.adk` Python namespace, the `philharmonica` command-line interface, and
  the full agent development toolkit.
