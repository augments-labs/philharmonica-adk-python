# Tasks

Declarative units of work: an agent, a description, and per-call overrides
packaged into named, documented work units executed by the Runner.

## Core

- `philharmonica.adk.tasks.Task`
- `philharmonica.adk.tasks.TaskDependency`
- `philharmonica.adk.tasks.TaskInputFilter`

## Pipelines

- `philharmonica.adk.tasks.TaskPipeline`
- `philharmonica.adk.tasks.TaskPipelineResult`
- `philharmonica.adk.tasks.TaskPipelineState`

## Task groups

- `philharmonica.adk.tasks.TaskGroup`
- `philharmonica.adk.tasks.TaskGroupResult`
- `philharmonica.adk.tasks.ErrorPolicy`

## Input and output

- `philharmonica.adk.tasks.TaskInputData`
- `philharmonica.adk.tasks.TaskOutput`

## Exceptions

- `philharmonica.adk.tasks.TaskPipelineDefinitionError`

Tasks run via `Runner.arun_task`, `Runner.arun_task_pipeline`, and
`Runner.arun_task_group`. Usage lives in the
[Tasks guide](../../tasks/tasks.md).
