"""Tests for idle_timeout on MCPServerStreamableHttpParams / MCPServerStreamableHttp.

Feature: expose idle_timeout: timedelta | None = None on
MCPServerStreamableHttpParams and forward it to the httpx2 client's
Limits.keepalive_expiry via the _build_http_client factory.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any
from unittest.mock import patch

import httpx2
import pytest

from philharmonica.adk.mcp.http import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# ── Parameter construction ─────────────────────────────────────────────────


def test_idle_timeout_default_is_none() -> None:
    params = MCPServerStreamableHttpParams(url="http://localhost/mcp")
    assert params.idle_timeout is None


def test_idle_timeout_accepts_timedelta() -> None:
    td = timedelta(seconds=120)
    params = MCPServerStreamableHttpParams(url="http://localhost/mcp", idle_timeout=td)
    assert params.idle_timeout == td


# ── _build_http_client integration ────────────────────────────────────────


def _make_server(idle_timeout: timedelta | None = None) -> MCPServerStreamableHttp:
    params = MCPServerStreamableHttpParams(
        url="http://localhost/mcp",
        idle_timeout=idle_timeout,
    )
    return MCPServerStreamableHttp(name="test-server", params=params)


def _capture_limits_init(
    captured: list[httpx2.Limits],
) -> Any:
    """Return a patched __init__ that records the ``limits`` kwarg passed to AsyncClient."""
    original_init = httpx2.AsyncClient.__init__

    def _patched(self: httpx2.AsyncClient, *args: Any, **kwargs: Any) -> None:
        if "limits" in kwargs:
            captured.append(kwargs["limits"])
        original_init(self, *args, **kwargs)

    return _patched


def test_build_http_client_no_idle_timeout_omits_limits_kwarg() -> None:
    """When idle_timeout is None the 'limits' kwarg is not passed to AsyncClient.

    Passing httpx2.Limits() explicitly would silently override httpx2's built-in
    pool defaults (max_connections=100) with unlimited values.  Omitting the
    kwarg lets httpx2 apply its defaults, preserving existing resource bounds.
    """
    server = _make_server(idle_timeout=None)
    captured: list[httpx2.Limits] = []

    with patch.object(httpx2.AsyncClient, "__init__", _capture_limits_init(captured)):
        server._build_http_client(headers={}, timeout=None, auth=None)

    # No limits kwarg must be passed when idle_timeout is None.
    assert len(captured) == 0


def test_build_http_client_with_idle_timeout_sets_keepalive_expiry() -> None:
    """When idle_timeout is set, Limits.keepalive_expiry equals the timedelta in seconds."""
    td = timedelta(seconds=90)
    server = _make_server(idle_timeout=td)
    captured: list[httpx2.Limits] = []

    with patch.object(httpx2.AsyncClient, "__init__", _capture_limits_init(captured)):
        server._build_http_client(headers={}, timeout=None, auth=None)

    assert len(captured) == 1
    assert isinstance(captured[0], httpx2.Limits)
    assert captured[0].keepalive_expiry == pytest.approx(td.total_seconds())


def test_build_http_client_idle_timeout_fractional_seconds() -> None:
    """Sub-second timedeltas convert correctly to seconds."""
    td = timedelta(milliseconds=500)
    server = _make_server(idle_timeout=td)
    captured: list[httpx2.Limits] = []

    with patch.object(httpx2.AsyncClient, "__init__", _capture_limits_init(captured)):
        server._build_http_client(headers={}, timeout=None, auth=None)

    assert len(captured) == 1
    assert captured[0].keepalive_expiry == pytest.approx(0.5)


def test_build_http_client_idle_timeout_keeps_pool_bounded() -> None:
    """Setting keepalive_expiry must NOT uncap the connection pool.

    ``httpx2.Limits(keepalive_expiry=...)`` alone leaves max_connections /
    max_keepalive_connections at ``None`` (unbounded) — a silent resource
    regression. The factory must restate httpx2's bounded defaults (100 / 20).
    """
    server = _make_server(idle_timeout=timedelta(seconds=60))
    captured: list[httpx2.Limits] = []

    with patch.object(httpx2.AsyncClient, "__init__", _capture_limits_init(captured)):
        server._build_http_client(headers={}, timeout=None, auth=None)

    assert len(captured) == 1
    limits = captured[0]
    assert limits.max_connections == 100
    assert limits.max_keepalive_connections == 20
    assert limits.keepalive_expiry == pytest.approx(60.0)
