# PR #6 Baseline Review Checklist

| Field | Value |
|---|---|
| **PR** | `#6` |
| **Baseline** | RB-2026-001-v4.2 |
| **Purpose** | File-by-file review control for the proposed baseline |
| **Author self-check** | Completed for the commit proposed by this PR |
| **Independent methodology/RG6 review** | PENDING |
| **Merge status** | BLOCKED until required independent decisions are recorded |

## Use and status semantics

`PASS` below means the author-side structural, consistency, or executable check
has passed. It is not independent approval. An independent reviewer must replace
`PENDING` with a gate-record reference and disposition before the PR becomes
Ready for Review. Any semantic or translation finding reopens the affected row.

## File checklist

| File | Author check | Independent review | Primary review focus |
|---|---|---|---|
| `.gitignore` | PASS | PENDING | local research-source exclusion |
| `PROJECT_PLAN.md` | PASS | PENDING | roadmap, gates, migration |
| `README.md` | PASS | PENDING | status and claim wording |
| `RESEARCH_OUTLINE.md` | PASS | PENDING | contribution and publication boundaries |
| `TRACKS.md` | PASS | PENDING | domain ownership, boundary contracts, trace spine |
| `docs/02_thesis_outline.md` | PASS | PENDING | supersession wording |
| `docs/BASELINE.md` | PASS | PENDING | authority, freeze status, acceptance |
| `docs/README.md` | PASS | PENDING | lifecycle and navigation |
| `docs/architecture.md` | PASS | PENDING | controlled objects, dependency direction, and trace rules |
| `docs/design/EVIDENCE_MANIFEST.md` | PASS | PENDING | timestamp/error budget and cross-domain artifact/gate references |
| `docs/design/README.md` | PASS | PENDING | design ownership and gates |
| `docs/engineering/IMPLEMENTATION_PLAN.md` | PASS | PENDING | implementability and ERROR separation |
| `docs/management/CHANGE_CONTROL.md` | PASS | PENDING | revision and migration controls |
| `docs/management/RISK_REGISTER.md` | PASS | PENDING | timing, shared-bias, and contract-drift risks |
| `docs/management/changes/CR-2026-001.md` | PASS | PENDING | change rationale and disposition |
| `docs/management/changes/CR-2026-002.md` | PASS | PENDING | product boundaries and migration |
| `docs/proposal/PR0004_METHODOLOGY_REFINEMENT.md` | PASS | PENDING | historical/superseded status |
| `docs/requirements/APPLICABILITY_TEMPLATE.md` | PASS | PENDING | observation and clock assumptions |
| `docs/requirements/CRS_SCHEMA.md` | PASS | PENDING | timing obligation completeness |
| `docs/requirements/README.md` | PASS | PENDING | requirements governance |
| `docs/requirements/TRACEABILITY_SCHEMA.md` | PASS | PENDING | timed traceability completeness |
| `docs/research/CLAIM_EVIDENCE_MATRIX.md` | PASS | PENDING | allowed and prohibited wording |
| `docs/research/EXPERIMENT_PLAN.md` | PASS | PENDING | held-out design and timing controls |
| `docs/research/RESEARCH_PLAN.md` | PASS | PENDING | RQs, hypotheses, and sequencing |
| `docs/review/DESIGN_DECISIONS.md` | PASS | PENDING | DD-012/DD-013 remain Proposed |
| `docs/review/GATE_RECORD_TEMPLATE.md` | PASS | PENDING | independence and sign-off fields |
| `docs/review/REVIEW_GUIDELINE.md` | PASS | PENDING | blocking severity and gate logic |
| `docs/methodology/00_INDEX.md` | PASS | PENDING | authority and downstream-consumer boundaries |
| `docs/methodology/RR-2026-001_test_analysis_conformance_methodology.md` | PASS | PENDING | equations, timing semantics, claims, EN/ZH parity |
| `docs/terminology.md` | PASS | PENDING | controlled term consistency |
| `thesis/README.md` | PASS | PENDING | publication inputs and claim traceability |
| `tutorial/README.md` | PASS | PENDING | non-normative dependency contract |
| `tutorial/common/README.md` | PASS | PENDING | protocol-independent scope and reuse boundary |
| `tutorial/arinc615a/README.md` | PASS | PENDING | baseline/tool/example trace requirements |
| `scripts/README.md` | PASS | PENDING | validator claim accuracy |
| `scripts/check_repo_baseline.py` | PASS | PENDING | bilingual and mathematical checks |
| deleted legacy English report | PASS | PENDING | superseded path removal |
| deleted parallel Chinese report | PASS | PENDING | single-file bilingual policy |
| `docs/review/PR6_BASELINE_REVIEW_CHECKLIST.md` | PASS | PENDING | checklist completeness |

---

# 中文版

