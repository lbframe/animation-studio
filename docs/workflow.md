# How Animation Studio works

Animation Studio gives an agent a production workflow for turning a description or reference into an animation. Its [core instructions](../skills/create-animation/SKILL.md) cover the brief, implementation, rendering, review, and delivery.

## Start with the intent

Describe what should move, what the viewer should notice, and where the result will be used. Attach an image or video when its appearance or movement matters. Add exact text, duration, aspect ratio, audio, and export requirements when you have them; the agent can choose reasonable defaults for the rest.

| Input | What the agent establishes |
| --- | --- |
| Written description | Subject, action, visual direction, timing, and deliverables |
| Image | Visible composition and identity, then a proposed motion treatment |
| Video or accessible reference link | Observable timing and movement in the actual accessible media |
| Audio with text | Exact wording, timing cues, readable typography, and the relationship between sound and motion |

A still image does not establish timing. A contact sheet does not establish continuous playback. The workflow separates observed details from estimates and creative proposals.

## Produce, inspect, improve

1. **Define the brief.** Preserve the subject, wording, hierarchy, and delivery constraints. Decide whether the animation loops, ends, or responds to interaction.
2. **Choose the tools.** Match the output to an available renderer or generator. Verify native formats and export capabilities before promising them.
3. **Design the motion.** Plan key poses, rhythm, transitions, readable holds, and continuity. Give moving elements a clear role.
4. **Build and render.** Produce editable source and a playable result. Keep assets and dependencies traceable.
5. **Review and correct.** Inspect the actual render for clipping, identity changes, awkward timing, loop seams, and delivery problems. Re-render the affected passage after a correction.
6. **Deliver with evidence.** Provide the preview or export, useful source files, and an accurate account of what was checked.

## Tools follow the result

The skill can guide vector motion, procedural drawing, kinetic typography, image compositing, interactive animation, 3D, and generated footage. Each route depends on the tools available in the current environment. Installing the skill does not install those engines or make an unavailable service accessible.

For precise vector motion, SVG or Canvas may be appropriate. Audio-led typography benefits from a seekable timeline. Native 3D and generated footage need their respective authoring or generation tools. See [backend selection](../skills/create-animation/references/backends.md) for the decision criteria.

## Read the showcase accurately

The showcase contains existing renders made from the user's original requests. Each example distinguishes the faithful English translation of that request from a newly edited recommended prompt. Rewording a prompt does not retroactively change how its historical render was created.

Canvas studies, HyperFrames projects, and the garden cinemagraph use different production routes. The garden is image compositing; the hero study animates a supplied screenshot. Source availability and successful encoding do not certify every browser, device, or animation engine.

Review the [examples](../README.md#showcase) for prompts and results, and the skill's [quality guide](../skills/create-animation/references/quality.md) for its inspection criteria.
