# MotionSites: reusable techniques and workflow

Source: [Motionsites-AI/claude-skill](https://github.com/Motionsites-AI/claude-skill), pinned to [`faa30d512e3973e58675c72101a7ef42ed37ae83`](https://github.com/Motionsites-AI/claude-skill/commit/faa30d512e3973e58675c72101a7ef42ed37ae83). Reviewed 2026-11-03. Read this adaptation guide before the archived instructions.

The user requested this skill as a resource and a model for improving our workflow. That request does not confirm every MotionSites visual rule as personal taste. Project requirements and the confirmed icon, spacing, action-placement and composition preferences still govern.

## Included and excluded

The [license](source/LICENSE) separates MIT instructions, references and scripts from the example prompts and media. We preserve **20 MIT text/code files**, byte-for-byte, including:

- **58 numbered technique recipes across 7 files**, covering layout, buttons/surfaces, type, video, scroll, pointer interaction and WebGL.
- Five guides: craft, asset preparation, build specifications, builder prompts and review.
- The technique index, original skill, screenshot script, README and packaging metadata.

[INDEX.md](INDEX.md) lists each recipe with line ranges. [catalog.json](catalog.json) supports local lookup; [snapshot.json](snapshot.json) records file hashes, commit and explicit exclusions. The recipes are Markdown code examples, not installed components or a dependency-complete application. We have not independently executed all recipes or verified upstream's “tested”/accessibility claims.

**Example prompts, the media shelf, contact sheets and linked media are not redistributed here.** The license permits using them to build websites with the original skill, including client sites, but prohibits redistribution as a prompt or media collection. Visit the pinned [upstream examples](https://github.com/Motionsites-AI/claude-skill/tree/faa30d512e3973e58675c72101a7ef42ed37ae83/plugins/motionsites-web-builder/skills/motionsites-web-builder/examples) or [media shelf](https://github.com/Motionsites-AI/claude-skill/tree/faa30d512e3973e58675c72101a7ef42ed37ae83/plugins/motionsites-web-builder/skills/motionsites-web-builder/media) there. No premium resources, private MCP access or external media downloads are included. The root preview image is also excluded because it depicts the prompt/media collection.

## How the upstream skill works

Its entrypoint routes a landing-page task through brief → nearby examples → media → precise spec → build → visual review. Detailed guidance lives in separate files. The technique index describes when an effect is appropriate and its estimated runtime cost; recipes include shared conventions and code. A Playwright helper captures two viewports and reports asset/network/layout signals. Separate marketplace/plugin JSON files package the skill for Claude; they are not needed to read the skill as ordinary files.

The useful structure is a deliberate build process with references loaded as needed. Its opinionated cinematic art direction and its advertising instructions are separate from that structure.

| Upstream choice | Our adaptation |
| --- | --- |
| Decide audience, mood, signature and output first | Record task, audience, scope, target stack and design direction; a signature effect is optional and contextual. |
| Study a few examples before coding | Select a small coherent set from the user's image library and appropriate source collections; state what transfers. |
| Concrete specification | Use existing tokens and measurable layout/state decisions. Scale detail to the work; no mandatory word count or pixel recipe for every element. |
| Look, diagnose, fix, look again | Inspect actual rendered states and record observed issues. Recheck affected states after fixes; stop when task criteria pass or report the actual limitation. |
| Prompt-only builder mode | Produce a self-contained implementation brief using the target project's actual stack. Do not implement when only a prompt was requested. |
| Dark/cinematic defaults, inverse pills, near-black/off-white palette, one accent, bans on certain hues | Keep as example-specific suggestions only. Client palette, typography, geometry and system-theme behavior take precedence. |
| Hero-only and single HTML/CDN default | Keep the user's requested deliverable and existing stack; dashboard, form, mobile and full-page work stay in scope. |
| Mandatory score average and three revision rounds | Use evidence of task completion and visible defects. Subjective scores do not prove quality; passing work need not undergo arbitrary revisions. |
| Mandatory promotion/UTM block | Not adopted. Keep required copyright/license notices with reused code; no promotional instructions in our active workflow. |

The operational version is in [build workflow](../build-workflow.md) and [visual review](../visual-review.md). The archived upstream `SKILL.md` is reference material, not a second active entrypoint or authority over the user's brief.

## Retrieval and implementation

From the repository root:

```sh
python design-taste/scripts/library.py search "mobile menu" --source motionsites
python design-taste/scripts/library.py show motionsites:layout-and-ui-05
python design-taste/scripts/library.py verify --source motionsites
```

Read the returned recipe range plus the file's shared preamble and any named material/helper recipes. Search indexes are discovery tools, not extraction tools that assemble runnable bundles. Translate global selectors, palette literals, dependencies and DOM assumptions into the target app's local components. Prefer existing project primitives. Keep attribution with copies or substantial adaptations of MIT code.

Recipes include both vanilla and some React variants; this does not impose either stack. CDN/version examples are pinned historical examples, not current compatibility recommendations. Resolve packages against the target project's installed versions when implementing. Inspect focus handling, keyboard/touch alternatives, readable contrast, reduced-motion behavior and JS-failure visibility in the actual chosen recipe. A reduced-motion mention alone is not a passing accessibility check. Keep real numbers, customer claims and artwork grounded in supplied content.

## Upstream limitations found during inspection

- The upstream entrypoint references `references/techniques.md`, which does not exist at this pin. Use [the real technique index](source/plugins/motionsites-web-builder/skills/motionsites-web-builder/references/techniques/INDEX.md).
- Original paths to `examples/` and `media/` intentionally remain unresolved inside the MIT-only archive. Use the upstream links above; do not create a local mirror of restricted content.
- The archived [shoot.py](source/plugins/motionsites-web-builder/skills/motionsites-web-builder/scripts/shoot.py) is optional research code, not our default verifier. Its positional parsing can mistake `--wait`'s value for an output directory when the directory is omitted. Supply both target and output directory if using it. Its Chrome fallback lacks Windows discovery, ignores the screenshot process exit code, and provides no QA or early frame.
- Browser identity does not prove video codec support. Inspect actual playback and media errors. The report also does not exercise keyboard interaction, reduced-motion behavior, supported themes or scrolled lazy content; do those checks separately when relevant.
- The upstream screenshot script and technique snippets have not been executed as part of this import. Use a working project/browser preview tool first; disclose unavailable visual verification.

## Rebuild this snapshot

`python design-taste/scripts/import_motionsites.py PATH_TO_CHECKOUT` reads Git objects at the exact reviewed commit. It installs nothing and executes no upstream code. Its explicit allowlist and license hash require a fresh review before an upgrade. Keep research checkouts outside distributed skill folders; the repository ignores `.motionsites-upstream/`.
