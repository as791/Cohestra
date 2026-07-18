---
sidebar_position: 6
---

# Deployment

## Local (Kind + Helm)

`./scripts/bootstrap.sh` stands up the full stack in a local Kind cluster via
the Helm chart in `deploy/helm/dataflow` — web, API, workers, PostgreSQL,
Redis, ClickHouse, Temporal, and Ollama. See
[Getting started](getting-started.md).

## GCP demo topology

`infra/` provisions a pre-release demo topology with Terraform:

- One GCE VM running a Kind cluster and the DataFlow Helm release.
- Caddy on the VM for HTTPS (automatic Let's Encrypt certificates).
- A static public IP; the app URL derives from it.
- A separate persistent disk mounted at `/var/lib/docker` holding PostgreSQL,
  Redis, ClickHouse, and Ollama PVC contents — `prevent_destroy` protected,
  with daily snapshots (14-day retention). Replacing the VM does not delete
  the database disk.
- Secrets in GCP Secret Manager, readable only by a dedicated runtime service
  account.

This improves demo persistence; it is **not** highly available. One VM, one
zone, one Kubernetes node, one database replica are shared failure domains.

Full runbook:
[DEPLOYMENT_GCP.md](https://github.com/Cohestra/cohestra-dataflow/blob/main/docs/DEPLOYMENT_GCP.md).

## Security posture

- Tenant-aware PostgreSQL row-level security on every tenant-facing query.
- Encrypted credentials and payloads; AES-256-GCM Temporal payload codec.
- Audit events for security-relevant actions.
- CI: secret scan, CodeQL/SAST, dependency and license policy,
  vulnerability scans.

Compliance readiness and gaps:
[SECURITY_COMPLIANCE.md](https://github.com/Cohestra/cohestra-dataflow/blob/main/docs/SECURITY_COMPLIANCE.md).
