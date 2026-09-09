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
- `rhoRA` is a closed candidate binding (`relation`, `sourceCoverageId`,
  `status`) and may not carry proprietary transcription fields;
- every registered source PDF page is either inside a controlled section span
  or an explicit exclusion range;
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
- public M1 records contain only a logical-statement hash and non-reconstructive
  generated bilingual semantic projections, never proprietary source text;
- unknown and unbounded timing endpoints are distinct controlled states;
- compound statements are split with stable atomic-part identity or carry an
  inseparability rationale.
- `generatedSemanticProjectionEn/Zh` are deterministic renderings of the
  structured semantic tuple. They are drift anchors, not approved paraphrases
  and not independent RG1 evidence;
- M1 does not store the redundant `roles`, `operations`, `category`, or
  `obligations` fields. Review views derive role, operation and action directly
  from `semantic`; compound source propositions are split into atomic CRS items;
- symbolic and message-carried timing propositions reference at least one
  independently owned source unit. A self-reference is sufficient only for an
  exact fixed constant whose lower and upper values are equal;
- requirement-level 615A-to-665 edges remain deferred under the controlled
  `bounded665EdgePolicy` until attachment-anchored reconciliation in M2.
  M2 records those candidate edges in the model package; it does not copy or
  replace the M1 requirement list. See `MODEL_SCHEMA.md`.

---

## Bounded network reference review

`networkReferenceReview` distinguishes edition-bound inspection regions from atomic
CRS coverage. Region hashes and owner/target relations support review; they do not
prove complete standard coverage. The manifest inventories regions, relations,
issues, scope decision and infrastructure premises; semantic assertions protect
the candidate snapshot against drift. These are not independent approval records.

Source bindings reconcile full identity with acquisition records. Public source
receipts reconcile with the source register. Acquired sources retain unresolved
dependency and capability obligations. `networkMode` records the selected scope;
Compliant mode excludes P3-specific deviations, not the applicable IETF obligations.
`infrastructureAssumptions` retain those underlying-service prerequisites as
NOT-ESTABLISHED until their substantiation is planned and reviewed before execution
Configuration approval. They do not claim complete RFC coverage or implementation
compliance. Resolved scope choices, acquired-but-unreviewed sources and open
edition/deployment issues remain distinct. Independent RG0/RG1 must review the
historical edition choice, source fidelity and the protocol/infrastructure boundary.

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

ID 唯一且不得重用；来源和版本强制；公开产物仅保存 hash 或批准释义；每个已批准适用条目至少含一个义务；解释或适用性变化必须形成新评审版本；复合规范语句原则上拆分。含 `timing` 义务的项目必须有完整时序对象，空上下界表示该界不存在而不是未知；触发、响应、取消、替代、关联/配对、并发、静默、端点包含性、单位、时钟启动/复位和误差预算引用均是经评审语义，不能由测试代码推断。歧义配对属于测量配置无效并产生 `ERROR`，不得记作 IUT `FAIL`。`rhoRA` 必须是封闭的候选绑定，不得携带专有转录字段。登记来源的每一 PDF 页必须落入受控 section span 或明确排除区间。

## M1 增补

M1 的机器契约与唯一数据权威分别为 `configs/requirements/m1_crs_package.schema.json` 和 `configs/requirements/arinc_615a3_m1_crs.json`。来源定位必须结构化；原始模态与符合性效果分离；`SHOULD` 保留来源规定的最低兼容性效果；`MAY` 能力与其实现后的条件义务拆分。公开记录只保存逻辑语句 hash 与不可逆的中英文生成语义投影。未知界限与真正无界必须分开；复合语句必须拆分或登记不可分理由。

`generatedSemanticProjectionEn/Zh` 是结构化语义元组的确定性生成投影，仅用于漂移锚定，不是批准释义，也不是独立 RG1 证据。M1 不再存储与 `semantic` 完全重复的 `roles`、`operations`、`category` 或 `obligations`；评审视图直接从语义元组导出角色、操作和行为。符号时序及消息携带时序必须引用至少一个独立拥有的来源单元；只有上下界相等的精确固定常量可以仅自引用。需求级 615A→665 边按照 `bounded665EdgePolicy` 延期到 M2 的 attachment 锚定协调。M2 在模型数据包中记录那些候选边，不复制或替换 M1 需求清单。参见 `MODEL_SCHEMA.md`。

## 有边界网络引用评审

`networkReferenceReview` 区分绑定版次的检查区域与原子 CRS 覆盖。
区域 hash 与所有者／目标关系支持评审，不证明完整标准覆盖。
manifest 登记区域、关系、问题、范围决策与基础设施前提；语义断言防止候选快照漂移，
但不是独立批准记录。

来源绑定的完整身份与接收记录对账；公共来源接收身份与来源登记册对账。
已取得来源仍保留未解决的依赖与能力义务。`networkMode` 记录所选范围；
Compliant 模式排除 P3 特有偏差，不排除适用的 IETF 义务。
`infrastructureAssumptions` 将这些底层服务前提保持为 NOT-ESTABLISHED，
须在执行 Configuration 批准前规划其验证并评审，不声称完整 RFC 覆盖或实现符合性。
已解决的范围选择、已取得但待审的来源和开放的版次／部署问题分别记录。
独立 RG0/RG1 须复核历史版次选择、来源忠实度及协议／基础设施边界。
