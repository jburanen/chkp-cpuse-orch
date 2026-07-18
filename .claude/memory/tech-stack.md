---
name: tech-stack
description: Chosen stack (Python + Typer + Paramiko/Pydantic) and the reasons
metadata:
  type: project
---

**Language: Python 3.11+.** The default for Check Point / network-security
automation — first-class SSH, REST, and the ecosystem ops engineers already use.
`src/` layout, packaged with `pyproject.toml` (setuptools + wheel).

**Key libraries** (declared in `pyproject.toml`, pinned loosely):
- **Typer** — CLI framework (Click-based); subcommands map to orchestration verbs.
- **Pydantic v2** — typed config + inventory models with validation.
- **Paramiko** — SSH transport to Gaia (clish + expert). Fabric optional later.
- **PyYAML** — inventory / config files.
- **Rich** — console tables, progress, and readable run output.
- **structlog** — structured, auditable logging (deployments must be traceable).
- **httpx** — Gaia REST API and Check Point Management (`web-api`) calls.
- **tenacity** — retry/backoff for flaky SSH/API during maintenance windows.

**Dev tooling:** `pytest` (tests), `ruff` (lint+format), `mypy` (types),
`pre-commit` optional. Line length 100.

**Why not Ansible?** Ansible is a reasonable alternative and may wrap this later,
but CDT orchestration needs stateful, health-gated sequencing and rollback logic
that is cleaner as first-class Python than as playbook YAML. Revisit if the team
prefers a playbook front-end. See [[architecture]].
