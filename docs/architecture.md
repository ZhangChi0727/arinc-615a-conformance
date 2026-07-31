# Research and Verification Architecture

| Field | Value |
|---|---|
| **Version** | 2.2 |
| **Status** | Baseline-aligned |
| **Governing method** | RB-2026-001-v4.2 |

## End-to-end control flow

```text
Standard + applicability + observation boundary
                     |
                     v
          CRS and obligation model
                     |
          +----------+----------+
          |                     |
          v                     v
 Clock-augmented EFSM    Test Purposes / VCs
          |                     |
          +----------+----------+
                     v
             Test execution path
        configuration -> stimulus -> oracle
                     |
                     v
  verdicts + timestamped traces + measurements
                     |
                     v
              Analysis path
 traceability | timed coverage | faults | uncertainty | diagnosis
                     |
                     v
          scoped assurance argument
                     |
                     v
           engineering/research decision
```

Review and Inspection gates act across the flow. They do not replace dynamic
execution or quantitative analysis.

## Domain boundaries and traceable dependencies

The repository has three deliberately distinct product domains, with governance
and controlled requirements acting as a shared contract layer:

| Domain | Authoritative inputs | Owned outputs | Required outward references |
|---|---|---|---|
| Methodology research and publication | baseline, applicability, CRS/source hashes, registered protocols | formal semantics, analyses, claim decisions, papers | baseline/report version, experiment/evidence IDs, gate records |
| Engineering implementation | frozen method contracts, controlled schemas and cases | tool releases, executable VCs, immutable evidence manifests | baseline, model/VCS, tool/config/environment versions |
| Verification tutorials | named method baseline; named tool release and examples when executable | common teaching modules and ARINC 615A walkthroughs | explained baseline, tool release if used, example/evidence IDs |

Dependencies are directional. Engineering imports method contracts but not
research prose; research consumes engineering evidence through immutable
manifests but not implementation internals; tutorials are downstream views and
never define requirements, verdict semantics, or releasable claims. Evidence
that challenges an upstream assumption enters through a CR/DD and applicable
Review gate. This controlled feedback is not a direct reverse dependency.

Every cross-domain reference must resolve to an artifact ID and version. A file
path or hyperlink improves navigation but does not replace the trace record.

## Controlled objects

| Object | Canonical form | Owner |
|---|---|---|
| Applicability | PICS-like declaration | Requirements |
| CRS | Versioned requirement items and source hashes | Requirements |
| Protocol model | Clock-augmented observable EFSM/timed IOLTS | Modeling |
| Traceability | \(\rho_{RT}\), \(\rho_{TV}\), model-target relations | Method |
| Verification case | Preconditions, stimulus, robust oracle, timing/error schema, reset, evidence schema | Test |
| Evidence | Immutable run and analysis datasets | Engineering/experiment |
| Inference model | Registered likelihood, calibration, diagnosis model | Analysis |
| Claim | Claim ID, tier, scope, evidence, gate decision | Governance |

## Gates

| Artifact progression | Static gate | Evidence gate |
|---|---|---|
| Scope enters CRS work | RG0 | G0 |
| CRS enters modeling | RG1 | — |
| Model/trace enters case derivation | RG2 | G1 preparation |
| VCs/oracles enter implementation | RG3 | G1 |
| Tool/config enters execution | RG4 | G2 |
| Evidence enters analysis/publication | RG5 | G3–G6 as applicable |
| Claim enters release | RG6 | achieved G0–G7 |

## Base and extended VCS

The base VCS is derived from the controlled applicable standard requirements.
The extended VCS is project-specific and additive. Results, configuration, and
claims for the two sets remain distinguishable. Adding extended cases cannot
repair missing base traceability or silently change the base claim.

## Version spine

Every run and derived result must identify:

\[
(\text{baseline},S,P,O,\text{CRS},G_T,V,\text{IUT},E,\text{clock},\text{tool},\text{experiment}).
\]

The tuple is implemented as manifest identifiers, not inferred from folder
names or the latest Git commit.

## Repository realization

