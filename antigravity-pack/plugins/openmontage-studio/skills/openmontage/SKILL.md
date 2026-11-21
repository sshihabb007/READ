---
name: openmontage
description: >-
  Open-source agentic video production studio orchestrating 12 structured video
  pipelines (animated-explainer, cinematic, documentary-montage, clip-factory,
  talking-head, screen-demo, podcast-repurpose, animation, character-animation,
  hybrid, avatar-spokesperson, localization-dub), 100+ scored Python tools,
  Backlot living storyboard, Ink Theater doodle engine, style playbooks, and
  human approval gates. Use when the user asks for an end-to-end agentic video
  production pipeline, documentary montage from open archives, Ink Theater
  doodle animation, Backlot storyboarded production, or explicitly invokes
  OpenMontage.
---

# OpenMontage — Agentic Video Production Studio

The complete OpenMontage studio runtime lives two directories up at `../../runtime/`:

- **Master Operating Contract:** [`AGENT_GUIDE.md`](../../runtime/AGENT_GUIDE.md)
- **Architecture & Conventions:** [`PROJECT_CONTEXT.md`](../../runtime/PROJECT_CONTEXT.md)
- **Layer-2 Skill Index (150+ Director, Creative & Meta Skills):** [`skills/INDEX.md`](../../runtime/skills/INDEX.md)
- **Tested Prompts & Cost Estimates:** [`PROMPT_GALLERY.md`](../../runtime/PROMPT_GALLERY.md)

## Rule Zero — Always Run Through a Pipeline

1. **Locate `OM_ROOT`:** Resolve the absolute path to `../../runtime/` relative to this `SKILL.md` (e.g., `~/.gemini/config/plugins/openmontage-studio/runtime`).
2. **Run Mandatory Preflight First:**
   ```bash
   cd "$OM_ROOT" && python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
   ```
   Present the capability menu (configured vs. available ratios, free local options, and composition runtimes) before doing creative work.
3. **Select a Pipeline Manifest (`runtime/pipeline_defs/*.yaml`):**
   - `animated-explainer` — research -> proposal -> script -> scene_plan -> assets -> edit -> compose -> publish
   - `documentary-montage` — retrieval-first real-footage montage from Archive.org, NASA, Wikimedia, Pexels, Unsplash
   - `cinematic` — trailers, teasers, mood-led edits
   - `animation` / `character-animation` — motion graphics, Manim, SVG/GSAP rigs, Ink Theater doodles
   - `clip-factory` / `podcast-repurpose` / `talking-head` / `screen-demo` / `hybrid` / `avatar-spokesperson` / `localization-dub`
4. **Read Stage Director & Meta Skills Before Executing:**
   - Read the matching manifest in `runtime/pipeline_defs/<pipeline>.yaml`.
   - Before each stage, read `runtime/skills/pipelines/<pipeline>/<stage>-director.md`.
   - Use [`runtime/skills/meta/reviewer.md`](../../runtime/skills/meta/reviewer.md), [`runtime/skills/meta/checkpoint-protocol.md`](../../runtime/skills/meta/checkpoint-protocol.md), and [`runtime/skills/meta/taste-direction.md`](../../runtime/skills/meta/taste-direction.md).
5. **Respect Governance & Approval Gates:**
   - Initialize workspaces via `lib.checkpoint.init_project` under `projects/<project-id>/` (and optionally launch the Backlot storyboard via `python -m backlot open <project-id>`).
   - Present composition runtime choices explicitly (Remotion vs. HyperFrames vs. FFmpeg) and pause at every `human_approval_default: true` gate.
   - Announce provider, model, and cost estimate before paid calls; never silently downgrade a motion-led brief into static slides.
