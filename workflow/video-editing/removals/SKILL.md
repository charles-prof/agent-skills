---
name: video-logo-removal
description: >-
  Procedure and runbook for detecting, tracking, and cleanly removing logos,
  watermarks, TV screen graphics, and transition slides from video footage using
  FFmpeg spatial inpainting (delogo) and drawbox filters without dropping frames
  or desyncing audio.
---

# Video Logo & In-Scene Graphic Removal Runbook

Follow this workflow when removing logos, watermarks, TV overlays, or full-screen transition graphics from video files without cutting frames or desyncing audio.

## Overview

When editing promotional, architectural, or raw footage, brands and logos often need to be cleanly removed without altering the overall runtime, scene sequence, or background audio. 

This runbook covers two primary removal scenarios:
1. **In-Scene Surfaces (e.g. TV screens, displays, framed art):** Using FFmpeg's spatial inpainting (`delogo`) to sample neighboring pixels and interpolate cleanly across camera motion.
2. **Full-Screen Cards & Transitions (e.g. intro/outro slides, room divider cards):** Using color matting (`drawbox`) to convert branding cards into clean cinematic black dips while preserving exact audio sync and runtime.

---

## Step 1: Reference Frame Extraction & Coordinate Detection

1. **Extract Reference Frame:**
   ```bash
   ffmpeg -ss <TIMESTAMP> -i input.mov -vframes 1 -update 1 frame.png
   ```

2. **Isolate Logo Coordinates & Envelope:**
   - Sample pixel boundaries `[x_min, x_max]` and `[y_min, y_max]` of the target graphic.
   - For moving cameras, check start, middle, and end frames across the scene to establish the total bounding envelope:
     ```python
     # Bounding box calculation:
     # x = x_min - padding, y = y_min - padding
     # w = (x_max - x_min) + 2 * padding, h = (y_max - y_min) + 2 * padding
     ```

---

## Step 2: Frame-Accurate Cut / Transition Boundary Timing

1. **Sub-Second Boundary Analysis:**
   - Visual cuts and cross-fades frequently begin 0.1s to 0.35s earlier or later than whole-second timestamps.
   - Inspect frames at 0.05s increments at the cut boundaries to avoid transition leaks.
   - Apply boundary timestamps to the filter's `enable` expression:
     `enable='between(t, START_TIME, END_TIME)'`

---

## Step 3: Filter Strategy Selection

| Target Scenario | Recommended Filter | Syntax Example |
| :--- | :--- | :--- |
| **TV / Display Screens** | Spatial Inpainting (`delogo`) | `delogo=x=1130:y=425:w=170:h=100:enable='between(t,171.30,177.25)'` |
| **Solid / Transition Cards** | Clean Color Fill (`drawbox`) | `drawbox=x=0:y=0:w=1920:h=1080:color=black:t=fill:enable='between(t,98.15,99.65)'` |
| **Complex Textured Scenes** | AI Optical Flow Inpaint | ProPainter / IOPaint (LaMa) |

---

## Step 4: Multi-Segment Chaining & High-Fidelity Render

1. **Filter Chaining:** Chain all sequential removals in a single comma-separated `-vf` string.
2. **Audio Preservation:** Always pass `-c:a copy` to preserve original uncompressed audio streams bit-for-bit with zero drift.
3. **Visually Lossless Video:** Encode with `libx264` at `CRF 17` and `preset slow`:

```bash
ffmpeg -y -i input.mov \
  -vf "delogo=x=1130:y=425:w=170:h=100:enable='between(t,171.30,177.25)',\
delogo=x=700:y=465:w=115:h=125:enable='between(t,206.60,212.45)',\
drawbox=x=0:y=0:w=1920:h=1080:color=black:t=fill:enable='between(t,98.15,99.65)',\
drawbox=x=0:y=0:w=1920:h=1080:color=black:t=fill:enable='between(t,152.80,155.20)',\
drawbox=x=0:y=0:w=1920:h=1080:color=black:t=fill:enable='between(t,185.20,187.00)',\
drawbox=x=0:y=0:w=1920:h=1080:color=black:t=fill:enable='between(t,261.00,266.96)'" \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p \
  -c:a copy \
  output_cleaned.mov
```

---

## Step 5: Automated Verification

Always verify rendered footage across every target interval using automated pixel-level checks before delivering final files. See [scripts/verify_removal.py](./scripts/verify_removal.py) for the reusable automated test script.
