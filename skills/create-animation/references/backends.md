# Backend selection

## Contents

- Selection criteria
- Vector and procedural 2D
- Interactive vector
- 3D
- Typography, audio, and compositing
- Raster and generated video
- Capability and export checks

## Selection criteria

Choose by output, subject, required control, available assets, and actual tool access. Do not make every task use a favorite renderer. Preserve an existing project architecture unless a concrete limitation warrants a change. First verify a small representative render/export when a route is unfamiliar or tool availability is uncertain.

GSAP is a timeline/tweening layer. SVG, Canvas, WebGL, and native engines draw the result. A scene evaluator can feed multiple renderers when that improves verification, but implementing two renderers is not a requirement for every task.

## Vector and procedural 2D

**SVG** is a good starting point for a modest number of crisp editable paths, icons, logos, diagrams, and geometric loops. Use coherent shapes and intentional line caps/joins. Set a viewBox and test the actual delivered size. Handle transform origins explicitly. Keep text exact and font availability verified.

**CSS/WAAPI** can cover simple transforms, opacity, and state transitions. **GSAP** is useful for labels, overlapping actions, nested timelines, seeking, reversal, and more complex orchestration. Verify the current API rather than copying old tutorial syntax. Advance a shared phase or timeline, not many unrelated clocks.

**Canvas** suits dense drawing, particles, trails, and generative geometry. Scale the backing store for the intended pixel density, reset drawing state deliberately, and separate evaluation from drawing. Use seeded randomness. Accumulating trails need a reproducible reset/export strategy.

**WebGL** is appropriate when shaders, dense scenes, or effects justify its complexity. Measure actual target performance before claiming a particular frame rate. Keep coordinate spaces, aspect ratio, color handling, and resolution explicit. Prevent thin repeated patterns from aliasing; more geometry is not automatically more detail.

Offline tools such as resvg or Skia-backed Canvas can produce inspectable frames when usable. Their successful renders establish those renderers' output, not browser layout, user interaction, or sustained browser performance.

## Interactive vector

Use **Rive** when editable vector assets and runtime state transitions are central and the necessary authoring/export tools are accessible. Model idle, entry, action, interruption, and exit states as appropriate. Test rapid retriggering and changing inputs, not just one uninterrupted playback.

Inspect the installed tool's version and help. CLI flags and export support can change. A valid source document, compilation, a screenshot, and a `.riv` export are separate milestones. Verify the actual exported file in a compatible runtime before claiming delivery. Keep source and editable structure when possible; do not route around unavailable export through an undisclosed raster replacement.

## 3D

Use **Three.js** for browser-based 3D interactions and scenes. Determine whether the subject needs rigid transforms, skeletal animation, morph targets, or authored clips. Check imported assets and animation names; do not assume every model format includes animation. Control camera, materials, lighting, color space, and render size deliberately.

Use **Blender** when a native editable scene, controlled lighting/materials, simulations, or offline film rendering better match the request and Blender is actually usable. Keep a reproducible scene setup. Bake simulations when needed for stable export. Render a representative segment before expensive full output. Prefer resumable frame sequences when useful, then assemble and inspect the encoded result.

For character action, prioritize a suitable rig and clear key poses. Foot contacts, center of mass, joint limits, expressions, and silhouette matter more than adding arbitrary surface detail. Do not imply a rudimentary geometric stand-in is a finished character animation.

## Typography, audio, and compositing

Use a seekable timeline in the available environment: GSAP, an appropriate video/compositing tool, or an installed specialized workflow. If an audio-led typography skill is available and relevant, read it and apply the user's existing authorization; do not invent a new approval gate.

Preserve exact text, punctuation, line breaks when intentional, and font shaping. Animate letters, words, or lines at a level that serves meaning. Ensure enough readable time. Establish audio cues before choreographing; keep one time origin and map pause/resume/seek correctly. With Web Audio, `currentTime` is an audio timeline, not the system clock.

For multi-shot work, design transitions through shared action, geometry, composition, or sound. Do not force every transition to be a crossfade. Keep safe framing and readable captions at the destination size.

## Raster and generated video

Discover whether a real image/video generation tool is exposed. Image generation alone does not imply video-generation capability. Use the host's dedicated generation/editing tools and their reference rules. Inspect source assets before requesting animation.

Break a complex request into shots with a clear subject, action, camera, environment, lighting, duration, and preservation constraints. Use supported reference frames, keyframes, motion controls, or masks when available. Generate a representative shot, inspect it, and adjust the concrete defect before expanding.

Review identity, limbs, contact, geometry, material consistency, text, temporal flicker, unwanted morphing, camera drift, and transition continuity. Add exact titles/logos in compositing when that gives reliable control. Use a deterministic overlay only when it belongs in the result.

For loops, prefer tool-supported boundary control or a justified edit; a reverse “boomerang” changes the action and should be a deliberate design choice. Do not claim perfect reference fidelity, native editability, or exact physics from a model description alone.

## Capability and export checks

Check tools, dependencies, assets, fonts, codecs, alpha support, and native export early. Follow host authorization rules for external services, paid runs, account actions, and publishing. Do authorized reversible local work without unnecessary confirmation.

When a route is blocked, evaluate a legitimate alternative against the actual acceptance criteria. Explain any material loss of fidelity or format. A storyboard or prepared prompt can be useful progress, but the completed animation still requires an actual playable output.
