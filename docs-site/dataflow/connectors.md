---
sidebar_position: 4
---

# Connectors

Connectors come in two flavors, both served by the Go connector registry that
feeds worker dispatch, the API catalog (`GET /api/connectors/catalog`), the
canvas palette, and the AI builder:

1. **Manifest connectors** — a single JSON file. No code. For REST/HTTP
   sources with cursor/page/offset pagination and optional incremental
   watermarking.
2. **Coded connectors** — hand-written Go for anything a manifest can't
   express (OAuth, changes-feeds, GraphQL, SDK auth). The Google Sheets,
   Drive, Excel, and Zendesk connectors are coded.

## A REST source with zero code

Drop a `*.manifest.json` file into a directory the registry loads:

- **Bundled:** `connectors/manifests/` (mounted into the image).
- **Your own, no rebuild:** set `CONNECTORS_DIR` to a mounted directory and
  restart the worker + API.

It then appears in the catalog, palette, and AI builder, and the worker can
run it.

```json
{
  "activityType": "rest.jsonplaceholder.fetch",
  "label": "JSONPlaceholder (demo REST)",
  "kind": "source",
  "url": "https://jsonplaceholder.typicode.com/posts",
  "method": "GET",
  "pagination": { "style": "page", "param": "_page", "limitParam": "_limit", "limit": 20 },
  "fields": [
    { "key": "userId", "label": "Filter by userId (optional)", "type": "text" }
  ]
}
```

## Manifest schema

| Field | Required | Notes |
|-------|----------|-------|
| `activityType` | yes | Unique catalog key, e.g. `rest.acme.fetch`. |
| `label` | yes | Display name in the palette/AI. |
| `kind` | yes | `source` or `sink`. |
| `url` | yes | May contain `{placeholders}` filled from node config. |
| `method` | no | Default `GET`. |
| `recordsPath` | no | Dotted path to the records array (e.g. `data.items`). |
| `headers` | no | Static headers merged with per-node config. |
| `auth` | no | `{ "type": "bearer"\|"header"\|"basic", "tokenField": "<config key>", "headerName": "..." }` — the secret comes from node config. |
| `pagination` | no | `{ "style": "cursor"\|"page"\|"offset", "param", "cursorPath", "limitParam", "limit" }`. |
| `incremental` | no | `{ "sinceParam": "updated_after", "recordTimestampPath": "updated_at" }`. |
| `fields` | no | Extra config inputs rendered on the node. |

## Coded plugins

When a manifest is not enough, register a source or sink in the Go runtime
(`apps/workflow-go/internal/connectors/`):

```go
func (r *Runtime) registerAcme() {
    r.Sources["acme.fetch"] = r.acmeFetch
}

func (r *Runtime) acmeFetch(ctx context.Context, p SourceParams) (SourceResult, error) {
    return SourceResult{Records: []interface{}{}, NextCursor: p.Cursor}, nil
}
```

Add catalog metadata on the frontend when the connector needs canvas
configuration fields. Full detail:
[CONNECTORS.md](https://github.com/Cohestra/cohestra-dataflow/blob/main/docs/CONNECTORS.md).
