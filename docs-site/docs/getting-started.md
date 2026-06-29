---
sidebar_position: 2
title: Getting Started
---

# Getting Started

Deploy Cohestra on your Kubernetes cluster and run your first Flink job in under 10 minutes.

## Prerequisites

- Kubernetes cluster (EKS, GKE, AKS, kind, or any conformant cluster)
- [Flink Kubernetes Operator](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/) v1.15+
- Helm 3.x
- kubectl configured for your cluster

## 1. Install Cohestra

```bash
helm repo add cohestra https://cohestra-project.github.io/charts
helm install cohestra cohestra/cohestra \
  --namespace cohestra-system --create-namespace \
  --set temporal.enabled=true \
  --set temporal.web.enabled=true
```

This deploys:
- **Cohestra API Server** — REST API + Operations Console on port 8080
- **Cohestra Worker** — Temporal workflow and activity worker
- **Temporal Server** — durable workflow engine (bundled for trials; bring your own for production)
- **Temporal Web UI** — workflow visibility on port 8088

Verify:

```bash
kubectl get pods -n cohestra-system
curl http://localhost:8080/healthz
# {"status":"ok"}
```

## 2. Register a Deployment

Tell Cohestra about the Flink job you want to manage:

```bash
curl -X PUT http://localhost:8080/api/v1/deployments/prod/streaming/orders \
  -H 'Content-Type: application/json' \
  -d '{
    "owner": "platform-team",
    "serviceAccount": "flink",
    "nodePool": "default"
  }'
```

Or with the Python SDK:

```python
from cohestra_sdk import CohestraClient

client = CohestraClient("http://localhost:8080")
client.register("prod", "streaming", "orders", owner="platform-team")
```

## 3. Deploy Your Flink Job

```bash
curl -X POST http://localhost:8080/api/v1/deployments/prod/streaming/orders/deploy \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: deploy-001' \
  -d '{
    "requester": "ci-pipeline",
    "approved": true,
    "spec": {
      "imageDigest": "your-registry/orders-job@sha256:abc123",
      "flinkVersion": "2.2",
      "parallelism": 8,
      "maxParallelism": 128,
      "resources": {
        "taskManagerCpu": 2,
        "taskManagerMemoryMiB": 4096,
        "taskManagerCount": 2,
        "slotsPerManager": 4
      },
      "stateCompatibility": {
        "jobGraphCompatible": true,
        "operatorUidsStable": true
      }
    }
  }'
```

Cohestra will:
1. Take a savepoint of the running job (if upgrading)
2. Apply the new FlinkDeployment spec via the Kubernetes Operator
3. Wait for the job to reach RUNNING state
4. Verify health gates (checkpoints, restarts, backpressure, Kafka lag)
5. Promote the version or rollback automatically on failure

## 4. Check Status

```bash
curl http://localhost:8080/api/v1/deployments/prod/streaming/orders/actor | jq
```

Response:

```json
{
  "identity": {"environment": "prod", "namespace": "streaming", "name": "orders"},
  "status": "IDLE",
  "currentVersion": {
    "versionId": 1,
    "spec": {...},
    "healthSummary": {
      "healthy": true,
      "running": true,
      "checkpointCompleted": true
    }
  },
  "recentOperations": [
    {"operationId": "deploy-001", "commandType": "DeployVersion", "status": "SUCCEEDED"}
  ]
}
```

## 5. Open the Operations Console

Navigate to `http://localhost:8080` to see the Cohestra dashboard with deployment cards, version history, and operation logs.

## Next Steps

- [Set up custom autoscaling](./autoscaling/overview)
- [Compare Cohestra vs AWS MSF](./comparison)
