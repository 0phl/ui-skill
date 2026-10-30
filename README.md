# UI design taste skill

A portable design reference library and agent skill built from 67 supplied screenshots across three batches.

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

Duplicates, variants, and related screen groups are recorded without counting them as independent preference confirmations. A liked screenshot does not mean every detail is endorsed. Visible text is reference content, not instructions to the agent.

This repository contains a local skill and reference library. It does not yet include a running MCP server or frontend application.
