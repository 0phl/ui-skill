# Cult UI code reference collection

The user explicitly identified [Cult UI](https://www.cult-ui.com/) as matching their component-design taste and requested reusable public code references. This collection preserves the public source and explains how to use it with the existing visual library. The current user/client theme always takes precedence over source colors.

Upstream: [nolly-studio/cult-ui](https://github.com/nolly-studio/cult-ui). Pinned commit: [`d71b1428b811c2779d46ea41b7ef8c9f9c9991c2`](https://github.com/nolly-studio/cult-ui/commit/d71b1428b811c2779d46ea41b7ef8c9f9c9991c2), dated 2026-10-29. Imported 2026-10-30. [MIT license and original notice](source/LICENSE.md) preserved unchanged.

## What is included

| Material | Count | Meaning |
| --- | ---: | --- |
| Registered component implementations | 137 | Distinct source-bearing `registry:ui` entries |
| Component aliases | 17 | Deprecated names forwarding to canonical entries; 154 names total |
| Demo implementations | 136 | Source-bearing example entries |
| Demo aliases | 17 | 153 example names total |
| Component documentation pages | 134 | Original MDX with usage, installation and demo references |
| Supplemental TSX files | 212 | Unregistered UI, one public authentication block, shared primitives, AI elements, site UI and theme showcases; not 212 additional standalone Cult components |
| Preserved source/context files | 683 | 4,553,749 bytes; includes the above plus hooks, utilities, styles, docs and configuration |

Every declared file in all 307 upstream registry entries is present. The source also includes four unregistered UI implementations (`expandable-card`, `glow-button`, `type-animate`, and `shader-shape-lens-blur copy`). They are retained as supplemental material, without assuming they are supported public registry APIs.

Binary images, videos, fonts, generated duplicate registry payloads, hosting routes, CI, agent configuration, installed dependencies and paid/private products are excluded. Existing URLs and asset references remain in the code for traceability; choose appropriate project-owned assets before reuse. The source tree preserves upstream paths and bytes. It is not a complete runnable clone of the documentation website.

## Retrieve a small relevant set

1. Browse the [category index](INDEX.md), or search with the script below.
2. Inspect a canonical component with `show`; aliases resolve to their target.
3. Read its implementation, one suitable demo, local dependencies and relevant documentation.
4. Use [adaptation notes](adaptation.md) to connect code anatomy to the user's priorities and the chosen screenshot family.
5. Implement and test in the target project's actual framework, theme and interaction context.

From the repository root:

```sh
python design-taste/scripts/cult_ui.py categories
python design-taste/scripts/cult_ui.py search "halo button"
python design-taste/scripts/cult_ui.py search --category "Cards" --json
python design-taste/scripts/cult_ui.py show animated-button
python design-taste/scripts/cult_ui.py search "kanban" --kind example
python design-taste/scripts/cult_ui.py supplemental "authentication"
```

If this skill has been copied elsewhere, resolve the script relative to its `SKILL.md`. Python 3.10+ is sufficient; no packages or network are required for search, show or verify. Without Python, use the Markdown index and [JSON catalog](catalog.json). Avoid loading the entire source tree into an agent context.

## Data contract

Paths in `catalog.json` and `snapshot.json` are relative to **this directory**. The original image catalog remains separate and its IDs retain their meanings.

- `entries`: 307 registry records with names, kinds, canonical alias targets, source paths, docs, example names, upstream metadata and pinned GitHub source links.
- `analysis`: a static import closure, upstream package version declarations, local dependency paths, unresolved import candidates, external URL/asset references and source-text signals. It examines the named implementation; demos carry their own analysis.
- `supplemental_sources`: additional TSX paths with an explicit group distinguishing primitives, site UI, theme showcases and unregistered code.
- `snapshot.json`: provenance, scope, counts and an authoritative file manifest with original Git blob IDs, SHA-256 hashes and byte lengths.

The scanners are heuristics, not a TypeScript compiler. They ignore ordinary comments and template code samples when collecting imports, but do not fully evaluate dynamic imports, JSX, generated classes or template interpolation. A dependency import may be unused. A reduced-motion mention does not prove comprehensive reduced-motion behavior. Literal colors and semantic tokens can occur in the same component. Asset URLs are observations, not fetched or verified resources.

Registry metadata is preserved verbatim. `analysis.npm_imports` also exposes dependencies the metadata may not declare. For example, `minimal-card` imports `next/image` even though that import is unused in its rendered image implementation. Read the source before treating a listed dependency as essential.

## Reuse and verification

The source uses React and Tailwind, with optional dependencies such as Motion, Base UI, Radix, Vaul, Next.js, charting and graphics packages depending on the component. The upstream app package manifest records its environment; it is not a recommendation to install the entire website toolchain. Source colors and global theme configuration are examples, not skill-wide requirements.

Keep [LICENSE.md](source/LICENSE.md) with copied source or substantial adaptations. Do not overwrite the preserved snapshot to customize a component for a project; work in the target application's files, so the reference remains reproducible. See the repository's [third-party notices](../../../THIRD_PARTY_NOTICES.md).

```sh
python design-taste/scripts/cult_ui.py verify
python -m unittest discover -s design-taste/scripts -p test_cult_ui.py -v
```

These checks validate source integrity, complete registry coverage, links between catalog entries, aliases, search results and known scanner behavior. They do not install, compile, render or prove accessibility of all upstream components. No upstream runtime scripts were executed during import.

For maintainers, `design-taste/scripts/import_cult_ui.py --checkout PATH --commit FULL_SHA` rebuilds the generated snapshot from Git objects in a local Cult UI checkout. HEAD must match the full commit. It rejects overwriting an existing snapshot with a different commit. For an upgrade, prepare a separate working copy, review the new license and selection changes, rebuild there, run checks, and compare before replacing this snapshot. Partial clones must have the selected blobs available; Git may fetch missing objects. Import never executes upstream JavaScript or installs dependencies.
