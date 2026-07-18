"""Typed exceptions for the orchestrator.

Keeping these distinct lets the CLI and orchestrator fail *closed* with clear,
actionable messages instead of leaking raw SSH/API tracebacks into audit logs.
"""

from __future__ import annotations


class OrchestratorError(Exception):
    """Base class for all chkp-cpuse-orch errors."""


class ConfigError(OrchestratorError):
    """Invalid or missing tool configuration."""


class InventoryError(OrchestratorError):
    """Invalid or missing inventory (sites, servers, gateways)."""


class TransportError(OrchestratorError):
    """SSH / REST transport failure reaching a target host."""


class CDTError(OrchestratorError):
    """The Central Deployment Tool reported a failure."""


class CPUSEError(OrchestratorError):
    """A CPUSE / Deployment Agent operation failed on a Gaia host."""


class PreCheckError(OrchestratorError):
    """A pre-deployment health check failed; the run must not proceed."""


class SafetyViolation(OrchestratorError):
    """An action would violate an operational safety constraint (e.g. patching

    both cluster members at once, or running outside the maintenance window).
    """
