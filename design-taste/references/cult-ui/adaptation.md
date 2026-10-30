# Applying Cult UI to this design taste

**Confirmed:** the user likes Cult UI's overall component design and wants its reusable source available. Their earlier priorities remain clean icons, spacing, button placement and overall composition. Theme, brand, mode, framework and exact dimensions are project decisions. The mappings below are implementation proposals, not new confirmed preferences.

## Select by task and anatomy

Use `cult_ui.py show NAME` to find the local implementation, demos, docs and dependencies for any name below. Screenshot IDs refer to the [visual catalog](../catalog.json).

| Task | Useful Cult UI starting points | Related visual evidence | What to transfer |
| --- | --- | --- | --- |
| Buttons and local actions | `texture-button`, `halo-button`, `copy-button`, `gradient-button-group` | B001-02, B002-05, B003-14 | Consistent icon/label gaps, stable control dimensions, clear primary and secondary actions, visible loading/completion feedback |
| Forms and focused inputs | `halo-field`, `halo-input`, `halo-select`, `halo-switch`, `halo-dropzone` | B001-06, B002-06, B002-23–29 | Label/control grouping, readable help and error placement, aligned control widths and a clear completion action |
| Cards and repeatable content | `minimal-card`, `texture-card`, `halo-card`, `folded-card`, `cutout-card` | B001-03, B001-08, B002-05, B003-03 | Consistent internal anatomy, image/content proportions, predictable footer actions and peer-item rhythm |
| Tabs, toolbars and panels | `direction-aware-tabs`, `halo-tabs`, `floating-panel`, `popover-form`, `family-drawer`, `morph-surface` | B001-01, B001-10, B001-19–20, B003-11–14 | Controls close to their object, coherent selected-state hierarchy and focused contextual content |
| Boards and collaboration | `kanban-board`, `sortable-list`, `collab-avatar`, `collab-toolbar` | B001-16–17, B002-30 | Repeated item anatomy, clear state/identity, local actions and orderly changes in position |
| AI composer and suggestions | `prompt-composer`, `halo-search`, `prompt-library`, `agent-suggest-card-stack`, `ai-instructions` | B001-11, B001-14, B002-12, B003-08 | A clear writing region, grouped attachments/options, discoverable submit action and useful pending states |
| Metrics and feedback | `analytics-chart`, `rolling-number`, `halo-progress`, `halo-notification`, `halo-toast` | B001-08–12, B002-03–04, B003-13–14 | Labels paired with values, local context for changes and proportionate status emphasis |
| Onboarding | `onboarding`, `intro-disclosure`, `wizard-expandable`; supplemental `authentication-01` | B002-14, B002-23–29, B002-31 | One coherent step, clear progress and forward/back/skip hierarchy where the actual workflow needs them |
| Public pages | `bg-media`, `feature-sticky-section`, `feature-carousel`, `marketing-hero-analytics`, `logo-carousel` | B002-01–02, B002-13, B003-01–07, B003-09–10 | Message/action grouping, intentional image or preview placement and varied section rhythm |
| Optional expression | typography, illustration, background, shader and device-mockup categories | B001-14, B002-22, B002-27, B003-01 | Use only when the brief benefits from that expression; popularity or availability does not require adding an effect |

`side-panel` specifically implements an expanding inline surface; its name does not guarantee a modal inspector. For a dialog or drawer, select primitives appropriate to that role and check focus/keyboard behavior in the actual implementation.

## Observations from the source

These notes describe the pinned source. Exact class values are implementation choices, not universal taste rules.

