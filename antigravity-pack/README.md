# REA Enhanced — Antigravity Companion Pack

This `enhanced` branch pairs **REA (`rea-agents`)** with a curated, zero-collision ecosystem of **Google Antigravity Plugins, Skills, Specialist Subagents, and Companion MCP Servers** for end-to-end reverse engineering, vulnerability auditing, clean-room system architecture, TDD implementation, Core Web Vitals optimization, E2E browser verification, and programmatic/agentic video production.

---

## Quick Install (Windows / macOS / Linux)

```bash
# 1. Preview planned global Antigravity plugin & MCP runtime actions
npm run setup:antigravity-pack -- --dry-run

# 2. Install all 19 plugins & local/remote MCP runtimes into ~/.gemini/config/
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

| Plugin | Skills | Subagents | MCP Server | License | Purpose |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **`rea-security-forensics`** | 13 | `rea-security-auditor` | — | MIT | Master `rea-end-to-end-pipeline` playbook + 12 Trail of Bits binary/APK/crypto/variant/YARA/static-analysis skills |
| **`architecture-studio`** | 4 | `system-architect` | — | MIT | 5-phase EventStorming `system-design`, `interactive-architecture-diagram`, `layered-architecture-diagram`, and `documentation-and-adrs` |
| **`engineering-craft`** | 20 | `staff-code-reviewer`, `qa-test-engineer`, `web-perf-auditor` | — | MIT | Curated Addy Osmani & Vercel Labs SDLC, API design, incremental dev, UI craft, React/Next & Core Web Vitals optimization skills (deduplicated against Superpowers) |
| **`ecc-core`** | 32 | 15 specialists (`build-error-resolver`, `database-reviewer`, `refactor-cleaner`, `silent-failure-hunter`, `type-design-analyzer`, `pr-test-analyzer`, `e2e-runner`, `a11y-architect`, `doc-updater`, `spec-miner`, `code-explorer`, `commit-reviewer`, `csharp-reviewer`, `php-reviewer`, `bengali-reviewer`) | — | MIT | Active core from [`affaan-m/ecc`](https://github.com/affaan-m/ecc) (`v2.2.3`): zero-overlap engineering specialists plus Database, Backend, C#/.NET, PHP/Laravel, Python, Windows E2E, DevOps, OWASP 2025, Bengali NLP & Eval skills |
| **`ecc-languages`** *(off by default)* | 80 | 26 language/framework reviewers & build resolvers | — | MIT | On-demand polyglot pack from `affaan-m/ecc` (`"disabled": true` until toggled on): Go, Rust, C++, Java/Spring/Quarkus, Kotlin, Swift/Apple, Flutter/Dart, Vue/Nuxt/Angular, Rails, Perl, F#, Godot & UI motion |
| **`ecc-agentic-ai`** *(off by default)* | 118 | 24 agentic, ML, planning & OSS subagents | — | MIT | On-demand agentic & AI pack from `affaan-m/ecc` (`"disabled": true` until toggled on): autonomous loops, multi-model councils, GAN/eval harnesses, PyTorch/MLE, scientific literature DBs, OSINT & deep research |
| **`ecc-ops-business`** *(off by default)* | 86 | 7 network, homelab, healthcare, SEO & marketing subagents | — | MIT | On-demand ops & domain pack from `affaan-m/ecc` (`"disabled": true` until toggled on): Cisco/VLAN/WireGuard, ClickHouse, DeFi/EVM security, HIPAA, supply chain, SEO, content, social & investor ops |
| **`replica-suite`** | 11 | — | — | MIT | Clean-room app-cloning lifecycle (`replica-recon` -> `architect` -> `design` -> `build` -> `backend` -> `test` -> `diff` -> `entrepreneur` -> `brand` -> `launch` -> `deploy`) + 6 stdlib Python tools |
| **`remotion-suite`** | 13 | — | — | MIT | Official `@remotion/skills` (`v4.0.545`): `remotion-best-practices` router plus `create`, `markup`, `interactivity`, `studio`, `render`, `maps`, `captions`, `multimedia`, `saas`, `docs`, `license`, and `upgrade` |
| **`hyperframes`** | 9 | — | — | Apache-2.0 | Official **HyperFrames by HeyGen** (`v0.9.104`): HTML/CSS/GSAP deterministic motion graphics (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `remotion-to-hyperframes`, `reverse-any-video`, `style-sampling`, `slideshow`, `figma`) |
| **`ghost-editor`** | 1 | — | — | MIT | Talking-head raw footage to finished `1080x1920` reels (`github.com/kurbaitaev/ghost-editor`): take selection, pause removal, face tracking, 19 named visual style recipes, approval sheets, and render QA |
| **`ffmpeg-skill`** | 1 | — | `ffmpeg-skill` (local stdio Python) | MIT | Local FFmpeg video/audio editor (`github.com/kajisho5/ffmpeg-skill` v4.3.6): 42 zero-dependency stdlib Python tools, machine-readable contract, loudness, silence removal, captions, HDR-to-SDR, and platform checks |
| **`whisper-captions`** | 1 | — | — | MIT | Local Whisper / `faster-whisper` / WhisperX auto-captions & transcription with bundled Python exporter for `.srt`, `.vtt`, Remotion `.captions.json`, and viral 9:16 `.ass` karaoke/pop subtitles |
| **`yt-dlp-media`** | 1 | — | — | MIT | Zero-API-key `yt-dlp` video, audio, subtitle, metadata, and time-range clip downloader (`--download-sections`, edit-ready H.264/MP4) with safe shell-free Python helper |
| **`higgsfield-studio`** | 10 | — | `higgsfield-mcp` (`https://mcp.higgsfield.ai/mcp`) | MIT | **`editorial-motion-graphics`** (Vox/documentary cutout & mixed-media explainers) + official Higgsfield Streamable HTTP MCP + all 9 official `higgsfield-ai/skills` (`v0.14.0`: `faceless-video`, `generate`, `soul-id`, `product-photoshoot`, `brandkit`, `marketplace-cards`, `websites`, `youtube-thumbnail`, `video-explainer`) |
| **`claude-shorts`** | 1 | — | — | MIT | Interactive 10-step longform-to-shortform pipeline (`github.com/AgriciDaniel/claude-shorts`): faster-whisper transcription, 5-dimension viral scoring, audio-aware boundary snapping, Remotion Bold/Bounce/Clean captions, and platform export |
| **`openmontage-studio`** | 2 | — | — | **AGPL-3.0** | Agentic video production studio (`github.com/OpenMontageInc/OpenMontage`): `openmontage` (12 YAML pipelines, 150+ Layer-2 director/creative skills, 100+ scored Python tools, Backlot storyboard, Ink Theater) + `openmontage-reference-analyst` (5-aspect reference deconstruction) |
| **`playwright-qa`** | 1 | — | `playwright` (`@playwright/mcp`) | MIT | Automated Chrome E2E testing, accessibility snapshots, and Playwright trace / HAR capture for REA |
| **`chrome-devtools-plugin`** | 1 | — | `chrome-devtools` (`chrome-devtools-mcp`) | MIT | Live Chrome DevTools Core Web Vitals, CPU/memory flamecharts, and runtime network payload inspection |

