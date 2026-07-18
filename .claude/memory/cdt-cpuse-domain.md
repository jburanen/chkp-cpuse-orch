---
name: cdt-cpuse-domain
description: How Check Point CDT and CPUSE work — the tools this project orchestrates
metadata:
  type: reference
---

The two Check Point mechanisms this tool drives. (SK numbers below are the known
reference articles; verify against the customer's version before relying on exact
CLI syntax — Check Point changes these across releases.)

**CPUSE — Check Point Upgrade Service Engine** (aka the Deployment Agent / DA)
- Runs on a *single* Gaia machine (mgmt server or gateway). Source of truth for
  local install state.
- Lifecycle per package: `import` → `verify` → `install` → (optional reboot) →
  `uninstall`. Packages: hotfixes, Jumbo Hotfix Accumulators (JHF/HFA), and major
  version upgrades.
- CLI via Gaia clish `installer` verbs, e.g. `show installer packages`,
  `installer import`, `installer verify <pkg>`, `installer install <pkg>`. Also a
  Gaia Portal web UI. Reference: sk92449.
- **Management servers are patched with CPUSE locally**, not via CDT.

**CDT — Central Deployment Tool** (reference: sk111158)
- Runs *on a Security Management Server or Multi-Domain Server*. Pushes packages and
  scripts to *many* managed Security Gateways / clusters at once, using CPUSE on each
  target under the hood.
- Driven by an **XML deployment configuration** plus a **target list** (gateways).
  Handles: copy package → verify → install → reboot, with concurrency/batch limits.
- Invoked as the `cdt` command on the management server shell (expert mode).
- Good for gateway fleets; NOT used to upgrade the management server itself.

**Typical end-to-end upgrade this tool orchestrates**
1. Pre-checks: HA state, cluster member roles, connectivity, free disk, current
   versions. (see [[safety-constraints]])
2. Patch the **management server** via CPUSE (local, one host, often HA pair).
3. Stage package to the CDT repository on the management server.
4. Deploy to **gateways** in batches via CDT, respecting cluster failover order.
5. Post-checks: version confirmed, policy installed, cluster healthy, logs clean.

**How we reach the boxes:** SSH to Gaia (clish/expert) is the baseline transport;
Gaia REST API and the Check Point Management API (`mgmt_cli`) are used where
available. See [[tech-stack]] and [[architecture]].
