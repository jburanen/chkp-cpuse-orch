from __future__ import annotations

from pathlib import Path

import pytest

from chkp_cpuse_orch.errors import InventoryError
from chkp_cpuse_orch.inventory import Inventory, Role


def test_lookup_and_role_filter(inventory: Inventory) -> None:
    assert inventory.host("mgmt-01").role is Role.MANAGEMENT
    gateways = inventory.hosts_by_role(Role.GATEWAY)
    assert [h.name for h in gateways] == ["fw-01"]


def test_missing_host_raises(inventory: Inventory) -> None:
    with pytest.raises(InventoryError):
        inventory.host("nope")


def test_example_inventory_loads() -> None:
    """The committed example inventory must always be valid."""
    example = Path(__file__).resolve().parents[1] / "examples" / "inventory.example.yaml"
    inv = Inventory.load(example)
    assert inv.hosts_by_role(Role.MANAGEMENT)
    assert any(s.clusters for s in inv.sites)