> **Licensing Note:** `openmontage-studio` is packaged as a standalone companion plugin under **GNU AGPL v3.0** (preserving its full upstream `LICENSE`), separate from REA's MIT core.

---

## End-to-End Workflows

### Software Forensics, Architecture & Engineering
1. **Forensics & Product Recon (`rea` + `rea-security-forensics` / `replica-recon`)**: Extract verified observations, call paths, network captures, and reconstruction obligations with REA — or build a clean-room `replica/recon.md` + `features.csv` screen/flow/data inventory.
2. **Architecture & Design Tokens (`architecture-studio` / `replica-architect` + `replica-design`)**: Synthesize clean-room EventStorming catalogs, Mermaid ERDs/sequences, ADRs, SQL schemas, WCAG-checked `tokens.json`, and interactive HTML architecture diagrams.
3. **Implementation (`superpowers` + `engineering-craft` + `replica-build` / `replica-backend` + `context7`)**: Pull version-pinned docs via Context7 and implement screen-by-screen in thin, TDD-verified slices.
4. **Verification, Parity & Launch (`playwright-qa` + `chrome-devtools-plugin` + `replica-suite` + `rea-security-auditor`)**: Run E2E browser suites, benchmark Core Web Vitals, score parity, sweep rebrand leftovers, verify reconstruction coverage, and complete differential security review.

### Video Production, Motion Graphics & Short-Form Editing
- **Media Ingest & Auto-Captions (`yt-dlp-media` + `whisper-captions` + `ffmpeg-skill`)**: Pull edit-ready H.264 MP4s, clip sections, or audio tracks via `yt-dlp`, transcribe locally with Whisper/faster-whisper to `.srt`/`.vtt`/Remotion `.captions.json`/viral 9:16 `.ass`, normalize LUFS, and validate platform delivery.
- **HTML/GSAP & React Motion Graphics (`hyperframes` + `remotion-suite`)**: Author deterministic HTML/GSAP motion graphics (`hyperframes` + ~450 `hyperframes-registry` blocks + `reverse-any-video` + `figma`) or programmatic React compositions (`remotion-suite`).
- **Longform-to-Shorts Extraction (`claude-shorts` + `remotion-suite` + `ffmpeg-skill`)**: Transcribe, score viral moments, snap audio boundaries, reframe `9:16`, render animated Remotion captions, normalize LUFS, and validate platform delivery.
- **Talking-Head Reels (`ghost-editor` + `ffmpeg-skill`)**: Pick best takes, trim pauses, face-track captions, apply one of 19 named editorial/HUD/whiteboard styles, approve via contact sheet, and render QA-checked masters.
- **Editorial Motion Graphics & AI Explainers (`higgsfield-studio`)**: Connect to `https://mcp.higgsfield.ai/mcp` for Vox-style mixed-media cutouts, faceless explainers, consistent Soul ID characters, and YouTube thumbnails.
- **Full Agentic Studio Pipelines (`openmontage-studio`)**: Deconstruct any reference video via `openmontage-reference-analyst` and orchestrate research, scripting, asset generation, Backlot storyboard review, and Remotion/HyperFrames/FFmpeg composition across 12 pipelines.
