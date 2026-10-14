# AWS AI Agent Lab

A hands-on learning project exploring how to build AI agents with practical governance controls.

The project is inspired by a simple question:

> How can small and medium-sized enterprises keep AI agents responsible and accountable without immediately investing in complex engineering or expensive governance tooling?

## Current focus

The first implementation demonstrates two basic governance controls:

1. **Tool registry** — defines which capabilities are available.
2. **Action policy** — defines which available capabilities are permitted.

The current agent is deliberately local and mocked. It does not call Amazon Bedrock, access AWS resources or execute real infrastructure changes.

## Governance flow

```text
User request
    ↓
Agent identifies intended action
    ↓
Tool registry checks availability
    ↓
Policy checks permission
    ↓
Action executes or is blocked
    ↓
Trace records the outcome
