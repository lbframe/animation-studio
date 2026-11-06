# Motion design

## Contents

- Readability and hierarchy
- Timing and spacing
- Procedural loops
- Physical and character action
- Typography and audio
- Camera and transitions
- Common visible defects

## Readability and hierarchy

Start with the most important action and a strong silhouette. Establish a stable reference frame before adding secondary movement. A viewer should understand what changes and why. Preserve negative space; give large motion room rather than shrinking everything to fit.

Create a small pose/beat plan: setup, action, response, and settle where applicable. Do not force that sequence onto ambient loops or direct manipulation. Style follows the subject: geometric precision, tactile weight, elastic play, or cinematic realism require different motion choices.

## Timing and spacing

Timing determines when an event occurs; spacing determines perceived velocity between samples. Adjust both. A long duration with nearly uniform spacing can still feel mechanical; a short acceleration followed by a hold can communicate intent clearly.

Use linear phase for genuinely constant motion. Use ease-out for a deliberate arrival, ease-in for departure or acceleration, and smooth reversals for oscillation when appropriate. Elasticity and overshoot should have a reason and a stable endpoint. A UI transition's timing guidance should not become an arbitrary limit on an entire film or ambient cycle.

Stagger elements to communicate a wave or dependency. Determine whether they share a period, travel speed, or trigger sequence. Make phase offsets intentional, not random decoration. Test the maximum overlap, where collisions and excess density often appear.

## Procedural loops

Use a normalized unwrapped phase `t` for analysis. For integer `k`, `sin(2πkt + phase)` and `cos(2πkt + phase)` are periodic over a unit cycle. Combine frequencies only when their periods align with the intended cycle. Derive motion from time rather than accumulated frame increments.

The visible state should agree across repeated phases, and velocity should be continuous at the seam when the action requires smooth motion. Merely applying `t % 1` can hide a jump in endpoint checks. Inspect the two sides of the seam and the sequence of neighboring rendered frames.

Keep primitive identity and topology stable when useful. For deliberate birth/death events, fade or mask at justified locations. A disappearing particle can be correct; an accidental shape-count change usually is not. A numerical checker of fixed topology needs a canonical adapter for variable scenes.

For trails, first determine whether the trail represents actual motion history, a geometric stroke, or a composited glow. Many overlapping round-capped segments can create beads and dark joins. A continuous path, deliberate cap treatment, or premultiplied compositing can be more coherent.

If adding motion blur, sample a controlled shutter interval around each output time and combine in the appropriate color/alpha space. Wrap samples correctly for a seamless loop. Blur should convey motion, not hide malformed geometry or low-quality timing.

## Physical and character action

Separate root movement, articulation, and secondary response. Establish contacts and anchors first: feet should not slide unintentionally, a hinge should rotate about its pivot, and a pendulum's bob should remain attached to its rod. Check center of mass, arcs, balance, and apparent weight.

Use anticipation, follow-through, overlap, and squash/stretch only when they suit the style and preserve recognizable volume or construction. Keep important poses readable. Secondary motion should follow the primary action's energy and settle plausibly.

For generated characters, inspect identity and anatomy over time, not just the best frame. For rigs, test extreme poses and transitions between clips. For simulations, make initial conditions and baking reproducible.

## Typography and audio

Build hierarchy around words and meaning. Preserve spelling and glyph shaping. Provide readable holds, avoid excessive simultaneous motion, and choose transformations that reinforce the message. Test thin strokes and small labels at the actual display size.

Create cue points from real audio evidence. Map hits, syllables, or phrases to movement according to intent; not every beat needs a visual event. Keep video and audio on a defined common timeline. Verify drift and sync around pauses, cuts, resuming, and the end.

## Camera and transitions

Separate camera transformation from subject transformation. Use parallax, occlusion, scale, and perspective coherently. A camera move should reveal or emphasize something, not compensate for an unfinished scene.

Choose a transition's carrier: shared shape, object movement, mask, camera, typography, or sound. Match outgoing and incoming velocity when continuity matters. Check the whole transition, including the frames where both scenes overlap.

## Common visible defects

| Observation | Likely cause | Useful correction |
| --- | --- | --- |
| Dark bumps along a trail | Overlapping segment caps/alpha | Continuous geometry or deliberate joins |
| Bobs, particles, letters merge | Phase/amplitude/spacing conflict | Adjust anchors, spacing, overlap, or timing |
| A loop briefly catches | Position/velocity mismatch or duplicate endpoint | Inspect both sides; correct timing and export grid |
| A path jitters at small size | Aliasing, unstable rounding, subpixel treatment | Render at target size; adjust stroke/density/sample strategy |
| Motion feels uniformly mechanical | Unmotivated identical easing and timing | Establish lead/response and purposeful spacing |
| Text is crisp enlarged but unreadable in use | Wrong display-size assumptions | Increase actual readable size or simplify layout |
| Character changes between frames | Inconsistent identity/rig/generation | Improve references, constraints, rig, or regenerate the affected shot |

These are diagnostic possibilities, not automatic rules. Preserve intentional visual effects when they serve the reference or brief.
