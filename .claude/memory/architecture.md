---
name: architecture
description: Module layout and data flow of the orchestrator
metadata:
  type: project
---

Package: `src/chkp_cpuse_orch/`. Layered so the CDT/CPUSE wrappers stay thin and the
orchestration/safety logic is testable without live gear.

```
chkp_cpuse_orch/
  cli.py            # Typer entrypoint; verbs: plan, deploy, status, precheck, rollback
  config.py         # Pydantic settings (global tool config, defaults, paths)
  inventory.py      # Pydantic models: Site, ManagementServer, Gateway, Cluster; loader
  transport/
    ssh.py          # Paramiko SSH to Gaia (clish + expert), command runner
    gaia_api.py     # Gaia REST API client (httpx)
    mgmt_api.py     # Check Point Management API (mgmt_cli / web-api) client
  cpuse.py          # Thin wrapper over CPUSE installer verbs on ONE Gaia host
  cdt.py            # Thin wrapper: build XML plan + target list, invoke `cdt`, parse
  orchestrator.py   # Fleet sequencing: batching, HA-aware ordering, gating on checks
  checks.py         # Pre/post health checks (version, cluster state, policy, disk)
  reporting.py      # structlog + Rich run records; write auditable reports/
  errors.py         # Typed exceptions
```

**Data flow:** `inventory.yaml` + `config.yaml` → Pydantic models → `orchestrator`
builds a run plan → `checks` gate each step → `cpuse`/`cdt` execute via `transport`
→ `reporting` records everything.

**Design rules**
- Wrappers (`cpuse.py`, `cdt.py`) never make policy decisions; they execute and
  parse. All sequencing/safety lives in `orchestrator.py` + `checks.py`.
- Every mutating operation supports **dry-run** and emits an audit record.
- Nothing hardcodes hostnames/IPs/credentials — all from inventory/config/secrets
  store. See [[security-hygiene]] and [[safety-constraints]].
