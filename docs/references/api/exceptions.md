(references/api/exceptions)=

# Exceptions

The framework exception hierarchy. Every exception derives from
`PhilharmonicaError`, so a single `except PhilharmonicaError` catches all
framework-raised failures.

## Base

- `philharmonica.adk.exceptions.PhilharmonicaError`

## Concrete exceptions

- `philharmonica.adk.exceptions.AgentInputGuardrailTripwireTriggered`
- `philharmonica.adk.exceptions.AgentOutputGuardrailTripwireTriggered`
- `philharmonica.adk.exceptions.AgentToolDeferral`
- `philharmonica.adk.exceptions.ApplyPatchError`
- `philharmonica.adk.exceptions.CheckpointConflictError`
- `philharmonica.adk.exceptions.ConfigError`
- `philharmonica.adk.exceptions.ConfigParseError`
- `philharmonica.adk.exceptions.ConfigResolutionError`
- `philharmonica.adk.exceptions.DocumentLoadError`
- `philharmonica.adk.exceptions.ExecFailureError`
- `philharmonica.adk.exceptions.ExecNonZeroError`
- `philharmonica.adk.exceptions.ExecTimeoutError`
- `philharmonica.adk.exceptions.ExecTransportError`
- `philharmonica.adk.exceptions.ExposedPortUnavailableError`
- `philharmonica.adk.exceptions.GitArtifactError`
- `philharmonica.adk.exceptions.GraphNodeTimeoutError`
- `philharmonica.adk.exceptions.GuardrailTripwireTriggered`
- `philharmonica.adk.exceptions.HandoffDefinitionError`
- `philharmonica.adk.exceptions.HandoffRejection`
- `philharmonica.adk.exceptions.InvalidCompressionSchemeError`
- `philharmonica.adk.exceptions.InvalidManifestPathError`
- `philharmonica.adk.exceptions.LocalArtifactError`
- `philharmonica.adk.exceptions.MaxTurnsExceeded`
- `philharmonica.adk.exceptions.MemoryExtractionError`
- `philharmonica.adk.exceptions.ModelRefusalError`
- `philharmonica.adk.exceptions.MountArtifactError`
- `philharmonica.adk.exceptions.NoRoutingCandidateError`
- `philharmonica.adk.exceptions.NodeRetriesExhaustedError`
- `philharmonica.adk.exceptions.PtySessionNotFoundError`
- `philharmonica.adk.exceptions.QuotaExceeded`
- `philharmonica.adk.exceptions.SandboxArtifactError`
- `philharmonica.adk.exceptions.SandboxCommandRejected`
- `philharmonica.adk.exceptions.SandboxConcurrencyError`
- `philharmonica.adk.exceptions.SandboxConfigurationError`
- `philharmonica.adk.exceptions.SandboxError`
- `philharmonica.adk.exceptions.SandboxNetworkPolicyViolation`
- `philharmonica.adk.exceptions.SandboxResourceLimitExceeded`
- `philharmonica.adk.exceptions.SandboxRuntimeError`
- `philharmonica.adk.exceptions.SandboxSelectionError`
- `philharmonica.adk.exceptions.SandboxStartFailed`
- `philharmonica.adk.exceptions.SandboxStopFailed`
- `philharmonica.adk.exceptions.SessionAppendConflictError`
- `philharmonica.adk.exceptions.SkillsConfigError`
- `philharmonica.adk.exceptions.SnapshotError`
- `philharmonica.adk.exceptions.SnapshotNotRestorableError`
- `philharmonica.adk.exceptions.SnapshotPersistError`
- `philharmonica.adk.exceptions.SnapshotRestoreError`
- `philharmonica.adk.exceptions.TenantBudgetExceeded`
- `philharmonica.adk.exceptions.ToolDependencyError`
- `philharmonica.adk.exceptions.ToolGuardrailTripwireTriggered`
- `philharmonica.adk.exceptions.ToolNotPermittedForTenant`
- `philharmonica.adk.exceptions.ToolRetry`
- `philharmonica.adk.exceptions.ToolTimeoutError`
- `philharmonica.adk.exceptions.ToolsetNameConflictError`
- `philharmonica.adk.exceptions.TracingDependencyError`
- `philharmonica.adk.exceptions.UnsupportedDocumentSourceError`
- `philharmonica.adk.exceptions.UnsupportedManifestEntryError`
- `philharmonica.adk.exceptions.UnsupportedMountPatternError`
- `philharmonica.adk.exceptions.UnsupportedMountStrategyError`
- `philharmonica.adk.exceptions.UnsupportedSandboxClientError`
- `philharmonica.adk.exceptions.UnsupportedSnapshotFeatureError`
- `philharmonica.adk.exceptions.UsageLimitExceeded`
- `philharmonica.adk.exceptions.UserError`
- `philharmonica.adk.exceptions.WorkspaceArchiveReadError`
- `philharmonica.adk.exceptions.WorkspaceArchiveWriteError`
- `philharmonica.adk.exceptions.WorkspaceIOError`
- `philharmonica.adk.exceptions.WorkspaceReadNotFoundError`

Domain-specific exceptions also live next to their modules — see
[Flows](flows.md) (flow execution), [MCP](mcp.md),
and [A2A](a2a.md).
