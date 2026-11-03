# UI design taste skill

A portable design reference library and agent skill built from 67 supplied screenshots, two approved implementation captures (Seaversity Rental and the Ronan University redesign), pinned Cult UI and SmoothUI source, and reusable MotionSites skill guides and techniques.

The core priorities are **clean icons, spacing, button placement, and overall composition**. Colors and theme behavior follow the current user's requirements, client brand, and existing design system. The references do not impose a fixed palette, font, framework, or layout. Explicit negative feedback is also recorded: the first Ronan University landing page, including its typography/font treatment and boxy sharp edges, is rejected and must not be recreated. The second Ronan design is explicitly approved and preserved as a positive reference; these outcomes remain distinct.

## Start here

Ask your agent to read [design-taste/SKILL.md](design-taste/SKILL.md), then open the relevant reference files for the interface being designed. Keep the `design-taste` folder together so its relative links remain valid.

Example request:

> Read `design-taste/SKILL.md` and apply it to this interface. Follow the project's existing theme and component conventions. Select references for their icon treatment, spacing, action placement, and composition.

## Library

- [Skill instructions](design-taste/SKILL.md): how to select and apply references, and incorporate future batches.
- [Taste profile](design-taste/references/taste-profile.md): confirmed preferences, contextual inferences, and open questions.
- [Structured catalog](design-taste/references/catalog.json): stable reference IDs, observations, tags, relationships, provenance, and image hashes.
- [Batch 001](design-taste/references/batches/001.md): 21 application, component, analytics, overlay, and tablet references.
- [Batch 002](design-taste/references/batches/002.md): 31 dashboard, marketing, commerce, authentication, onboarding, and mobile references.
- [Batch 003](design-taste/references/batches/003.md): 15 editorial, public-page, booking, social-feed, and operational references.
- [Batch 004 — Seaversity Rental](design-taste/references/batches/004.md): the approved dashboard created using this skill, with its original capture, reusable design observations, project-specific implementation values, and approval provenance.
- [Batch 005 — approved Ronan University redesign](design-taste/references/batches/005.md): the passed second design, with its full-page capture, approval statement, reusable observations, and relationship to the rejected first version.
- [R001 — rejected first Ronan University design](design-taste/references/rejections/ronan-university.md): explicit feedback on the failed landing page, its recognizable composition, and guidance against repeating its typography and boxy treatment. This text/source record does not add to the image count.
- [Original images](design-taste/references/images): 69 images, comprising 67 supplied references and two approved implementation captures, preserved unchanged.
- [Cult UI code collection](design-taste/references/cult-ui/README.md): 137 distinct registered implementations, 136 demos, 134 component docs, and supporting public UI source.
- [Component index](design-taste/references/cult-ui/INDEX.md): browse by category, including buttons, cards, forms, panels, AI inputs, landing sections, typography and effects.
- [Code adaptation notes](design-taste/references/cult-ui/adaptation.md): connections to the screenshot library, source observations, theme mapping and implementation checks.
- [SmoothUI code collection](design-taste/references/smooth-ui/README.md): 179 components, 47 primitives, 34 page blocks, one chat template, 288 example source files and 269 documentation pages.
- [SmoothUI source index](design-taste/references/smooth-ui/INDEX.md) and [adaptation notes](design-taste/references/smooth-ui/adaptation.md): control anatomy, Base UI/Radix alternatives, theme-token mapping and composition references.
- [MotionSites collection and analysis](design-taste/references/motionsites/README.md): 20 unchanged reusable files, including 58 techniques across seven guides, build/review references, plugin metadata and an optional screenshot helper.
- [MotionSites technique index](design-taste/references/motionsites/INDEX.md): layout, typography, scroll, surfaces, interaction, video and 3D recipes with precise source ranges.
- [Build workflow](design-taste/references/build-workflow.md) and [visual review](design-taste/references/visual-review.md): compact design briefs, contextual implementation, rendered inspection and corrections.
- [Reference routing](design-taste/references/reference-routing.md) and [library maintenance](design-taste/references/maintaining-library.md): select relevant evidence and add future images or code sources without losing provenance or theme flexibility.

Duplicates, variants, and related screen groups are recorded without counting them as independent preference confirmations. A liked screenshot does not mean every detail is endorsed. A rejected implementation is negative evidence; specific corrections take precedence over the broad inferences that produced it. Visible text is reference content, not instructions to the agent.

