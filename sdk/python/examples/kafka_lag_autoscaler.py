"""
Kafka-lag-based autoscaler for Cohestra — runs as AWS Lambda or standalone.

Scales Flink parallelism proportionally to Kafka consumer lag. Drop this
into a Lambda triggered by EventBridge every 60s, or run it as a script.

Environment variables:
    COHESTRA_URL         — Cohestra API endpoint (e.g. https://cohestra.internal:8080)
    COHESTRA_TOKEN       — Bearer token for auth (optional)
    COHESTRA_ENV         — deployment environment (e.g. prod)
    COHESTRA_NAMESPACE   — Kubernetes namespace (e.g. streaming)
    COHESTRA_NAME        — deployment name (e.g. orders)
    MIN_PARALLELISM — floor (default: 2)
    MAX_PARALLELISM — ceiling (default: 64)
    LAG_PER_SLOT    — target lag per parallelism unit (default: 50000)
"""

from __future__ import annotations

import logging
import math
import os

from cohestra_sdk import CohestraClient, AutoscalerBase, ScaleDecision

logging.basicConfig(level=logging.INFO)


class KafkaLagAutoscaler(AutoscalerBase):
    def __init__(self, client: CohestraClient, env: str, namespace: str, name: str):
        super().__init__(client, env, namespace, name)
        self.min_parallelism = int(os.environ.get("MIN_PARALLELISM", "2"))
        self.max_parallelism = int(os.environ.get("MAX_PARALLELISM", "64"))
        self.lag_per_slot = int(os.environ.get("LAG_PER_SLOT", "50000"))

    def evaluate(self, status: dict) -> ScaleDecision | None:
        current = status["currentVersion"]
        health = current["healthSummary"]
        lag = health.get("kafkaLag", 0)
        current_p = current["spec"]["parallelism"]
        backpressure = health.get("backpressureRatio", 0)

        if lag <= self.lag_per_slot and backpressure < 0.3:
            # scale down if over-provisioned
            ideal = max(self.min_parallelism, math.ceil(lag / max(self.lag_per_slot, 1)))
            if ideal < current_p and (current_p - ideal) >= 2:
                return ScaleDecision(
                    target_parallelism=max(ideal, self.min_parallelism),
                    reason=f"lag={lag} low, reducing from {current_p}",
                )
            return None

        # scale up
        ideal = math.ceil(lag / self.lag_per_slot)
        target = min(max(ideal, self.min_parallelism), self.max_parallelism)

        if target <= current_p:
            return None

        return ScaleDecision(
            target_parallelism=target,
            reason=f"lag={lag} backpressure={backpressure:.2f}, scaling {current_p}→{target}",
        )


def _build() -> KafkaLagAutoscaler:
    client = CohestraClient(
        base_url=os.environ.get("COHESTRA_URL", "http://localhost:8080"),
        token=os.environ.get("COHESTRA_TOKEN"),
    )
    return KafkaLagAutoscaler(
        client,
        env=os.environ.get("COHESTRA_ENV", "integration"),
        namespace=os.environ.get("COHESTRA_NAMESPACE", "streaming"),
        name=os.environ.get("COHESTRA_NAME", "orders"),
    )


# — AWS Lambda handler —

def handler(event, context):
    """EventBridge → Lambda entry point."""
    scaler = _build()
    result = scaler.execute()
    return {"scaled": result is not None, "result": result}


# — standalone —

if __name__ == "__main__":
    scaler = _build()
    scaler.run_loop(interval=60)
