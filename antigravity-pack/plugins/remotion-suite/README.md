# Remotion Video & Motion Studio (`remotion-suite`)

Bundles the complete official `@remotion/skills` suite (`v4.0.545`) from [`remotion-dev/remotion`](https://github.com/remotion-dev/remotion/tree/main/packages/skills) for Antigravity:

- **`remotion-best-practices`** — Master router directing agents to the appropriate Remotion workflow skill
- **`remotion-create`** — Project scaffolding (`create-video`), video layout geometry, and Tailwind integration
- **`remotion-markup`** — Core animations (`useCurrentFrame`, `interpolate`, `Easing.spring`), `@remotion/media`, effects, fonts, Lottie, 3D, FFmpeg, and silence detection
- **`remotion-interactivity`** — Editable timelines, `Interactive.*` primitives, schemas, inline keyframes, and SVG path morphing for Remotion Studio
- **`remotion-studio`** — Launching, configuring, and verifying compositions in Remotion Studio
- **`remotion-render`** — Headless rendering (`mp4`, stills, transparent WebM/ProRes) and OpenTimelineIO exports
- **`remotion-maps`** — Static maps, Mapbox, MapLibre, MapTiler, and 3D CesiumJS flyovers
- **`remotion-captions`** — Transcription, `.srt` import, and TikTok/word-highlighted `Caption` rendering
- **`remotion-multimedia`** — Browser-based video/audio metadata inspection with Mediabunny
- **`remotion-saas`** — `<Player>` embedding, Next.js/framework templates, and Lambda/Vercel/Cloudflare rendering
- **`remotion-docs`** — Algolia docs search + raw `.md` page retrieval
- **`remotion-license`** — Free vs. company license guidance
- **`remotion-upgrade`** — Coordinated Remotion, Mediabunny, and skill version upgrades

Cross-skill `./remotion-*` symlink stubs are normalized to portable `../remotion-*` relative paths so every link resolves cleanly on Windows, macOS, and Linux. Verify bundle integrity anytime with:

```bash
python3 -m unittest discover -s tests -v
```
