"""OpenTelemetry bridge for the Philharmonica tracing layer.

Opt-in integration: install the ``otel`` extra with
``pip install 'philharmonica-adk[otel]'``. If the OpenTelemetry packages are
not importable, constructing ``OTelTracer`` or calling
``setup_otel`` raises
``TracingDependencyError`` with the install
command.

See ``docs/tracing/otel.md`` for the full walkthrough.
"""

from __future__ import annotations

from philharmonica.adk.tracing.otel.otel_span import OTelSpan
from philharmonica.adk.tracing.otel.otel_tracer import OTelTracer
from philharmonica.adk.tracing.otel.setup import setup_otel, setup_otel_from_env

__all__ = [
    "OTelSpan",
    "OTelTracer",
    "setup_otel",
    "setup_otel_from_env",
]
