"""CDT wrapper — drives Check Point's Central Deployment Tool on a management server.

CDT pushes a package to *many* gateways at once using an XML deployment
configuration plus a target list. This wrapper builds those inputs, invokes the
``cdt`` command over a ``CommandRunner`` (SSH to the management server, expert mode),
and parses the result. All fleet sequencing / batching / safety gating lives in the
orchestrator, not here. See .claude/memory/cdt-cpuse-domain.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .errors import CDTError
from .transport.ssh import CommandRunner


@dataclass
class CDTPlan:
    """Inputs for one CDT deployment.

    Real generated plans reference production gateways and are git-ignored; only the
    shape is defined here. ``build_xml`` / ``build_targets_csv`` render them.
    """

    package_name: str
    targets: list[str]  # gateway names/IPs from the inventory
    reboot: bool = True
    max_concurrent: int = 2  # blast-radius cap; orchestrator sets this
    extra_options: dict[str, str] = field(default_factory=dict)

    def build_targets_csv(self) -> str:
        """Render the CDT target list (one gateway per line)."""
        return "\n".join(self.targets) + "\n"

    def build_xml(self) -> str:
        # TODO: render the CDT deployment XML from this plan. Stubbed so the plan
        # shape is stable and testable before wiring the exact schema.
        raise NotImplementedError("CDT XML rendering not yet implemented")


@dataclass(frozen=True)
class CDTResult:
    """Parsed outcome of a CDT run, per target."""

    succeeded: list[str]
    failed: list[str]
    raw_output: str

    @property
    def all_ok(self) -> bool:
        return not self.failed


class CDT:
    """Central Deployment Tool operations, executed on a management server host."""

    def __init__(self, runner: CommandRunner) -> None:
        self._runner = runner

    def version(self) -> str:
        result = self._runner.run("cdt --version")
        if not result.ok:
            raise CDTError(f"cdt not available on management server: {result.stderr.strip()}")
        return result.stdout.strip()

    def deploy(self, plan: CDTPlan, *, dry_run: bool = True) -> CDTResult:
        """Run a CDT deployment for ``plan``.

        With ``dry_run`` (default) the wrapper renders inputs and returns a preview
        without invoking ``cdt``. Real execution requires ``dry_run=False`` AND that
        the caller (orchestrator) has already passed safety + pre-checks.
        """
        if dry_run:
            return CDTResult(succeeded=[], failed=[], raw_output="[dry-run] no changes made")
        # TODO: stage plan.build_xml()/build_targets_csv() to the mgmt server, invoke
        # `cdt ...`, stream/collect output, then parse via _parse_result.
        raise NotImplementedError("CDT deploy execution not yet implemented")

    @staticmethod
    def _parse_result(_stdout: str) -> CDTResult:
        # TODO: parse cdt run output into per-target success/failure.
        raise NotImplementedError("CDT result parsing not yet implemented")
