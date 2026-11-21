---
name: openmontage-reference-analyst
description: >-
  Deconstruct a reference YouTube video, Short, Reel, TikTok, or local clip into
  a grounded 5-aspect production brief (Subject, Subject Motion, Scene, Spatial
  Framing, Camera), pacing/motion classification, and 2-3 differentiated original
  concepts with realistic tool paths and cost estimates. Use when the user says
  "make me a video like this", "inspired by this Short/Reel", "analyze this
  reference video style", or pastes a video URL/file as creative inspiration
  rather than raw footage to cut.
---

# OpenMontage Reference Video Analyst

Follow the complete protocol in [`runtime/skills/meta/video-reference-analyst.md`](../../runtime/skills/meta/video-reference-analyst.md), paired with [`runtime/skills/meta/taste-direction.md`](../../runtime/skills/meta/taste-direction.md) and [`runtime/skills/meta/bespoke-composition.md`](../../runtime/skills/meta/bespoke-composition.md).

## Workflow

1. **Distinguish Intent First:**
   - *Reference inspiration* ("make something like this on topic X") -> use this skill.
   - *Raw footage editing* ("cut/edit this video") -> route to `ffmpeg-skill`, `claude-shorts`, `ghost-editor`, or OpenMontage's `clip-factory` / `talking-head` pipeline.
2. **Analyze Structure, Motion & Keyframes:**
   - Probe transcript, scene boundaries, shot durations, and motion classification (`motion_clip` vs. `animated_still` vs. `static_image`) using OpenMontage's `VideoAnalyzer` (`runtime/tools/analysis/`) or local FFmpeg frame strips.
   - Visually inspect extracted keyframes and output the mandatory **5-aspect structured breakdown** per shot group:
     - **Subject**
     - **Subject Motion**
     - **Scene** (call out overlays/typography separately from environment)
     - **Spatial Framing**
     - **Camera**
     *(Mark non-applicable aspects explicitly as `N/A`; never silently omit.)*
3. **Audit Available Capabilities & Propose Differentiated Concepts:**
   - Run OpenMontage preflight (`registry.provider_menu_summary()`) or local tool inventory.
   - Present **2–3 differentiated concepts** (what structure/pacing to keep, what topic/visual language to change, realistic tool path, and estimated cost) and wait for user approval before launching full production via `openmontage`, `remotion-suite`, or `higgsfield-studio`.