| Architecture layer | Location |
|---|---|
| Baseline/method | `docs/BASELINE.md`, `docs/methodology/` |
| Research control | `docs/research/` |
| Requirements and traceability | `docs/requirements/`, future `configs/` schemas |
| Model/design | `docs/design/` |
| Instrument | `src/a615a_sim/` |
| Automated checks | `tests/` |
| Experiment evidence | `artifacts/experiments/` or controlled external store |
| Review/change/risk | `docs/review/`, `docs/management/` |
| Publication | `thesis/` |
| Common tutorial | `tutorial/common/` |
| ARINC 615A tutorial | `tutorial/arinc615a/` |

---

# 中文版

端到端控制流从标准、适用性和观测边界进入 CRS/义务模型，再分流至带时钟可观测 EFSM 与 TP/VC，汇合后执行测试，产生判定、带时戳迹和测量，随后分析追踪、离散/时序覆盖、故障、不确定性和诊断，最后形成范围受限保证论证。评审与检查横跨整个流程。

## 端到端控制流

```text
标准 + 能力声明 + 观测边界
              |
       适用 CRS / 义务
          /           \
 带时钟可观测 EFSM     TP / VC
          \           /
        受控测试执行
              |
 判定 + 带时戳迹 + 测量
              |
覆盖 + 故障 + 不确定性 + 诊断
              |
      有范围的保证论证
```

## 领域边界与可追踪依赖

仓库区分三个产品领域，并以治理和受控需求作为共享契约层：

| 领域 | 权威输入 | 自有输出 | 必需外部引用 |
|---|---|---|---|
| 方法论研究与出版 | 基线、适用性、CRS/来源哈希、已注册研究协议 | 形式语义、分析、主张决定、论文 | 基线/报告版本、实验/证据 ID、门禁记录 |
| 工程实现 | 冻结方法契约、受控 schema 和用例 | 工具发布、可执行 VC、不可变证据清单 | 基线、模型/VCS、工具/配置/环境版本 |
| 验证教程 | 具名方法基线；可执行时还包括具名工具发布和示例 | 通用教学模块和 ARINC 615A 实例讲解 | 所解释基线、所用工具发布、示例/证据 ID |

依赖必须保持方向性。工程导入方法契约而不是研究叙述；研究通过不可变清单消费工程证据而不是实现内部结构；教程是下游视图，不得定义需求、判定语义或可发布主张。若证据质疑上游假设，必须通过 CR/DD 和相应评审门反馈，这种受控反馈不是直接反向依赖。

每个跨领域引用必须解析到产物 ID 和版本。文件路径或超链接有助于导航，但不能代替追踪记录。

## 受控对象

受控对象包括适用性、CRS、带时钟协议模型、追踪关系、含时序/误差 schema 的 VC、不可变证据、独立注册的推断模型和由门禁控制的主张。每次运行和派生结果必须记录

\[
(\text{基线},S,P,O,\text{CRS},G_T,V,\text{IUT},E,\text{时钟},\text{工具},\text{实验}).
\]

不得从目录名或“最新提交”推断版本。

## 门禁

RG0–RG6 控制静态产物和主张，G0–G7 控制证据层级；缺失上游批准时，下游实现或实验不能补偿规范空缺。

## 基础与扩展 VCS

基础 VCS 保存规范义务和逻辑 oracle；扩展 VCS 仅改变运行制度、故障注入或诊断实验，不得改变基础 PASS/FAIL 语义。

## 版本脊柱

基线、标准、适用性、CRS、模型、VCS、IUT、环境、时钟、工具和实验标识构成每次运行及派生分析的显式版本脊柱。

## 仓库实现

`docs/methodology/` 承载权威方法，`docs/research/` 与 `thesis/` 承载研究控制和出版，`src/`、`tests/`、`configs/` 与 `docs/engineering/` 承载工具及其受控输入，`artifacts/` 承载生成证据，`tutorial/common/` 和 `tutorial/arinc615a/` 分别承载通用教程与 615A 实例教程；`docs/review/` 和 `docs/management/` 横向治理各边界。
