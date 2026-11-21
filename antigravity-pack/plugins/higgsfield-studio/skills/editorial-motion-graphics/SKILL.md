---
name: editorial-motion-graphics
description: >-
  Create Vox-style and documentary editorial motion graphics, faceless explainers,
  mixed-media cutout montages, animated maps/charts, and kinetic typography videos
  using the Higgsfield MCP server (https://mcp.higgsfield.ai/mcp) and Higgsfield
  faceless-video production workflows. Use when the user asks for "editorial motion
  graphics", "Vox style explainer", "mixed media documentary", "Higgsfield MCP",
  "paper cutout motion graphics", or "animated editorial breakdown".
---

# Editorial Motion Graphics (Higgsfield MCP)

Produce high-craft editorial and documentary motion graphics — combining layered paper/archival cutouts, restrained halftone texture, single-accent color systems, diagrams/maps, deliberate pacing, voiceover narration, and synced typography — orchestrated through **Higgsfield MCP** (`https://mcp.higgsfield.ai/mcp`) and the bundled [`higgsfield-faceless-video`](../higgsfield-faceless-video/SKILL.md) production system.

## Visual Language & Aesthetic Contract

Use the editorial collage grammar defined in [`higgsfield-faceless-video/references/styles.md`](../higgsfield-faceless-video/references/styles.md):

- **Surface & Texture:** Warm cream or archival newsprint base with subtle fiber grain, monochrome halftone cutouts, torn/rough paper edges, and soft drop shadows.
- **Palette Discipline:** Lock one muted neutral canvas + one sharp editorial accent color (e.g., vermilion, cobalt, or highlighter gold) across every scene.
- **Information Design:** Pair abstract diagrams, timelines, highlight callouts, and map zooms with deliberate visual holds — never spam rapid-fire stock cuts over explanatory narration.
- **Typography & Captions:** Keep on-screen text purposeful (section headers, data labels, highlighted quotes) and keep spoken words in narration unless captions are requested.

## Workflow (Higgsfield MCP + CLI + Local Assembly)

1. **Authenticate & Discover Capabilities:**
   - **MCP Path (Preferred when connected):** Use the plugin's `higgsfield-mcp` Streamable HTTP server (`https://mcp.higgsfield.ai/mcp`) to discover active presets, models, voices, and cost estimates directly inside the conversation. Sign in via Higgsfield OAuth when prompted.
   - **CLI Fallback:** Verify `higgsfield account status`, inspect live presets via `higgsfield preset list video-explainer --json`, and inspect voices via `higgsfield voices list --json`. Never invent preset or voice IDs.
2. **Research & Storyboard (10-Second Editorial Blocks):**
   - Research factual claims first and keep a short source list.
   - Break the script into ordered 10-second editorial blocks (or a shorter final block to match requested duration exactly), following [`higgsfield-faceless-video/references/creative.md`](../higgsfield-faceless-video/references/creative.md) and [`higgsfield-faceless-video/references/production.md`](../higgsfield-faceless-video/references/production.md).
   - For fast-cut editorial channel episodes, use the 5-shot-per-block schema and validation gate in [`higgsfield-faceless-video/references/channel-motion.md`](../higgsfield-faceless-video/references/channel-motion.md).
3. **Style Key & Reference Consistency:**
   - Generate one approved hero style key first (editorial collage / paper diorama / monochrome halftone + accent color) before batching scenes.
   - Pass that style reference and any recurring subject/mascot references into subsequent image/video calls (`higgsfield-generate`) to prevent drift.
4. **Narration Timing & Motion Generation:**
   - Generate narration takes first and verify timing against each block window (`check_voice.sh` / `measure_narration_takes.py`) before spending video credits — rewrite and regenerate failing takes rather than speeding up speech.
   - Estimate and disclose generation costs before submitting full batch renders.
5. **Assembly, Captions & QC:**
   - Assemble ordered visual + narration blocks using [`higgsfield-faceless-video/scripts/assemble_blocks.sh`](../higgsfield-faceless-video/scripts/assemble_blocks.sh) (or `assemble_final.sh` for channel-motion scripts), or refine locally with `ffmpeg-skill` / `remotion-suite`.
   - When subtitles are requested, follow [`higgsfield-faceless-video/references/captions.md`](../higgsfield-faceless-video/references/captions.md) and visually verify safe areas, contrast, sync, and duration before delivery.