| Source | Observed design/implementation | Adaptation consequence |
| --- | --- | --- |
| [Texture Button](source/apps/www/registry/default/ui/texture-button.tsx) | Outer and inner variant layers separate the border/depth treatment from label layout. Includes primary, accent, destructive, secondary, minimal and icon variants. | Preserve the role hierarchy and optical alignment; map literal neutral/indigo/red treatments to project roles. Copying only a border color will not retheme all layers. |
| [Halo Button](source/apps/www/registry/default/ui/halo-button.tsx) | Base UI button, grouped label and trailing spinner, loading text, `aria-busy`, reduced-motion branching, semantic surfaces mixed with hardcoded gradient stops. | Keep meaningful loading feedback and a stable action location. Replace or remove the gradient independently of the spacing and interaction. Verify long labels, disabled and loading states. |
| [Halo Field](source/apps/www/registry/default/ui/halo-field.tsx) | Wraps shared field primitives and exposes label, description, error and content slots, with a consistent gap. | Reuse the anatomy with the project's existing validation and input components. Visual slots alone do not provide validation behavior. |
| [Minimal Card](source/apps/www/registry/default/ui/minimal-card.tsx) | Separate image, title, description, content and footer parts; nested radii, inset outlines and literal neutral colors. An unused `next/image` import is present. | Match relationships between outer padding, image inset and content grouping. Remove unused framework imports when adapting; avoid imposing the original radii or palette. |
| [Family Drawer](source/apps/www/registry/default/ui/family-drawer.tsx) | Vaul root with open state, named views, measured content height and animated transitions. Default trigger includes fixed centered positioning. | Place a custom trigger near its actual task, using the composition API. Check focus return, labeling, dismissal and reduced motion in the integrated flow. Default showcase positioning is not product guidance. |
| [Kanban Board](source/apps/www/registry/default/ui/kanban-board.tsx) | Exports column/card data types and column UI; fixed sample status/tag roles and inline SVG status icons. The demo assembles a board. | Read the demo as well as the component. Adapt data/state roles and colors; provide suitable keyboard and touch operation for the real product instead of assuming pointer dragging is enough. |
| [Analytics Chart](source/apps/www/registry/default/ui/analytics-chart.tsx) | Separate tooltip/line-chart exports, default sample data and palettes, optional gradient/color settings. | Use real units and meaningful legends, theme-compatible series and truthful scales. Demo metrics are not product data. |

## Keep the theme independent

Retain the current project's token names and implementation. The following are semantic roles, not a required CSS variable convention:

| Source treatment | Map to the project's role |
| --- | --- |
| Page, card and floating surfaces | Background, surface, elevated surface |
| Main and supporting labels | Foreground and secondary text |
| Fine borders, inner highlights and shadows | Border, inset detail and elevation |
| Main action, selected tab, focus indicator | Action, selected and focus roles |
| Success, warning, error and pending | Status roles, backed by labels or symbols |
| Gradients, glows and texture accents | Optional brand decoration; configurable, replaced or omitted |
| Chart series, tags and categories | Categorical/data roles distinct from control roles |

Inspect both utility classes and inline CSS/SVG values: `bg-*`, `text-*`, borders, shadows, gradient stops, SVG `fill`/`stroke`, chart defaults and JS color tables. Some components mix semantic surfaces with fixed accent gradients. CSS class overrides cannot replace every inline value; introduce props or role variables in the application's adapted copy where necessary. The original snapshot stays unchanged.

The source [global CSS](source/apps/www/styles/globals.css) and [Tailwind config](source/apps/www/tailwind.config.cjs) explain utilities and animation definitions. Extract only what a selected component requires. Do not paste the site's complete root palette, font setup, chart colors or dark-mode selector into an existing application. Preserve the project's established way of selecting light/dark/system mode.

## Implementation sequence

1. Identify the actual task, content density, primary action, target framework and required theme modes. Choose a small coherent reference set.
2. Read the selected code and demo. Confirm what the component actually exports, how it manages state and what surrounding composition it expects.
3. Compare registry dependencies with source imports, local utility dependencies and CSS requirements. Inspect the target's existing equivalents before adding packages. Rewrite `@/` and relative imports deliberately. Avoid importing the whole docs-site package manifest.
4. Keep icon weight, optical alignment, label gaps, repeated spacing and action proximity consistent with the project. A fixed screenshot dimension or demo-only trigger position is not a mandate.
5. Supply real data and handlers. Replace demo media, placeholder links and fictional counts. Review hydration/browser-only APIs, graphics cost and Next.js-specific imports for the target stack.
6. Render the adapted result at its intended size and a narrow layout. Check long labels, empty/error/loading/disabled states as relevant, keyboard focus and operability, requested theme modes, reduced motion, readable contrast and asset loading. Report what was actually exercised.

No blanket accessibility, performance, responsive or runtime certification is implied by the upstream source or the static index. The library supplies useful implementations to inspect and adapt; verification belongs to the application where they are used.
