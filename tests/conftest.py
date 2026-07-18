from __future__ import annotations

import pytest

from chkp_cpuse_orch.config import Config
from chkp_cpuse_orch.inventory import Cluster, Host, Inventory, Role, Site


@pytest.fixture
def inventory() -> Inventory:
    """A small estate: one mgmt server, one standalone gateway, one 2-member cluster."""
    return Inventory(
        sites=[
            Site(
                name="dc1",
                hosts=[
                    Host(name="mgmt-01", address="192.0.2.10", role=Role.MANAGEMENT),
                    Host(name="fw-01", address="192.0.2.20", role=Role.GATEWAY),
                    Host(name="fw-a1", address="192.0.2.31", role=Role.CLUSTER_MEMBER),
                    Host(name="fw-a2", address="192.0.2.32", role=Role.CLUSTER_MEMBER),
                ],
                clusters=[Cluster(name="cluster-a", members=["fw-a2", "fw-a1"])],
            )
        ]
    )


@pytest.fixture
def config() -> Config:
    return Config()
