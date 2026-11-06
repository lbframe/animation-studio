# Quality checks and delivery

## Contents

- Evidence levels
- Visual inspection
- Procedural loop checker
- Interaction and audio
- Export and final delivery

## Evidence levels

Report precisely what each method establishes:

| Method | What it can establish | What it does not establish |
| --- | --- | --- |
| Compile or syntax validation | Code/source can be processed | Correct visible animation |
| State sampling | Geometry/state invariants at sampled times | Raster appearance or all-time correctness |
| Offline rendered frames | Actual pixels in that renderer | Browser layout or real-time performance |
| DOM simulation | Selected control and event logic | Browser rendering, accessibility, or FPS |
| Real playback in target runtime | Observed motion and behavior under tested conditions | Universal device performance |
| Encoded video metadata | File duration, dimensions, codec, nominal cadence | Smooth real-time runtime playback |

Do not invent beauty scores, claim “60 FPS” from a 60 fps export, or claim to hear audio from stream metadata. A second reviewer should inspect the raw request/reference/output, without the author's preferred conclusions.

## Visual inspection

Watch the available motion at normal speed, then inspect fast events and boundaries more closely. Read full-size frames at significant poses. If continuous playback is unavailable, use a sufficiently dense chronological sample and state that review scope. Never substitute a successful render command for looking at the pixels.

Check the actual delivery scale and a close-up. For a responsive component, inspect a small and a representative larger viewport when the runtime allows it. Verify the visible subject and important details against the reference, using aligned framing/phase where meaningful. A pixel difference between different renderers or retimed creative interpretations is not a universal fidelity score.

Review geometry and identity: stable shapes, attachment points, correct layering, meaningful contacts, readable silhouettes, exact text, no unintended clipping or morphing. Review line caps, joins, opacity, transparent edges, material/light continuity, and dense-pattern aliasing.

Review timing: purposeful acceleration, holds, stagger, action/reaction, camera motion, transition logic, beginning, and ending. For a loop, inspect multiple cycles and the join. Compare the last-to-first frame change with nearby frame changes as a diagnostic; no universal numeric threshold proves an invisible seam.

Record defects concretely: “the trail has dark knots at segment joins around 0.8 s,” not “needs polish.” Change the relevant geometry/compositing/timing, render again, and inspect the corrected region and its neighbors. A fresh full review is warranted when a change affects the whole sequence; otherwise avoid rerunning unrelated checks.

## Procedural loop checker

The helper uses Node.js 18+ without npm dependencies and requires a local trusted JavaScript module exporting `sample(t)`. Importing a module executes its code. Use the generated project module or a reviewed adapter; do not import untrusted downloaded code merely to inspect a reference.

The return value must contain a stable object/array of finite numbers, strings, booleans, or null, with at least one number. Time is normalized to one cycle and must work outside `[0,1]`. An adapter can sample actual visible landmarks from the production evaluator:

```javascript
export function sample(t) {
  const angle = 2 * Math.PI * t;
  return { x: 80 * Math.cos(angle), y: 80 * Math.sin(angle) };
}
```

Do not replace the real scene with a convenient unrelated circle just to obtain a pass. Supply canonical geometry for equivalent rotations. For variable topology, select stable landmarks and visibility weights, then visually inspect births/deaths separately. Do not force periodic tests onto a finite animation or interactive state machine.

```bash
node scripts/check_loop.mjs /absolute/project/loop-state.mjs --samples 128 --atol 0.000001 --rtol 0.00001 --step 0.0001
```

Defaults: 128 phases, absolute tolerance `1e-6`, relative tolerance `1e-5`, finite-difference step `1e-4` cycles. Position and derivative tolerances use the sampled state's units; velocity is per cycle. Options accept 8–4096 samples and a step from `1e-7` to `0.01`.

The helper compares `F(t)` and `F(t+1)`, checks finite values and structure, and estimates both sides of the position/velocity seam at phases 0 and 1. This catches a modulo ramp whose exact endpoints misleadingly agree and a triangle wave whose position closes but velocity jumps. It does not prove smoothness at every interior time, inspect pixels, or measure FPS.

Exit codes: 0 means the sampled checks passed; 1 means a state/loop defect; 2 means an input/runtime error. Read the JSON errors and the affected field/phase. A borderline numerical result can be checked with a second step size and unit-aware tolerance. Do not loosen tolerances simply to conceal a real discontinuity.

For rendered closure, compare the same phase one cycle apart when reproducible. The last exported frame is normally at `(N-1)/N`, not at phase 1, so it should not be forced to equal the first frame. Inspect their transition instead. Verify that the export contains the intended number of distinct time samples and no appended duplicate endpoint.

For a finite ending, verify the intended hold in the actual scene state and rendered output. Distinguish lossless source-frame identity from small decoded-pixel differences introduced by lossy encoding; diagnose the difference before calling it residual motion or claiming exact encoded-pixel equality.

## Interaction and audio

For interactive work, test the intended inputs, enter/leave, rapid repeat, reversal, interruption, completion, and return to idle where relevant. Verify cleanup and restart in the actual runtime when possible. Respect reduced-motion preferences and provide pause/stop where appropriate to the surrounding interface. A real progress indicator should reflect the real task rather than introduce artificial delay.

For audio, verify timing around early and late cues to detect drift, plus pause/seek behavior if interactive. Inspect the actual exported audio track and playback when accessible. Clearly distinguish a cue sheet derived from waveform/transcript from a listening review.

## Export and final delivery

Check the final encoded artifact, not only its source frames. Verify requested dimensions/aspect ratio, duration, frame count/cadence, codec, alpha, audio, and loop/end behavior as applicable. Inspect an actual frame after encoding for color, clipping, or transparency changes. A format conversion does not guarantee an alpha channel survives.

Make editable sources usable: include required assets, document dependencies/versions and a concise render/run command. Avoid absolute paths to the author's temporary workspace inside the delivered project. Provide only meaningful controls. Keep debug overlays and implementation details out of the finished animation unless requested.

Follow the host's current preview, file persistence, and repository instructions. Do not publish externally without authorization, and do not create a deployment merely to avoid a restricted local preview. A legitimate offline renderer is a separate verification route, not a way to claim forbidden browser execution.

In the final reply, lead with the animation and chosen result. State what was corrected and verified in ordinary language. Include only limitations that materially affect use or confidence. If an essential route is unavailable, deliver useful completed preparation while identifying the remaining step; do not call that preparation a completed film.
