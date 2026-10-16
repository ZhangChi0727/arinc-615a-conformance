---
name: cltav-model-figures
description: Redraw, revise, export, or audit CL-TAV architecture, workflow, state, sequence, parametric, and experiment model figures for the IEEE TAES manuscript while preserving the controlled PlantUML semantics. Use for FIG-CL-TAV model diagrams; use cltav-research-figures for data-derived plots instead.
---

# CL-TAV Model Figures

Use the controlled PlantUML source and its registered model identity as the
semantic authority. Draw.io is the editable publication view, not a second
method or algorithm. A prettier figure is invalid if it adds, removes,
reverses, weakens, or relabels a scientific relationship.

## Route the task

- For an existing `FIG-CL-TAV-*` redraw or edit, read
  [semantic-redraw-contract.md](references/semantic-redraw-contract.md) and
  work from the matching PlantUML plus
  `configs/research/cltav_model_figure_manifest.json`.
- For layout, typography, colour, final-size readability, or export choices,
  read [taes-style-contract.md](references/taes-style-contract.md).
- For provenance or when updating borrowed guidance, read
  [third-party-provenance.md](references/third-party-provenance.md).
- Route quantitative plots and data-derived panels to
  `cltav-research-figures`; do not put them in this model-figure manifest.

## Required workflow

1. Identify the figure ID and read its complete PlantUML source, relevant
   registry row, manuscript use, and current rendered SVG.
2. Establish the semantic inventory before styling: entities, boundaries,
   ports/states/steps, directed relations, edge meanings, guards, notes, and
   explicit prohibitions. Do not infer missing architecture for visual balance.
3. Verify that the manifest source hash matches the PlantUML file. If it does
   not, stop the redraw and reconcile the derived manifest with the changed
   authority first. Hash text with the declared `UTF8-LF-v1` identity so LF
   and CRLF checkouts are equivalent while content changes remain visible.
4. Create or edit native, uncompressed `.drawio` XML. Keep labels as editable
   text and use stable `node-*`, `edge-*`, `group-*`, and `note-*` identifiers.
5. Run the finite mechanical consistency checks with:

   ```text
   python .agents/skills/cltav-model-figures/scripts/model_drawio.py --check
   ```

   Use `--build-missing` only for absent initial drafts. Use `--force` only
   when the requested work explicitly replaces existing Draw.io geometry; it
   must never bypass the registered checks. These checks cover declared source
   units, topology, labels, visibility, identities, and review exports; they do
   not prove full PlantUML/Draw.io semantic equivalence. Generation preflights the complete
   nine-figure batch and installs it transactionally; any failure must leave
   every prior output byte unchanged.
6. Export SVG and PDF when Draw.io CLI is available. Keep the existing reader
   SVG authoritative until the replacement passes semantic checks, final-size
   visual inspection, manuscript insertion inspection, and human review.
7. Inspect a rendered preview at IEEE single-column width and, when intended,
   double-column width. Check clipping, overlaps, edge crossings, arrow
   direction, guard placement, grayscale meaning, font embedding, and
   manuscript terminology.
8. Report status without overclaiming:
   `SEMANTIC_STATUS`, `STYLE_STATUS`, `REPRODUCIBILITY_STATUS`,
   `EXPORT_STATUS`, and `INTEGRITY_STATUS`. File validity alone is not human
   approval of the engineering meaning.

## Non-negotiable boundaries

- PlantUML remains the semantic authority unless a separately reviewed change
  explicitly changes that policy.
- Never use image generation to decide nodes, edges, guards, states, ports,
  requirements, evidence status, or algorithm behaviour. A raster concept may
  inspire spacing only after the semantic inventory is frozen.
- Do not introduce external icons unless their licence, attribution, source,
  and semantic necessity are recorded. Prefer native geometric shapes.
- Keep evaluator-only truth visibly separated from algorithm-visible inputs.
- Bind every title, object, relation, and interpretation note to finite source
  units. Object-parent and relation-endpoint bindings must agree with the
  manifest. The checker can reject omissions and direct-edge drift within this
  declared subset; independent review remains required for activity ordering,
  implicit PlantUML meaning, layout, and coordinated changes outside the subset.
- Reject absolute, drive-qualified, backslash, traversal, symlink, junction,
  reparse-point, and non-ordinary-file paths before any write.
- Preserve uncertainty, forbidden leakage, planned/not-established status,
  retry/stop polarity, and SysML-notation disclaimers.
- Do not call a view IEEE TAES-compliant or submission-ready without current
  official requirements, successful export checks, and human visual review.

## Completion packet

Return the edited `.drawio` source, generated exports if available, source and
output hashes, finite consistency-check result, final-size visual-QA result, style status,
and unresolved review items. Do not silently replace manuscript figures.