| 字段 | 内容 |
|---|---|
| **PR** | `#6` |
| **基线** | RB-2026-001-v4.2 |
| **用途** | 对提议基线进行逐文件评审控制 |
| **作者自检** | 已对本 PR 提议提交完成 |
| **独立方法/RG6 评审** | 待完成 |
| **合并状态** | 在记录必需独立决定前保持阻塞 |

## 使用方法与状态语义

下表的 `PASS` 仅表示作者侧结构、一致性或可执行检查通过，不代表独立批准。PR
转为 Ready for Review 前，独立评审者必须把 `PENDING` 替换为门禁记录和处理结论。
任何语义或翻译发现都会重新打开相应行。

## 文件清单

| 文件 | 作者检查 | 独立评审 | 主要评审重点 |
|---|---|---|---|
| `.gitignore` | PASS | PENDING | 本地研究素材排除规则 |
| `PROJECT_PLAN.md` | PASS | PENDING | 路线、门禁和迁移 |
| `README.md` | PASS | PENDING | 状态与主张措辞 |
| `RESEARCH_OUTLINE.md` | PASS | PENDING | 贡献和发布边界 |
| `TRACKS.md` | PASS | PENDING | 领域所有权、边界契约和追踪脊柱 |
| `docs/02_thesis_outline.md` | PASS | PENDING | 取代关系措辞 |
| `docs/BASELINE.md` | PASS | PENDING | 权威、冻结状态和接受条件 |
| `docs/README.md` | PASS | PENDING | 生命周期和导航 |
| `docs/architecture.md` | PASS | PENDING | 受控对象、依赖方向和追踪规则 |
| `docs/design/EVIDENCE_MANIFEST.md` | PASS | PENDING | 时间戳/误差预算及跨领域产物/门禁引用 |
| `docs/design/README.md` | PASS | PENDING | 设计责任和门禁 |
| `docs/engineering/IMPLEMENTATION_PLAN.md` | PASS | PENDING | 可实现性和 ERROR 分离 |
| `docs/management/CHANGE_CONTROL.md` | PASS | PENDING | 修订和迁移控制 |
| `docs/management/RISK_REGISTER.md` | PASS | PENDING | 时序、共享偏差和契约漂移风险 |
| `docs/management/changes/CR-2026-001.md` | PASS | PENDING | 变更理由和处理 |
| `docs/management/changes/CR-2026-002.md` | PASS | PENDING | 产品边界与迁移 |
| `docs/proposal/PR0004_METHODOLOGY_REFINEMENT.md` | PASS | PENDING | 历史/已取代状态 |
| `docs/requirements/APPLICABILITY_TEMPLATE.md` | PASS | PENDING | 观测和时钟假设 |
| `docs/requirements/CRS_SCHEMA.md` | PASS | PENDING | 时序义务完整性 |
| `docs/requirements/README.md` | PASS | PENDING | 需求治理 |
| `docs/requirements/TRACEABILITY_SCHEMA.md` | PASS | PENDING | 时序追踪完整性 |
| `docs/research/CLAIM_EVIDENCE_MATRIX.md` | PASS | PENDING | 允许和禁止措辞 |
| `docs/research/EXPERIMENT_PLAN.md` | PASS | PENDING | 留出设计和时序控制 |
| `docs/research/RESEARCH_PLAN.md` | PASS | PENDING | RQ、假设和顺序 |
| `docs/review/DESIGN_DECISIONS.md` | PASS | PENDING | DD-012/DD-013 保持 Proposed |
| `docs/review/GATE_RECORD_TEMPLATE.md` | PASS | PENDING | 独立性和签字字段 |
| `docs/review/REVIEW_GUIDELINE.md` | PASS | PENDING | 阻塞严重度和门禁逻辑 |
| `docs/methodology/00_INDEX.md` | PASS | PENDING | 权威顺序和下游消费者边界 |
| `docs/methodology/RR-2026-001_test_analysis_conformance_methodology.md` | PASS | PENDING | 公式、时序语义、主张和中英对等 |
| `docs/terminology.md` | PASS | PENDING | 受控术语一致性 |
| `thesis/README.md` | PASS | PENDING | 出版输入和主张追踪 |
| `tutorial/README.md` | PASS | PENDING | 非规范依赖契约 |
| `tutorial/common/README.md` | PASS | PENDING | 协议无关范围和复用边界 |
| `tutorial/arinc615a/README.md` | PASS | PENDING | 基线/工具/示例追踪要求 |
| `scripts/README.md` | PASS | PENDING | 验证器主张准确性 |
| `scripts/check_repo_baseline.py` | PASS | PENDING | 双语和数学检查 |
| 已删除旧英文报告 | PASS | PENDING | 旧路径删除 |
| 已删除平行中文报告 | PASS | PENDING | 单文件双语政策 |
| `docs/review/PR6_BASELINE_REVIEW_CHECKLIST.md` | PASS | PENDING | 清单完整性 |
