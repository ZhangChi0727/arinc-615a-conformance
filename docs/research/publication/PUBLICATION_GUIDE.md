# Publication Workspace

This workspace belongs to the methodology-research domain but has an independent
writing and release lifecycle. Manuscripts are downstream of controlled method,
experiment, evidence, and claim decisions; they are not a second methodology
baseline.

## Workspace layout

| Folder | Use |
|---|---|
| `drafts/` | Manuscript sections |
| `notes/` | Annotated literature and exploratory notes |
| `figures/` | Reproducibly generated publication figures |
| `models/` | SysML 1.6 notation-based PlantUML sources (FIG-CL-TAV-01..08) |

Reader exports live in `artifacts/publications/cltav/figures/`. The single reader
entry is [`../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md`](../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md).

## Authoritative inputs

- baseline and method: [`../../control/baselines/RB-2026-001-v4.2.md`](../../control/baselines/RB-2026-001-v4.2.md) and
  [`../methodology/METHODOLOGY_CATALOG.md`](../methodology/METHODOLOGY_CATALOG.md);
- structure: [`RESEARCH_OUTLINE.md`](RESEARCH_OUTLINE.md);
- evidence wording: [`../CLAIM_EVIDENCE_MATRIX.md`](../CLAIM_EVIDENCE_MATRIX.md);
- experiments: [`../EXPERIMENT_PLAN.md`](../EXPERIMENT_PLAN.md);
- dependency contracts: [`../../control/contracts/DOMAIN_BOUNDARIES.md`](../../control/contracts/DOMAIN_BOUNDARIES.md).

## Publication traceability

Every reported result identifies the method baseline, experiment registration,
dataset/evidence manifest, analysis version, and gate decision that permits its
wording. Drafts may describe planned methods, but exploratory results remain
separate from confirmatory tables. Implementation completion or a PASS suite is
not itself a publication result or unrestricted conformance proof.

If manuscript work exposes a method defect, it opens a CR/DD; it does not edit
the controlled baseline meaning through publication prose.

## CL-TAV manuscript and evidence limits

Working titles are CL-TAV: Closed-Loop Test–Analysis Verification for Protocol
Conformance and Fault Localization—An ARINC 615A Case Study, and
《CL-TAV：面向协议符合性验证与故障定位的闭环测试—分析协同方法——以 ARINC 615A 为例》.
Each outline chapter must state the claim, research question, algorithm or
architecture, and required experiment. Combination of Test and Analysis is not
claimed as a first invention. The freeze-commit display-math check proves only
that historical objects were not rewritten; it does not prove successor CL-TAV
mathematics. Keep `independentMathematicalApproval` and
`independentReviewApproval` false.

## SysML 1.6 notation inventory

These are notation-based views, not an executable SysML metamodel.

| Construct | Used in | Not claimed |
|---|---|---|
| Block / class box | FIG-CL-TAV-03 BDD | complete SysML Block stereotype execution |
| Port / IBD connector | FIG-CL-TAV-04 | generated code or simulation |
| Activity / action | FIG-CL-TAV-05 | fUML token semantics |
| Sequence message | FIG-CL-TAV-06 | MSC conformance |
| State machine | FIG-CL-TAV-07 | composite-state protocol EFSM |
| Constraint / parametric (`class <<constraint>>` stand-in) | FIG-CL-TAV-08 | solved constraint network |
| Requirement layer package | FIG-CL-TAV-02 | one mixed CRS |

`satisfy` and `verify` are model relations. They are not executed verification.
Reader SVG exports are in `artifacts/publications/cltav/figures/` and must match
the PlantUML sources in `models/`.

---

# 中文版

本工作区属于方法论研究领域，但具有独立写作和发布生命周期。论文是受控方法、实验、证据和主张决定的下游产物，不是第二套方法论基线。

## 工作区结构

| 目录 | 用途 |
|---|---|
| `drafts/` | 论文段落 |
| `notes/` | 文献批注与探索性笔记 |
| `figures/` | 可复现生成的出版图表 |
| `models/` | SysML 1.6 记法 PlantUML 源（FIG-CL-TAV-01..08） |

读者导出在 `artifacts/publications/cltav/figures/`。单一读者入口为
[`../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md`](../../../artifacts/publications/cltav/CLTAV_RESEARCH_PLAN.md)。

## 权威输入

- 基线与方法：[`../../control/baselines/RB-2026-001-v4.2.md`](../../control/baselines/RB-2026-001-v4.2.md) 和
  [`../methodology/METHODOLOGY_CATALOG.md`](../methodology/METHODOLOGY_CATALOG.md)；
- 结构：[`RESEARCH_OUTLINE.md`](RESEARCH_OUTLINE.md)；
- 证据措辞：[`../CLAIM_EVIDENCE_MATRIX.md`](../CLAIM_EVIDENCE_MATRIX.md)；
- 实验：[`../EXPERIMENT_PLAN.md`](../EXPERIMENT_PLAN.md)；
- 依赖契约：[`../../control/contracts/DOMAIN_BOUNDARIES.md`](../../control/contracts/DOMAIN_BOUNDARIES.md)。

## 出版追踪

每项报告结果都必须标明允许该措辞的方法基线、实验注册、数据集/证据清单、分析版本和门禁决定。草稿可以描述计划方法，但探索性结果必须与验证性结果表分离。实现完成或测试套件 PASS 本身不是出版结果，也不是无限定符合性证明。

如果论文工作发现方法缺陷，应发起 CR/DD，而不是通过出版叙述修改冻结含义。

## CL-TAV 文稿与证据限度

工作题目为 CL-TAV: Closed-Loop Test–Analysis Verification for Protocol
Conformance and Fault Localization—An ARINC 615A Case Study，以及
《CL-TAV：面向协议符合性验证与故障定位的闭环测试—分析协同方法——以 ARINC 615A 为例》。
大纲每章必须写明论点、研究问题、算法或架构、所需实验。Test 与 Analysis 的组合
不被声称首次发明。冻结提交上的显示数学核验只证明历史对象未被改写，不证明后继
CL-TAV 数学正确。保持 `independentMathematicalApproval` 与
`independentReviewApproval` 为 false。

## SysML 1.6 记法清单

这些是记法视图，不是可执行 SysML 元模型。

| 构造 | 用于 | 不声称 |
|---|---|---|
| Block／class 框 | FIG-CL-TAV-03 BDD | 完整 SysML Block 版型执行 |
| 端口／IBD 连接器 | FIG-CL-TAV-04 | 生成代码或仿真 |
| 活动／动作 | FIG-CL-TAV-05 | fUML 令牌语义 |
| 序列消息 | FIG-CL-TAV-06 | MSC 符合性 |
| 状态机 | FIG-CL-TAV-07 | 复合状态协议 EFSM |
| 约束／参数（`class <<constraint>>` 记法替代） | FIG-CL-TAV-08 | 已求解约束网 |
| 需求层次包 | FIG-CL-TAV-02 | 混成一类 CRS |

`satisfy` 与 `verify` 是模型关系，不是已执行验证。读者 SVG 导出位于
`artifacts/publications/cltav/figures/`，须与 `models/` 中的 PlantUML 源对应。
