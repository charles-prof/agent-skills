# Video In-Scene Logo & Graphic Removal Skill

This skill provides an automated, frame-accurate runbook for removing logos, TV screen overlays, and full-screen transition cards from video files using CLI tools (`ffmpeg` and Python).

## Capabilities

- **Zero Frame Dropping:** Replaces or inpaints graphics without cutting scenes or altering video pacing.
- **Perfect Audio Sync:** Directly copies the audio stream (`-c:a copy`) to guarantee 0 ms audio drift.
- **Spatial Inpainting (`delogo`):** Seamlessly interpolates TV and display surfaces using surrounding pixel context.
- **Cinematic Matting (`drawbox`):** Converts transition slides into clean black dips while keeping timeline length intact.
- **Frame-Accurate Boundary Analysis:** Inspects 0.05s increments to prevent start/end transition leaks.

## Quick Usage

```bash
# Apply spatial inpainting on a TV display
ffmpeg -i input.mov -vf "delogo=x=1130:y=425:w=170:h=100:enable='between(t,171.3,177.25)'" -c:a copy output.mov
```

See [SKILL.md](./SKILL.md) for full instructions and multi-filter chaining recipes.
