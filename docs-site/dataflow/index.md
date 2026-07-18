---
slug: /
sidebar_position: 1
---

# DataFlow

Visual, durable data pipelines powered by Go and Temporal.

DataFlow is an Apache-2.0 open-core data-pipeline platform. A React canvas
creates versioned DAGs; a Go API and workers execute them durably through
Temporal. PostgreSQL stores tenant and pipeline state, Redis carries bounded
events and rate limits, ClickHouse serves analytics, and encrypted `DataRef`
objects move larger payloads outside workflow history.

**Try it:** [dataflow.cohestra.dev](https://dataflow.cohestra.dev) ·
**Source:** [github.com/Cohestra/cohestra-dataflow](https://github.com/Cohestra/cohestra-dataflow)

## Highlights

- **Visual builder** — React Flow canvas with Mermaid round-trip editing and a
  local-LLM AI builder that drafts pipelines from plain English.
- **Durable execution** — immutable pipeline versions, Integration → Production
  lifecycle, backfills, pause/resume/cancel, and Temporal retries.
- **Connectors** — manifest-driven HTTP connectors (a JSON file, no code) plus
  coded database, SaaS, file, Kafka, Snowflake, ClickHouse, Iceberg, SFTP,
  Google, Microsoft, and Zendesk paths.
- **Data engineering built in** — cursor/CDC checkpoints, dedupe state, data
  contracts, lineage, quality checks, alerts, analytics dashboards, and
  OpenLineage import/export.
- **Multi-tenant by default** — tenant-aware PostgreSQL row-level security,
  encrypted credentials and payloads, audit events, and workspace access roles.

## Current status

Pre-release demo stage. Good fit: local development, controlled product demos,
architecture and connector validation. Not yet claimed: production readiness,
HA, SOC 2/ISO 27001 compliance, or penetration-test assurance. Release
blockers and acceptance criteria are tracked in the
[roadmap](https://github.com/Cohestra/cohestra-dataflow/blob/main/docs/ROADMAP.md).

## Where next

- [Getting started](getting-started.md) — run the full stack locally.
- [Building pipelines](building-pipelines.md) — canvas, AI builder, lifecycle.
- [Connectors](connectors.md) — add a REST source with zero code.
- [Architecture](architecture.md) — processes, stores, and boundaries.
- [Editions](editions.md) — what is free and what is commercial.
