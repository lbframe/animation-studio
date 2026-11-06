# Expert techniques and primary sources

Reviewed for this workflow on 2026-11-05. These are focused starting points, not an exhaustive ranking of practitioners. Recheck current APIs and tool capabilities when implementing. Use authors' methods as knowledge; respect licenses and attribution when reusing code or assets.

## Motion judgment and procedural animation

| Source | Technique to apply | Scope |
| --- | --- | --- |
| [Étienne Jacob — Looping with phase offsets](https://bleuje.com/tutorial2/) | Periodic functions and intentional phase offsets for coherent loops | Procedural loops; not a prescription for every narrative scene |
| [Étienne Jacob — Rendering workflow](https://bleuje.com/tutorial6/) | Controlled frame sampling and motion-blur workflow | Adapt the method to the actual renderer and color/alpha handling |
| [Dave Whyte / Bees & Bombs — original sketch](https://gist.github.com/beesandbombs/d9dc07757fd7e7d7a1dcf205cdc8b535) | Compact geometry driven by normalized time; study original implementation | A specific sketch, not evidence about the software behind another reference |
| [Chris Gannon — Jump Loader, SVG and GSAP](https://tympanus.net/codrops/2015/03/25/jump-loader-animation-svg-gsap/) | Orchestrated overlap and timing that give a simple loader personality | Historical article; verify modern APIs and code license before reuse |
| [Sarah Drasner — Advanced SVG Animation materials](https://github.com/sdras/frontendmasters-svganimation) | SVG structure and coordinated timeline animation | Historical teaching examples; adapt to current libraries |
| [Emil Kowalski — Train your judgement](https://emilkowal.ski/ui/train-your-judgement) | Compare concrete variants and learn to identify the visible defect | Interface motion judgment; not a universal film timing rule |
| [Emil Kowalski — Agents with taste](https://emilkowal.ski/ui/agents-with-taste) | Explicit quality criteria and review rather than accepting first output | Apply contextually; distinguish UI response timing from loop duration |

The practical correction loop is: render, inspect, name the defect, change the responsible variable, render again. In the motivating procedural study, continuous trails avoided cap artifacts, anchor/phase changes avoided crowded pendulums, and display-size checks improved label readability. These are diagnostic examples, not a template to impose on new subjects.

## Official implementation references

| Area | Primary documentation | Use |
| --- | --- | --- |
| GSAP | [Timeline](https://gsap.com/docs/v3/GSAP/Timeline/), [easing](https://gsap.com/docs/v3/Eases/), [staggers](https://gsap.com/resources/getting-started/Staggers/) | Orchestration, controlled timing, seek/reverse, phase relationships |
| Browser clock | [MDN requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) | Timestamp-based playback rather than counting callbacks |
| Browser performance | [MDN animation performance](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Animation_performance_and_frame_rate) | Measure the real target and distinguish animation from rendering cost |
| Three.js | [Animation system](https://threejs.org/manual/pages/animation-system.html) | Clips, tracks, mixer, skeletal and morph animation |
| Blender | [Rendering animations](https://docs.blender.org/manual/en/latest/render/output/animation.html) | Match documentation to installed version; frame sequences and encoding |
| Rive | [State machines](https://rive.app/docs/editor/state-machine/state-machine), [CLI](https://rive.app/docs/cli/overview) | Inputs, transitions, native authoring/export checks |
| Audio | [MDN BaseAudioContext.currentTime](https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/currentTime), [W3C Web Audio](https://www.w3.org/TR/webaudio/#dom-baseaudiocontext-currenttime) | Audio time origin and scheduling; separate audio and system clocks |
| Offline Canvas | [Skia-backed Canvas](https://github.com/Brooooooklyn/canvas) | Actual offline Canvas pixels when the package is available |
| Offline SVG | [resvg-js](https://github.com/thx/resvg-js) | Actual offline SVG rasterization; not a browser layout test |

For a new generator, renderer, codec, rig, or simulation, find its current official documentation and a representative primary example. Tool availability, a documentation claim, a successful local test, and a delivered export are separate facts. This skill routes to broader animation workflows; each task must validate its selected route.

## Packaging reference

[Agent Skills specification](https://agentskills.io/specification) defines the portable `SKILL.md` package format, metadata, relative resources, and progressive disclosure. [The official reference validator](https://github.com/agentskills/agentskills/tree/main/skills-ref) checks metadata and package structure. Passing it does not certify animation quality, script behavior, or every host integration.
