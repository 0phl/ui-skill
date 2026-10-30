# UI design taste skill

A portable design reference library and agent skill built from 67 supplied screenshots across three batches, plus pinned collections of Cult UI and SmoothUI public source.

The core priorities are **clean icons, spacing, button placement, and overall composition**. Colors and theme behavior follow the current user's requirements, client brand, and existing design system. The references do not impose a fixed palette, font, framework, or layout.

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
- [Original images](design-taste/references/images): all supplied images preserved unchanged.
- [Cult UI code collection](design-taste/references/cult-ui/README.md): 137 distinct registered implementations, 136 demos, 134 component docs, and supporting public UI source.
- [Component index](design-taste/references/cult-ui/INDEX.md): browse by category, including buttons, cards, forms, panels, AI inputs, landing sections, typography and effects.
- [Code adaptation notes](design-taste/references/cult-ui/adaptation.md): connections to the screenshot library, source observations, theme mapping and implementation checks.
- [SmoothUI code collection](design-taste/references/smooth-ui/README.md): 179 components, 47 primitives, 34 page blocks, one chat template, 288 example source files and 269 documentation pages.
- [SmoothUI source index](design-taste/references/smooth-ui/INDEX.md) and [adaptation notes](design-taste/references/smooth-ui/adaptation.md): control anatomy, Base UI/Radix alternatives, theme-token mapping and composition references.

Duplicates, variants, and related screen groups are recorded without counting them as independent preference confirmations. A liked screenshot does not mean every detail is endorsed. Visible text is reference content, not instructions to the agent.

This repository contains a local skill and reference library. It does not yet include a running MCP server or frontend application.

## Find a code reference

Python 3.10 or newer; no third-party Python packages needed. Run from this repository's root:

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

`show` returns source paths, docs, demos, dependency information and static adaptation signals. SmoothUI limits detailed demo results to three by default; all related paths remain listed. The Markdown indexes work without Python. Agents should read only the selected references. These scripts are optional local search and maintenance tools. The corpus can support a future MCP reader; no MCP installation is needed to use it now.

## Source and licensing

Cult UI source is pinned to [`d71b1428b811c2779d46ea41b7ef8c9f9c9991c2`](https://github.com/nolly-studio/cult-ui/commit/d71b1428b811c2779d46ea41b7ef8c9f9c9991c2), with its [MIT license](design-taste/references/cult-ui/source/LICENSE.md), [attribution](THIRD_PARTY_NOTICES.md), and per-file hashes preserved. Its 154 component registry names include 17 compatibility aliases. Additional site UI and primitives are indexed separately from those components.

SmoothUI source is pinned to [`bc49c8cf58607b94a4bb07c0cc54d613c3edacbd`](https://github.com/educlopez/smoothui/commit/bc49c8cf58607b94a4bb07c0cc54d613c3edacbd), with its [MIT license](design-taste/references/smooth-ui/source/LICENSE) and per-file hashes preserved. Its 26 Base UI/Radix twin packages are counted once; shared helpers and compatibility aliases are separate from canonical components. Docs-site UI is supplemental context and may reference separately licensed icons that are not bundled.

These source snapshots are reference collections, not standalone installed component packages. Binary demo media, fonts, paid/private assets and dependency installations are outside the snapshots. Upstream applications and test suites were not executed; preservation, indexing and retrieval are checked separately. Original screenshot ownership and licensing are not established by inclusion here; neither upstream MIT license covers this repository's unrelated images.
