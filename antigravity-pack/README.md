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
| **`playwright-qa`** | 1 | — | `playwright` (`@playwright/mcp`) | Automated Chrome E2E testing, accessibility snapshots, and Playwright trace / HAR capture for REA (`inspect_playwright_trace`, `inspect_web_network_capture`) |
| **`chrome-devtools-plugin`** | 1 | — | `chrome-devtools` (`chrome-devtools-mcp`) | Live Chrome DevTools Core Web Vitals, CPU/memory flamecharts, and runtime network payload inspection |

---

## End-to-End Workflow

1. **Forensics (`rea` + `rea-security-forensics`)**: Extract verified observations, call paths, network captures, and reconstruction obligations with REA.
2. **Architecture (`architecture-studio`)**: Synthesize clean-room EventStorming catalogs, Mermaid ERDs/sequences, ADRs, and interactive HTML architecture diagrams.
3. **Implementation (`superpowers` + `engineering-craft` + `context7`)**: Pull version-pinned docs via Context7 and implement in thin, TDD-verified slices inside isolated branches/worktrees.
4. **Verification (`playwright-qa` + `chrome-devtools-plugin` + `rea-security-auditor`)**: Run E2E browser suites, benchmark Core Web Vitals, verify reconstruction coverage in REA, and complete differential security review.
