---
sidebar_position: 2
---

# Getting started

## Requirements

- Docker Desktop with at least 8 GB RAM and 4 CPUs
- Node.js 20+ and npm
- Kind, `kubectl`, and Helm
- Go version declared by `apps/workflow-go/go.mod` (backend development only)

## Full local stack

```bash
git clone https://github.com/Cohestra/cohestra-dataflow.git
cd cohestra-dataflow
./scripts/bootstrap.sh
./scripts/smoke-test.sh
```

Bootstrap creates `.env`, generates JWT/OAuth/Temporal keys and the worker
keypair, builds local images, creates a Kind cluster, and installs the Helm
release (including Ollama for the AI builder).

| Service | URL |
| --- | --- |
| Web | `http://localhost:3002` |
| API health | `http://localhost:3002/api/health` |
| Temporal UI | `http://localhost:8082` |

Tear down deliberately:

```bash
kind delete cluster --name dataflow
```

## Frontend development

```bash
npm install
npm -w apps/web run dev     # Vite at :3000, proxies /api to :4000
npm -w apps/web run build
npm -w apps/web test
```

## Backend development

```bash
cd apps/workflow-go
go test -race ./...
go vet ./...
```

Run the three processes separately when debugging:

```bash
npm run dev:api
npm run dev:workflow-worker
npm run dev:activity-worker
```

## Hosted demo

A live demo runs at [dataflow.cohestra.dev](https://dataflow.cohestra.dev).
It is a single-VM demo deployment — see
[deployment](deployment.md) for the topology and its limits.
