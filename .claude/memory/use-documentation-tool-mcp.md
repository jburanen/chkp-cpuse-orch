---
name: use-documentation-tool-mcp
description: Always use the documentation-tool MCP for this project's docs lookups
metadata:
  type: feedback
---

Always leverage the **documentation-tool MCP** for this project when looking up
documentation — prefer it over guessing from memory or general web search for
Check Point / CDT / CPUSE facts and any other docs it covers.

**Why:** the user set this expectation explicitly (2026-07-17). CDT/CPUSE CLI syntax
and SK articles change across Check Point releases; authoritative docs beat recall.
See [[cdt-cpuse-domain]], which flags that SK references must be verified.

**How to apply:** when a task needs documentation, reach for the documentation-tool
MCP first. If the server is not connected/authorized in the current session, say so
and ask the user to enable it rather than silently falling back.
