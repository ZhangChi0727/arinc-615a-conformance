# CRS Schema

Each controlled Conformance Requirement Set item uses the following conceptual
schema. For M1, `configs/requirements/m1_crs_package.schema.json` is the
machine-readable contract and `configs/requirements/arinc_615a3_m1_crs.json`
is the sole package authority.

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
    "supersedingTrigger": "",
    "correlationKey": "",
    "pairingPolicy": "unique_key|fifo|most_recent|declared",
    "concurrencyPolicy": "replace|concurrent|declared",
    "silenceSemantics": "",
    "lowerBound": null,
    "upperBound": null,
    "unit": "s|ms|us|ns",
    "clockStart": "",
    "clockResets": [],
    "lowerBoundary": "closed|open|unbounded",
    "upperBoundary": "closed|open|unbounded",
    "errorBudgetRef": {
      "id": "",
      "version": "",
      "environmentId": ""
    },
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
- trigger, response, cancellation, supersession, correlation/pairing,
  concurrency, silence, endpoint inclusivity, units, clock start/reset, and the
  applicable error-budget reference are reviewed semantic fields, not inferred
  from test code;
- an ambiguous trigger/response/cancellation match is invalid measurement
  configuration and produces `ERROR`, not an IUT `FAIL`.

## M1 additions

- every locator is structured as source, clause, table/figure, document page,
  PDF page, fragment kind and ordinal;
- source modality and conformance effect are separate controlled fields;
- `SHOULD` retains the source convention's minimum-compatibility effect;
- `MAY` capability and its implemented-case constraints are separate items;
- public records contain only a logical-statement hash and non-reconstructive
  bilingual paraphrases, never proprietary source text;
- unknown and unbounded timing endpoints are distinct controlled states;
- compound statements are split with stable atomic-part identity or carry an
  inseparability rationale.

---

# 中文版

每个 CRS 项包含稳定 ID、标准版本和来源、文本 hash、批准释义、模态、适用表达式、类别、解释、义务、状态和评审记录。含 `timing` 义务的条目还必须完整定义触发、响应、取消、替代触发、关联键、配对/并发策略、静默语义、上下界及端点包含性、单位、计时开始、复位、适用误差预算引用和来源引用。`null` 表示该界不存在，不能表示“未知”。这些字段必须经需求/方法评审，不得由测试代码反推。

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
    "supersedingTrigger": "",
    "correlationKey": "",
    "pairingPolicy": "unique_key|fifo|most_recent|declared",
    "concurrencyPolicy": "replace|concurrent|declared",
    "silenceSemantics": "",
    "lowerBound": null,
    "upperBound": null,
    "unit": "s|ms|us|ns",
    "clockStart": "",
    "clockResets": [],
    "lowerBoundary": "closed|open|unbounded",
    "upperBoundary": "closed|open|unbounded",
    "errorBudgetRef": {
      "id": "",
      "version": "",
      "environmentId": ""
    },
    "sourceReference": ""
  },
  "status": "draft|adjudicated|approved|retired",
  "reviewRecord": ""
}
```

## 不变量

ID 唯一且不得重用；来源和版本强制；公开产物仅保存 hash 或批准释义；每个已批准适用条目至少含一个义务；解释或适用性变化必须形成新评审版本；复合规范语句原则上拆分。含 `timing` 义务的项目必须有完整时序对象，空上下界表示该界不存在而不是未知；触发、响应、取消、替代、关联/配对、并发、静默、端点包含性、单位、时钟启动/复位和误差预算引用均是经评审语义，不能由测试代码推断。歧义配对属于测量配置无效并产生 `ERROR`，不得记作 IUT `FAIL`。

## M1 增补

M1 的机器契约与唯一数据权威分别为 `configs/requirements/m1_crs_package.schema.json` 和 `configs/requirements/arinc_615a3_m1_crs.json`。来源定位必须结构化；原始模态与符合性效果分离；`SHOULD` 保留来源规定的最低兼容性效果；`MAY` 能力与其实现后的条件义务拆分。公开记录只保存逻辑语句 hash 与不可逆中英文释义。未知界限与真正无界必须分开；复合语句必须拆分或登记不可分理由。
