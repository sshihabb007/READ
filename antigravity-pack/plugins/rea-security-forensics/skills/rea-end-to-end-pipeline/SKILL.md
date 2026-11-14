---
name: rea-end-to-end-pipeline
description: "End-to-end workflow connecting REA forensics (binaries, Electron, APKs, web bundles, HAR/Playwright traces) to clean-room System Design, Architecture Diagrams, Context7 + Superpowers TDD implementation, and Playwright/Chrome DevTools verification. Activate when reconstructing, cloning, auditing, or upgrading a feature analyzed with REA."
---

# REA End-to-End Forensics-to-Production Pipeline

Use this playbook whenever turning **REA (`rea` MCP / CLI)** forensic findings into a clean-room architecture, reconstruction, security audit, or production implementation.

## Core Provenance Contract (Non-Negotiable)
1. **Separate Evidence Tiers**: Keep REA `observation` (shipped bytes, imports, captured frames), `derivation` (CFG, call graphs, decoded AST), `inference` (named roles, hypothesized intent), and `unknown` strictly distinct across every stage.
2. **Never Fabricate Unobserved Behavior**: Carry unresolved gaps forward using REA's `record_unknown` / `list_unknowns` and `build_reconstruction_obligation_ledger` rather than guessing.

## Stage 1: Forensic Extraction (REA + Live Capture)
- **Target Triage**: Activate `reverse-engineer-anything` first. Use `binary_overview`, `inspect_desktop_application`, `inspect_android_package`, `analyze_web_bundle`, or `inspect_web_network_capture` depending on target format.
- **Live Web / Extension Capture (when authorized)**: If fresh runtime traces are needed, capture browser scenarios with REA (`capture_browser_scenario`, `observe_web_session`) or `playwright` MCP, then analyze traces via `inspect_playwright_trace` / `inspect_web_network_capture`.
- **Deep Context**: For security or complex native/JS logic, pair REA call-path tracing (`trace_feature`, `trace_application_feature`, `trace_javascript_semantics`) with `audit-context-building`.

## Stage 2: Clean-Room System Blueprint (Architecture Studio)
- Convert verified REA obligations and feature traces into clean-room specifications **before writing application code**:
  1. Run `system-design` for EventStorming domain events, state machines, ERDs, and sequence flows.
  2. Use `interactive-architecture-diagram` for animated click-through HTML packet-flow walkthroughs or `layered-architecture-diagram` for collision-free layered HTML/SVG component topologies.
  3. Record major trade-offs using `documentation-and-adrs`.

## Stage 3: Disciplined Implementation (Superpowers + Engineering Craft + Context7)
- Look up live, version-accurate SDK/framework APIs via **Context7** (`resolve-library-id` -> `query-docs`) for every library discovered in Stage 1.
- Execute inside an isolated branch/worktree using **Superpowers** (`writing-plans` -> `test-driven-development`) paired with `incremental-implementation`, `source-driven-development`, and `constraint-driven-development`.

## Stage 4: Verification, Performance & Security Gate
- **Reconstruction Parity**: Run REA's `evaluate_reconstruction_coverage`, `compare_static_and_observed_endpoints`, or `verify_reconstruction` when rebuilding an existing artifact.
- **Live Browser & CWV Profiling**: Verify E2E flows with `playwright` MCP (`playwright-e2e-har`) and profile Core Web Vitals / CPU / memory with `chrome-devtools` MCP (`chrome-devtools-perf`).
- **Security Sign-off**: Dispatch the `rea-security-auditor` subagent (and `differential-review` / `variant-analysis` / `sharp-edges`) before shipping.
