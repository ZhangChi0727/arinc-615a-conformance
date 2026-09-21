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
| `models/` | SysML 1.6 notation-based PlantUML sources (FIG-CL-TAV-01..09) |

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

Working titles are CL-TAV: Closed-Loop Test–Analysis Verification for
ARINC 615A Data Loading under Timing Uncertainty, and
《CL-TAV：时序不确定条件下面向 ARINC 615A 数据加载的闭环测试—分析协同验证》.
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

## Tentative venue (verified 2026-09-20; not institutional selection)

This is a **writing target**, not an acceptance, not a CAS-quartile confirmation,
and not a reason to change protocol facts or add experiment promises.

### IEEE Transactions on Aerospace and Electronic Systems (TAES) — primary target

Accessed 2026-09-20:

- Author information: https://ieee-aess.org/publications/transactions-aes/author-information
- Technical areas: https://ieee-aess.org/publications/transactions-aes/technical-areas-editors/descriptions

Official scope (author-information page): organization, design, development,
integration and operation of complex systems for space, air, ocean or ground
environments, including avionics. Regular Papers are a well-rounded treatment
of a problem area; Correspondence is a concise one-or-two-point item. Survey
papers go to the Magazine tutorials track, not this manuscript type.

Closest listed technical areas for this manuscript: **Aerospace Information
Systems** (verification/validation, requirements, model-based development) and
**Avionics Systems** (aircraft electronics, airborne networking, certification
framework evolution). The Editor-in-Chief may reassign the area.

Format constraints that affect this draft (re-check before submission):

- Regular Paper type in https://ieee.atyponrex.com/journal/taes
- Two-column/single-spaced 10 pt estimate for over-length charges; IEEE LaTeX
  template via the IEEE Author Center
- Over-length: USD 200 per printed page beyond 10 for Regular Papers (author
  information page, 2026-09-20)
- Avoid “new”/“novel” in title and abstract (AESS recommendation)
- Originality, single-anonymous review, minimum two reviewers
- IEEE Author Center governs AI-use disclosure; this increment does not
  register authors or submit

### Aerospace Science and Technology (AST) — alternate

Accessed 2026-09-20 from the official Elsevier guide:

- Aims and scope / guide: https://www.sciencedirect.com/journal/aerospace-science-and-technology/publish/guide-for-authors
- Journal home: https://www.sciencedirect.com/journal/aerospace-science-and-technology

Official aims: fundamental and applied aerospace research whose potential
applications relate to aircraft, helicopters, missiles, launchers and
satellites, their environment, and systems they support or target. Closest
listed topics: complex system engineering, information processing,
instrumentation and test facilities. Avionics data-loading verification is an
application of those topics, not a named AST keyword.

Constraints that affect this draft (re-check before submission):

- Elsevier Guide for Authors; supplementary files allowed and appear as
  received
- Generative AI used in manuscript preparation must be declared; AI artwork
  for graphical abstracts is not permitted
- Open-access APC is journal-specific and is **not paid in this PR**;
  subscription publication remains an option
- Do not treat third-party mirrors as the official guide

### Institutional CAS ranking

SJTU-authorized CAS large/small-category lookup is
`PENDING-INSTITUTIONAL-RANKING-CHECK`. JCR Q1 is not a CAS substitute. The
user must supply the authorized screenshot before any “selected journal”
wording. This pending check does not block 645 binding or algorithm/experiment
specification.

### Nearby papers (bounded; not a new literature review)

Compare on feedback, fault domain, uncertainty, cost and stopping. Do not claim
that cited methods have no loop.

| Paper | Contribution | Carrier | Evidence depth | Body use |
|---|---|---|---|---|
| Tretmans 1996 [4] | ioco / LTS test generation | labelled transition systems | formal relation, not timed avionics IUT | related work: conformance without closed-loop next-action under resource |
| Petrenko, Nguena Timo, Ramesh 2016 [7] | constraint-solving mutant killing | FSM | algorithm + ICTSS study | related work: generation, not residual-ambiguity feedback |
| Li, Pierce, Zdancewic 2021 [10] | model-based testing of networked apps | ISSTA networked systems | implementation + tests | related work: network MBT, not 615A integrity/timing loop |
| Jia and Harman 2011 [8] | mutation-testing survey | software testing | survey | related work: mutation evidence, not CL-TAV stops |
| Yang et al. 2025 [9] | requirements-based test generation survey | TOSEM | survey | related work: requirements tests, not analysis feedback into selection |

Hard IEEE/Elsevier format rules are not this repository’s eight-chapter
outline. Chapter 6 stays empty until registered confirmatory runs exist.

### Local render commands (2026-09-20)

