"""Agent status tracking and cumulative quota enforcement.

This module provides persistent tracking of agent run metrics
(tokens, requests, errors, duration) and time-windowed quota
enforcement.  It integrates with the Runner via
``StatusTrackingHooks`` — no Runner changes needed.

Usage::

    from philharmonica.adk.status import (
        AgentStatusStore,
        StatusTrackingHooks,
        AgentQuota,
    )

    store = AgentStatusStore(path="agent_status.db")
    hooks = StatusTrackingHooks(
        store=store,
        quotas=[
            AgentQuota(agent_name="*", window_seconds=86400, max_total_tokens=500_000),
        ],
    )
    result = await Runner.arun(agent, "Hello!", hooks=hooks)
"""

from philharmonica.adk.status.hooks import StatusTrackingHooks
from philharmonica.adk.status.store import AgentStatusStore
from philharmonica.adk.status.types import AgentQuota, AgentRunRecord, AgentStatus

__all__ = [
    "AgentQuota",
    "AgentRunRecord",
    "AgentStatus",
    "AgentStatusStore",
    "StatusTrackingHooks",
]
