# Applying SmoothUI to this design taste

This guide combines inspected source with proposed applications. The confirmed preference is the overall SmoothUI direction, with the same icon, spacing, action-placement and composition priorities as the image library. It does not establish a required animation style, pink accent, font, framework or component package.

## Choose by the task

| Task | Useful source references | Connection to supplied images |
| --- | --- | --- |
| Buttons and local actions | [SmoothButton](source/packages/smoothui/components/smooth-button/smooth-button.base.tsx), [demo](source/apps/docs/examples/smooth-button.tsx) | C04; page/panel/item action hierarchy in B002-05, B002-17 and B003-14 |
| Forms and authentication | [AuthForm](source/packages/smoothui/components/auth-form/index.tsx), [FloatInput](source/packages/smoothui/components/float-input/index.tsx) | Label/control rhythm and a clear submit area in B001-06 and B002-23–29 |
| Navigation and overlays | [Sidebar](source/packages/smoothui/components/sidebar/index.tsx), [Dialog](source/packages/smoothui/components/dialog/index.tsx), [Command](source/packages/smoothui/components/command/index.tsx) | Expanded/compact navigation in B002-08/09; focused overlays in B001-19/20 and B003-11–14 |
| AI composition | [Prompt input](source/packages/smoothui/components/ai-prompt-input/index.tsx), [chat template](source/packages/smoothui/templates/chat-template/index.tsx), [template docs](source/apps/docs/content/docs/templates/chat.mdx) | Composer focus in B001-11/14 and B002-12; local attachments and actions |
| Public page sections | [CTA 1](source/packages/smoothui/blocks/ctas/cta-1/index.tsx), [block index](INDEX.md#block) | Message/action grouping and section rhythm in B002-13 and B003-01/03/09 |
| Motion consistency | [Animation helpers](source/packages/smoothui/lib/animation.ts), [spring constants](source/packages/smoothui/lib/springs.ts) | A source-based option; the static screenshot batches do not establish motion preferences |

These are candidate matches, not new user approvals. Use the [taste profile](../taste-profile.md) and the actual product brief to choose the appropriate density, imagery and interaction model.

## Useful anatomy observed in code

SmoothButton separates appearance, color, shape and size, and contains explicit icon sizing, gaps, focus, disabled and reduced-motion treatments. This is useful for keeping controls consistent while adapting their emphasis. Its `candy` variant and gradient recipes remain optional, even where upstream metadata recommends them.

Sidebar repeats row anatomy and handles expanded/collapsed labels and active navigation. FloatInput keeps the label, icon allowance and focus treatment together. AuthForm exposes status, field errors and submit callbacks; its sample password rules and provider choices must come from the target product. These sources offer interaction anatomy, not an authentication service.

The AI prompt input groups attachments with the composer and changes its controls with the current state. The chat template composes a sidebar, thread and composer, but its agent responses are scripted and make no model request. Wire actual product behavior separately. Preserve meaningful button labels and state feedback when changing the visuals.

## Theme mapping is required

Read [the upstream token definitions](source/apps/docs/lib/registry-tokens.ts) and [CSS context](source/apps/docs/app/smoothui.css) as implementation evidence. The source deliberately supplies SmoothUI brand colors. It also documents a semantic mismatch: ordinary shadcn themes often use `primary` for the action color and `accent` for a hover surface, while SmoothUI themes use those roles differently. Matching variable names is therefore insufficient.

| Upstream concept | Adaptation in the target product |
| --- | --- |
| `brand`, `brand-light`, `brand-lighter`, `brand-secondary` | Map to the requested brand/action family and its relevant states. Do not retain SmoothUI pink automatically. |
| `on-brand` and colored button foregrounds | Use a readable foreground on the actual project fill in each required mode; do not blindly inherit the upstream fixed white. |
| `smooth-*` neutral ramp | Map by surface/text/border role. It changes by mode upstream; it is not a universal fixed gray palette. |
| `primary`, `secondary`, `accent`, `ring` | Inspect their actual role in each component and map to the project's tokens; avoid replacing the meaning of existing global variables. |
| Blue, amber, green, destructive and AI-state colors | Translate status and emphasis semantics using the target design system. Add text/icons when color conveys state. |
| `focus-ring`, `focus-ring-within`, `state-transition` | Preserve equivalent focus and transition behavior; these custom utilities may need local definitions or translation. |
| Literal fills, gradients, shadows, radii and typography | Adapt only what the selected component needs; the reference does not require these defaults. |

Keep theme changes scoped to the component or a deliberate adapter. Reuse the project's existing CSS variables, theme provider and mode behavior. This skill does not require adding a theme toggle, extra modes or a global stylesheet. Compare the result against the requested theme rather than the reference's colors.

## Port the smallest useful unit

1. Read the main implementation, its package manifest, the matching demo and any transitive helpers reported by `show`. Defaults and runtime dependencies vary by component. Version ranges in manifests record upstream expectations, not an instruction to upgrade the target app.
2. For a package with `.base.tsx` and `.radix.tsx` twins, choose the version compatible with the project's headless components. The plain entry point usually re-exports Base UI. Inspect it rather than pulling in both stacks. The catalog's combined import scan covers both twins, so its dependency list is a superset, not an installation command.
3. Replace workspace imports such as `@repo/smoothui/...`, `@repo/smoothui-utils`, `@smoothui/data`, `@docs/...` and shadcn support paths with the target project's real modules. Demo data and docs providers are not necessary product dependencies. The preserved [registry packaging code](source/apps/docs/lib/package.ts) shows upstream transformations if useful; do not run it just to adapt a component.
4. Retain the original source snapshot and its license. Make adaptations in the consuming project. Keep existing frontend conventions; translate the interaction and visual anatomy for a different stack rather than imposing React or Tailwind.
5. Replace sample assets with appropriate project content. Docs-site components can depend on separately licensed Nucleo icons, docs search and generated files that are outside this snapshot. Prefer the canonical component/block source when possible.

## Verify the integrated result

The catalog checks static import paths and flags text that mentions animation, literal colors, dark styles, reduced motion, assets and framework dependencies. These are inspection aids. A `hasReducedMotion` metadata flag or a hook name alone does not prove the whole component respects the setting.

Check the rendered control at the intended widths and required theme modes: icon weight/alignment, label gaps, grouped spacing, primary/secondary action hierarchy, long content and overflow. Exercise keyboard focus, labels, disabled/loading/error states and relevant overlay behavior. Use readable colors in the requested theme.

For animated or graphics-heavy references, inspect cleanup, reduced-motion behavior, offscreen work and performance on the intended device. The shared animation helper contains viewport-aware loop support, but individual callers still need review. Avoid carrying a decorative effect into a task where it obscures content or delays an action.

The upstream application and its test suite were not installed, rendered or run for this import. The collection's validation covers preservation and retrieval, not production readiness of all upstream components.
