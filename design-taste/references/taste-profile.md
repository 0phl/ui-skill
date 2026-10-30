# Personal design taste profile

Updated: 2026-10-30. Evidence: [Batch 001](batches/001.md), 21 files; [Batch 002](batches/002.md), 31 files; and [Batch 003](batches/003.md), 15 files: **67 submitted files total**. B001-15/B001-18 show one design at different resolutions; B002-07 is an exact-file repeat of B001-08. Paired themes, navigation variants, and related screen/component groups are tracked separately from independent examples. This profile remains open to correction and expansion.

## Confirmed by the user

| ID | Preference or instruction | Scope and evidence |
| --- | --- | --- |
| C01 | The user likes the first batch of designs. | Overall approval of B001; the later clarification identifies shared qualities, not approval of every detail in every image. |
| C02 | Prioritize **the overall look and feel**. | Initial explicit answer, refined by C04 to include the qualities that contribute to that impression. |
| C03 | Build a durable, growing design knowledge base for use by coding agents. | Conversation goal: preserve references and design taste for Claude Code, Codex, or another agent. |
| C04 | The most valued qualities are **clean icons, spacing, button placement, and overall appearance**. | Explicit follow-up about what the user likes most in the reference batch. These are confirmed priorities; exact implementation recipes remain proposals. |
| C05 | **Keep the skill flexible across themes, client brands, and design systems. Theme colors must follow the current user's requirements.** | Explicit follow-up. Applies to this skill and its use by any user; reference palettes must not become restrictions or defaults that override a project's theme. |
| C06 | Cult UI's component design matches the user's taste; include its publicly reusable source as code references. | Explicit request linking [Cult UI](https://www.cult-ui.com/) and its [public repository](https://github.com/nolly-studio/cult-ui). This approves the overall design direction, not every component, effect or source default. See the [pinned code collection](cult-ui/README.md). C05 continues to govern theme choices. |
| C07 | SmoothUI also matches the user's taste; include its public code with the same treatment as Cult UI. | Explicit request linking [SmoothUI](https://smoothui.dev/) and its [public repository](https://github.com/educlopez/smoothui). See the [pinned code collection](smooth-ui/README.md). Overall approval does not confirm every animation, component or default; C04 and C05 continue to govern implementation. |

There are no confirmed favorite fonts, exact colors, spacing values, icon packages, fixed button positions, or preferred light/dark mode. Theme flexibility itself is confirmed. No explicit visual dislikes have been supplied. Cult UI and SmoothUI add inspectable implementation examples for composition, controls and motion; neither source collection has been rendered or tested here as a complete application. They do not establish a mandatory React, Next.js, Tailwind, animation or icon stack. SmoothUI's own brand tokens, primitive variants and motion metadata are source observations, not additional preferences.

## Theme independence

The current user/client requirements determine palette and theme behavior. Reuse the project's established design tokens and component conventions unless a change is requested. When the project follows system light/dark preferences or supports a theme choice, preserve that behavior; this skill does not require adding modes to a project that does not need them.

Extract structure and visual relationships from the references: icon consistency, grouping, gaps, alignment, action hierarchy, and page proportions. Express these through the requested theme's surface, text, border, action, selection, and status roles. A saturated client theme is fully compatible with this skill; neutral or pastel surfaces are not mandatory.

Select references for structural relevance even when their colors differ. An analytics page can use B001-10/B001-12's control placement and information hierarchy with a light orange brand theme. B001-15's member layout can use a dark theme. A system-following application can retain the same icon and spacing relationships across its supported modes. These are examples, not additional theme requirements.

B002-03/B002-04 provides direct visual evidence of one dashboard composition in dark and light treatments: panel order, icon positions, grouping and action locations remain closely matched. The pair illustrates the confirmed C05 rule; it does not establish a preferred accent color or prove a working system-theme implementation.

## Working design direction

**Confirmed emphasis:** clean icons, spacing, button placement, and overall composition, adaptable to the project's required theme.

**Still inferred:** a preference for intentional composition with precise alignment, clear typography, and considered visual hierarchy. Soft geometry, information density, and surface treatments vary by context.

The originals show several ways to distinguish the overall composition from areas of emphasis: pastel details on light surfaces, rich data colors on dark surfaces, or atmospheric gradients around an AI composer. These describe the source evidence. Use the requested palette to achieve a clear hierarchy rather than copying those colors.

The evidence now covers applications, public marketing, an outdoor commerce hero, institutional/property/food editorial pages, authentication/onboarding, provider booking, a social feed, operational overview/detail groups, a tablet service interface, and one three-screen mobile event sequence. Batches 002 and 003 expand the earlier application-heavy reading: expressive photography, playful illustration, serif display typography, long-page composition and compact admin grids can coexist with the confirmed structural priorities. No single dashboard style should govern every context. Games, motion, comprehensive phone patterns and end-to-end commerce remain weakly represented or unobserved.

## Inferred patterns

Confidence is qualitative and relative to the cited evidence. B002 and B003 continue the liked-reference intake without new item-level rankings. Related mockups, paired themes, navigation variants, composites and duplicates do not count as independent user confirmations. The icon/spacing/action qualities are confirmed; the detailed recipes inferred from them remain proposals.

| ID | Inference | Evidence | Confidence and scope | Decision it should influence |
| --- | --- | --- | --- | --- |
| I01 | Neutral foundations with concentrated emphasis recur in the source images. | B001-02, 06, 10, 12, 15, 17, 19, 21 | Strong visual observation; C05 explicitly prevents treating this as a palette preference | Transfer the hierarchy and placement of emphasis using the requested theme. Neutral surfaces are optional. |
| I02 | Clear hierarchy and consistent alignment recur across both sparse and dense screens. | B001-03, 04, 10, 15, 16, 17; B002-05, B002-12, B002-16, B002-21 | Strong cross-context evidence supporting C04 | Resolve page regions, text levels, and row rhythm before adding decorative detail. |
| I03 | Corner treatment varies substantially with context. | B001-02, 05, 06, 21; B002-02, B002-10, B002-17, B002-28; B003-02, B003-03, B003-06, B003-11 | Strong evidence of variation; no exact radii or universal softness confirmed | Use deliberate geometry compatible with the project; generous rounded cards, compact restrained panels and rectilinear editorial layouts are represented. |
| I04 | Depth tends to come from nearby surface tones, fine borders, and selective elevation in the initial application examples. | B001-02, 06, 07, 10, 12, 15, 19 | Strong within B001; not a restriction on expressive later references | Differentiate layers gently when this family fits; make overlays more elevated than ordinary rows. |
| I05 | Typography scale and display style change with the communication task. | B001-03, 10, 15; B002-01, B002-02, B002-13, B002-17, B002-22, B002-26; B003-09, B003-10 | Strong source observation; serif display and script accents are now visible, but exact font identities and preferred weights are unknown | Use compact tiers for application detail and deliberate display typography for public/editorial messages. Sans-serif, serif and contextual decorative accents are options, not required fonts. |
| I06 | Structure can transfer between light and dark treatments. | B001 contains both; B002-03/B002-04 directly pair one composition in two themes | Direct paired observation; C05 confirms freedom to use any required theme | Preserve useful arrangement and action roles while adapting surfaces, text and emphasis to the requested theme. |
| I07 | Subtle texture and tactile details may be part of the appeal. | B001-02, 07 tick dividers; 08 progress texture; 10–12 chart hatching; 06 raised icon | Moderate; repeats partly within related groups | Consider a small purposeful texture or elevated control when the chosen family supports it. |
| I08 | Dense information can still fit the taste if the frame remains orderly. | B001-10, 11, 12, 17; B002-15; related group B002-17–21 | Strong in analytical and operational contexts; related console screens grouped | Keep consistent alignment and clear hierarchy using the project's visual system; density does not dictate a palette. |
| I09 | Generous empty space is acceptable when the task has little content. | B001-14, 15; B002-12, B002-25, B002-31; exterior framing excluded | Repeated across settings, start screens and authentication | Allow sparse content and clear task columns without filling every region with extra panels. |
| I10 | Some liked AI start-screen references use ambient color. | Four quadrants of B001-14 | Limited source observation; no confirmed gradient preference | Borrow the composer focus and spacious layout. Add a gradient only when the project direction supports one. |
| I11 | Focused floating surfaces fit the visual language. | B001-01, 10, 12, 19, 20 | Strong appearance evidence; behavior unknown | Use contrast, layering, and careful grouping to focus drawers, menus, and modals. |
| I12 | A content area paired with a narrower control or detail region is a recurring composition. | B001-10, 12, 15, 16, 21; B003-05, B003-08, related B003-11–14 group | Repeated across different functional roles; no universal column count or sticky behavior | Consider split regions when the actual task calls for context beside booking, insights or controls. |
| I13 | Functional icon clarity comes from consistent anatomy and placement, not the number of icons. | B002-05, B002-12, B002-14, B002-16, B002-17, B002-28, B002-30 | Repeated evidence supporting confirmed C04; exact icon style still open | Align visual weight, icon/label gaps and containers within the product; omit icons when they add little. |
| I14 | Spacing communicates groups at several scales. | B002-05 cards; B002-16 task rows; B002-23–29 forms; B002-30 activity rows | Strong across distinct contexts; no fixed scale extracted | Keep related label/control or icon/text pairs close, separate larger groups, and maintain repeated edges and row rhythm. |
| I15 | Actions are placed according to their scope. | B002-05, B002-06, B002-10, B002-13, B002-14, B002-17, B002-20, B002-30; B003-05, B003-08, B003-11, B003-14, B003-15 | Strong evidence supporting confirmed C04; the cloud group is related | Put page, panel, input, item, form and purchase actions near their relevant context; keep filter, exception and selected-object actions distinguishable. Avoid a universal button location. |
| I16 | A focused form can be paired with expressive supporting imagery. | B002-14, B002-23–25, B002-27, B002-28, B002-31 | Repeated across several authentication presentations; direction and imagery choice remain open | Separate the task column from optional illustration, photography or product evidence; either left/right orientation is supported. |
| I17 | Public-page compositions allow expressive visual focal points. | B002-01, B002-02, B002-13, B002-22, B002-26; B003-01–04, B003-06, B003-07, B003-09, B003-10 | Repeated contextual evidence; no universal art direction | Group message and actions clearly while giving photography, artwork or a product preview a deliberate role. Playful illustration and expressive editorial type can coexist with clean functional controls. |
| I18 | Navigation width can change without changing the main content hierarchy. | B002-08/B002-09 | One paired example; interaction and breakpoints unknown | Preserve section order and action roles when adapting an expanded sidebar to a compact rail, if the product needs that mode. |
| I19 | A mobile flow can maintain visual continuity while changing each screen's task. | B002-10 discovery/detail/ticket composite | One three-screen example; limited generalization | Reuse clear icon and content grouping while tailoring actions to discovery, purchase and confirmation; do not infer stickiness or motion. |
| I20 | Long public pages vary composition while maintaining alignment and section rhythm. | B003-02, B003-04, B003-06, B003-07, B003-09, B003-10 | Several montages plus one full long page; section order is not a fixed template | Separate ideas with broader intervals, keep message/action groups tight, and vary image/text arrangements according to the content. |
| I21 | Operational overview and detail can share identity, state and control anatomy. | B003-11–14 | One coherent related source group; strong within-group appearance evidence, limited independent breadth | Maintain selected-object continuity, local actions, contextual failure explanations and clear disabled-action reasons. Derive actual behavior from product requirements. |
| I22 | Repeatable card or row anatomy can organize expressive or dense content. | B003-03 club cards; B003-08 posts; B003-15 campaign rows; earlier B002-05 lead cards | Repeated across distinct contexts; exact anatomy remains task-dependent | Keep the same content/action locations across peer items while allowing imagery, copy and state to vary. |

## Visual directions and when to use them

Family names and color descriptions label the original evidence. They do not constrain the implementation's theme or which references can be combined structurally.

| Catalog family | Reference IDs | Visual character | Relevant contexts |
| --- | --- | --- | --- |
| `soft-light-utility` | B001-01–09; B002-06, B002-07, B002-30 | Rounded cards, soft nesting, focused control groups; B002-07 repeats B001-08. | Billing, forms, calendars, reports, upload tools, status/activity lists, notifications. |
| `dark-analytical-workspace` | B001-10–13 | Charcoal layers, fine outlines, dense toolbars, bright data colors, contextual popovers, selective texture. | Analytics, data tools, inspectors, AI analysis, technical onboarding. |
| `atmospheric-ai-workspace` | B001-14 | Dark sidebar, large open canvas, a prompt/composer focal point, variable ambient glow or gradients. | AI start screens and creative workspaces. |
| `quiet-light-workspace` | B001-15–20, with 18 a duplicate; B002-05, B002-12; B003-15 | Broad surfaces, precise dividers, restrained rounding, regular navigation and local actions. | Settings, member management, CRM grids, campaign rows, empty states, boards, task operations, overlays. |
| `spatial-service-interface` | B001-21 | Pale map context, rounded panels, a blue selection/action system, a large visual area beside booking details. | Map-led and service-booking interfaces; only one example so far. |
| `modular-dashboard` | B002-03, B002-04, B002-08, B002-09, B002-11, B002-15, B002-16 | Aligned card grids, summary/detail grouping, local controls; includes paired theme and navigation variants. | Platform overviews, CRM, finance, people operations, assistance beside analytics. |
| `dense-admin-console` | B002-17–21 | Compact iconography, small radii, regular headers, aligned table rows and contextual toolbars. | Operational dashboards, logs, usage, integrations, admin tables; related source group. |
| `editorial-commerce` | B002-01 | Layered photographic hero, oversized display type, searchable header, section-specific shopping actions. | Outdoor/retail landing compositions; one example. |
| `institutional-editorial` | B002-02 | Offset text/photo grid, thin rules, headline hierarchy and editorial rows. | Education/information-heavy public sites; one composition. |
| `product-marketing` | B002-13, B002-22, B002-26; B003-01, B003-03, B003-04, B003-07, B003-09 | Message/CTA grouping with product preview, photographic bands, illustrated cards or layered artwork; includes one long page through pricing. | Public product, agency, service and club pages. |
| `split-auth-onboarding` | B002-14, B002-23–25, B002-27, B002-28, B002-31 | A focused task column beside optional brand imagery, with either side orientation and varied proportions. | Authentication, account creation, onboarding. |
| `compact-authentication` | B002-29 | Self-contained nested form with provider and credential groups. | Focused authentication without a supporting image panel; source copy is inconsistent. |
| `mobile-event-flow` | B002-10 | Image-led discovery, focused purchase detail and organized ticket artifact. | Phone event/booking sequences; one composite. |
| `property-editorial` | B003-02, B003-06 | Large architecture photos, offset columns, thin rules, broad whitespace and restrained local actions. | Property and image-led editorial sites; two distinct supplied compositions. |
| `food-editorial` | B003-10 | Serif display type, occasional script, food cutouts, people imagery and a varied editorial grid. | Food/lifestyle editorial pages; one montage, not a universal font or palette. |
| `profile-booking` | B003-05 | Identity, evaluation and appointment choices in adjacent regions, with a grouped booking action. | Provider profiles and scheduling; one desktop example. |
| `social-feed-workspace` | B003-08 | Navigation, composer/feed and secondary insights in three clear regions; local post actions. | Social/publishing workspaces; one desktop example. |
| `resource-operations` | B003-11–14 | Nested scope navigation, dense aligned tables, contextual alerts, related detail panels and consistent component anatomy. | Resource/deployment operations; one related screen/component group. |

The first and fourth families overlap but differ in softness, density, and surface treatment. The analytical and AI-home examples have substantially different density and focal hierarchy despite sharing dark source palettes. Preserve useful structural differences while adapting their colors freely to requirements.

## Practical translation of the visual taste

These are **implementation proposals**, not exact specifications extracted from the screenshots.

- Compose the page with clear region proportions and aligned edges. Evaluate icons, spacing, and action placement as part of that overall composition.
- Use the project's theme roles so that an inset, selected row, floating menu, and page background remain distinguishable. Preserve required brand colors and theme behavior.
- Choose a coherent icon family with consistent optical size, stroke/fill treatment, baseline alignment, and icon-to-label gaps. Follow the client's icon system when one exists; no package or icon color is mandated.
- Keep functional icon consistency separate from expressive brand artwork. A form can use few icons; a hero can include larger decorative marks without making them the navigation icon style.
- Use consistent padding and gaps, with spacing that communicates grouping. Adapt to the project's scale and density instead of extracting universal pixel values from screenshots.
- Place buttons near the tasks they affect: page actions with page context, form actions with the form, and item actions with their item. Make primary and secondary choices clear without imposing one fixed screen position or button color.
- Maintain a consistent radius hierarchy appropriate to the chosen family. Avoid giving every boundary the same large radius.
- Establish readable title/body/metadata tiers appropriate to the context. Dense application text and large public-site display headings need different scale. Serif headings and expressive lettering are available where the brand and content support them; source softness does not require faint functional labels.
- Use the required theme to distinguish actions, selection, status, and data. The client's palette may be neutral or vivid; retain readable contrast and a coherent hierarchy in either case.
- Treat texture as an optional detail with a clear role. A repeated tick divider, a hatched forecast, and an empty-state illustration serve different purposes.
- Match density to the task. A long table, a task board, a member settings page, and a first-run AI composer need different amounts of space.
- For authentication, keep fields, recovery/options, submission and alternative-provider choices in understandable groups. Optional supporting imagery can sit on either side; compact standalone forms also belong in the library.
- For public pages, establish a clear message/action/image sequence with proportions appropriate to the content. Source brand claims, testimonials and trust logos are not reusable verified evidence.
- On longer public pages, vary text/image arrangements with consistent alignment and section rhythm; choose sections for the brief rather than copying a universal feature/proof/pricing checklist.
- In operational list/detail views, retain object identity and state across surfaces. Place recovery actions, recommendations and reasons for disabled controls near the affected context; verify real business rules independently of reference copy.
- If combining evidence, combine compatible structural traits deliberately: for example, a precise workspace shell with a softly grouped calendar widget. Map both into the project's shared theme instead of mixing source palettes.

## Do not turn missing evidence into rules

The user explicitly requires freedom to use any theme or client palette. Purple, blue, green, black, white, charcoal, and pastel colors in the references are descriptive evidence only. There is no established preference for one font, a UI framework, a CSS library, exact animation timing, or a particular icon package.

No explicit visual dislikes have been supplied. Coherent grouping, intentional geometry, and consistent spacing are useful ways to apply the confirmed priorities. Color intensity, saturation, or a departure from the source palette must not be treated as a violation of the user's taste.

Motion, hover transitions, full focus handling, keyboard behavior and responsive transitions remain unobserved. B002-10 supplies limited phone-layout evidence; B002-25 shows one visible field-focus state; B002-08/B002-09 shows two navigation widths. None proves behavior across devices or interaction states. Design and validate those for the actual product.

Browser frames, device bezels, exterior backgrounds, curation strips, and very large margins around isolated widgets belong to the supplied presentations. Photography and illustrations inside actual page sections are part of their composition. Tiny screens inside a supporting collage are not individual reference endorsements. Visible brand/curator labels are recorded as source cues without asserting current product state or original authorship.

## Open questions for future evidence

No answer is required before incorporating the next batch.

- Which directions should dominate particular projects, and are any favorite references stronger than the rest?
- Is the appeal of textures and small shadows deliberate, or is it mainly the overall softness and order?
- Which icon treatments, spacing relationships, and action layouts recur across unrelated examples? Fonts remain open; palettes continue to follow each project's requirements.
- Which mobile and marketing examples are strongest favorites, and what additional motion, responsive states or alternative directions should expand this initial coverage?
- Which examples or details does the user actively dislike?

## Evidence history

- 2026-10-30, B001: archived the original 21 files; cataloged appearance, context, limitations, and relationships; recorded C02 after the user's clarification.
- 2026-10-30, B001 clarification: added C04 and C05 for clean icons, spacing, button placement, overall appearance, and mandatory theme flexibility. Earlier color descriptions remain source observations; they do not determine future projects' palettes.
- 2026-10-30, B002: preserved 31 more original files and added image-level icon, spacing and action-placement observations. Expanded coverage to public pages, commerce, editorial layouts, authentication/onboarding and a mobile event sequence. New interpretation broadens the early application-heavy framing; C04 and C05 remain the governing confirmed priorities.
- 2026-10-30, B003: preserved 15 more originals, with no new byte-identical repeats. Added property and food editorial compositions, expressive typography, long-page pacing, provider booking, social publishing and resource/deployment detail patterns. C01–C05 are unchanged; inferred options supplement earlier directions.
- B001-15/B001-18 are one design at two resolutions. B001-02/B001-07 are related billing variations. B001-10–13 share a visual family whose original provenance is unknown. B001-14 is a four-panel composite.
- B002-07 is byte-identical to B001-08; B002-03/B002-04 are theme variants; B002-08/B002-09 are navigation variants. B002-17–21 share a console system. B002-12–14 carry the same visible product label. These relationships are recorded to avoid overstating independent evidence.
- B003-11–14 share the CloudNexus system, including repeated views and isolated components. B003-02/B003-06 are structurally related property pages with unknown original provenance. Composites and related screens do not increase independent preference weight.
