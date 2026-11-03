# Inspect the result, then fix what the evidence shows

This adapts MotionSites' screenshot-and-fix idea to the user's four priorities and multiple interface types. Prefer the project's existing browser/preview/testing tools. The archived MotionSites helper has [documented limitations](motionsites/README.md); it is not required. Do not install a browser tool solely to satisfy a fixed workflow if a working preview is already available.

## Capture relevant evidence

Inspect the intended viewport and a relevant narrower layout. Check supported theme modes when the change touches them; preserve system-following behavior when required. Do not add modes as part of verification. For an existing interface, compare before and after under the same content, viewport and state.

Open screenshots as images; creating files alone is not visual inspection. For long pages, scroll through relevant sections, allow lazy assets to load and inspect any sticky/scroll-triggered states. Early and settled frames help diagnose entry flashes or hidden text, but cannot prove smooth motion or all interactions. Test changed controls with keyboard and pointer/touch as applicable. Inspect reduced motion when adding animation.

If preview tooling is unavailable, review implementation and state exactly which visual/interaction checks remain unperformed. Do not claim a generated screenshot, a static source signal or a numerical score proves usability.

## Diagnose by the actual task

| Priority | Look for | Concrete correction |
| --- | --- | --- |
| Clean icons | Mixed optical size, inconsistent stroke/fill, uneven baselines, missing accessible names on icon-only controls | Use the project's icon family and align icon boxes with labels; name the actual control. |
| Spacing | Unclear grouping, inconsistent panel padding, drifting columns, clipped labels | Adjust the relevant spacing token or layout rule; retain density appropriate to the task. |
| Action placement | Page action lost among row actions, competing primaries, unrelated footer controls | Move/group actions with the content they affect; preserve a clear primary/secondary relationship. |
| Composition | No clear reading order, equal emphasis everywhere, disproportionate regions | Adjust region proportions, text tiers and grouping according to the selected evidence and task. |
| Project fit | Lost client colors, replaced typography, broken system-theme behavior, mismatched primitives | Restore project roles/conventions and map borrowed structure through them. |

Check implemented states for broken assets, unexpected network/runtime errors, clipped text, accidental horizontal overflow, unreadable contrast, obstructed controls and missing feedback. Interpret errors in context: a deliberately failed fixture or intentionally scrollable data region is different from a broken layout. Do not conceal layout defects by globally clipping content.

For media, inspect cropping and text legibility at multiple relevant frames. A paused video can be intentional; browser name alone does not establish codec capability. For menus and overlays, check focus entry/return, dismissal and scrolling behavior. For tables, forms and boards, inspect selected, loading, empty, invalid and failed states affected by the change. For a static content edit, limit verification to its actual impact.

## A bounded correction loop

Record **location/state → observed issue → change → recheck result**. Fix functional/readability defects first, then the visual issue with the greatest effect on the four priorities. Recheck affected states after changes. Stop once the task's acceptance criteria pass; broaden testing only for a demonstrated concern. If a missing asset/tool/service prevents a check or fix, report it plainly without claiming completion of that check.

Subjective ratings can help compare alternatives, but there is no required score, forced three-round redesign, mandatory signature effect, one-accent rule, or universal type scale. The goal is a working interface that fits this brief and the user's taste.
