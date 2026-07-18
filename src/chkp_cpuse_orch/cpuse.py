"""CPUSE wrapper — drives the Deployment Agent on a *single* Gaia host.

Thin by design: it builds clish ``installer`` commands, runs them over a
``CommandRunner``, and parses results. It makes NO sequencing or safety decisions —
those belong to the orchestrator. See .claude/memory/cdt-cpuse-domain.md.

Used primarily to patch **management servers** locally (management servers are not
targeted by CDT).
"""

from __future__ import annotations

from dataclasses import dataclass

from .errors import CPUSEError
from .transport.ssh import CommandRunner


@dataclass(frozen=True)
class PackageState:
    """Parsed state of one CPUSE package on the host."""

    identifier: str
    status: str  # e.g. "Installed", "Imported", "Available"
    description: str = ""


class CPUSE:
    """CPUSE / Deployment Agent operations for one Gaia host."""

    def __init__(self, runner: CommandRunner) -> None:
        self._runner = runner

    # -- read-only -------------------------------------------------------------

    def list_packages(self) -> list[PackageState]:
        """`show installer packages` → parsed package states."""
        result = self._runner.run("clish -c 'show installer packages'")
        if not result.ok:
            raise CPUSEError(f"failed to list packages: {result.stderr.strip()}")
        return self._parse_packages(result.stdout)

    # -- lifecycle (mutating; caller must gate on safety checks) ---------------

    def import_package(self, package_id: str) -> None:
        self._run_installer(f"import imported-package-name {package_id}", "import")

    def verify(self, package_id: str) -> None:
        self._run_installer(f"verify {package_id}", "verify")

    def install(self, package_id: str) -> None:
        self._run_installer(f"install {package_id}", "install")

    def _run_installer(self, verb: str, action: str) -> None:
        result = self._runner.run(f"clish -c 'installer {verb}'")
        if not result.ok:
            raise CPUSEError(f"CPUSE {action} failed: {result.stderr.strip()}")

    # -- parsing ---------------------------------------------------------------

    @staticmethod
    def _parse_packages(_stdout: str) -> list[PackageState]:
        # TODO: parse the tabular `show installer packages` output. Kept as a stub
        # so the shape is fixed and unit-testable with captured fixtures.
        raise NotImplementedError("CPUSE package parsing not yet implemented")
