"""Framework-level tracing for the Philharmonica Agents ADK.

The tracing layer is opt-in and provider-agnostic:

- ``Tracer`` — protocol that observability backends implement.
- ``NoOpTracer`` — default; records nothing and costs nothing.
- ``get_tracer`` / ``set_tracer`` — install a tracer
  process-wide.
- ``Span`` — generic span wrapper parameterised by a
  ``SpanData`` payload.
- ``*_span()`` factories — one per built-in span kind, plus
  ``custom_span`` for developer-authored spans.
- ``MultiTracer`` — fan-out composite that forwards every span
  to an arbitrary number of inner tracers simultaneously. Pair an
  ``OTelTracer`` with an in-memory recorder for tests, or fan
  out to two observability backends at once.
- ``TracingConvention`` —
  span-attribute vocabulary selector (``DEFAULT`` vs ``OPENINFERENCE``).
  Unconditionally available; no optional extra required.
- ``log_event`` — emit a structured log
  record carrying an event name and arbitrary key/value fields.
  Unconditionally available.

OpenTelemetry bridge
--------------------

``OTelTracer``, ``setup_otel``, ``MetricsTracer``, and
``setup_metrics`` are re-exported at the package level **only** when
the optional ``opentelemetry`` extras are installed. Install via::

    pip install 'philharmonica-adk[otel]'

When the extras are missing these names resolve to ``None`` (so the
import does not raise) — guard with ``if OTelTracer is None``.
"""

from __future__ import annotations

from philharmonica.adk.tracing.logging import log_event
from philharmonica.adk.tracing.multi_tracer import MultiTracer
from philharmonica.adk.tracing.spans import (
    NoOpSpan,
    Span,
    agent_span,
    current_span,
    custom_span,
    function_span,
    generation_span,
    graph_node_span,
    graph_span,
    graph_superstep_span,
    guardrail_span,
    handoff_span,
    response_span,
    sandbox_span,
    swarm_span,
    swarm_turn_span,
)
from philharmonica.adk.tracing.tracer import Flushable, NoOpTracer, Tracer, flush_traces, get_tracer, set_tracer
from philharmonica.adk.types.tracing.convention import TracingConvention

__all__ = [
    "Flushable",
    "MultiTracer",
    "NoOpSpan",
    "NoOpTracer",
    "Span",
    "Tracer",
    "TracingConvention",
    "agent_span",
    "current_span",
    "custom_span",
    "flush_traces",
    "function_span",
    "generation_span",
    "get_tracer",
    "graph_node_span",
    "graph_span",
    "graph_superstep_span",
    "guardrail_span",
    "handoff_span",
    "log_event",
    "response_span",
    "sandbox_span",
    "set_tracer",
    "swarm_span",
    "swarm_turn_span",
]


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Type-check-time: the extras are assumed installed. Downstream code
    # that wants to narrow on missing-extra should compare
    # ``OTelTracer is None`` / ``setup_otel is None`` /
    # ``MetricsTracer is None`` / ``setup_metrics is None`` explicitly.
    from philharmonica.adk.tracing.metrics import MetricsTracer, setup_metrics
    from philharmonica.adk.tracing.otel import OTelTracer, setup_otel, setup_otel_from_env

    __all__.extend(["MetricsTracer", "OTelTracer", "setup_metrics", "setup_otel", "setup_otel_from_env"])
else:
    try:
        from philharmonica.adk.tracing.metrics import MetricsTracer, setup_metrics
        from philharmonica.adk.tracing.otel import OTelTracer, setup_otel, setup_otel_from_env

        __all__.extend(["MetricsTracer", "OTelTracer", "setup_metrics", "setup_otel", "setup_otel_from_env"])
    except ImportError as _exc:
        # Only swallow "opentelemetry not installed" — any other ImportError
        # (e.g. a typo inside otel_tracer.py or metrics/) must surface, not
        # be masked as "extra missing".
        if _exc.name is None or not _exc.name.startswith("opentelemetry"):
            raise
        OTelTracer = None
        setup_otel = None
        setup_otel_from_env = None
        MetricsTracer = None
        setup_metrics = None
