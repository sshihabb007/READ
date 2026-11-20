# REA Enhanced — Antigravity Companion Pack

This `enhanced` branch pairs **REA (`rea-agents`)** with a curated, zero-collision ecosystem of **Google Antigravity Plugins, Skills, Specialist Subagents, and Companion MCP Servers** for end-to-end reverse engineering, vulnerability auditing, clean-room system architecture, TDD implementation, Core Web Vitals optimization, and E2E browser verification.

---

## Quick Install (Windows / macOS / Linux)

```bash
# 1. Preview planned global Antigravity plugin & MCP runtime actions
npm run setup:antigravity-pack -- --dry-run

# 2. Install plugins & fast-boot local MCP runtimes into ~/.gemini/config/
npm run setup:antigravity-pack

# 3. Register REA MCP & skill with Antigravity (after building REA)
npm run build:cached
node scripts/rea.mjs setup --client antigravity --skill-client antigravity --skill
```

Also add the two companion Antigravity Marketplace plugins from the Antigravity UI:
- **Superpowers** (`antigravity-plugins-partners/plugin/superpowers`) — `brainstorming` -> `writing-plans` -> `using-git-worktrees` -> `subagent-driven-development` -> `test-driven-development`
- **Context7** (`antigravity-plugins-partners/plugin/context7`) — Live, version-accurate SDK/framework documentation lookup

---

## Bundled Modular Plugins (`antigravity-pack/plugins/`)

| Plugin | Skills | Subagents | MCP Server | Purpose |
| :--- | :---: | :--- | :--- | :--- |
| **`rea-security-forensics`** | 13 | `rea-security-auditor` | — | Master `rea-end-to-end-pipeline` playbook + 12 Trail of Bits binary/APK/crypto/variant/YARA/static-analysis skills |
| **`architecture-studio`** | 4 | `system-architect` | — | 5-phase EventStorming `system-design`, `interactive-architecture-diagram` (animated HTML flows), `layered-architecture-diagram` (collision-free HTML/SVG), and `documentation-and-adrs` |
| **`engineering-craft`** | 20 | `staff-code-reviewer`, `qa-test-engineer`, `web-perf-auditor` | — | Curated Addy Osmani & Vercel Labs SDLC, API design, incremental dev, UI craft, React/Next & Core Web Vitals optimization skills (deduplicated against Superpowers) |
| **`replica-suite`** | 11 | — | — | Clean-room app-cloning lifecycle (`replica-recon` -> `architect` -> `design` -> `build` -> `backend` -> `test` -> `diff` -> `entrepreneur` -> `brand` -> `launch` -> `deploy`) + 6 stdlib Python tools (`contrast.py`, `imgdiff.py`, `parity.py`, `reviews.py`, `sweep.py`, `listing.py`) |
| **`remotion-suite`** | 13 | — | — | Official `@remotion/skills` (`v4.0.545`): `remotion-best-practices` router plus `create`, `markup`, `interactivity`, `studio`, `render`, `maps` (Mapbox/MapLibre/MapTiler/CesiumJS), `captions`, `multimedia`, `saas`, `docs`, `license`, and `upgrade` |
| **`playwright-qa`** | 1 | — | `playwright` (`@playwright/mcp`) | Automated Chrome E2E testing, accessibility snapshots, and Playwright trace / HAR capture for REA (`inspect_playwright_trace`, `inspect_web_network_capture`) |
| **`chrome-devtools-plugin`** | 1 | — | `chrome-devtools` (`chrome-devtools-mcp`) | Live Chrome DevTools Core Web Vitals, CPU/memory flamecharts, and runtime network payload inspection |

---

## End-to-End Workflow

1. **Forensics & Product Recon (`rea` + `rea-security-forensics` / `replica-recon`)**: Extract verified observations, call paths, network captures, and reconstruction obligations with REA — or build a clean-room `replica/recon.md` + `features.csv` screen/flow/data inventory from public docs and user-owned workflows.
2. **Architecture & Design Tokens (`architecture-studio` / `replica-architect` + `replica-design`)**: Synthesize clean-room EventStorming catalogs, Mermaid ERDs/sequences, ADRs, SQL schemas, WCAG-checked `tokens.json` (`contrast.py`), and interactive HTML architecture diagrams.
3. **Implementation (`superpowers` + `engineering-craft` + `replica-build` / `replica-backend` + `context7`)**: Pull version-pinned docs via Context7 and implement screen-by-screen in thin, TDD-verified slices inside isolated branches/worktrees.
4. **Verification, Parity & Launch (`playwright-qa` + `chrome-devtools-plugin` + `replica-suite` + `rea-security-auditor`)**: Run E2E browser suites (`replica-test`), benchmark Core Web Vitals, score feature & edge-map layout parity (`replica-diff`: `parity.py`, `imgdiff.py`), mine linked user complaints (`replica-entrepreneur`: `reviews.py`), sweep rebrand leftovers (`replica-brand`: `sweep.py`), verify reconstruction coverage in REA, complete differential security review, and run preflight (`replica-launch` / `replica-deploy`).