```text
xelatex -interaction=nonstopmode -halt-on-error ALG-CLTAV-01-wrapper.tex
java -jar plantuml-1.2026.8.jar -tsvg -o artifacts/publications/cltav/figures ^
  docs/research/publication/models/FIG-CL-TAV-09-experiment-architecture.puml
```

PlantUML 1.2026.8 SHA-256
`5e1ecfa8ecd32c90b03bbf3b1eb6f020943f98ab0fcf4032be31a0002ee2c462`.
This environment’s `java` stub crashed (`0xC0000409`). Reader SVGs for
FIG-CL-TAV-01/05/09 are equivalent node/edge exports: XML-valid, PlantUML
source in a CDATA `desc`, visible `line` edges for control flow and the
forbidden-truth dashed edge. They are not a second architecture authority.
A later JRE re-render may replace the export; it is not a deferred delivery
gate for this increment. Typeset ALG-CLTAV-01 is copied to
`artifacts/publications/cltav/ALG-CLTAV-01.pdf`. Chinese mapping uses stable
step labels S0–S10, not volatile typeset line numbers.

---

# 中文版

本工作区属于方法论研究领域，但具有独立写作和发布生命周期。论文是受控方法、实验、证据和主张决定的下游产物，不是第二套方法论基线。

## 工作区结构

| 目录 | 用途 |
|---|---|
| `drafts/` | 论文段落 |
| `notes/` | 文献批注与探索性笔记 |
| `figures/` | 可复现生成的出版图表 |
| `models/` | SysML 1.6 记法 PlantUML 源（FIG-CL-TAV-01..09） |

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

工作题目为 CL-TAV: Closed-Loop Test–Analysis Verification for
ARINC 615A Data Loading under Timing Uncertainty，以及
《CL-TAV：时序不确定条件下面向 ARINC 615A 数据加载的闭环测试—分析协同验证》。
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

## 暂定投稿目标（2026-09-20 核验；不是学校正式选刊）

这是**写作靶标**，不是录用、不是中科院分区确认，也不得反过来修改协议事实或加实验承诺。

### IEEE Transactions on Aerospace and Electronic Systems（TAES）——第一靶标

IEEE TAES Regular Paper 为第一靶标。官方作者信息与技术领域页于 2026-09-20 访问。范围包括航空电子等复杂系统；Regular Paper 是对问题域的完整处理。最接近的技术领域为 Aerospace Information Systems 与 Avionics Systems。超出 10 印刷页的 Regular Paper 按作者页所述每页 200 美元计超长页费。避免在题目／摘要使用 “new”／“novel”。IEEE Author Center 管辖 AI 使用声明；本增量不登记作者、不投稿。

### Aerospace Science and Technology（AST）——另一候选

AST 为另一候选。官方 Guide for Authors 于 2026-09-20 访问。范围是与飞行器及其环境／系统相关的航空航天研究；最接近主题为复杂系统工程、信息处理、仪器与试验设施。补充材料按收到原样发布。稿件准备中的生成式 AI 须声明。开放获取 APC **不在本 PR 支付**。

### 学校中科院分区

学校中科院分区保持 `PENDING-INSTITUTIONAL-RANKING-CHECK`。JCR Q1 不能代替中科院分区。须由用户提供授权查询截图后才能写“已选刊”。该未决项不阻塞 645 绑定与算法／实验规格。

### 附近论文（有界，不是新综述）

附近论文（有界，不是新综述）：Tretmans 1996、Petrenko 等 2016、Li/Pierce/Zdancewic 2021、Jia/Harman 2011、Yang 等 2025。按反馈、故障域、不确定性、成本、停止比较，不声称已有方法都没有闭环。期刊硬性格式不是本仓库自定的八章结构。第 6 章在确认性运行登记前保持空。

### 本地渲染命令（2026-09-20）

```text
xelatex -interaction=nonstopmode -halt-on-error ALG-CLTAV-01-wrapper.tex
java -jar plantuml-1.2026.8.jar -tsvg -o artifacts/publications/cltav/figures ^
  docs/research/publication/models/FIG-CL-TAV-09-experiment-architecture.puml
```

PlantUML 1.2026.8 SHA-256 为 `5e1ecfa8ecd32c90b03bbf3b1eb6f020943f98ab0fcf4032be31a0002ee2c462`。
本环境 `java` 崩溃（`0xC0000409`）。FIG-CL-TAV-01／05／09 的读者 SVG 为等价节点／边导出：XML 有效、PlantUML 源放在 CDATA `desc`、控制流与禁止真值虚线均为可见 `line`。它们不是第二套架构权威。后继可用 JRE 重渲染可以替换该导出，但不是本增量的延期交付门。排版 ALG-CLTAV-01 已复制到 `artifacts/publications/cltav/ALG-CLTAV-01.pdf`。中文对应使用稳定步骤标签 S0–S10，不引用易变排版行号。
