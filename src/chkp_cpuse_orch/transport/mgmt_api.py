"""Check Point Management API client (thin).

Used for management-plane facts and actions the orchestrator needs around a
deployment — e.g. verifying policy install status after patching gateways. Wraps
``mgmt_cli`` / the web-api. Stub for now.
"""

from __future__ import annotations

from ..inventory import Host


class ManagementAPIClient:
    """Minimal Check Point Management API client. Stub."""

    def __init__(
        self, server: Host, *, api_key: str | None = None, verify_tls: bool = True
    ) -> None:
        self.server = server
        self._api_key = api_key
        self._verify_tls = verify_tls

    def login(self) -> None:
        # TODO: POST /web_api/login (api key or user/pass), store sid.
        raise NotImplementedError("Management API login not yet implemented")

    def gateway_policy_status(self, gateway_name: str) -> dict[str, object]:
        # TODO: query installed policy / last-install state for a gateway.
        raise NotImplementedError("Management API gateway_policy_status not yet implemented")