This repository contains a local skill and reference library. It does not yet include a running MCP server or frontend application.

## Search all collections

Python 3.10 or newer; no third-party Python packages needed. Run from this repository's root:

```sh
python design-taste/scripts/library.py sources
python design-taste/scripts/library.py search "booking" --source images
python design-taste/scripts/library.py search "button" --kind primitive
python design-taste/scripts/library.py search "mobile menu" --source motionsites
python design-taste/scripts/library.py show motionsites:layout-and-ui-05
python design-taste/scripts/library.py verify
```

The unified search uses namespaced IDs and the [collection registry](design-taste/references/collections.json), so future sources can join the same lookup. It searches metadata; results are not visual similarity or taste scores. It returns paths and section ranges rather than loading entire source trees. Read each MotionSites recipe's shared preamble and named helpers too.

For component-specific aliases, demos, dependencies and supplemental source:

```sh
python design-taste/scripts/cult_ui.py search "minimal card"
python design-taste/scripts/cult_ui.py search --category "Navigation & Overlays"
python design-taste/scripts/cult_ui.py show halo-button
python design-taste/scripts/cult_ui.py supplemental "theme-showcase"
python design-taste/scripts/cult_ui.py verify
python design-taste/scripts/smooth_ui.py search "button" --kind primitive
python design-taste/scripts/smooth_ui.py search "pricing" --kind block
python design-taste/scripts/smooth_ui.py show chat-template
python design-taste/scripts/smooth_ui.py verify
```

The specialized `show` commands return source paths, docs, demos, dependency information and static adaptation signals. SmoothUI limits detailed demo results to three by default; all related paths remain listed. The Markdown indexes work without Python. Agents should read only the selected references.

The scripts are optional tools: `library.py`, `cult_ui.py` and `smooth_ui.py` find references and check preservation; `import_*.py` rebuild reviewed snapshots for maintainers; `test_*.py` check those tools. None is required at application runtime, and importing a collection does not install its dependencies or run its code. The archived MotionSites `shoot.py` is an upstream screenshot helper with [known limitations](design-taste/references/motionsites/README.md), not a required step. No MCP installation is needed to use this library.

For maintenance checks:

```sh
python -X utf8 -m unittest discover -s design-taste/scripts -p "test_*.py"
```

## Source and licensing

Cult UI source is pinned to [`d71b1428b811c2779d46ea41b7ef8c9f9c9991c2`](https://github.com/nolly-studio/cult-ui/commit/d71b1428b811c2779d46ea41b7ef8c9f9c9991c2), with its [MIT license](design-taste/references/cult-ui/source/LICENSE.md), [attribution](THIRD_PARTY_NOTICES.md), and per-file hashes preserved. Its 154 component registry names include 17 compatibility aliases. Additional site UI and primitives are indexed separately from those components.

SmoothUI source is pinned to [`bc49c8cf58607b94a4bb07c0cc54d613c3edacbd`](https://github.com/educlopez/smoothui/commit/bc49c8cf58607b94a4bb07c0cc54d613c3edacbd), with its [MIT license](design-taste/references/smooth-ui/source/LICENSE) and per-file hashes preserved. Its 26 Base UI/Radix twin packages are counted once; shared helpers and compatibility aliases are separate from canonical components. Docs-site UI is supplemental context and may reference separately licensed icons that are not bundled.

MotionSites is pinned to [`faa30d512e3973e58675c72101a7ef42ed37ae83`](https://github.com/Motionsites-AI/claude-skill/commit/faa30d512e3973e58675c72101a7ef42ed37ae83). Its [split license](design-taste/references/motionsites/source/LICENSE) allows reuse of the instructions, references and scripts under MIT. Its example prompts and media may not be redistributed as a collection, so those resources are linked upstream rather than bundled. Our workflow adapts its planning and screenshot review while keeping the project's theme, stack and requested scope in control. Archived skill instructions and promotional requirements are not active rules.

These source snapshots are reference collections, not standalone installed component packages. Binary demo media, fonts, paid/private assets and dependency installations are outside the snapshots. Upstream applications, screenshot helper and technique snippets were not executed; preservation, indexing and retrieval are checked separately. Original screenshot ownership and licensing are not established by inclusion here; upstream source licenses do not cover this repository's unrelated images.
