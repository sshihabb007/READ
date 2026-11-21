# FFmpeg Skill (`ffmpeg-skill` v4.3.6)

Packaged from [`kajisho5/ffmpeg-skill`](https://github.com/kajisho5/ffmpeg-skill) (MIT) for the REA Enhanced Antigravity Pack.

- **Skill:** `ffmpeg-skill` — 42 zero-dependency Python 3.10+ stdlib FFmpeg tools (no cloud, no API keys) with a machine-readable contract (`scripts/_contract.py`) and probe-first / verify-last workflow.
- **Local MCP Server:** `ffmpeg-skill` (stdio Python MCP via `mcp/server.py`, wired automatically by `npm run setup:antigravity-pack`). Exposes the 12 core tools by default; set `FFMPEG_SKILL_MCP_FULL=1` to list all 42.
