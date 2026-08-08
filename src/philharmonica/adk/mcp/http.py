"""Streamable HTTP transport MCP server.

Connects to an MCP server over HTTP using ``streamable_http_client``
(HTTP POST + SSE for server-pushed messages). Per-request header
injection is implemented via an HTTP request event hook that reads from
the ``active_header_provider`` ``ContextVar`` — concurrent agent runs
each see their own headers without cross-contamination.

The MCP client library builds on ``httpx2``, so every client, timeout,
limit, and auth object on this transport is an ``httpx2`` one. That is a
distribution distinct from ``httpx``; the two can coexist in one
environment but their types are not interchangeable.

Reference: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#streamable-http
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, override

import httpx2
from mcp.client.streamable_http import streamable_http_client

from philharmonica.adk.mcp.auth import HeaderProvider, active_header_provider
from philharmonica.adk.mcp.exceptions import MCPConnectionError
from philharmonica.adk.mcp.mcp_server import MCPServerWithClientSession, extract_first_exception
from philharmonica.adk.mcp.run_hooks_bridge import (
    fire_on_mcp_connect,
    fire_on_mcp_connected,
    fire_on_mcp_error,
)

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class MCPServerStreamableHttpParams:
    """Parameters for a streamable HTTP MCP transport.

    Attributes:
        url: The MCP server endpoint URL (typically ending in ``/mcp``).
        headers: Static headers attached to every request. Merged
            with any per-request headers from ``header_provider``;
            provider headers win on key collision.
        header_provider: Optional callable returning per-request
            headers. Called fresh on every outbound HTTP request,
            so token rotation works without re-creating the session.
            May be sync or async.
        timeout_seconds: Per-request timeout (HTTP-level). Default
            30 s matches the MCP SDK's default.
        sse_read_timeout_seconds: Maximum time the client will wait
            for the next SSE event before giving up. Default 300 s
            handles long-running tool calls.
        terminate_on_close: When ``True`` (default), send the MCP
            session-terminate signal on cleanup so the server can
            release resources. Set ``False`` only if your server
            needs to keep the session alive across reconnects.
    """

    url: str
    """MCP server endpoint URL (e.g. ``"https://api.example.com/mcp"``)."""

    headers: dict[str, str] | None = field(default=None, repr=False)
    """Static headers attached to every request. ``repr=False`` so
    bearer tokens cannot leak through ``str(params)`` or default
    logging."""

    header_provider: HeaderProvider | None = None
    """Optional per-request callable returning fresh headers (sync or async)."""

    timeout_seconds: float = 30.0
    """HTTP-level per-request timeout (default 30 s, matches MCP SDK)."""

    sse_read_timeout_seconds: float = 300.0
    """Max wait between SSE events (default 300 s, accommodates long calls)."""

    terminate_on_close: bool = True
    """Send MCP session-terminate on cleanup so the server releases resources."""

    idle_timeout: timedelta | None = None
    """Maximum time an idle keep-alive connection may remain open before the
    HTTP client closes it.  Wired via ``httpx2.Limits.keepalive_expiry`` on
    the underlying client pool — the MCP client library exposes no
    idle-timeout parameter of its own.  ``None`` (default) leaves the
    built-in pool defaults unchanged, preserving existing behaviour."""

    httpx_client: httpx2.AsyncClient | None = field(default=None, repr=False)
    """Pre-built ``httpx2.AsyncClient`` to use for all HTTP requests.

    Configure timeouts and pool limits on the client itself —
    ``timeout_seconds`` and the other client-construction fields do not
    apply on this path (``headers``/``idle_timeout`` are rejected
    outright when combined with a pre-built client).

    When set, the server's ``connect()`` forwards the client to
    ``streamable_http_client(http_client=...)`` instead of constructing one
    via ``_build_http_client``.  A client supplied here stays the caller's
    to close: neither this transport nor the MCP client library enters or
    closes a client it did not create.

    Mutually exclusive with ``httpx_client_factory``: setting both raises
    ``ValueError`` at construction time.

    ``repr=False`` so credentials embedded in custom clients cannot leak
    through ``str(params)`` or default logging."""

    httpx_client_factory: Any | None = None
    """Optional factory callable used to construct the ``httpx2.AsyncClient``.

    Conforms to ``mcp.shared._httpx_utils.McpHttpClientFactory`` —
    ``(headers, timeout, auth) -> httpx2.AsyncClient``.  When ``None``
    (the default), the server builds its own client via
    ``_build_http_client`` which installs the dynamic-header event hook
    for per-request token rotation.

    A client the factory returns is closed with the transport, since this
    server is the one that asked for it.

    Mutually exclusive with ``httpx_client``: setting both raises
    ``ValueError`` at construction time."""

    def __post_init__(self) -> None:
        if self.httpx_client is not None and self.httpx_client_factory is not None:
            raise ValueError(
                "MCPServerStreamableHttpParams: 'httpx_client' and 'httpx_client_factory' "
                "are mutually exclusive — supply at most one."
            )
        if self.httpx_client is not None:
            # A pre-built client carries its own headers/limits; these
            # fields would be silently ignored on that path, so reject
            # the ambiguous combination outright.
            ignored = [
                name
                for name, value in (("headers", self.headers), ("idle_timeout", self.idle_timeout))
                if value is not None
            ]
            if len(ignored) > 0:
                raise ValueError(
                    f"MCPServerStreamableHttpParams: {', '.join(ignored)} cannot be combined with "
                    f"'httpx_client' — configure them on the client you pass in instead."
                )


class MCPServerStreamableHttp(MCPServerWithClientSession):
    """MCP server over the streamable HTTP transport.

    Per-request header injection lets a single connection serve
    rotating tokens. The HTTP client is built once at ``connect``
    time with both static ``headers`` and the request event hook
    that consults ``active_header_provider`` on every call.

    Example::

        server = MCPServerStreamableHttp(
            name="github",
            params=MCPServerStreamableHttpParams(
                url="https://api.example.com/mcp",
                header_provider=lambda: {"Authorization": f"Bearer {fresh_token()}"},
            ),
        )
        async with server:
            tools = await server.list_tools()
    """

    def __init__(
        self,
        *,
        name: str,
        params: MCPServerStreamableHttpParams,
        cache_tools_list: bool = True,
        use_structured_content: bool = False,
        llm: Any | None = None,
        elicitation_callback: Any | None = None,
    ) -> None:
        """Initialise the streamable HTTP MCP server.

        Args:
            name: Human-readable server name used in log messages and
                error reports.
            params: Connection and timeout parameters for the HTTP
                transport.
            cache_tools_list: When ``True`` (default), the tool list
                is cached between turns and invalidated by push
                notifications.
            use_structured_content: When ``True``, pass
                ``structuredContent`` through to the artifact channel.
                Default ``False`` avoids duplicate content.
            llm: Optional ``LLM`` for serving MCP
                ``sampling/createMessage`` requests.
            elicitation_callback: Optional async callable invoked on
                ``elicitation/create`` requests from the server.
        """
        super().__init__(
            name=name,
            cache_tools_list=cache_tools_list,
            use_structured_content=use_structured_content,
            header_provider=params.header_provider,
            llm=llm,
            elicitation_callback=elicitation_callback,
        )
        self._params = params
        self._exit_stack: AsyncExitStack | None = None

    @override
    async def connect(self) -> None:
        """Open the HTTP client and initialise the MCP session.

        ``streamable_http_client`` takes a ready client rather than the
        ingredients for one, so whatever ``headers`` / ``timeout_seconds`` /
        ``sse_read_timeout_seconds`` / ``idle_timeout`` describe is composed
        onto the client here, before the transport opens.

        Two client-construction paths are available:

        1. ``params.httpx_client`` is set — the pre-built client is
           forwarded as-is and stays the caller's to close. Neither this
           method nor the transport enters a client it did not create, so
           the same client can outlive the session or serve several.
        2. Neither field is set, or ``params.httpx_client_factory`` is —
           the client is built here, by the factory when one is supplied
           and otherwise by ``_build_http_client``, which installs the
           dynamic-header event hook for per-request token rotation via
           ``active_header_provider``. A client built here is entered on
           the exit stack, so ``cleanup`` closes it.
        """
        async with self._connect_lock:
            if self._session is not None:
                return
            await fire_on_mcp_connect(self._name)
            stack = AsyncExitStack()
            try:
                client = self._params.httpx_client
                if client is None:
                    factory = self._params.httpx_client_factory or self._build_http_client
                    client = factory(
                        headers=self._params.headers,
                        timeout=httpx2.Timeout(
                            self._params.timeout_seconds,
                            read=self._params.sse_read_timeout_seconds,
                        ),
                        auth=None,
                    )
                    # Entered before the transport, so it is closed after it:
                    # the transport still has a live client while it sends
                    # the session-terminate signal on the way out.
                    await stack.enter_async_context(client)
                streams = await stack.enter_async_context(
                    streamable_http_client(
                        self._params.url,
                        http_client=client,
                        terminate_on_close=self._params.terminate_on_close,
                    )
                )
                read, write, *_ = streams
                session = await stack.enter_async_context(
                    self._make_client_session(
                        read,
                        write,
                        read_timeout_seconds=timedelta(seconds=self._params.sse_read_timeout_seconds),
                    )
                )
                await self._attach_session(session)
                self._exit_stack = stack
                logger.info("MCP HTTP server %r connected (%s)", self._name, self._params.url)
                await fire_on_mcp_connected(self._name)
            except (Exception, asyncio.CancelledError) as exc:
                # CancelledError handling: anyio task groups inside the
                # MCP SDK cancel the parent task on internal failure
                # (e.g. ``httpcore.ConnectError`` from a background HTTP
                # task). The cancellation surfaces here as
                # ``asyncio.CancelledError``; ``stack.aclose()`` then
                # propagates the underlying error as an
                # ``ExceptionGroup`` from the SDK's task group. We
                # close the stack defensively so a more specific
                # error from there supersedes the CancelledError, and
                # always end with ``MCPConnectionError`` so callers
                # have a stable exception type. External cancellation
                # (``task.cancelling() > 0``) is re-raised intact.
                root_exc: BaseException = exc
                try:
                    await stack.aclose()
                except (Exception, BaseExceptionGroup) as close_exc:
                    # Prefer the cleanup error when the outer was a
                    # bare CancelledError — the group typically carries
                    # the actual httpx / httpcore root cause.
                    if isinstance(exc, asyncio.CancelledError):
                        root_exc = extract_first_exception(close_exc)
                if isinstance(root_exc, asyncio.CancelledError):
                    task = asyncio.current_task()
                    if task is not None and task.cancelling() > 0:
                        raise
                logger.error("MCP HTTP server %r failed to connect: %s", self._name, root_exc)
                await fire_on_mcp_error(self._name, root_exc)
                raise MCPConnectionError(f"MCP HTTP server '{self._name}' failed to connect: {root_exc}") from root_exc

    @override
    async def cleanup(self) -> None:
        """Close the session and HTTP client; idempotent.

        Anyio's ``RuntimeError("Attempted to exit ...cancel scope...")``
        is demoted to DEBUG. Same rationale as
        ``MCPServerStdio.cleanup``: the SDK opens an internal task
        group whose background cancellation surfaces as a scope
        mismatch on close. ``startswith("Attempted to exit")`` is
        the deliberate narrow filter — the MCP SDK's
        ``"No active cancel scope"`` is left at WARNING.
        """
        async with self._connect_lock:
            if self._exit_stack is None:
                return
            await self._detach_session()
            try:
                await self._exit_stack.aclose()
            except RuntimeError as exc:
                if str(exc).startswith("Attempted to exit"):
                    logger.debug(
                        "MCP HTTP server %r cleanup: anyio cancel-scope mismatch (HTTP client already torn down)",
                        self._name,
                    )
                else:
                    logger.warning("MCP HTTP server %r cleanup raised", self._name, exc_info=True)
            except Exception:
                logger.warning("MCP HTTP server %r cleanup raised", self._name, exc_info=True)
            finally:
                self._exit_stack = None
                logger.info("MCP HTTP server %r disconnected", self._name)

    # ------------------------------------------------------------------
    # HTTP client construction with per-request header injection
    # ------------------------------------------------------------------

    def _build_http_client(
        self,
        headers: dict[str, str] | None = None,
        timeout: httpx2.Timeout | None = None,
        auth: httpx2.Auth | None = None,
    ) -> httpx2.AsyncClient:
        """``McpHttpClientFactory`` implementation.

        Called from ``connect`` with the ``headers`` / ``timeout`` composed
        from the transport params. We install the dynamic header event hook
        so per-request headers from ``active_header_provider`` apply on
        every outbound call — a single client handles per-call token
        rotation without forcing a reconnect.

        When ``MCPServerStreamableHttpParams.idle_timeout`` is set,
        an ``httpx2.Limits`` object is passed with ``keepalive_expiry`` equal
        to that duration.  When ``idle_timeout`` is ``None`` (the default),
        the ``limits`` kwarg is omitted entirely so the built-in pool
        defaults apply (``max_connections=100``,
        ``max_keepalive_connections=20``).

        Args:
            headers: Static headers for every request on this client.
            timeout: Composed timeout object; ``None`` uses the default.
            auth: Composed auth object; ``None`` for no authentication.

        Returns:
            An ``httpx2.AsyncClient`` with the dynamic-header event
            hook installed.
        """
        # Only pass `limits` when idle_timeout is explicitly set.  Passing
        # httpx2.Limits() (even with all defaults) overrides the built-in
        # pool limits (max_connections=100, max_keepalive_connections=20) with
        # unlimited values, which is a silent resource regression for callers
        # who do not set idle_timeout.
        if self._params.idle_timeout is not None:
            # httpx2.Limits defaults max_connections / max_keepalive_connections
            # to None (unbounded) unless given explicitly, so we must restate
            # the bounded defaults alongside keepalive_expiry — passing
            # keepalive_expiry alone would silently uncap the pool.
            return httpx2.AsyncClient(
                headers=headers or {},
                timeout=timeout,
                auth=auth,
                limits=httpx2.Limits(
                    max_connections=100,
                    max_keepalive_connections=20,
                    keepalive_expiry=self._params.idle_timeout.total_seconds(),
                ),
                event_hooks={"request": [_inject_dynamic_headers]},
            )
        return httpx2.AsyncClient(
            headers=headers or {},
            timeout=timeout,
            auth=auth,
            event_hooks={"request": [_inject_dynamic_headers]},
        )


async def _inject_dynamic_headers(request: httpx2.Request) -> None:
    """Apply headers from the active ``HeaderProvider`` to ``request``.

    Sync providers are called inline; async providers are awaited.
    Provider exceptions are logged and swallowed so a transient
    auth failure does not crash the entire request lifecycle —
    callers see the underlying server response (typically 401).

    Args:
        request: The outbound ``httpx2.Request`` whose headers will be
            mutated in place with values from the provider.
    """
    provider = active_header_provider.get()
    if provider is None:
        return
    try:
        result = provider()
        if inspect.isawaitable(result):
            headers = await result
        else:
            headers = result
    except Exception:
        logger.warning(
            "MCP header_provider raised; sending request without dynamic headers",
            exc_info=True,
        )
        return
    for key, value in headers.items():
        request.headers[key] = value
