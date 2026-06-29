---
sidebar_position: 4
title: API Reference
---

# API Reference

Base URL: `http://localhost:8080` (or your Cohestra server)

All mutating endpoints require an `Idempotency-Key` header — use any unique string (UUID, pipeline run ID, etc.) to make operations safe to retry.

---

## Health

### `GET /healthz`

Returns `{"status":"ok"}` when the server is healthy.

---

## Deployments

All deployment endpoints are scoped to `{env}/{namespace}/{name}` — e.g. `prod/streaming/orders`.

### `GET /api/v1/deployments`

List all active deployment actors.

**Query parameters**

| Param | Type | Description |
|---|---|---|
| `environment` | string | Filter by environment |
| `namespace` | string | Filter by namespace |
| `limit` | integer | Page size (1–500, default 100) |
| `pageToken` | string | Pagination cursor |

**Response `200`**
```json
{
  "deployments": [
    {
      "identity": {
        "environment": "prod",
        "namespace": "streaming",
        "name": "orders",
        "owner": "platform-team"
      },
      "workflowId": "...",
      "startedAt": "2024-01-01T00:00:00Z"
    }
  ],
  "nextPageToken": "..."
}
```

---

### `PUT /api/v1/deployments/{env}/{namespace}/{name}`

Register a deployment and start its actor. Idempotent — safe to call if already running.

**Request body**
```json
{
  "owner": "platform-team",
  "serviceAccount": "flink",
  "nodePool": "default",
  "flinkDashboardUrl": "http://flink-dashboard:8081"
}
```

**Response `201`** — actor started or already running.

---

### `GET /api/v1/deployments/{env}/{namespace}/{name}/actor`

Query the full actor state — current version, health, recent operations.

**Response `200`**
```json
{
  "identity": { "environment": "prod", "namespace": "streaming", "name": "orders" },
  "status": "IDLE",
  "currentVersion": {
    "versionId": 3,
    "spec": { "imageDigest": "...", "parallelism": 8 },
    "healthSummary": {
      "healthy": true,
      "running": true,
      "checkpointCompleted": true
    }
  },
  "recentOperations": [
    { "operationId": "deploy-003", "commandType": "DeployVersion", "status": "SUCCEEDED" }
  ]
}
```

---

### `POST /api/v1/deployments/{env}/{namespace}/{name}/deploy`

Submit a controlled rollout. Cohestra takes a savepoint, applies the new spec, waits for RUNNING, checks health gates, and rolls back automatically on failure.

**Headers**
- `Idempotency-Key: <unique-string>` *(required)*

**Request body**
```json
{
  "requester": "ci-pipeline",
  "approved": true,
  "spec": {
    "imageDigest": "registry/job@sha256:abc123",
    "flinkVersion": "2.0",
    "parallelism": 8,
    "maxParallelism": 128,
    "jobArgs": { "topic": "orders" },
    "flinkConfig": { "taskmanager.numberOfTaskSlots": "4" },
    "autoscalerEnabled": false
  }
}
```

| Field | Required | Description |
|---|---|---|
| `imageDigest` | yes | OCI image digest |
| `flinkVersion` | yes | e.g. `"2.0"` |
| `parallelism` | yes | Task parallelism |
| `maxParallelism` | yes | Max for rescaling |
| `requester` | no | Who triggered this |
| `approved` | no | Pre-approval flag |
| `incident` | no | Skip safety gates during incidents |

**Response `202`** — command accepted and queued.

---

### `POST /api/v1/deployments/{env}/{namespace}/{name}/rollback`

Roll back to the last known-good version using its savepoint.

**Headers:** `Idempotency-Key` *(required)*

**Response `202`** — rollback queued.

---

### `POST /api/v1/deployments/{env}/{namespace}/{name}/scale`

Submit a controlled scale operation (parallelism change).

**Headers:** `Idempotency-Key` *(required)*

**Response `202`** — scale queued.

---

### `POST /api/v1/deployments/{env}/{namespace}/{name}/savepoint`

Trigger a savepoint without deploying.

**Headers:** `Idempotency-Key` *(required)*

**Response `202`** — savepoint queued.

---

### `POST /api/v1/deployments/{env}/{namespace}/{name}/suspend`

Suspend a running deployment (takes savepoint, stops job).

**Headers:** `Idempotency-Key` *(required)*

**Response `202`** — suspend queued.

---

### `POST /api/v1/deployments/{env}/{namespace}/{name}/resume`

Resume a suspended deployment from its savepoint.

**Headers:** `Idempotency-Key` *(required)*

**Response `202`** — resume queued.

---

## Cluster

### `POST /api/v1/clusters/{env}/{namespace}/freeze`

Freeze all runtime mutations in a namespace. Queued deploys, scales, and rollbacks are blocked until unfrozen. Use before node pool maintenance or incident triage.

**Response `202`** — freeze signal accepted.

---

### `POST /api/v1/clusters/{env}/{namespace}/unfreeze`

Remove the freeze from a namespace.

**Response `202`** — unfreeze signal accepted.
