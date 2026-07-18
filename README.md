# chkp-cpuse-orch

Orchestration layer for Check Point's **Central Deployment Tool (CDT)** and **CPUSE**.
It coordinates staged, health-gated deployment of patches and upgrades — hotfixes,
Jumbo Hotfix Accumulators, and major-version upgrades — across fleets of **Security
Management Servers and Security Gateways**.

> Internal, **defensive** operations tooling for authorized maintenance on
> infrastructure you own. It *drives* Check Point's own CDT/CPUSE agents; it does not
> replace them.

## Why

CDT and CPUSE are powerful but operate one plan / one host at a time and lack
fleet-level guardrails. Real maintenance needs staged rollouts, per-site batching,
cluster-aware ordering, pre/post health checks, maintenance-window gating, and an
auditable record. This tool is that orchestration layer.

## Status

**Early scaffolding.** The structure, models, CLI, and safety/planning logic are in
place and unit-tested. The live-gear integrations (SSH/CDT/CPUSE execution, result
parsing, health checks) are typed stubs marked `TODO` / `NotImplementedError`, ready
to be filled in. Dry-run planning works today.

## Install

```bash
python -m venv .venv && . .venv/Scripts/activate   # Windows; use bin/activate on *nix
pip install -e ".[dev]"
```

## Usage

```bash
# Copy and fill the templates (real files are git-ignored):
cp examples/inventory.example.yaml inventory.yaml
cp examples/config.example.yaml    config.yaml
cp .env.example .env               # or export/secret-store the CHKP_* vars

# Validate inputs (never touches a host):
chkp-cpuse-orch validate -i inventory.yaml -c config.yaml

# Preview a deployment run plan:
chkp-cpuse-orch plan "Check_Point_R81.20_JHF_T99.tgz" -i inventory.yaml

# Deploy — DRY-RUN by default; --execute to apply:
chkp-cpuse-orch deploy "Check_Point_R81.20_JHF_T99.tgz" -i inventory.yaml
chkp-cpuse-orch deploy "Check_Point_R81.20_JHF_T99.tgz" -i inventory.yaml --execute
```

## Safety model

This tool changes production firewalls. It is built to fail closed:

- **Dry-run by default** — real execution is explicit (`--execute`).
- **Cluster-aware ordering** — never patches two members of a cluster at once;
  standby-first, with live role confirmation.
- **Health gating** — a step proceeds only if pre-checks pass; a batch advances only
  if post-checks pass.
- **Bounded blast radius** — gateways roll out in size-capped batches.
- **Maintenance windows & rollback** — window-gated; snapshot-before-install.
- **Auditable** — every action and outcome is logged (structlog).

See [.claude/memory/safety-constraints.md](.claude/memory/safety-constraints.md).

## Security & public-repo hygiene

This repo is **public-bound**. Only `*.example.*` templates with placeholder values
are tracked. Real inventories, CDT plans, keys, `.env`, logs, and run reports are
git-ignored (and `.claudeignore`d). See
[.claude/memory/security-hygiene.md](.claude/memory/security-hygiene.md). **Never
commit real infrastructure detail or secrets.**

## Layout

```
src/chkp_cpuse_orch/   package (cli, config, inventory, transport/, cdt, cpuse,
                       checks, orchestrator, reporting, errors)
examples/              *.example.yaml templates (tracked)
tests/                 pytest suite (pure logic; no live gear)
.claude/memory/        project memory for Claude Code (start at MEMORY.md)
CLAUDE.md              project instructions
```

## Development

```bash
pytest
ruff check . && ruff format .
mypy src
```

## Disclaimer

Not affiliated with or endorsed by Check Point Software Technologies. "Check Point",
"CDT", and "CPUSE" refer to their products. Use only on infrastructure you are
authorized to maintain.
