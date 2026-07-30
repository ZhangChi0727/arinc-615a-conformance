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
  "timing": {
    "trigger": "",
    "response": "",
    "cancellation": "",
    "silenceSemantics": "",
    "lowerBound": null,
    "upperBound": null,
    "unit": "s|ms|us|ns",
    "clockStart": "",
    "clockResets": [],
    "boundaryInclusivity": "closed|declared",
    "sourceReference": ""
  },
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
- an item with a `timing` obligation has a complete `timing` object; `null`
  lower/upper bounds mean absent bounds, not unknown values;
- trigger, response, cancellation/silence, inclusivity, units, clock start and
  resets are reviewed semantic fields, not inferred from test code.

---

## 中文版

每个 CRS 项包含稳定 ID、标准版本和来源、文本 hash、批准释义、模态、适用表达式、类别、解释、义务、状态和评审记录。含 `timing` 义务的条目还必须完整定义触发、响应、取消、静默语义、上下界、单位、计时开始、复位、边界包含性和来源引用。`null` 表示该界不存在，不能表示“未知”。这些字段必须经需求/方法评审，不得由测试代码反推。
