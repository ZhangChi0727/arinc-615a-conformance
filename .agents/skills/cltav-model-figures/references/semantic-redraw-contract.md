# Controlled model-candidate contract

## Authority order

1. Accepted method, algorithm, CRS/model, and experiment contracts.
2. The matching `docs/research/publication/models/FIG-CL-TAV-*.puml` candidate input.
3. Existing controlled graph and generated-artifact registries.
4. `configs/research/cltav_model_figure_manifest.json`, a hash-bound candidate
   inventory and review-state record, not an authority or correctness proof.
5. Draw.io geometry and style.

If a lower item disagrees with a higher item, fix or withdraw the lower item.

## Equality rules

Every Draw.io redraw must preserve:

- all registered semantic entities and their exact manuscript terminology;
- directed source/target pairs, including reverse observation paths;
- relation type and polarity: flow, dependency, association, retry, stop,
  continuation, planned, forbidden, or evidence-only;
- boundary membership, port ownership, state-machine separation, ordering,
  guards, multiplicity, and declared visibility;
- notes that bound interpretation, including `NOT-ESTABLISHED`,
  evaluator-only, no-unrun-numbers, and notation-only disclaimers.

Permitted changes are geometry, whitespace, alignment, font, line routing,
non-semantic grouping, and redundant visual cues. A label may be shortened only
when the manifest retains the exact semantic label and the caption or legend
defines the abbreviation.

## Stable Draw.io identities

- semantic entity: `node-<manifest-id>`;
- relation: `edge-<manifest-id>`;
- semantic boundary: `group-<manifest-id>`;
- interpretation note: `note-<manifest-id>`.

The checker compares those identities, endpoints, semantic labels, relation
roles, actual vertex/edge flags, parents, arrow polarity, guard references,
the finite title/object/relation/note source bindings, the bound canonical
PlantUML SHA-256, the canonical Draw.io source SHA-256, and registered review
export identities. This is a finite consistency check, not a proof that the
two notations are semantically equivalent. Canonical text
identity is UTF-8 with every line ending normalized to LF; this tolerates
platform checkout conversion but not content drift. After an
intentional manual layout edit, review the rendered result and deliberately
refresh `drawioSha256`; unexplained hash drift is a failed integrity check.

Each registered candidate inventory is closed: rendered or semantic cells not declared in
the inventory are errors. Source bindings also retain object parents and
relation endpoints, and the checker extracts complete title/note units plus
directly expressed relation endpoints from the PlantUML source. These checks
reject covered omissions and drift, but cannot exclude coordinated changes to
implicit activity order or other meaning outside the extracted subset. Short visible labels require a bound source label and
an explicit note or legend that restores the interpretation.

All paths are repository-relative forward-slash paths to ordinary files.
Generation rejects traversal and link/reparse escapes, preflights the current
registered candidate set (whose size is not fixed) before writing, stages on the repository
volume, and restores every prior output if installation fails.

## Redraw lifecycle

Retain, revise, split, merge, or retire a candidate only through a versioned
revision record. Layout-only work and semantic proposals must be distinguished.
Any new meaning remains pending until a human reviews its effect on method,
algorithm, engineering, CRS, M2, experiment, and manuscript consumers.

Use `DRAFT-REDRAW` and `DRAFT-NOT-PROMOTED` until all gates below pass:

1. source hash current;
2. semantic manifest complete;
3. Draw.io XML well formed and editable;
4. finite consistency checker passes and independent semantic review remains open;
5. SVG/PDF export succeeds or is explicitly `NEEDS-RENDER`;
6. preview inspected at final size;
7. manuscript insertion inspected;
8. human reviewer accepts the meaning and visual hierarchy.

Only then may the reader SVG be replaced and downstream hashes/manifests be
updated. Never overwrite a user-edited `.drawio` source during regeneration
unless the user explicitly requests a full redraw.
