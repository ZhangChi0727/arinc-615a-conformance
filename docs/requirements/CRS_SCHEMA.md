# CRS Schema

Each controlled Conformance Requirement Set item uses the following conceptual
schema. A machine-readable JSON Schema should implement it in engineering
increment E0.

```json
{
  "id": "CRS-615A-0001",
  "standardEdition": "controlled identifier",
  "sourceReference": {
    "clause": "",
    "tableOrFigure": "",
    "page": ""
  },
  "textHash": "",
  "approvedParaphrase": "",
  "modality": "shall|shall_not|conditional_shall",
  "applicabilityExpression": "",
  "category": "",
  "interpretation": "",
  "obligations": [
    "functional",
    "state",
    "transition",
    "data",
    "timing",
    "negative",
    "sequence"
  ],
  "status": "draft|adjudicated|approved|retired",
  "reviewRecord": ""
}
```

## Invariants

- `id` is unique and never reused;
- source and edition are mandatory;
- public artifacts use a hash/approved paraphrase, not proprietary clause text;
- every approved applicable item has at least one obligation;
- interpretation and applicability changes require a new reviewed version;
- compound normative statements are split unless their semantics are
  inseparable, in which case the rationale is recorded.
