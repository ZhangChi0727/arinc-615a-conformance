# Workstreams, Ownership, and Traceable Dependencies

The project minimizes coupling between engineering implementation, methodology
research/publication, and tutorials without pretending that they are
independent. They integrate through controlled contracts, explicit version
references, and reviewed change requests rather than through undocumented
knowledge or implementation internals.

For the v4.3 migration, generic method authority is outside this repository.
The dependency chain is external Candidate GVS Core → local Conformance-Testing
Profile candidate → ARINC 615A Product Binding candidate → Project
Configuration. Instance evidence then flows to local research and reporting.

```text
standard + applicability
          |
          v
methodology contracts ---------> engineering implementation
          |                               |
          v                               v
research protocol <------------- versioned evidence
          |
          v
reviewed claims + publications

methodology baseline -----------> common tutorial
methodology baseline + tool release + examples -----------> ARINC 615A tutorial
```

Review, Inspection, and change control govern every boundary. Research findings
may propose a methodology change, but they do not silently mutate a frozen
baseline.

## Workstream ownership

| Workstream | Canonical locations | Owns | Does not own |
|---|---|---|---|
| Governance and requirements | `docs/control/` | applicability, CRS, authority, gates, changes, reader-release contract | artifacts it independently approves |
| Methodology research | `docs/research/` | method semantics, research questions, protocols, analyses, claim boundaries | engineering internals or unreviewed raw-evidence changes |
| Engineering implementation | `src/`, `tests/`, `configs/`, `docs/engineering/` | executable VCs, instrument, schemas, environments, evidence production | normative interpretation or scientific claim promotion |
| Publication | `docs/research/publication/`, `artifacts/reports/` | manuscripts, figures, replication and reader reports | new method semantics or claims unsupported by passed gates |
| Common Verification Tutorial | `docs/tutorial/sources/COMMON_TUTORIAL_PLAN.md`, `artifacts/tutorials/` | protocol-independent verification teaching and exercises | ARINC-specific requirements or normative project decisions |
| ARINC 615A Tutorial | `docs/tutorial/sources/ARINC615A_TUTORIAL_PLAN.md`, `artifacts/tutorials/` | reproducible instance walkthroughs and operating procedures | baseline changes, implementation internals, or unrestricted conformance claims |
| External generic method | commit-bound `ZhangChi0727/complex-system-verification-assurance` material | Generic GVS Core definitions and cross-repository method contract | ARINC Profile/Binding details, configuration values, or instance findings disposition |
| ARINC Profile/Binding/Configuration | `docs/control/contracts/`, controlled instance artifacts | local policy, ARINC realization, selected project values, and instance traceability | Generic Core definition or direct upstream mutation |

One person may serve multiple workstreams, but independence requirements at a
named gate still apply.

## Boundary contracts

| Producer | Consumer | Required interface | Prohibited shortcut |
|---|---|---|---|
| Governance/requirements | Methodology and engineering | baseline ID, applicability ID, source hashes, CRS version | copying proprietary or unversioned requirement prose |
| Methodology research | Engineering | controlled terminology, model/trace semantics, verdict rules, evidence schema, gate criteria | depending on a Python class, private function, or mutable worktree state |
| Engineering | Research/publication | immutable raw evidence plus manifest and tool/configuration versions | treating a green test suite as a scientific result |
| Methodology research | Publication | approved method version, registered protocol, claim/evidence decision | promoting exploratory results into confirmatory claims |
| Methodology/engineering | Tutorials | named baseline, named tool release when used, stable example artifacts | letting tutorial prose redefine requirements, verdicts, or claims |

A cross-domain trace record identifies the producer artifact ID/version, the
consumer artifact ID/version, and, where applicable, the gate decision. A prose
hyperlink alone is not sufficient.

## Shared traceability spine

Every run, analysis, publication result, and ARINC 615A tutorial exercise must
carry the applicable subset of:

```text
baseline_id
standard_edition
applicability_id
crs_version
model_version
vcs_version
iut_version
tool_version
environment_id
experiment_id
evidence_manifest_id
verification_objective_id
objective_satisfaction_id
compliance_evidence_index_id
test_conformity_ref
problem_closure_id
claim_id
gate_record_id
```

Common tutorials that do not execute the project instrument record
`baseline_id` and concept/source references; they explicitly mark the remaining
fields not applicable. This spine connects the three domains without relying on
folder names, the latest commit, or informal prose.

## Dependency and change rules

- Normative obligation or scope questions go to governance/requirements.
- Formal semantics, adequacy, uncertainty, or diagnosis questions go to
  methodology research and the applicable research gate.
- Observable behavior, execution, or evidence-production questions go to
  engineering.
- Claim wording goes to the claim/evidence matrix and release gate.
- Tutorials consume released or explicitly proposed artifacts; they never
  become an upstream authority by repetition.
- Downstream evidence may trigger a CR/DD, but only an approved baseline change
  can alter an upstream contract.
- Core-directed findings become Framework Change Proposal inputs; they do not
  create a reverse dependency or edit the external method in place.

---

# 中文版

