# Installation

## Install with your agent

Copy the installation prompt from [Quick install](../README.md#quick-install) into your agent. It identifies the complete skill directory and asks the agent to verify its installation using the method supported by its host.

The installable unit is **`skills/create-animation/`**. Keep the directory together: `SKILL.md` links to the scripts, reference guides, and assets beside it. The public project name is **Animation Studio**; the skill identifier is **`create-animation`**.

## Install manually

1. Obtain the repository or a release containing the complete skill directory.
2. Read `skills/create-animation/SKILL.md` and inspect its bundled resources.
3. Copy `create-animation/` into a skill location supported by your agent. Use the host's current installation instructions to choose between project and personal scope.
4. Confirm that the copied folder still contains `SKILL.md`, `references/`, `scripts/`, and `assets/`. Preserve `agents/` when present.
5. Refresh skill discovery if the host requires it, then ask the agent to use `create-animation`.

Installation paths, discovery, and invocation syntax vary by host. The [Agent Skills specification](https://agentskills.io/specification) defines the portable folder format; the host determines how that folder is installed and activated.

## Dependencies are selected per task

Installing the instructions does not require every animation engine. The agent checks the tools needed for the chosen output before starting production.

| Task | Requirements |
| --- | --- |
| Read and use the skill | An agent that can load the skill and access the supplied reference files |
| Run `scripts/inspect_reference.py` on an image | Python 3.10+ and Pillow |
| Run the reference helper on a video | Python 3.10+, Pillow, and `ffmpeg` / `ffprobe` on `PATH` |
| Run `scripts/check_loop.mjs` | Node.js 18+ and a trusted module exporting `sample(t)`; no npm package is required by this helper |
| Render or export an animation | The renderer, fonts, assets, codecs, and other dependencies required by that project |
| Use a generation service or a native authoring application | Actual access to that tool and its supported output format |

The [backend guide](../skills/create-animation/references/backends.md) explains how the skill chooses a route. Individual showcase projects may have additional requirements; their dependencies are separate from the skill's two helpers.

## Verify and start

Ask the agent to report the installed location, resolved resource links, discovery status, and any missing dependencies. A successful file copy does not by itself verify rendering or video export.

Start with a description or attach a reference:

```text
Use the create-animation skill to create a five-second animation from the
attached image. Preserve its composition and colors, choose a suitable
motion treatment, and deliver a playable preview with editable source.
Inspect the result and correct visible defects before delivering it.
```

For updates, compare the installed version with the new version and preserve local customizations before replacing files.
