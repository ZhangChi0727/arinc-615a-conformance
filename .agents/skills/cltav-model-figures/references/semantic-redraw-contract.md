# Semantic redraw contract

## Authority order

1. Accepted method, algorithm, CRS/model, and experiment contracts.
2. The matching `docs/research/publication/models/FIG-CL-TAV-*.puml` file.
3. Existing controlled graph and generated-artifact registries.
4. `configs/research/cltav_model_figure_manifest.json`, which is a
   hash-bound derived redraw inventory and never a second semantic authority.
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
roles, the bound PlantUML SHA-256, and the Draw.io source SHA-256. After an
intentional manual layout edit, review the rendered result and deliberately
refresh `drawioSha256`; unexplained hash drift is a failed integrity check.

## Redraw lifecycle

Use `DRAFT-REDRAW` until all gates below pass:

1. source hash current;
2. semantic manifest complete;
3. Draw.io XML well formed and editable;
4. semantic equality checker passes;
5. SVG/PDF export succeeds or is explicitly `NEEDS-RENDER`;
6. preview inspected at final size;
7. manuscript insertion inspected;
8. human reviewer accepts the meaning and visual hierarchy.

Only then may the reader SVG be replaced and downstream hashes/manifests be
updated. Never overwrite a user-edited `.drawio` source during regeneration
unless the user explicitly requests a full redraw.
