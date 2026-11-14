---
name: chrome-devtools-perf
description: "Use when profiling Core Web Vitals (LCP, INP, CLS), recording CPU/performance traces, inspecting live Chrome network payloads, or debugging runtime DOM/memory bottlenecks with Chrome DevTools MCP."
---

# Chrome DevTools MCP Performance & Runtime Debugging

## When to Use
- Measuring real Core Web Vitals (LCP, CLS, INP) and recording performance traces via `chrome-devtools` MCP tools.
- Inspecting live network request/response headers, payloads, initiator chains, and console diagnostics.
- Pairing runtime performance measurements with `web-perf-auditor` and `performance-optimization`.

## Discipline
- Always separate cold-load vs warm-cache runs when reporting performance metrics.
- Never report static source heuristics as measured Core Web Vitals — record a real trace first.
