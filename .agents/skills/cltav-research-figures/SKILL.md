---
name: cltav-research-figures
description: Create or revise reproducible data-derived figures for CL-TAV experiments and the IEEE TAES manuscript; not for controlled PlantUML architecture views.
---

# CL-TAV Research Figures

Use this skill for quantitative plots, statistical graphics, and data-derived
tables. Route controlled FIG-CL-TAV model, architecture, activity, sequence,
state-machine, parametric, and experiment-architecture views to
`cltav-model-figures`. Their PlantUML sources remain the semantic authority;
the Draw.io files produced by that skill are editable publication views.

Read `docs/research/RESEARCH_ENVIRONMENT.md`, the applicable experiment
registration, and
`configs/research/quantitative_figure_manifest.json`. Verify that input data are
registered and that their visibility does not leak evaluator truth into an
algorithm-facing artifact.

Develop interactively if useful, but place the authoritative transformation in
a script. Record inputs, generator, parameters, seed, outputs, hashes, and
review state in the manifest. Never insert illustrative values into a result
figure without visibly marking the artifact as synthetic or schematic.

Prefer PDF/SVG for TAES figures. Produce raster output only when needed. Inspect
the rendered result for clipping, unreadable labels, ambiguous encodings,
grayscale failure, and single-/double-column legibility. A valid file or passing
script is not human approval of its engineering meaning.

Read [references/figure-contract.md](references/figure-contract.md) when adding a
manifest entry or deciding output formats.
