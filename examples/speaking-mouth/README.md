# Speaking mouth

[Back to the showcase](../../README.md#showcase) · [Watch the original video](https://github.com/lbframe/animation-studio/releases/download/v0.1.0/speaking-mouth.mp4)

![Animation preview](../../docs/assets/showcase/speaking-mouth/preview.gif)

A stylized mouth moves through distinct speech poses with smooth transitions, brief holds, and a stable center.

## Showcase render

| Input | Output | Method |
| --- | --- | --- |
| Supplied mouth-pose chart | 6-second loop · 720 × 720 · 30 fps · silent | Hand-authored Canvas paths and a deterministic JavaScript timeline; FFmpeg video export |

The red lips, dark cavity, teeth, and tongue are redrawn as editable shapes inspired by the chart. Closed, narrow, rounded, and open poses flow into one another. This is a silent articulation study; audio synchronization is demonstrated separately in the lyric examples.

## Original request — English translation

> @Animation Studio, use my reference image to animate a mouth.

No further correction was recorded for this example.

## Recommended prompt

Attach the mouth-pose chart, then paste:

```text
Use $create-animation to build a six-second silent mouth-animation loop
from the attached pose chart.

Keep the mouth centered and preserve the reference's red illustrated
lips, dark cavity, white teeth, and red tongue. Use coherent editable
shapes that transition smoothly between closed, narrow, rounded, and
open speech poses. Include short holds and natural rests. Keep the
teeth and tongue contained within the mouth opening.

Start and end in compatible resting poses so the loop has no visible
jump. No speech audio is supplied for this study.

Deliver editable source, a playable preview, and a 720 × 720 MP4 at
30 fps. Inspect the lip contours, interior clipping, pose differences,
and loop transition, then correct any visible defects.
```

The six-second duration, silent loop, and output settings are recommendations based on the delivered study. The original request supplied the subject and visual reference.

## Source and review notes

The original project contains `mouth.js`, `loop-state.mjs`, `render.cjs`, `build-html.py`, a motion brief, and a standalone HTML preview. The preview includes playback, seeking, speed, and background controls.

The showcased render was created before the recommended prompt was written. The prompt describes a reusable direction for this type of study; it has not been rerun to certify an identical result.