项目在不假装三者彼此独立的前提下，尽量降低工程实现、方法论研究/出版和教程之间的耦合。三者通过受控契约、明确版本引用和经评审变更请求集成，而不依赖未记录知识或实现内部细节。

对 v4.3 迁移而言，通用方法权威位于本仓库之外。依赖链为：外部 Candidate GVS Core →
本地 Conformance-Testing Profile 候选 → ARINC 615A Product Binding 候选 → Project
Configuration，随后实例证据流向本地研究和报告。

```text
标准 + 适用性
      |
      v
方法论契约 ---------------------> 工程实现
      |                              |
      v                              v
研究协议 <---------------------- 版本化证据
      |
      v
已评审主张 + 出版物

方法论基线 ---------------------> 通用教程
方法论基线 + 工具发布 + 示例 ----> ARINC 615A 教程
```

评审、检查和变更控制治理每个边界。研究发现可以提出方法论变更，但不能静默修改冻结基线。

## 工作流所有权

| 工作流 | 权威位置 | 拥有 | 不拥有 |
|---|---|---|---|
| 治理与需求 | `docs/control/` | 适用性、CRS、权威顺序、门禁、变更和读者发布契约 | 其需要独立批准的产物 |
| 方法论研究 | `docs/research/` | 方法语义、研究问题、协议、分析、主张边界 | 工程内部结构或未经评审的原始证据修改 |
| 工程实现 | `src/`、`tests/`、`configs/`、`docs/engineering/` | 可执行 VC、工具、schema、环境、证据生产 | 规范解释或科学主张晋级 |
| 出版 | `docs/research/publication/`、`artifacts/reports/` | 论文、图表、复现报告和读者报告 | 新方法语义或未通过门禁支持的主张 |
| 通用验证教程 | `docs/tutorial/sources/COMMON_TUTORIAL_PLAN.md`、`artifacts/tutorials/` | 协议无关的验证教学与练习 | ARINC 专用需求或项目规范性决定 |
| ARINC 615A 教程 | `docs/tutorial/sources/ARINC615A_TUTORIAL_PLAN.md`、`artifacts/tutorials/` | 可复现实例讲解与操作规程 | 基线变更、实现内部结构或无限定符合性主张 |
| 外部通用方法 | 提交绑定的 `ZhangChi0727/complex-system-verification-assurance` 材料 | Generic GVS Core 定义与跨仓库方法契约 | ARINC Profile/Binding 细节、配置值或实例 finding 处置 |
| ARINC Profile/Binding/Configuration | `docs/control/contracts/` 与受控实例产物 | 本地政策、ARINC 实现、选定项目值和实例追踪 | Generic Core 定义或直接修改上游 |

同一人可以承担多个工作流角色，但具名门禁的独立性要求仍然适用。

## 边界契约

| 生产者 | 消费者 | 必需接口 | 禁止的捷径 |
|---|---|---|---|
| 治理/需求 | 方法论与工程 | 基线 ID、适用性 ID、来源哈希、CRS 版本 | 复制专有或未版本化的需求原文 |
| 方法论研究 | 工程 | 受控术语、模型/迹语义、判定规则、证据 schema、门禁准则 | 依赖 Python 类、私有函数或可变工作树状态 |
| 工程 | 研究/出版 | 不可变原始证据及清单、工具/配置版本 | 把绿色测试套件当作科学结果 |
| 方法论研究 | 出版 | 已批准方法版本、已注册协议、主张/证据决定 | 把探索性结果晋级为验证性主张 |
| 方法论/工程 | 教程 | 具名基线、使用工具时的具名发布版、稳定示例产物 | 让教程重定义需求、判定或主张 |

追踪记录必须标明生产者与消费者产物 ID/版本，并在适用时记录门禁决定；仅有叙述性超链接不足以构成受控追踪。

## 共享追踪脊柱

每次运行、分析、出版结果和 ARINC 615A 教程练习必须携带以下字段的适用子集：

```text
baseline_id
standard_edition
applicability_id
crs_version
model_version
vcs_version
iut_version
tool_version
environment_id
experiment_id
evidence_manifest_id
verification_objective_id
objective_satisfaction_id
compliance_evidence_index_id
test_conformity_ref
problem_closure_id
claim_id
gate_record_id
```

不执行项目工具的通用教程记录 `baseline_id` 和概念/来源引用，并将其他字段明确标为不适用。该脊柱无需依赖目录名、最新提交或非正式叙述即可连接三个领域。

## 依赖与变更规则

- 规范义务或范围问题回到治理/需求。
- 形式语义、充分性、不确定性或诊断问题回到方法论研究及相应研究门禁。
- 可观测行为、执行或证据生产问题回到工程。
- 主张措辞回到主张—证据矩阵和发布门。
- 教程消费已发布或明确标为提议的产物，不会因反复转述而成为上游权威。
- 下游证据可以触发 CR/DD，但只有批准的基线变更才能修改上游契约。
- 指向 Core 的 finding 形成 Framework Change Proposal 输入，不产生反向依赖，也不原地编辑外部方法。
