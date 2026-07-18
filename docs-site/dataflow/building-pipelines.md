---
sidebar_position: 3
---

# Building pipelines

## On the canvas

1. Sign in and land on the pipeline canvas.
2. Drag a **source** node from the palette (any connector in the catalog) onto
   the canvas and configure its fields (URL, auth, filters).
3. Drag a **sink** node and connect source → sink, adding transforms in
   between as needed.
4. **Save** — this creates an immutable pipeline version.
5. Promote through the lifecycle: **Integration** (test run) → **Production**.
6. Run manually, or let Temporal schedule and trigger it; watch progress,
   retries, and backfills from the run view.
7. Check the **Lineage**, **Data Quality**, and **Analytics** tabs for output
   visibility and OpenLineage export.

## With the AI builder

Describe the pipeline in plain English and a **local** LLM (Ollama — no API
key, data stays on your box) drafts the graph:

```
NL prompt ──▶ POST /api/ai/generate ──▶ Ollama (format: json)
                     │  catalog-aware system prompt (every installed connector)
                     │  validated as a DAG  ·  one repair retry
                     ▼
        { mermaid, definition }  ──▶  Mermaid editor ⇄ ReactFlow canvas
```

The system prompt embeds the live connector catalog, so drafts only use
connectors you actually have — including your own manifest connectors. Output
is validated as a well-formed DAG; on failure the model gets one repair
round-trip. `nodes`/`edges` are authoritative — the Mermaid diagram is
regenerated from them, so diagram and definition never disagree.

## Mermaid round-trip

Mermaid is a first-class editing surface: edit the diagram text and the canvas
updates, edit the canvas and the diagram regenerates. Mermaid carries
**structure only** (node ids, labels, activity types, edges, conditions);
node field values are preserved by node id and configured in the canvas.

## Lifecycle and durability

- Every save is an **immutable version** — no in-place edits of running
  definitions.
- **Integration vs Production** run on separate Temporal task queues; a
  pipeline needs a green test run before production promotion.
- Runs survive process restarts: Temporal owns workflow history, retries,
  timers, and signals. Backfills, pause/resume, and cancel are first-class
  operations.
