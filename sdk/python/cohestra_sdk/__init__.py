"""Cohestra SDK — Python client for the control plane."""

from cohestra_sdk.client import CohestraClient, Deployment, DeploymentSpec, ResourceShape, StateCompatibility
from cohestra_sdk.autoscaler import AutoscalerBase

__version__ = "0.1.0"
__all__ = [
    "CohestraClient",
    "Deployment",
    "DeploymentSpec",
    "ResourceShape",
    "StateCompatibility",
    "AutoscalerBase",
]
