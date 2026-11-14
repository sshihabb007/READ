---
name: playwright-e2e-har
description: "Use when running automated E2E browser verification, accessibility tree snapshots, network/console error assertions, or recording browser traces with Playwright MCP to feed into REA's inspect_playwright_trace and inspect_web_network_capture tools."
---

# Playwright MCP E2E & REA Trace Workflow

## When to Use
- Automated browser E2E testing against local dev servers or staging apps.
- Inspecting live accessibility snapshots, console errors/warnings, and network requests via `playwright` MCP tools.
- Capturing browser traces or network traffic and feeding them directly into **REA**:
  - `inspect_playwright_trace` for Playwright `.zip` trace artifacts.
  - `inspect_web_network_capture` for `.har`, HTTP/3, or qlog captures.

## Guidelines
1. Prefer accessibility snapshots over pixel coordinates for resilient UI interaction.
2. Assert zero unexpected `console.error` / `pageerror` events and verify HTTP status codes on critical API calls before claiming a UI flow passes.
3. For visual interactive browsing in the user's own session, use Antigravity's built-in `browser` subagent; use `playwright` MCP for repeatable automated E2E verification and trace/network capture.
