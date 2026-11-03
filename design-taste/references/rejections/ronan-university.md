# R001 — rejected Ronan University landing page

Created 2026-10-30; rejected 2026-11-03. **Outcome: does not meet the user's design standards. Do not reproduce this design or close variants.**

This is implementation feedback backed by the conversation and local source inspection. No screenshot is archived with this record. It adds one negative outcome, not another image or a positive reference. See C09 in [the taste profile](../taste-profile.md) and `implementation_feedback` in [the catalog](../catalog.json).

## Confirmed feedback

The user initially wrote:

> this output is not align and not passed on my standards on my design preference

They clarified the scope:

> everything, typohraphy, the used font, boxy sharp edges, etc.. all. look how's the UI sample and what you did here. its so different. so what i want on my ui skill is to not create this same UI design.

The rejection covers the entire resulting design. Typography, the font treatment, and boxy sharp edges are explicitly named dislikes. Do not reduce this feedback to a minor spacing adjustment or record the result as an approved interpretation of the skill.

## What was requested

A fictional Ronan University landing page using this skill, with black, white, and maroon branding and images generated with Codex Image Gen. The user requested a fast mockup and no tests. The brief did not request a traditional academic crest, historic-campus aesthetic, serif/italic headline system, or sharp rectangular controls.

## Identify the rejected composition

The following are facts from the implementation and generation prompts. They identify this result; they are not additional verbatim complaints.

| Area | Treatment used in the rejected page |
| --- | --- |
| Masthead | Dark utility strip, solid maroon navigation, an outlined crest-like R mark, serif university wordmark, and a rectangular Apply now action. |
| Hero | Large edge-to-edge historic-campus photograph with dark overlays, left-aligned oversized thin serif copy, an italic final line, small uppercase metadata, and paired actions. |
| Typography | Libre Caslon Display/Georgia for headings and the wordmark, DM Sans/Arial for body and controls. The headline says “A world of possibility. A future that’s yours.” Repeated thin serif and italic phrases continue through the page. |
| Geometry and actions | Mostly hard rectangular buttons and program cards, thin dividers, underlined text actions, and small arrows. Round arrow badges do not change the dominant boxy treatment. |
| Page structure | Hero → numbered quick links → split introduction → statistics → three program cards → campus photo/accordion split → large maroon admissions band → dark footer. |
| Decorative treatment | Numbered sections, small widely spaced uppercase labels, a floating image caption panel, star marks, and a large faint background R. |
| Imagery | Generated limestone collegiate-gothic campus with clock tower and a second photograph of students on library steps. These reinforce the formal university prospectus direction chosen by the agent. |

Selected CSS facts: primary maroon `#530f25`; headline size `clamp(68px, 6.7vw, 105px)`; base section padding 96 px top/94 px bottom; hero height `clamp(600px, 48vw, 740px)`; default button min-height 50 px and padding 14 × 24 px. These values describe the rejected implementation; they are not thresholds for a universal ban.

## What went wrong in applying the skill

The local README cites B002-02 (institutional editorial) and B003-06 (architectural editorial). The agent also drew on broader editorial/serif guidance. Those references were treated as permission for a new formal brochure style without preserving a sufficiently similar overall UI.

The skill did not require this output. Its positive examples allow several type and geometry choices, and its confirmed priorities concern the overall result as well as icons, spacing, and buttons. Choosing an education-related reference and repeating broad words such as “editorial,” “airy,” or “photography-led” did not establish a visual match. The reported failure is design alignment, not the earlier localhost preview problem.

This is analysis of the implementation. The exact contribution of each design decision to the user's overall rejection is not independently measured; the explicit typography and sharp-edge feedback is confirmed.

## Guidance for future agents

- Treat this result as a negative example for this user's design taste. Do not reuse its composition, type system, or boxy component treatment as a template.
- Avoid close variants that only replace the university name, content, images, or palette. A few rounded corners or a font swap alone do not address rejection of the whole result.
- For comparable landing pages, select a coherent liked reference based on actual type weight/scale, control geometry, navigation anatomy, grouping, and composition. Prefer the softened controls and contemporary hierarchy evident in the selected positive example over Ronan's treatment.
- Do not infer thin serif headlines, italic promotional lines, or a crest-like identity from the word “university.” The brief supplies the subject; it does not supply a traditional academic visual preference.
- Make typography and corner treatment deliberate choices grounded in the selected reference. Do not default to Libre Caslon Display and hard rectangular program cards/buttons for this user's public pages.
- Check the proposed overall composition against both the chosen positive example and this rejection. Respect the user's requested speed and verification scope; this feedback does not impose a test suite, a mandatory approval round, or a redesign of an unrelated task.
- Keep required brand colors and functionality. Black/white/maroon and Codex-generated imagery were requested constraints, not confirmed standalone dislikes.
- Preserve the positive library, including approved Seaversity Rental (B004-01). Its use of DM Sans means this feedback does not establish an isolated, universal ban on DM Sans. No favorite replacement font, exact radius, or universal dashboard layout was specified.

## Source provenance

The inspected files are from the Ronan University sample workspace. They are not bundled here, and this record has no dependency on a running localhost page. SHA-256 identifies the inspected versions:

| File | SHA-256 |
| --- | --- |
| `index.html` | `95194b3a2e975f95f2f3684f3846d61e33de6509bb97e4e7933634a2b1c26a6a` |
| `styles.css` | `8975f4edff8f2d832230e51789bd69850ea2d56c4c8ef357393310797f830bfe` |
| `app.js` | `48c668017960df479cab2bed077ec0bd0194e8eaea92adcee48aeb7d2f7eba86` |
| `assets/campus-hero.png` | `7243028bab05ab6753cd000c5b66847d2e8573162ebdc175d825369d3e13f730` |
| `assets/campus-life.png` | `597cd0455ec8f16a1dac6fcc18d4adc29cb02d0e66ff64f306d3b56dd925330a` |

The page was not restarted or redesigned to collect this feedback. This record does not imply that a new rendered comparison or behavioral test was performed.
