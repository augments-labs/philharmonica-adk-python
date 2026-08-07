"""Smart model routing: cheap-first selection with fallback."""

from __future__ import annotations

from philharmonica.adk.llms.routing.cheapest_first import CheapestFirstRouter
from philharmonica.adk.llms.routing.latency_first import LatencyFirstRouter
from philharmonica.adk.llms.routing.router import LLMRouter, RoutedModel, RoutingContext

__all__ = [
    "CheapestFirstRouter",
    "LLMRouter",
    "LatencyFirstRouter",
    "RoutedModel",
    "RoutingContext",
]
