"""SSH transport to Gaia (clish + expert).

Baseline transport for every operation. Kept deliberately small: connect, run a
command, return (rc, stdout, stderr). No orchestration logic lives here.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType
from typing import Protocol

from ..errors import TransportError
from ..inventory import Host


@dataclass(frozen=True)
class CommandResult:
    """Outcome of a single remote command."""

    command: str
    exit_status: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.exit_status == 0


class CommandRunner(Protocol):
    """Interface the wrappers depend on. Real SSH and fakes both satisfy it."""

    def run(self, command: str, *, timeout: float | None = None) -> CommandResult: ...


class SSHClient:
    """Paramiko-backed Gaia SSH client.

    Usage::

        with SSHClient(host, password=resolve_secret(host.secret_ref)) as ssh:
            result = ssh.run("show version all")

    NOTE: implementation is a stub — wire up Paramiko in a follow-up. It is written
    against the ``CommandRunner`` protocol so callers and tests are already correct.
    """

    def __init__(
        self,
        host: Host,
        *,
        password: str | None = None,
        key_filename: str | None = None,
        connect_timeout: float = 30.0,
    ) -> None:
        self.host = host
        self._password = password
        self._key_filename = key_filename
        self._connect_timeout = connect_timeout
        self._client: object | None = None  # paramiko.SSHClient once connected

    def connect(self) -> None:
        # TODO: implement with paramiko.SSHClient; load host keys, set a strict
        # policy, honor connect_timeout, authenticate via key or password.
        raise NotImplementedError("SSH connect not yet implemented")

    def run(self, command: str, *, timeout: float | None = None) -> CommandResult:
        # TODO: exec_command on the live transport; capture rc/stdout/stderr.
        raise NotImplementedError("SSH run not yet implemented")

    def close(self) -> None:
        self._client = None

    def __enter__(self) -> SSHClient:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


def require_ok(result: CommandResult) -> CommandResult:
    """Raise TransportError unless the command succeeded. Fail closed."""
    if not result.ok:
        raise TransportError(
            f"command failed (rc={result.exit_status}): {result.command}\n{result.stderr.strip()}"
        )
    return result
